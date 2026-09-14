"""Source-only SQLite search foundation. No Gold reads or model execution."""
import argparse
import collections
import hashlib
import json
from pathlib import Path
import re
import sqlite3
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'src/extract'))
from evidence_v2 import prepare_unit, promote_table

VERSION = 'evidence-store-0.1.0'


def canonical(value):
    return json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(',', ':'))


def digest(value):
    return hashlib.sha256(value.encode() if isinstance(value, str) else value).hexdigest()


def load(path):
    return json.loads(path.read_text())


def validate_candidate(candidate, unit, blocks):
    spans = candidate['source_spans']
    if candidate['candidate_id'] != 'A' + digest(canonical([unit['unit_id'], spans]))[:20]:
        raise ValueError('Candidate identity changed')
    for span in spans:
        if len(span['source_block_ids']) != 1:
            raise ValueError('Unsupported multi-block coordinate frame')
        block = blocks[span['source_block_ids'][0]]
        a, b = span['block_char_start'], span['block_char_end']
        if (block['document_id'] != unit['document_id'] or not block['is_searchable']
                or span['pages'] != [block['page_start']]
                or not 0 <= a < b <= len(block['text'])
                or block['text'][a:b] != span['quote']):
            raise ValueError('Candidate source mapping changed')
    if candidate['text'] != ' '.join(s['quote'] for s in spans):
        raise ValueError('Candidate wording changed')


def add_classifications(conn, run):
    """Import persisted host-bound predictions, never evaluator labels."""
    manifest = load(run / 'run_manifest.json')
    if manifest['status'] != 'COMPLETE' or manifest['binding_status'] != 'PASS':
        raise ValueError('Unaccepted producer output')
    for file, field in [('results.json', 'results_sha256'), ('inputs.jsonl', 'input_sha256')]:
        if digest((run / file).read_bytes()) != manifest[field]:
            raise ValueError('Producer artifact hash mismatch')
    inputs = [json.loads(line) for line in (run / 'inputs.jsonl').read_text().splitlines()]
    outputs = load(run / 'results.json')
    if len(inputs) != len(outputs):
        raise ValueError('Classification inventory mismatch')
    for index, (item, result) in enumerate(zip(inputs, outputs)):
        if (result['assertion_id'] != item['assertion_id'] or result['request_index'] != index
                or result['identity_owner'] != 'HOST_REQUEST' or result['binding_status'] != 'PASS'
                or result['parse_status'] != 'PASS'):
            raise ValueError('Classification request binding mismatch')
        if json.loads(result['raw_model_text']) != {'evidence_type': result['normalized_label']}:
            raise ValueError('Classification raw output mismatch')
        members = []
        for cid in item['candidate_ids']:
            row = conn.execute('SELECT payload FROM records WHERE record_id=?', (cid,)).fetchone()
            if row is None:
                raise ValueError('Classification source candidate is absent')
            members.append(json.loads(row[0]))
        spans = [s for member in members for s in member['source_spans']]
        expected_id = 'B' + digest(canonical([item['unit_id'], item['candidate_ids']]))[:20]
        if (expected_id != item['assertion_id'] or spans != item['source_spans']
                or ' '.join(s['quote'] for s in spans) != item['focal_assertion']
                or any(m['unit_id'] != item['unit_id'] for m in members)):
            raise ValueError('Classification source group mismatch')
        annotation = dict(assertion_id=item['assertion_id'], evidence_type=result['normalized_label'],
                          candidate_ids=item['candidate_ids'], assertion_text=item['focal_assertion'],
                          actor=item['document']['source_actor'], source_spans=spans,
                          pages=item['pages'], document=item['document'], run=str(run.name),
                          results_sha256=manifest['results_sha256'])
        conn.execute('INSERT INTO classifications VALUES (?,?)', (item['assertion_id'], canonical(annotation)))
        for cid in item['candidate_ids']:
            conn.execute('INSERT INTO membership VALUES (?,?)', (cid, item['assertion_id']))


def logical_hash(conn, tables):
    return digest(canonical({table: conn.execute(f'SELECT * FROM {table} ORDER BY 1').fetchall()
                             for table in tables}))


