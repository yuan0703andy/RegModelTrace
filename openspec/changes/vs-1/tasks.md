# VS-1 Tasks

## Authorization boundary

Task 0 and Task 1 are accepted; Gate A and Gate B passed. Task 2 is authorized
only for the evidence-stage ledger and candidate packet. Tasks after Task 2
remain pending.

---

## Task 0 — Implementation inventory

**Status: accepted.**

Create:

```text
artifacts/vs-1/implementation_inventory.json
artifacts/vs-1/implementation_inventory.md
```

Inspect and reconcile:

- active repository;
- recovered artifacts;
- ER-1 outputs;
- corpus recovery manifests/receipts;
- parser outputs;
- retrieval assets;
- demo/workbench;
- active freeze/release receipts.

Every capability must receive one status:

```text
IMPLEMENTED
IMPLEMENTED_BUT_NOT_PRODUCTIZED
SYNTHETICALLY_VALIDATED_ONLY
PARTIALLY_IMPLEMENTED
NOT_IMPLEMENTED
OUT_OF_SCOPE_FOR_VS1
```

Every `IMPLEMENTED*` claim must cite actual repository/artifact evidence and a verification method.

**Do not modify code or run inference during Task 0.**

---

## Task 1 — Freeze corpus/source contracts

**Status: accepted; Gate B passed.**

- [x] implement/verify `CorpusSnapshot`;
- [x] implement/verify `SourceDocument`;
- [x] implement/verify `SourceSpan`;
- [x] separate `IndexBuildManifest`.
- [x] bind recovered versioned passage, FTS, record-store, and embedding artifacts;
- [x] verify a real-corpus passage/assertion round trip through canonical page text
  and the original PDF hash;
- [x] persist source-authority manifests and a Task 1 verification receipt.

## Task 2 — Evidence-stage ledger and candidate packet

**Status: completed; pending owner review.**

- [x] persist `RetrievalRun`;
- [x] persist `CandidateEvidence`;
- [x] serialize saved BM25, dense, and RRF results without running or changing retrieval;
- [x] create stable candidate IDs bound to corpus, index build, question, and passage;
- [x] record all eight stages using `NOT_REACHED | YES | NO`;
- [x] keep model and downstream stages `NOT_REACHED` in retrieval-only mode;
- [x] distinguish retrieval miss, ranking loss, context-packing loss, and model
  non-selection with bounded fixtures;
- [x] verify packet replay without rerunning retrieval.

The authoritative provenance resolver, hash/page/span verification, geometry
warnings, and precision labels were completed and accepted under Task 1.

## Task 5 — Retrieval-only workbench

Pending approval after Task 0.

- case header;
- candidate list;
- trace inspector;
- source-resolution state;
- original-PDF action.

## Task 6 — PDF navigation

Pending approval after Task 0.

- exact geometry where available;
- page-text fallback;
- page-only fallback;
- precision display.

## Task 7 — Human disposition persistence

Pending approval after Task 0.

- review session;
- append-only dispositions;
- broader-search event.

## Task 8 — Export

Pending approval after Task 0.

- `evidence_packet.json`;
- `evidence_packet.md`;
- `audit_record.jsonl`.

## Task 9 — Vertical-slice acceptance

Pending approval after Task 0.

Run accepted fixtures and one bounded frozen Florida demo case.

## Task 10 — Bounded Qwen reconnection

Only after Gate C.

Reuse existing model/evidence contracts. No new model study.
