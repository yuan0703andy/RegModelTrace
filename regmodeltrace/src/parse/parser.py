"""Serial source-preserving PDF structure parser. No annotation inputs or evidence semantics."""
import argparse
from collections import Counter, defaultdict
from decimal import Decimal, InvalidOperation
import hashlib
import json
import math
import os
from pathlib import Path
import re
import subprocess
import sys
import xml.etree.ElementTree as ET

import pyarrow as pa
import pyarrow.parquet as pq


def norm(t):
    return ' '.join(t.split())


def sha(t):
    return hashlib.sha256(t.encode() if isinstance(t, str) else t).hexdigest()


def canonical(obj):
    return json.dumps(obj, sort_keys=True, ensure_ascii=False, separators=(',', ':'))


def uid(*parts):
    return sha(canonical(parts))[:24]


def box(words):
    if not words:
        return None
    return [min(w['bbox'][0] for w in words), min(w['bbox'][1] for w in words),
            max(w['bbox'][2] for w in words), max(w['bbox'][3] for w in words)]


def cx(w):
    return (w['bbox'][0] + w['bbox'][2]) / 2


def numeric(t):
    return bool(re.fullmatch(r'[-+]?\d+(?:\.\d+)?%?', t))


def margin_key(t):
    return re.sub(r'\d+', '#', t)


def geometry_rows(words, tolerance):
    rows = []
    for w in sorted(words, key=lambda w: (w['bbox'][1], w['bbox'][0], w['word_id'])):
        if not rows or abs(w['bbox'][1] - rows[-1]['y']) > tolerance:
            rows.append(dict(y=w['bbox'][1], words=[]))
        rows[-1]['words'].append(w)
    for r in rows:
        r['words'].sort(key=lambda w: (w['bbox'][0], w['bbox'][1], w['word_id']))
        r['text'] = ' '.join(w['text'] for w in r['words'])
        r['bbox'] = box(r['words'])
    return rows


def raw_lines(raw, rows):
    """Canonical offsets are constructed from raw text, not geometry or any external annotation."""
    result, offset, used = [], 0, set()
    for line_no, raw_line in enumerate(raw.splitlines()):
        t = norm(raw_line)
        if not t:
            continue
        tokens = t.split()
        matched = None
        for ri, row in enumerate(rows):
            if ri in used:
                continue
            if row['text'] == t:
                matched = (ri, row['words'])
                break
        if matched is None:
            # A physical row may contain two separately emitted text columns.
            for ri, row in enumerate(rows):
                ws = row['words']
                for a in range(len(ws) - len(tokens) + 1):
                    part = ws[a:a + len(tokens)]
                    if [w['text'] for w in part] == tokens and not any(w['word_id'] in used for w in part):
                        matched = (None, part)
                        break
                if matched:
                    break
        if matched:
            ri, ws = matched
            if ri is not None:
                used.add(ri)
            used.update(w['word_id'] for w in ws)
        else:
            ws = []
        result.append(dict(text=t, start=offset, end=offset + len(t), raw_line=line_no,
                           bbox=box(ws), word_ids=[w['word_id'] for w in ws],
                           alignment='ALIGNED' if ws else 'ALIGNMENT_FAILED'))
        offset += len(t) + 1
    assert ' '.join(l['text'] for l in result) == norm(raw)
    return result


def header_groups(row, gap):
    groups = []
    for w in row['words']:
        if not groups or w['bbox'][0] - groups[-1][-1]['bbox'][2] > gap:
            groups.append([])
        groups[-1].append(w)
    return [dict(text=' '.join(w['text'] for w in g), bbox=box(g), word_ids=[w['word_id'] for w in g]) for g in groups]


