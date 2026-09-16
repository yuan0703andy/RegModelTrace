# VS-1 Task 0 — Implementation Inventory

**Change:** `VS-1`
**Inventory:** `vs-1-task0-inventory-1.0`
**Active checkout:** `codex/ft-1-facet-diagnostic@781d4bd7ddeeecf7ec93f4538b387fd34c8235c7`
**Spec-reviewed baseline:** `9b0c0d29f3970613e14b5411041a8a88e2e22f93`
**Disposition:** `READY_FOR_PROJECT_OWNER_REVIEW`
**Implementation started:** **No**

## Scope and custody

This inventory is the only VS-1 task executed. It made no code, model, retrieval, embedding, Ray, or UI-architecture changes. The checkout was already dirty before Task 0: `regmodeltrace/service.py` and `notes/extraction_failures.md` were modified, and ER-1/JA-1/model-comparison materials were untracked. Those files were inspected but not rewritten.

The revised specification was available as pasted attachment text. The named `RegModelTrace_VS1_OpenSpec_Package.zip` and `openspec/changes/vs-1/` were not present in the active workspace, so Task 0 did not copy, reconstruct, or infer those package files.

The recovered local data are real and substantial:

| Asset | Verified state |
|---|---:|
| Physical PDF copies | 45 |
| Unique PDF hashes | 33 |
| Candidate VS-1 three-document corpus | 3 PDFs / 710 pages |
| Candidate corpus hashes matching manifest | 3/3 |
| Parsed blocks | 8,390 |
| Semantic units | 1,443 |
| M4A narrative candidates | 9,750 |
| M4C retrieval passages | 6,009 |
| Passage roles | 2,672 standards / 627 reviewer / 2,710 vendor |
| SQLite stores passing `PRAGMA quick_check` | 3/3 |
| Offline system + ER-1 tests | 25/25 |

The parser retains 126 `ALIGNMENT_FAILED` and seven `UNSUPPORTED_TABLE_HEADERS` diagnostics. These are explicit limitations, not silent source loss.

## Executive finding

RegModelTrace does not need a new parser or a second RAG pipeline. Its reusable foundation is strong:

- immutable recovered PDFs and recorded hashes;
- deterministic pages, blocks, hierarchy, tables, and source geometry;
- deterministic assertions and passages;
- role-partitioned BM25 + dense + RRF retrieval;
- host-owned evidence references and strict output validation;
- bounded Qwen synthesis;
- synthetic ER-1 source-resolution and stage-accounting instrumentation.

The missing product is the reviewer workflow that connects those pieces. The active service cannot currently perform VS-1 end to end because:

1. no formal `CorpusSnapshot` exists;
2. historical index manifests are not bound to a runtime `IndexBuildManifest`;
3. `system_v1.json` points to missing compact-release paths rather than the recovered versioned retrieval assets;
4. the ER-1 provenance resolver is validated only on synthetic fixtures and does not verify a real physical PDF at resolution time;
5. the FastAPI service exposes only `/health` and `/ask`;
6. the existing workbench is a static replay, not a live retrieval-only product;
7. PDF navigation uses remote page links and lacks authoritative local hash/page/geometry resolution;
8. human review actions have no persistent reloadable product store;
9. broader search and human-readable evidence-packet export are absent.

## Capability matrix

