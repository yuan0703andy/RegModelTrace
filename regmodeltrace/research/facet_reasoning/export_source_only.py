"""Export an immutable, self-contained reviewer package without past outcomes."""
from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import html
import json
from pathlib import Path
import shutil


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    p = argparse.ArgumentParser()
    for name in ('pack', 'selection', 'inputs', 'raw', 'output'):
        p.add_argument('--' + name, type=Path, required=True)
    a = p.parse_args()
    if a.output.exists():
        raise ValueError('Refusing to overwrite an exported source-review package')
    cases = json.loads((a.pack / 'pilot_pack.json').read_text())
    receipt = json.loads((a.pack / 'preparation_receipt.json').read_text())
    raw_map = {sha(f): f.name for f in a.raw.glob('*.pdf')}
    if {name: h for h, name in raw_map.items()} != receipt['raw_pdfs']:
        raise ValueError('Raw source checksum mismatch before export')
    root = a.output
    root.mkdir(parents=True)
    (root / 'raw').mkdir()
    (root / 'cases').mkdir()
    for f in sorted(a.raw.glob('*.pdf')):
        shutil.copyfile(f, root / 'raw' / f.name)
    allowed = ('pilot_pack.json', 'impact_full_source_pool.json', 'verisk_full_source_pool.json',
               'preparation_receipt.json', 'preparation_issues.json',
               'source_scope_verification_template.json', 'adjudicator_a_return.json',
               'adjudicator_b_return.json', 'resolution_return.json')
    for name in allowed:
        shutil.copyfile(a.pack / name, root / name)
    shutil.copyfile(a.selection, root / 'source_only_selection.json')
    for corpus in ('regulator', 'impact', 'verisk'):
        dest = root / 'parser_inputs' / corpus
        dest.mkdir(parents=True)
        for name in ('parsed_blocks.parquet', 'source_pages.parquet',
                     'parser_run_manifest.json', 'diagnostics.json', 'continuations.json'):
            src = a.inputs / corpus / name
            if src.exists():
                shutil.copyfile(src, dest / name)
    for name in ('annotation_guide.md', 'aggregation_rule.json'):
        shutil.copyfile(Path(__file__).parent / name, root / name)
    instructions = '''# Independent source-only facet adjudication

This is a 24-case development candidate pack, not frozen Gold, an unseen test,
or a completed model evaluation. Selection used only regulator structure and a
fixed SHA-256 ordering: two full standards in each of six disciplines, applied
to two vendors. No class balance was targeted. Existing outcomes are excluded.

1. Have an independent source-scope verifier review candidate boundaries,
   original PDFs, material qualifications, exceptions, contradictory evidence,
   and cross-references. Resolve scope amendments BEFORE assigning outcomes;
   preserve the original version and hash any amended pilot. The scope template
   must bind the final pilot SHA-256 and identify the actual verifier.
2. Two actual human adjudicators who have not seen prior judgments/model outputs
   work independently using separate A/B forms. A second AI opinion is not a
   substitute. Do not inspect the other human's decisions before returns lock.
3. Mechanical subsection proposals are NOT atomic facets or human truth.
   Confirm or split them into genuinely adjudicable obligations. Preserve OR
   alternatives and conditional applicability; do not turn a permitted unused
   alternative into a missing obligation. Document each boundary amendment.
4. Determine applicability, documentary sufficiency, facet states, overall
   relation, independent review coverage, causal status, support/limitations,
   rationale, and unresolved dependencies. Use the included annotation guide.
   Vendor demonstration must come from vendor evidence, not copied requirements
   or reviewer verification. INSUFFICIENT is not CONFLICT; missing proof alone
   does not automatically establish a demonstrated partial match.
5. Explicitly search reversal evidence in the complete source pools/PDFs.
   Record full-pool additions and IDs, then amend and reverify bounded scope.
   A shortlist miss is NOT corpus absence. Form identifiers are not standards.
   Alignment warnings and unsupported table headers require visual checks of
   material evidence; exact text spans do not guarantee table/geometry fidelity.
6. The vendor final snapshots postdate the reports (Impact: May 28 vs April 25,
   Verisk: May 27 vs April 3, 2025). They cannot alone reconstruct initial
   submissions or establish that review caused model/method modification.
7. Lock both signed human returns, resolve disagreements without model output,
   and prospectively freeze truth. No model inference/training is performed by
   this package. Historical A on different bundles cannot identify an A-to-B/C
   representation improvement. Matched A/B/C protocol remains pending.

Start with index.html or human_audit_pack.md. Each case page shows exact source
block text, role, physical PDF page links, and proposition IDs. Full source pools
and canonical page/offset provenance are in the JSON and parser_inputs files.
All contexts are navigation candidates, not required Gold evidence. Assign no
semantic alignment label to isolated source blocks. No existing fixture labels,
model predictions, or known-error summaries are provided to adjudicators.
'''
    (root / 'CHAT_INSTRUCTIONS.md').write_text(instructions)
    index = ['# FT-1 independent source-only candidate audit pack', '',
             'Prepared: 24 comparison candidates. Human truth: NOT STARTED. Model inference: NOT RUN.', '',
             'Read CHAT_INSTRUCTIONS.md first. Proposed subsections require human atomic splitting.', '',
             '| Case | Candidate source blocks | Proposed subsections |', '|---|---:|---:|']
    links = []
    for case in cases:
        cid = case['case_id']
        index.append(f"| [{cid}](cases/{cid}.md) | {len(case['evidence'])} | {len(case['facets'])} |")
        links.append(f'<li><a href="cases/{cid}.html">{html.escape(cid)}</a></li>')
        md = [f'# {cid}', '', 'UNADJUDICATED. Broad mechanical navigation scope; no inference or Gold labels.', '',
              '## Frozen regulator requirement text', '', case['requirement_text'], '',
              '## Proposed subsections — human splitting required', '']
        web = [f'<h1>{html.escape(cid)}</h1>',
               '<p>Unadjudicated source candidates. Mechanical subsection proposals are not Gold.</p>',
               '<p><a href="../index.html">All cases</a> · <a href="../CHAT_INSTRUCTIONS.md">Instructions</a></p>',
               '<h2>Regulator requirement</h2><pre>' + html.escape(case['requirement_text']) + '</pre>',
               '<h2>Proposed subsections — split/confirm independently</h2>']
        for facet in case['facets']:
            md.extend([f"### {facet['facet_id']}", '', facet['text'], ''])
            web.append('<details><summary>' + html.escape(facet['facet_id']) + '</summary><pre>'
                       + html.escape(facet['text']) + '</pre></details>')
        for role in ('STANDARDS', 'VENDOR_SUBMISSION', 'PROFESSIONAL_TEAM_REPORT'):
            evidence = [e for e in case['evidence'] if e['actor_role'] == role]
            md.extend([f'## {role} — exact source candidates ({len(evidence)})', ''])
            web.append(f'<h2>{role} ({len(evidence)} source candidates)</h2>')
            for e in evidence:
                pdf = raw_map[e['document_sha256']]
                page = e['pages'][0]
                path = f'../raw/{pdf}#page={page}'
                heading = f"{e['proposition_id']} · {pdf} · physical pages {e['pages']}"
                context = (f"Standard: {e['standard_id']}; Form: {e['form_id']}; "
                           f"Context: {e['source_context_label']}; Parse: {e['parse_status']}")
                md.extend([f'### {heading}', '', f'[Open PDF](<{path}>)', '', context, '',
                           '```text', e['text'], '```', ''])
                primary = e['standard_id'] == case['requirement_id'] and not e['form_id']
                web.append('<details' + (' class="primary"' if primary else '') + '><summary>'
                           + html.escape(heading) + '</summary><p><a href="' + html.escape(path)
                           + '">Open original PDF</a></p><p>' + html.escape(context) + '</p><pre>'
                           + html.escape(e['text']) + '</pre></details>')
        (root / 'cases' / f'{cid}.md').write_text('\n'.join(md) + '\n')
        (root / 'cases' / f'{cid}.html').write_text(html_page(cid, '\n'.join(web)))
    (root / 'human_audit_pack.md').write_text('\n'.join(index) + '\n')
    (root / 'index.html').write_text(html_page('FT-1 source audit',
       '<h1>FT-1 source-only human audit</h1><p>24 development candidates. No frozen truth or model evaluation.</p>'
       '<p><a href="CHAT_INSTRUCTIONS.md">Read independent adjudication instructions</a></p><ul>'
       + '\n'.join(links) + '</ul>'))
    (root / 'README.md').write_text('# Source-only review package\n\nStart with index.html or human_audit_pack.md, '
      'then read CHAT_INSTRUCTIONS.md. Preserve this original package; save signed returns separately. '
      'Do not mistake unsigned templates or mechanical scope proposals for completed human adjudication.\n')
    manifest = {str(f.relative_to(root)): sha(f) for f in sorted(root.rglob('*')) if f.is_file()}
    (root / 'handoff_receipt.json').write_text(json.dumps({
      'status': 'PREPARATION_COMPLETE_HUMAN_GATES_PENDING', 'candidate_count': len(cases),
      'cases_by_vendor': dict(Counter(c['vendor_group'] for c in cases)),
      'source_block_references': sum(len(c['evidence']) for c in cases),
      'original_pdf_count': len(raw_map), 'independent_human_returns': 0, 'model_runs': 0,
      'source_scope_independently_verified': False, 'truth_frozen': False,
      'files': manifest}, indent=2, sort_keys=True) + '\n')


def html_page(title, body):
    return ('<!doctype html><html lang="en"><meta charset="utf-8"><title>' + html.escape(title)
            + '</title><style>body{max-width:1100px;margin:32px auto;padding:0 24px;'
            'font:16px/1.6 system-ui;color:#172b3a}pre{white-space:pre-wrap;overflow-wrap:anywhere;'
            'background:#f5f7fa;padding:16px}details{border:1px solid #ccd5df;margin:10px 0;padding:10px}'
            'details.primary{border-left:4px solid #38739b}summary{cursor:pointer}a{color:#185c91}'
            '</style><body>' + body + '</body></html>')


if __name__ == '__main__':
    main()