def parse_tables(doc, page, rows, cfg):
    """Infer numeric panels and nested header paths by geometry, without known labels or values."""
    runs, current = [], []
    for ri, r in enumerate(rows):
        eligible = (len(r['words']) >= cfg['dense_numeric_min_columns']
                    and all(numeric(w['text']) for w in r['words']))
        if eligible:
            if current and (r['y'] - rows[current[-1]]['y'] > cfg['numeric_row_max_gap']
                            or len(r['words']) != len(rows[current[-1]]['words'])):
                runs.append(current)
                current = []
            current.append(ri)
        elif current:
            runs.append(current)
            current = []
    if current:
        runs.append(current)
    tables, diagnostics = [], []
    for run in runs:
        if len(run) < cfg['dense_numeric_min_rows']:
            continue
        first = run[0]
        headers = []
        y = rows[first]['y']
        for j in range(first - 1, -1, -1):
            r = rows[j]
            if y - r['y'] > cfg['numeric_row_max_gap'] or re.match(r'^(Table|Figure)\s+\d', r['text'], re.I):
                break
            # Missing values or split decimal lexemes do not turn data rows into headers.
            if sum(numeric(w['text']) for w in r['words']) > len(r['words']) / 2:
                break
            headers.insert(0, header_groups(r, cfg['header_word_gap']))
            y = r['y']
            if len(headers) == cfg['table_header_max_rows']:
                break
        band_id = uid(doc['sha256'], page, 'table_panel', first)
        body_rows = [rows[i] for i in run]
        caption = next((r['text'] for r in reversed(rows[:first]) if re.match(r'^Table\s+\d+\s*:', r['text'])), None)
        if not headers or len(headers[-1]) != len(body_rows[0]['words']):
            diagnostics.append(dict(document_id=doc['document_id'], page=page, code='UNSUPPORTED_TABLE_HEADERS',
                                    bbox=box([w for r in body_rows for w in r['words']]), detail='Dense numeric rows preserved; header/column alignment not resolved.'))
            continue
        leaf = headers[-1]
        ncols = len(leaf)
        # An upper header is assigned by its horizontal span of descendant leaf centers.
        paths = []
        for col in range(ncols):
            x = cx(leaf[col])
            path = []
            evidence = []
            for level in headers[:-1]:
                if col == 0:
                    continue
                h = min(level, key=lambda g: abs(cx(g) - x))
                path.append(h['text'])
                evidence.append(h)
            path.append(leaf[col]['text'])
            evidence.append(leaf[col])
            paths.append((path, evidence))
        row_header = leaf[0]['text']
        data = []
        for row in body_rows:
            label = row['words'][0]
            row_path = [row_header, label['text']]
            for ci, w in enumerate(row['words'][1:], 1):
                path, hsource = paths[ci]
                data.append(dict(cell_id=uid(band_id, row_path, path), table_id=band_id,
                    row_key=uid(band_id, row_path), column_key=uid(band_id, path),
                    row_path=row_path, column_path=path, raw_value=w['text'],
                    value=str(Decimal(w['text'].rstrip('%'))), bbox=w['bbox'],
                    source_word_ids=[w['word_id']], row_label_word_id=label['word_id'],
                    column_headers=hsource, row_header=leaf[0]))
        table = dict(table_id=band_id, document_id=doc['document_id'], page=page, caption=caption,
            bbox=box([w for r in body_rows for w in r['words']] + [dict(bbox=g['bbox']) for hs in headers for g in hs]),
            header_levels=headers, row_header=row_header, row_count=len(body_rows), column_count=ncols - 1,
            numeric_word_ids=[w['word_id'] for r in body_rows for w in r['words']],
            row_label_word_ids=[r['words'][0]['word_id'] for r in body_rows], cells=data, status='OK')
        tables.append(table)
    return tables, diagnostics


CONTEXTS = {'Audit', 'Disclosures', 'Purpose:', 'Purpose', 'Pre-Visit Letter', 'Professional Team Comments:',
            'Professional Team Comments', 'Relevant Forms:', 'Editorial Items'}
