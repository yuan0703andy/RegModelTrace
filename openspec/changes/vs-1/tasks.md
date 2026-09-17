# VS-1 Tasks

## Authorization boundary

Tasks 0–2 are accepted; Gates A and B passed. Task 1/2 repository custody
is verified at `842e404f0cbb1301c0940314f10a37e2c0f808e0`.
Task 3 is accepted locally; this change performs its authorized custody checkpoint.
Task 4 human-disposition persistence is authorized by the project owner. Gate C is not yet passed.

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

**Status: accepted; repository custody verified at the baseline commit.**

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

## Task 3 — Retrieval-only workbench and PDF navigation

**Status: accepted; repository custody verified at `2d79734d7ea525a60fb3228007afeb92eeb10334`.**

- [x] replay the frozen Task 2 retrieval run and display all 9 candidates;
- [x] show case, corpus, index-build, candidate, retrieval-score, and stage identities;
- [x] resolve each candidate against authoritative local PDFs;
- [x] navigate by one-based physical PDF page;
- [x] render exact verified geometry as source highlights;
- [x] display `PAGE_TEXT` / `PAGE_ONLY` fallback without fabricated highlights;
- [x] fail closed for unknown candidate and out-of-binding page identities;
- [x] run without Qwen, retrieval execution, or human-disposition persistence.

Task 3 limitations: `EXACT_GEOMETRY` and `PAGE_TEXT` are real-corpus verified;
`PAGE_ONLY` is a contract path, not real-corpus verified. Candidate universe is
`RETURNED_RETAINED_CANDIDATES_ONLY`. Browser interaction QA is not human
adjudication and does not set `HUMAN_VERIFIED`. Gate C still requires persistent
human dispositions and evidence/audit export.

## Task 4 — Human disposition persistence

**Status: accepted; repository custody verified at
`6bf7a70bb11d1d86025d849e11065a92a9e2f9e4`.**

Human disposition persistence is PASS. The structured reason-code contract and
browser smoke requested in owner review are complete. Task 5 remains pending;
Gate C is still NOT_YET_PASS.

74 tests passed; lint/compile/JavaScript syntax/OpenSpec validation passed.
Browser smoke passed for session restore, initial decision, revision, reload,
and visible stale-write conflict.
See `artifacts/vs-1/task-4-dispositions/task4_report.md`.
Gate C remains NOT_YET_PASS.

- review session;
- append-only dispositions;

Broader search remains deferred and outside Task 4.

## Task 5 — Export

Not authorized; requires a subsequent bounded approval.

- `evidence_packet.json`;
- `evidence_packet.md`;
- `audit_record.jsonl`.

## Task 6 — Vertical-slice acceptance

Not authorized; requires a subsequent bounded approval.

Run accepted fixtures and one bounded frozen Florida demo case.

## Task 7 — Bounded Qwen reconnection

Only after Gate C.

Reuse existing model/evidence contracts. No new model study.