| Capability | Status | Evidence | VS-1 action |
|---|---|---|---|
| Original PDF custody | `IMPLEMENTED` | recovered PDF tree; ER-1 recovery report; 45 files / 33 hashes | `REUSE` |
| Deterministic parser | `IMPLEMENTED` | `regmodeltrace/src/parse/parser.py`; processed manifest/Parquet | `REUSE` |
| Canonical pages and hashes | `IMPLEMENTED` | `source_pages.parquet` | `REUSE` |
| Geometry/line alignment | `IMPLEMENTED` | `parsed_blocks.parquet`; diagnostics | `WIRE` |
| First-class product SourceSpan | `IMPLEMENTED_BUT_NOT_PRODUCTIZED` | parser spans + ER-1 synthetic receipts | `WIRE` |
| Assertions/passages | `IMPLEMENTED` | extraction modules; M4 foundation DB; M4C passages | `REUSE` |
| `CorpusSnapshot` | `NOT_IMPLEMENTED` | only precursor manifests exist | `IMPLEMENT` |
| Source-document registry | `PARTIALLY_IMPLEMENTED` | fragmented corpus manifests and DB documents | `WIRE` |
| `IndexBuildManifest` runtime identity | `PARTIALLY_IMPLEMENTED` | historical embedding/ranking manifests | `WIRE` |
| Hybrid three-role retrieval | `IMPLEMENTED_BUT_NOT_PRODUCTIZED` | `retrieval.py`; recovered indexes and vectors | `WIRE` |
| Per-run document scope before retrieval | `PARTIALLY_IMPLEMENTED` | fixed roles + resolver allowlist only | `WIRE` |
| Full retrieval stage-loss trace | `SYNTHETICALLY_VALIDATED_ONLY` | ER-1 synthetic ledger | `IMPLEMENT` |
| Candidate packet | `SYNTHETICALLY_VALIDATED_ONLY` | ER-1 synthetic packet | `WIRE` |
| Context payload accounting | `SYNTHETICALLY_VALIDATED_ONLY` | ER-1 synthetic context manifest | `WIRE` |
| Authoritative provenance resolver | `SYNTHETICALLY_VALIDATED_ONLY` | `evidence_recovery/source.py`; fixtures | `IMPLEMENT` |
| Host evidence-ID validation | `IMPLEMENTED` | `contracts.py`; `service.py`; tests | `REUSE` |
| Bounded Qwen synthesis | `IMPLEMENTED` | generation/service contracts and saved runs | `DEFER` until Gate C |
| Live service | `PARTIALLY_IMPLEMENTED` | `/health`, `/ask` only | `IMPLEMENT` |
| Static evidence demo | `IMPLEMENTED_BUT_NOT_PRODUCTIZED` | `demo/` | `REUSE` |
| Retrieval-only evidence workbench | `NOT_IMPLEMENTED` | static demo is not live retrieval | `IMPLEMENT` |
| Original-PDF navigation | `PARTIALLY_IMPLEMENTED` | remote `#page` links only | `IMPLEMENT` |
| Human disposition persistence | `SYNTHETICALLY_VALIDATED_ONLY` | append-only fixture behavior only | `IMPLEMENT` |
| Controlled broader search | `NOT_IMPLEMENTED` | no parent-linked rerun path | `IMPLEMENT` |
| Machine-readable case export | `SYNTHETICALLY_VALIDATED_ONLY` | ER-1 sidecar export | `WIRE` |
| Human-readable case export | `NOT_IMPLEMENTED` | no `evidence_packet.md` exporter | `IMPLEMENT` |
| Real-corpus PDF round trip | `NOT_IMPLEMENTED` | assets exist; no persisted real receipt | `IMPLEMENT` |
| Real recovery benchmark | `NOT_IMPLEMENTED` | explicitly `NOT_RUN` in ER-1 | `DEFER` |
| Longitudinal/as-of review | `OUT_OF_SCOPE_FOR_VS1` | deferred by spec | `DEFER` |
| Ray optimization | `OUT_OF_SCOPE_FOR_VS1` | systems lane closed | `DEFER` |
| GraphRAG/agents | `OUT_OF_SCOPE_FOR_VS1` | not required | `DEFER` |

The machine-readable inventory contains the exact repository paths, artifact paths, verification methods, limitations, and actions for every row.

## Material reconciliation details

### Recovered artifacts are present but not bound to the service

The production service expects:

```text
regmodeltrace/data/retrieval/passages.jsonl
regmodeltrace/data/retrieval/passages.sqlite
regmodeltrace/data/retrieval/records.sqlite
regmodeltrace/data/retrieval/embedding/manifest.json
regmodeltrace/data/retrieval/embedding/passages.npy
regmodeltrace/data/retrieval/embedding/passage_ids.json
```

Those paths do not exist. Equivalent historical assets are available under versioned locations such as:

```text
regmodeltrace/data/retrieval/m4-foundation-v1.sqlite
regmodeltrace/data/retrieval/m4c-v1/passages.sqlite
regmodeltrace/data/retrieval/m4c-v1/passages.jsonl
regmodeltrace/data/retrieval/m4c-v1/embedding-run/
```

This is a product wiring gap. It must be solved with explicit snapshot/build binding, not by copying files into ambiguous legacy paths.

### ER-1 is valuable but remains synthetic for the VS-1 source path

ER-1 already demonstrates:

- fail-closed assertion/passage identity checks;
- canonical text hash and character-span checks;
- printed-page and physical-page separation;
- context-packing loss attribution;
- append-only attempt/review event behavior;
- no-gold reports with `recall = null`.

Its current `SourceResolver` accepts in-memory dictionaries. It does not yet verify the real local PDF file and hash as part of resolution, and its persisted receipts are synthetic. It should be adapted as the basis of the VS-1 resolver rather than replaced.

### Existing UI is a reusable visual shell, not the vertical slice

The static demo presents preserved questions, claims, evidence cards, and remote PDF page links. It does not create a case, run retrieval, expose discarded candidates, open a hash-verified local source, persist dispositions, or export the current review session. It can provide layout components, but it cannot be accepted as the retrieval-only workbench.

## Gate A disposition

```text
INVENTORY_COMPLETE      = YES
INVENTORY_GROUNDED      = YES
RECONCILIATION          = COMPLETE_WITH_MATERIAL_GAPS_IDENTIFIED
IMPLEMENTATION_STARTED  = NO
RECOMMENDATION          = READY_FOR_PROJECT_OWNER_REVIEW
```

The inventory gate is complete. Gate B is not yet satisfied. The next bounded implementation, if separately approved, should freeze the three-document `CorpusSnapshot` and bind a real-corpus authoritative resolver before any workbench or Qwen changes.

No Task 1 or later VS-1 work was performed.