STANDARD = re.compile(r'^([A-Z]{1,3}-\d+)\s+([A-Za-z].+)')
DISCLOSURE = re.compile(r'^([A-Z]{1,3}-\d+)\.(\d+(?:\.[A-Z])?)\s+(.+)')
FORM = re.compile(r'^Form\s+([A-Z]-\d+)\s*:\s*(.+)', re.I)
DOMAIN = re.compile(r'^(METEOROLOGICAL|STATISTICAL|GENERAL|ACTUARIAL|VULNERABILITY|COMPUTER/INFORMATION)\s+STANDARDS\b')


def short_title(t):
    words = t.split()
    return (1 < len(words) <= 8 and not re.search(r'[.:;?!,=]', t) and
            all(w[:1].isupper() or w.lower() in {'and', 'of', 'to', 'for', 'in', 'or', 'the', 'at', '(or'} for w in words))


def structure_document(doc, pages, cfg):
    blocks, units, edges, diagnostics, tables = [], [], [], [], []
    unit_map = {}
    droot = uid(doc['sha256'], 'document')
    state = dict(domain=None, standard=None, subsection=None, disclosure=None, form=None, context=None, title=None)
    def make(kind, label, parent, p, start):
        ident = uid(doc['sha256'], kind, label, p, start)
        if ident not in unit_map:
            u = dict(unit_id=ident, kind=kind, label=label, parent_unit_id=parent,
                     document_id=doc['document_id'], page=p, start=start)
            unit_map[ident] = u
            units.append(u)
        return ident
    make('document', doc['title'], None, 0, 0)
    # Use one explicit document root.
    droot = units[0]['unit_id']
    repeats = Counter()
    for p in pages:
        for l in p['lines']:
            b = l['bbox']
            if b and (b[1] < p['height'] * cfg['header_top_fraction'] or b[3] > p['height'] * cfg['footer_bottom_fraction']):
                repeats[margin_key(l['text'])] += 1
    prior_body = None
    for p in pages:
        ptables, td = parse_tables(doc, p['page'], p['rows'], cfg)
        tables.extend(ptables)
        diagnostics.extend(td)
        pending = []
        page_blocks = []
        def parent():
            return state['title'] or state['context'] or state['disclosure'] or state['subsection'] or state['form'] or state['standard'] or state['domain'] or droot
        def emit(lines, typ='paragraph', ancestry=None):
            if not lines:
                return
            a, b = lines[0]['start'], lines[-1]['end']
            text = p['text'][a:b]
            b_id = uid(doc['sha256'], p['page'], a, b, typ)
            active = dict(state if ancestry is None else ancestry)
            anc = (active.get('title') or active.get('context') or active.get('disclosure') or active.get('subsection')
                   or active.get('form') or active.get('standard') or active.get('domain') or droot)
            def label(k):
                return unit_map[active[k]]['label'] if active.get(k) else None
            bb = box([dict(bbox=l['bbox']) for l in lines if l['bbox']])
            tmatch = next((t for t in ptables if bb and t['bbox'][1] <= bb[1] and bb[3] <= t['bbox'][3]), None)
            if tmatch and typ in {'paragraph', 'list'}:
                typ = 'table'
            status = 'OK' if all(l['alignment'] == 'ALIGNED' for l in lines) else 'ALIGNMENT_FAILED'
            if status != 'OK':
                diagnostics.append(dict(document_id=doc['document_id'], page=p['page'], code=status,
                    start=a, end=b, detail='Canonical text retained; one or more raw lines lack an exact geometry match.'))
            block = dict(block_id=b_id, document_id=doc['document_id'], document_sha256=doc['sha256'],
                page_start=p['page'], page_end=p['page'], printed_page_label=p['printed_page_label'],
                unit_id=b_id, parent_unit_id=anc, section_title=label('standard') or label('form') or label('domain'),
                standard_id=label('standard'), subsection_id=label('subsection'), disclosure_id=label('disclosure'),
                form_id=label('form'), source_context=label('domain'), source_context_label=label('context'),
                block_type=typ, text=text, text_sha256=sha(text), reading_order=len(blocks),
                source_spans=[dict(page=p['page'], start=a, end=b, page_text_sha256=p['page_text_sha256'])],
                bbox=bb, line_geometry=[dict(start=l['start'], end=l['end'], bbox=l['bbox'], word_ids=l['word_ids'], alignment=l['alignment']) for l in lines],
                is_searchable=typ not in {'header', 'footer'}, table_id=tmatch['table_id'] if tmatch else None,
                parse_status=status, parser_version=cfg['parser_version'])
            blocks.append(block)
            page_blocks.append(block)
        def flush():
            nonlocal pending
            emit(pending, 'list' if pending and re.match(r'^(?:\d+[.)]|[a-z][.)]|[▪•])\s', pending[0]['text']) else 'paragraph')
            pending = []
        for l in p['lines']:
            t, bb = l['text'], l['bbox']
            is_footer = bool(bb and bb[1] > p['height'] * cfg['footer_bottom_fraction'] and
                             (t.isdigit() or repeats[margin_key(t)] >= cfg['margin_repeat_min_pages']))
            is_header = bool(bb and bb[1] < p['height'] * cfg['header_top_fraction'] and
                             repeats[margin_key(t)] >= cfg['margin_repeat_min_pages'] and not DOMAIN.match(t))
            if is_header or is_footer:
                flush()
                emit([l], 'footer' if is_footer else 'header')
                continue
            in_table = any(bb and tb['bbox'][1] <= bb[1] and bb[3] <= tb['bbox'][3] for tb in ptables)
            m_domain, m_form, m_disc, m_std = DOMAIN.match(t), FORM.match(t), DISCLOSURE.match(t), STANDARD.match(t)
            kind, label = None, None
            if not in_table:
                if m_domain:
                    kind, label = 'domain', m_domain.group(0).title()
                elif m_form:
                    kind, label = 'form', m_form.group(1)
                elif m_disc:
                    kind, label = 'disclosure', m_disc.group(1) + '.' + m_disc.group(2)
                elif m_std and not t.endswith(('.', ';')):
                    kind, label = 'standard', m_std.group(1)
                elif t in CONTEXTS:
                    kind, label = 'context', t.rstrip(':')
                elif re.match(r'^[A-Z]\.\s', t) and state['standard']:
                    kind, label = 'subsection', t[0]
                elif short_title(t) and (not pending or l['raw_line'] > pending[-1]['raw_line'] + 1):
                    kind, label = 'title', t
            if kind:
                flush()
                if kind == 'domain':
                    state = dict(domain=make(kind, label, droot, p['page'], l['start']), standard=None, subsection=None, disclosure=None, form=None, context=None, title=None)
                elif kind in {'standard', 'form'}:
                    state.update(standard=None, subsection=None, disclosure=None, form=None, context=None, title=None)
                    state[kind] = make(kind, label, state['domain'] or droot, p['page'], l['start'])
                elif kind in {'subsection', 'disclosure'}:
                    ancestor = state['standard'] or state['form'] or state['domain'] or droot
                    if kind == 'disclosure' and '.' in label:
                        prefix = label.rsplit('.', 1)[0]
                        ancestor = next((u['unit_id'] for u in reversed(units)
                            if u['kind'] == 'disclosure' and u['label'] == prefix
                            and u['parent_unit_id'] == ancestor), ancestor)
                    state.update(subsection=None, disclosure=None, context=None, title=None)
                    state[kind] = make(kind, label, ancestor, p['page'], l['start'])
                elif kind == 'context':
                    state.update(context=None, title=None, subsection=None)
                    state[kind] = make(kind, label, state['standard'] or state['form'] or state['domain'] or droot, p['page'], l['start'])
                else:
                    state['title'] = make(kind, label, state['context'] or state['disclosure'] or state['subsection'] or state['standard'] or state['form'] or state['domain'] or droot, p['page'], l['start'])
                emit([l], 'heading')
            else:
                if pending and (l['raw_line'] > pending[-1]['raw_line'] + 1 or re.match(r'^(?:\d+[.)]|[▪•])\s', t)):
                    flush()
                pending.append(l)
        flush()
        body = [b for b in page_blocks if b['is_searchable']]
        if prior_body and body:
            first = body[0]
            if prior_body['parent_unit_id'] == first['parent_unit_id']:
                if prior_body['source_context_label'] == first['source_context_label'] and first['source_context_label']:
                    edges.append(dict(from_block_id=prior_body['block_id'], to_block_id=first['block_id'], kind='context_continuation', parent_unit_id=first['parent_unit_id']))
                elif prior_body['block_type'] in {'paragraph', 'list'} and first['block_type'] == 'paragraph' and not re.search(r'[.!?;:]$', prior_body['text']):
                    edges.append(dict(from_block_id=prior_body['block_id'], to_block_id=first['block_id'], kind='paragraph_continuation', parent_unit_id=first['parent_unit_id']))
        prior_body = body[-1] if body else prior_body
        if not p['text']:
            diagnostics.append(dict(document_id=doc['document_id'], page=p['page'], code='UNSUPPORTED_EMPTY_TEXT', detail='Page retained; text absent, OCR not implemented.'))
    return blocks, units, edges, tables, diagnostics


