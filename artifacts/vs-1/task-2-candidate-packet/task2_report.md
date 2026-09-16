# VS-1 Task 2 — Evidence Stage Ledger and Candidate Packet

**Status:** `PASS`
**Retrieval run:** `RR_861400a826be9e9aa4a2d0d0`
**Corpus snapshot:** `CS_815122cca84bcfd9c1637df6`
**Index build:** `IB_e922be7973b49bb13e2b340a`

## Result

- replayed the frozen Q1 retrieval result; retrieval was not rerun;
- persisted one `RetrievalRun` and 9 `CandidateEvidence` records;
- preserved BM25 rank, dense rank, RRF score, role rank, passage identity, and source provenance;
- preserved all three document roles: `{'STANDARDS': 3, 'PROFESSIONAL_TEAM_REPORT': 3, 'VENDOR_SUBMISSION': 3}`;
- assigned stable candidate IDs bound to corpus, index build, question, and passage;
- recorded all eight stages with `NOT_REACHED | YES | NO` semantics;
- all model and downstream stages remain `NOT_REACHED` in retrieval-only mode;
- replayed and validated the serialized packet without retrieval;
- verified fixtures for `RETRIEVAL_MISS`, `RANKING_LOSS`,
  `CONTEXT_PACKING_LOSS`, and `MODEL_NON_SELECTION`.

## Issue found and resolved

`MULTI_ASSERTION_PASSAGE_SEPARATOR_MISMATCH`: the Task 1 resolver accepted
space-joined assertion text, while some canonical passages use newline joins.
The resolver now accepts either deterministic separator while continuing to
require an exact match to the frozen passage text. A real four-assertion
passage regression test covers the fix.

## Boundaries

```text
new model inference runs = 0
retrieval executed in Task 2 = false
retrieval behavior changed = false
embedding rebuilt = false
retrieval tuned = false
```

The saved RAG v0 artifact exposes returned/retained passages, not the complete
discarded ranking universe. The packet therefore declares
`candidate_universe_scope = RETURNED_RETAINED_CANDIDATES_ONLY` and does not
invent ranking-loss events for candidates that the saved result did not record.