def build(destination, run=None):
    import pyarrow.parquet as pq
    destination = Path(destination)
    if destination.exists():
        raise FileExistsError('Choose a new store path; existing stores are immutable')
    paths = dict(units=ROOT / 'data/semantic/semantic_units.parquet',
                 unit_manifest=ROOT / 'data/semantic/semantic_units_manifest.json',
                 blocks=ROOT / 'data/processed/parsed_blocks.parquet',
                 pages=ROOT / 'data/processed/source_pages.parquet',
                 documents=ROOT / 'data/document_manifest.json',
                 parser=ROOT / 'data/processed/parser_run_manifest.json',
                 diagnostics=ROOT / 'data/processed/diagnostics.json',
                 continuations=ROOT / 'data/semantic/continuation_unit_links.json')
    hashes = {key: digest(path.read_bytes()) for key, path in paths.items()}
    um = load(paths['unit_manifest'])
    if hashes['units'] != um['output_sha256'] or hashes['blocks'] != um['input_sha256']['parsed_blocks.parquet']:
        raise ValueError('Semantic units or M2 inputs changed')
    if (paths['blocks'].parent / 'fatal_error.json').exists():
        raise ValueError('M2 has an unresolved fatal error')
    blocks = {b['block_id']: b for b in pq.read_table(paths['blocks']).to_pylist()}
    units = pq.read_table(paths['units']).to_pylist()
    pages = {(p['document_id'], p['page']): p for p in pq.read_table(paths['pages']).to_pylist()}
    docs = {d['document_id']: d for d in load(paths['documents'])}
    roles = {key: doc['document_type'] for key, doc in docs.items()}
    for block in blocks.values():
        if block['document_sha256'] != docs[block['document_id']]['sha256']:
            raise ValueError('Wrong PDF identity')
        source = []
        for span in block['source_spans']:
            page = pages[block['document_id'], span['page']]
            if digest(page['text']) != span['page_text_sha256']:
                raise ValueError('Canonical page text changed')
            source.append(page['text'][span['start']:span['end']])
        if ' '.join(' '.join(source).split()) != ' '.join(block['text'].split()):
            raise ValueError('M2 block no longer reconstructs from canonical pages')
    destination.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='store-build-', dir=destination.parent) as tmp:
        path = Path(tmp) / 'evidence.sqlite'
        conn = sqlite3.connect(path)
        conn.executescript('''
            CREATE TABLE records(record_id TEXT PRIMARY KEY, unit_id TEXT, document_id TEXT,
                                 standard_id TEXT, kind TEXT, payload TEXT NOT NULL);
            CREATE TABLE units(unit_id TEXT PRIMARY KEY, payload TEXT NOT NULL);
            CREATE TABLE blocks(block_id TEXT PRIMARY KEY, payload TEXT NOT NULL);
            CREATE TABLE documents(document_id TEXT PRIMARY KEY, payload TEXT NOT NULL);
            CREATE TABLE classifications(assertion_id TEXT PRIMARY KEY, payload TEXT NOT NULL);
            CREATE TABLE membership(candidate_id TEXT, assertion_id TEXT,
                                    PRIMARY KEY(candidate_id, assertion_id));
            CREATE TABLE metadata(key TEXT PRIMARY KEY, payload TEXT NOT NULL);
            CREATE VIRTUAL TABLE search_text USING fts5(text, structure);
        ''')
        for block in sorted(blocks.values(), key=lambda b: b['block_id']):
            conn.execute('INSERT INTO blocks VALUES (?,?)', (block['block_id'], canonical(block)))
        for doc in docs.values():
            conn.execute('INSERT INTO documents VALUES (?,?)', (doc['document_id'], canonical(doc)))
        counts = collections.Counter()
        for source in units:
            unit = prepare_unit(source, blocks, roles)
            catalog = unit['candidate_catalog']
            records = []
            if unit['unit_kind'] == 'table':
                for cell in promote_table(unit, blocks):
                    text = ' / '.join(cell['row_path']) + ' | ' + ' / '.join(cell['column_path']) + ' = ' + cell['raw_value']
                    records.append(dict(cell, record_id=cell['table_cell_ids'][0], text=text,
                                        text_kind='LABELLED_TABLE_VALUE_NOT_QUOTATION', classification_status='DETERMINISTIC'))
            else:
                for candidate in catalog['candidates']:
                    validate_candidate(candidate, unit, blocks)
                    records.append(dict(candidate, record_id=candidate['candidate_id'], record_kind='NARRATIVE',
                                        unit_id=unit['unit_id'], document_id=unit['document_id'],
                                        document_sha256=docs[unit['document_id']]['sha256'],
                                        standard_id=unit['standard_id'], section_path=unit['section_path'],
                                        source_context_label=unit['source_context_label'],
                                        form_ids=[s[6:] for s in unit['section_path'] if s.startswith('form: ')],
                                        pages=sorted({p for s in candidate['source_spans'] for p in s['pages']}),
                                        source_parse_warnings=unit['parse_warnings'], evidence_type=None,
                                        classification_status='UNCLASSIFIED', text_kind='SOURCE_QUOTATION'))
            disposition = dict(unit_id=unit['unit_id'], document_id=unit['document_id'],
                               source_block_ids=unit['source_block_ids'], context_block_ids=unit['context_block_ids'],
                               parse_warnings=unit['parse_warnings'], records=[r['record_id'] for r in records],
                               dispositions=catalog['dispositions'], heading_only=unit['heading_only'],
                               source_text=unit['text'], section_path=unit['section_path'])
            conn.execute('INSERT INTO units VALUES (?,?)', (unit['unit_id'], canonical(disposition)))
            for record in records:
                counts[record['record_kind']] += 1
                if record.get('kind') == 'LOCAL_PROPOSITION':
                    counts['LOCAL_PROPOSITION'] += 1
                cursor = conn.execute('INSERT INTO records VALUES (?,?,?,?,?,?)',
                                      (record['record_id'], unit['unit_id'], unit['document_id'],
                                       unit['standard_id'], record['record_kind'], canonical(record)))
                conn.execute('INSERT INTO search_text(rowid,text,structure) VALUES (?,?,?)',
                             (cursor.lastrowid, record['text'], ' / '.join(unit['section_path'])))
        pool_hash = logical_hash(conn, ['records', 'units', 'blocks', 'documents'])
        if run:
            add_classifications(conn, Path(run))
        code = [Path(__file__), ROOT / 'src/extract/evidence_v2.py', ROOT / 'src/extract/assertion_candidates.py']
        receipt = dict(version=VERSION, source_units=len(units), documents=len(docs), records=dict(counts),
                       classified_assertions=conn.execute('SELECT count(*) FROM classifications').fetchone()[0],
                       source_pool_sha256=pool_hash,
                       logical_sha256=logical_hash(conn, ['records', 'units', 'blocks', 'documents', 'classifications', 'membership']),
                       input_sha256=hashes, code_sha256={p.name: digest(p.read_bytes()) for p in code},
                       sqlite_version=sqlite3.sqlite_version, LLM_requests=0,
                       retrieval_quality='NOT_EVALUATED', MILESTONE_4='IN_PROGRESS',
                       source_parse_status=load(paths['parser'])['overall_parse_status'])
        for key, value in [('build', receipt), ('parser_diagnostics', load(paths['diagnostics'])),
                           ('continuation_links', load(paths['continuations']))]:
            conn.execute('INSERT INTO metadata VALUES (?,?)', (key, canonical(value)))
        conn.commit()
        conn.close()
        path.rename(destination)
    return receipt