def extract_document(doc, source, cfg):
    raw = subprocess.run(['pdftotext', '-layout', '-enc', 'UTF-8', str(source), '-'], capture_output=True, text=True, check=True)
    xml = subprocess.run(['pdftotext', '-bbox-layout', '-enc', 'UTF-8', str(source), '-'], capture_output=True, text=True, check=True)
    root = ET.fromstring(xml.stdout)
    for node in root.iter():
        node.tag = node.tag.split('}')[-1]
    xp = list(root.iter('page'))
    raw_pages = raw.stdout.split('\f')
    if raw_pages and not raw_pages[-1].strip():
        raw_pages.pop()
    if len(raw_pages) != doc['num_pages'] or len(xp) != len(raw_pages):
        raise ValueError('Physical page count differs from manifest')
    pages, words_all = [], []
    for page, (text, xpage) in enumerate(zip(raw_pages, xp), 1):
        words = []
        for index, word in enumerate(xpage.iter('word')):
            words.append(dict(word_id=uid(doc['sha256'], page, 'word', index), document_id=doc['document_id'], page=page,
                              text=word.text or '', bbox=[float(word.attrib[k]) for k in ['xMin', 'yMin', 'xMax', 'yMax']]))
        words_all.extend(words)
        rows = geometry_rows(words, cfg['row_y_tolerance'])
        lines = raw_lines(text, rows)
        height, width = float(xpage.attrib['height']), float(xpage.attrib['width'])
        printed = next((l['text'] for l in reversed(lines) if l['text'].isdigit() and l['bbox'] and l['bbox'][1] > height * cfg['footer_bottom_fraction']), None)
        pages.append(dict(document_id=doc['document_id'], document_sha256=doc['sha256'], page=page,
                          text=norm(text), page_text_sha256=sha(norm(text)), width=width, height=height,
                          printed_page_label=printed, lines=lines, rows=rows))
    diagnostics = []
    for result in (raw, xml):
        if result.stderr.strip():
            diagnostics.append(dict(document_id=doc['document_id'], page=None, code='EXTRACTOR_WARNING', detail=result.stderr.strip()))
    return pages, words_all, diagnostics


