"""Two-stage, outcome-free source pack construction; never adjudicates truth."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path

import pyarrow.parquet as pq

DISCIPLINES = ('G', 'M', 'S', 'V', 'A', 'CI')
SALT = 'ft1-source-only-standard-selection-2026-09-15-v1'


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def digest(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()


def write(path: Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False, sort_keys=True) + '\n')


def standard_groups(blocks: list[dict]) -> dict[str, list[dict]]:
    """Find full standards from structure and normative body, excluding TOC summaries."""
    groups = {}
    ids = sorted({b['standard_id'] for b in blocks if b.get('standard_id')
                  and re.fullmatch(r'(G|M|S|V|A|CI)-\d+', b['standard_id'])})
    for sid in ids:
        rows = [b for b in blocks if b['standard_id'] == sid and b.get('is_searchable')]
        headings = [b for b in rows if b['block_type'] == 'heading'
                    and b['text'].startswith(sid + ' ') and not b.get('form_id')
                    and not re.search(r'\d+\s*$|Significant Revision', b['text'])]
        candidates = []
        for heading in headings:
            body = [b for b in rows if b['reading_order'] >= heading['reading_order']]
            normative = [b for b in body if b.get('source_context_label') not in ('Audit', 'Disclosures')]
            if any(re.search(r'\bshall\b', b['text'], re.I) for b in normative):
                candidates.append(body)
        if candidates:
            groups[sid] = max(candidates, key=lambda bs: bs[0]['reading_order'])
    return groups


def choose(groups: dict[str, list[dict]]) -> list[str]:
    selected = []
    for discipline in DISCIPLINES:
        eligible = [s for s in groups if s.split('-')[0] == discipline]
        if len(eligible) < 2:
            raise ValueError(f'Fewer than two structurally eligible standards: {discipline}')
        selected.extend(sorted(eligible, key=lambda s: digest(SALT + ':' + s))[:2])
    return selected


def proposal_facets(rows: list[dict], case_id: str) -> list[dict]:
    """Mechanical subsection proposals; humans must split atomic/OR facets themselves."""
    chunks = []
    current = []
    for row in rows[1:]:
        if row.get('source_context_label') in ('Audit', 'Disclosures'):
            break
        if row['text'].strip().lower() == 'purpose':
            break
        if re.match(r'^[A-Z]\.\s', row['text']) and current:
            chunks.append(current)
            current = []
        current.append(row)
    if current:
        chunks.append(current)
    return [{'facet_id': f'{case_id}.P{n}', 'text': '\n'.join(b['text'] for b in chunk),
             'logic_group': 'UNRESOLVED_HUMAN_SPLIT_REQUIRED',
             'state': None, 'supporting_proposition_ids': [], 'limiting_proposition_ids': [],
             'annotation_status': 'MECHANICAL_SUBSECTION_PROPOSAL_NOT_HUMAN_FACET_TRUTH'}
            for n, chunk in enumerate(chunks, 1)
            if any(re.search(r'\bshall\b|\bis to\b', b['text'], re.I) for b in chunk)]


def verify_block(block: dict, pages: dict[tuple[str, int], dict]) -> None:
    text = block['text']
    if digest(text) != block['text_sha256']:
        raise ValueError(f"Block hash mismatch {block['block_id']}")
    pieces = []
    for span in block['source_spans']:
        page = pages[(block['document_id'], span['page'])]
        if digest(page['text']) != page['page_text_sha256']:
            raise ValueError('Canonical page hash mismatch')
        if page['page_text_sha256'] != span['page_text_sha256']:
            raise ValueError('Span/page hash mismatch')
        if not 0 <= span['start'] < span['end'] <= len(page['text']):
            raise ValueError('Invalid span offsets')
        pieces.append(page['text'][span['start']:span['end']])
    if ' '.join(' '.join(pieces).split()) != ' '.join(text.split()):
        raise ValueError(f"Block reconstruction failed {block['block_id']}")


def source_row(block: dict, role: str) -> dict:
    return {'proposition_id': 'SRC-' + block['block_id'], 'actor_role': role,
            'text': block['text'], 'document_id': block['document_id'],
            'document_sha256': block['document_sha256'],
            'pages': sorted({s['page'] for s in block['source_spans']}),
            'source_block_id': block['block_id'], 'source_spans': block['source_spans'],
            'text_sha256': block['text_sha256'], 'bbox': block.get('bbox'),
            'block_type': block['block_type'], 'standard_id': block.get('standard_id'),
            'form_id': block.get('form_id'), 'source_context_label': block.get('source_context_label'),
            'parse_status': block.get('parse_status'), 'evidence_role': None}


def select(args) -> None:
    if args.output.exists():
        raise ValueError('Refusing to overwrite source-only selection')
    groups = standard_groups(pq.read_table(args.regulator / 'parsed_blocks.parquet').to_pylist())
    ids = choose(groups)
    write(args.output, {'version': 'ft1-source-only-selection-1.0',
          'status': 'LOCKED_BEFORE_VENDOR_REVIEWER_READS',
          'selection_rule': 'two full standards per discipline; smallest SHA256(salt:standard_id)',
          'salt': SALT, 'eligible_standard_ids': sorted(groups), 'selected_standard_ids': ids,
          'candidate_count': 24, 'corpora': ['impact', 'verisk'],
          'alignment_labels_used': False, 'model_outputs_used': False,
          'regulator_inputs': {p.name: sha(p) for p in sorted(args.regulator.glob('*.parquet'))},
          'builder_sha256': sha(Path(__file__)),
          'dimensions': [{'standard_id': sid, 'source_block_ids': [b['block_id'] for b in groups[sid]],
                          'requirement_source_sha256': digest('\n'.join(b['text'] for b in groups[sid]))}
                         for sid in ids]})


def build(args) -> None:
    if args.output.exists():
        raise ValueError('Refusing to overwrite source-only pack')
    lock = json.loads(args.selection.read_text())
    if lock['status'] != 'LOCKED_BEFORE_VENDOR_REVIEWER_READS':
        raise ValueError('Missing prospective regulator selection')
    if lock['builder_sha256'] != sha(Path(__file__)):
        raise ValueError('Builder changed after selection lock')
    for name, h in lock['regulator_inputs'].items():
        if sha(args.inputs / 'regulator' / name) != h:
            raise ValueError('Regulator selection input drift')
    raw = {sha(p): p.name for p in args.raw.glob('*.pdf')}
    source_pools, reads, cases, warnings = {}, [], [], []
    reg_blocks = pq.read_table(args.inputs / 'regulator' / 'parsed_blocks.parquet').to_pylist()
    groups = standard_groups(reg_blocks)
    for corpus in ('impact', 'verisk'):
        folder = args.inputs / corpus
        blocks = pq.read_table(folder / 'parsed_blocks.parquet').to_pylist()
        pages = {(p['document_id'], p['page']): p for p in
                 pq.read_table(folder / 'source_pages.parquet').to_pylist()}
        for p in folder.iterdir():
            if p.is_file():
                reads.append({'corpus': corpus, 'file': p.name, 'sha256': sha(p)})
        pool = []
        by_id = {}
        for b in blocks:
            if b['document_sha256'] not in raw:
                raise ValueError(f"Exact raw PDF unavailable: {b['document_id']}")
            verify_block(b, pages)
            role = ('STANDARDS' if b['document_sha256'] == reg_blocks[0]['document_sha256']
                    else 'PROFESSIONAL_TEAM_REPORT' if 'team' in raw[b['document_sha256']]
                    else 'VENDOR_SUBMISSION')
            row = source_row(b, role)
            pool.append(row)
            by_id[b['block_id']] = row
        source_pools[corpus] = pool
        for sid in lock['selected_standard_ids']:
            case_id = f'FT1-SOURCE-{corpus.upper()}-{sid}'
            reg = groups[sid]
            normative = []
            for b in reg:
                if b.get('source_context_label') in ('Audit', 'Disclosures'):
                    break
                normative.append(b)
            # Retain the full standard (including Purpose, Disclosures, Audit) for interpretation.
            target = re.compile(r'(?<![A-Z0-9-])' + re.escape(sid) + r'(?!\d)')
            anchors = [b for b in blocks if b.get('is_searchable') and not b.get('form_id')
                       and (b.get('standard_id') == sid or target.search(b['text']))]
            hit_pages = {(b['document_id'], s['page']) for b in anchors for s in b['source_spans']}
            chosen = [b for b in blocks if b.get('is_searchable') and any(
                      (b['document_id'], s['page']) in hit_pages for s in b['source_spans'])]
            evidence = [by_id[b['block_id']] for b in chosen]
            # Source-only regulator blocks have different IDs under some parser manifests.
            source_ids = {e['source_block_id'] for e in evidence}
            for b in reg:
                if b['block_id'] not in source_ids:
                    evidence.append(source_row(b, 'STANDARDS'))
            issue_codes = []
            for role in ('VENDOR_SUBMISSION', 'PROFESSIONAL_TEAM_REPORT'):
                if not any(e['actor_role'] == role for e in evidence):
                    issue_codes.append('NO_MECHANICAL_SHORTLIST_HIT_' + role)
            if any(e['parse_status'] not in ('OK', None) for e in evidence):
                issue_codes.append('PARSER_STATUS_WARNING')
            if any(e['form_id'] for e in evidence):
                issue_codes.append('FORM_EVIDENCE_REQUIRES_HUMAN_SCOPE_CHECK')
            if any(e['block_type'] == 'table' for e in evidence):
                issue_codes.append('TABLE_EVIDENCE_REQUIRES_VISUAL_CHECK')
            warnings.append({'case_id': case_id, 'issues': issue_codes,
                             'shortlist_absence_is_not_corpus_absence': True})
            cases.append({'case_id': case_id, 'comparison_id': case_id,
              'corpus_id': f'{corpus}-2023-ft1-source-only-development', 'requirement_id': sid,
              'requirement_text': '\n'.join(b['text'] for b in normative),
              'constraint_status': 'UNADJUDICATED', 'facets': proposal_facets(reg, case_id),
              'evidence': evidence, 'evidence_sufficiency': None, 'relation': None,
              'vendor_group': corpus, 'model_version_group': f'{corpus}-2023-final-snapshot',
              'requirement_family': sid.split('-')[0],
              'regulator_text_group': digest('\n'.join(b['text'] for b in normative)),
              'source_group_ids': sorted({e['document_sha256'] for e in evidence}),
              'revision_ancestry': f'{corpus}-2023-final-snapshot-not-initial-submission',
              'review_ancestry': f'{corpus}-2023-professional-team-review',
              'leakage_group': 'FCHLPM-2023-shared-regulator-exposed-development',
              'truth_status': 'UNADJUDICATED_SOURCE_ONLY_CANDIDATE',
              'source_scope_status': 'MECHANICAL_SOURCE_ONLY_SCOPE_PENDING_INDEPENDENT_VERIFICATION',
              'regulator_source_block_ids': [b['block_id'] for b in reg]})
    args.output.mkdir(parents=True)
    write(args.output / 'pilot_pack.json', cases)
    for corpus, pool in source_pools.items():
        write(args.output / f'{corpus}_full_source_pool.json', pool)
    write(args.output / 'preparation_issues.json', warnings)
    write(args.output / 'source_scope_verification_template.json', {
          'status': 'PENDING_INDEPENDENT_SOURCE_SCOPE_VERIFICATION',
          'pilot_sha256': sha(args.output / 'pilot_pack.json'),
          'verifier_name': None, 'verification_date': None, 'attestation': None,
          'cases': [{'case_id': c['case_id'], 'source_scope_status': c['source_scope_status'],
                     'evidence_scope_frozen_without_truth': False, 'rationale': None} for c in cases]})
    for slot in ('A', 'B', 'RESOLUTION'):
        write(args.output / (f'adjudicator_{slot.lower()}_return.json' if slot != 'RESOLUTION'
                            else 'resolution_return.json'), {
          'status': 'UNSIGNED_NOT_HUMAN_TRUTH', 'adjudicator_slot': slot,
          'adjudicator_name': None, 'adjudication_date': None, 'attestation': None,
          'resolution_panel': None,
          'cases': [{'case_id': c['case_id'], 'constraint_status': None,
            'evidence_sufficiency': None, 'overall_relation': None, 'review_coverage': None,
            'causal_status': None, 'case_rationale': None, 'unresolved_dependencies': [],
            'facets': [{**f, 'rationale': None, 'text_confirmed_or_revised': None}
                       for f in c['facets']]} for c in cases]})
    write(args.output / 'preparation_receipt.json', {
      'status': 'PREPARED_NOT_ADJUDICATED_NOT_MODEL_EVALUATED', 'candidate_count': len(cases),
      'selection_sha256': sha(args.selection), 'builder_sha256': sha(Path(__file__)),
      'raw_pdfs': {name: h for h, name in sorted(raw.items())}, 'input_reads': reads,
      'all_source_blocks_exactly_reconstructed': True,
      'alignment_labels_read': False, 'model_outputs_read': False, 'inference_runs': 0,
      'independent_pilot_ready': 0, 'human_truth_frozen': False,
      'condition_a': 'HISTORICAL_REFERENCE_ONLY_DIFFERENT_BUNDLES',
      'pending_gates': ['Independent source-scope verification',
                        'Two actual independent human facet adjudications',
                        'Disagreement resolution and prospective truth freeze',
                        'Matched prospective A/B/C protocol before comparative compute']})


def main() -> None:
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(dest='command', required=True)
    s = sub.add_parser('select')
    s.add_argument('--regulator', type=Path, required=True)
    s.add_argument('--output', type=Path, required=True)
    b = sub.add_parser('build')
    b.add_argument('--selection', type=Path, required=True)
    b.add_argument('--inputs', type=Path, required=True)
    b.add_argument('--raw', type=Path, required=True)
    b.add_argument('--output', type=Path, required=True)
    args = p.parse_args()
    (select if args.command == 'select' else build)(args)


if __name__ == '__main__':
    main()