def connect(path):
    return sqlite3.connect(Path(path).resolve().as_uri() + '?mode=ro', uri=True)


def search(path, query, limit=10, document_id=None, standard_id=None):
    if not 1 <= limit <= 100:
        raise ValueError('limit must be between 1 and 100')
    tokens = list(dict.fromkeys(re.findall(r'\w+', query, re.UNICODE)))[:64]
    if not tokens:
        return []
    match = ' OR '.join('"' + token + '"' for token in tokens)
    sql = '''SELECT records.payload,bm25(search_text,1.0,0.2) AS score
             FROM search_text JOIN records ON search_text.rowid=records.rowid
             WHERE search_text MATCH ?'''
    params = [match]
    for key, value in [('document_id', document_id), ('standard_id', standard_id)]:
        if value is not None:
            sql += f' AND records.{key}=?'
            params.append(value)
    sql += ' ORDER BY score, records.record_id LIMIT ?'
    params.append(limit)
    with connect(path) as conn:
        results = []
        for payload, score in conn.execute(sql, params):
            record = json.loads(payload)
            labels = [json.loads(row[0]) for row in conn.execute('''
                SELECT c.payload FROM classifications c JOIN membership m USING(assertion_id)
                WHERE m.candidate_id=? ORDER BY c.assertion_id''', (record['record_id'],))]
            individual = [label for label in labels if len(label['candidate_ids']) == 1]
            if len(individual) == 1:
                record.update(evidence_type=individual[0]['evidence_type'], classification_status='CLASSIFIED')
            elif labels:
                record['classification_status'] = 'GROUP_MEMBER_ONLY'
            unit = json.loads(conn.execute('SELECT payload FROM units WHERE unit_id=?', (record['unit_id'],)).fetchone()[0])
            document = json.loads(conn.execute('SELECT payload FROM documents WHERE document_id=?', (record['document_id'],)).fetchone()[0])
            position = unit['records'].index(record['record_id'])
            record.update(score=score, classification_annotations=labels,
                          previous_id=unit['records'][position-1] if position else None,
                          next_id=unit['records'][position+1] if position+1 < len(unit['records']) else None,
                          source_links=[document['source_url'] + '#page=' + str(p) for p in record['pages']])
            results.append(record)
    return results


if __name__ == '__main__':
    cli = argparse.ArgumentParser(description=__doc__)
    sub = cli.add_subparsers(dest='command', required=True)
    make = sub.add_parser('build')
    make.add_argument('--output', type=Path, required=True)
    make.add_argument('--classifications', type=Path)
    query = sub.add_parser('search')
    query.add_argument('--store', type=Path, required=True)
    query.add_argument('--query', required=True)
    query.add_argument('--limit', type=int, default=10)
    query.add_argument('--document-id')
    query.add_argument('--standard-id')
    args = cli.parse_args()
    result = (build(args.output, args.classifications) if args.command == 'build' else
              search(args.store, args.query, args.limit, args.document_id, args.standard_id))
    print(json.dumps(result, indent=2, ensure_ascii=False))