def write_json(path, obj):
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + '\n')


def enforce_inputs(read_files, output_dir):
    allowed = {str(p.resolve()) for p in read_files}
    out = str(output_dir.resolve()) + os.sep
    accesses = set()
    def guard(event, args):
        if event != 'open' or not isinstance(args[0], (str, bytes, os.PathLike)):
            return
        p = str(Path(os.fsdecode(args[0])).resolve())
        if p in allowed or p.startswith(out):
            accesses.add(p)
            return
        # Imports are completed before installation. All data reads are explicit.
        raise PermissionError(f'Input allowlist rejected file access: {p}')
    sys.addaudithook(guard)
    return accesses


def run(args):
    manifest_path, config_path = Path(args.manifest).resolve(), Path(args.config).resolve()
    docs = json.loads(manifest_path.read_text())
    cfg = json.loads(config_path.read_text())
    root, output = Path(args.raw_root).resolve(), Path(args.output_dir).resolve()
    output.mkdir(parents=True, exist_ok=True)
    (output / 'fatal_error.json').unlink(missing_ok=True)
    sources = [root / d['local_path'] for d in docs]
    # Warm dependencies that lazily inspect Python distribution metadata before the data-read guard.
    pq.write_table(pa.Table.from_pylist([dict(warmup=True)]), output / '.warmup.parquet')
    (output / '.warmup.parquet').unlink()
    parser_hash = sha(Path(__file__).read_bytes())
    tool_version = subprocess.run(['pdftotext', '-v'], capture_output=True, text=True, check=True).stderr.strip()
    accesses = enforce_inputs([manifest_path, config_path, *sources], output)
    blocks, units, edges, tables, diagnostics, pages_out, words_out = [], [], [], [], [], [], []
    for doc, source in zip(docs, sources):
        if sha(source.read_bytes()) != doc['sha256']:
            raise ValueError('Input checksum mismatch')
        pages, words, warnings = extract_document(doc, source, cfg)
        b, u, e, t, diag = structure_document(doc, pages, cfg)
        blocks.extend(b); units.extend(u); edges.extend(e); tables.extend(t)
        diagnostics.extend(warnings + diag); words_out.extend(words)
        for p in pages:
            pages_out.append({k: v for k, v in p.items() if k not in {'rows', 'lines'}})
        print(f"Parsed {doc['document_id']}: {len(pages)} pages, {len(b)} blocks, {len(t)} numeric panels", flush=True)
    data = {'parsed_blocks.parquet': blocks, 'source_pages.parquet': pages_out, 'source_words.parquet': words_out}
    logical = {}
    for name, rows in data.items():
        temp = output / (name + '.tmp')
        pq.write_table(pa.Table.from_pylist(rows), temp, compression='zstd')
        temp.replace(output / name)
        logical[name] = sha(canonical(rows))
    for name, obj in [('units.json', units), ('continuations.json', edges), ('tables.json', tables), ('diagnostics.json', diagnostics)]:
        write_json(output / name, obj)
        logical[name] = sha(canonical(obj))
    run_manifest = dict(parser_version=cfg['parser_version'], parser_sha256=parser_hash, config=cfg,
        config_sha256=sha(config_path.read_bytes()), manifest_sha256=sha(manifest_path.read_bytes()),
        source_pdfs=[{k:d[k] for k in ['document_id','sha256','num_pages']} for d in docs],
        tool_version=tool_version, logical_hashes=logical, canonical_output_sha256=sha(canonical(logical)),
        pages=len(pages_out), blocks=len(blocks), tables=len(tables), table_cells=sum(len(t['cells']) for t in tables),
        diagnostics_by_code=dict(Counter(d['code'] for d in diagnostics)),
        input_guard='ENFORCED_EXPLICIT_FILE_ALLOWLIST', semantic_classification_performed=False,
        overall_parse_status='PARTIAL' if diagnostics else 'OK')
    write_json(output / 'parser_run_manifest.json', run_manifest)
    write_json(output / 'input_access_log.json', sorted(accesses))
    return run_manifest


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ['manifest','raw-root','output-dir','config']:
        parser.add_argument('--' + name, required=True)
    args = parser.parse_args()
    try:
        result = run(args)
        print('Canonical output:', result['canonical_output_sha256'])
    except Exception as exc:
        # Surface catastrophic extraction/alignment/input failures even if no block file can be written.
        path = Path(args.output_dir) / 'fatal_error.json'
        if path.parent.exists():
            write_json(path, dict(status='FAILED', error_type=type(exc).__name__, message=str(exc)))
        raise


if __name__ == '__main__':
    main()
