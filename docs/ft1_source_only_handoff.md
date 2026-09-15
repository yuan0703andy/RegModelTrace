# FT-1 source-only preparation handoff

Preparation is complete. Human adjudication and model evaluation are not complete.
The historical release and Test E remain closed; this development branch does not
change Base Qwen, the v2.2 contract, parser, retriever, or Ray configuration.

## Review package

The self-contained local package is `~/Downloads/RegModelTrace-FT1-SourceOnly-20260915/`.
Start with `index.html`, then read `CHAT_INSTRUCTIONS.md`. It contains:

- 24 new development candidates: the same 12 full requirements for Impact/Verisk.
- Five original PDFs with matching archive SHA-256 values.
- Exact source block text, IDs, canonical page offsets, and physical PDF links.
- Complete outcome-free source pools and required parser products.
- A regulator-only selection lock and preparation/source warning receipts.
- Unsigned scope-verification, two adjudicator, and resolution forms.

The public tree retains only preparation code, protocol, compact warning/selection
receipts, and a package hash inventory. Raw PDFs and full pools are external.
Do not delete either the original package or external inputs during cleanup.

## Selection and boundaries

The selection rule is two full standards per discipline, ordered by
SHA-256(`ft1-source-only-standard-selection-2026-09-15-v1:standard_id`). The selected
standards are G-5, G-3, M-6, M-1, S-4, S-5, V-2, V-3, A-1, A-6, CI-3, and CI-2.
Selection was locked before vendor/reviewer parser reads. It targets no class
balance and does not inherit historical outcome-dependent evidence memberships.
These are exposed-corpus development candidates, not new independent corpora or
held-out generalization evidence. Shared regulator/vendor lineage prevents random
splitting or a naive interpretation of 24 independent experimental units.

The 7,846 references are broad page/context navigation. They are neither Gold
facts nor required-recall targets. Mechanical subsection proposals are not atomic
human facets. An independent verifier must finalize source scope before outcomes,
and preserve/hash amendments. Real annotators must not have seen prior judgments
or model outputs. The package itself cannot certify their independence.

All retained text blocks reconstruct from canonical page spans. This does not
establish correct geometry or tables: retained parser products report alignment
and unsupported table-header diagnostics. Check material evidence against PDFs.
Shortlist absence never establishes fixed-corpus absence.

## What remains

1. Independent source-scope verification and any documented amendments.
2. Two actual independent human facet adjudications; no AI substitute.
3. Disagreement resolution, signature/identity validation, and prospective freeze.
4. A matched prospective A/B/C protocol before controlled comparison or inference.
5. DCC B/C execution and scoring only after the applicable gates actually pass.

Historical A predictions on different bundles are reference-only. Do not reopen
KCC. No inference or training occurred in this preparation. No LoRA finding or
training authorization can be inferred from it.

## Reproduction

The two-stage builder is `regmodeltrace.research.facet_reasoning.prepare_source_only`:
run `select` against regulator-only parser inputs into a NEW selection file before
reading paired source products; then run `build` against the source inputs/raw
PDFs into a NEW directory. Both commands refuse overwrite. The immutable original
selection also binds the builder SHA-256. The exporter is
`regmodeltrace.research.facet_reasoning.export_source_only`; it verifies raw hashes
and exports only an explicit allowlist of source-only products.

Actual CPU preparation ran through `dcc-agent` on a compute node using the existing
project runtime. Its external workspace is
`/hpc/home/yh421/CIRCAD-LLM/research-runs/ft1-source-only-20260915/`.
No work was executed on a login node. Informal development issues are appended to
`notes/extraction_failures.md`; they are not Gold or acceptance-criterion changes.

## Context-budget diagnostic

The initial CPU budget diagnostic was invalid: tokenizer output was a mapping, and len() counted mapping fields rather than token IDs. The preserved v1 receipt is invalid; corrected token-ID counting supersedes it. This is not an actual B/C request assessment or model evaluation. Scope finalization must keep material evidence while meeting the frozen context budget; count the exact final template again before compute. Silent truncation is prohibited.

Corrected CPU token-ID counting found 19/24 broad navigation prototypes over budget. This remains a pre-adjudication navigation diagnostic; actual B/C counts must be checked after verified scope and facets freeze.
