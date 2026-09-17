# VS-1 Task 3 - Retrieval-Only Workbench and PDF Navigation

**Status:** `PASS`
**Baseline commit:** `842e404f0cbb1301c0940314f10a37e2c0f808e0`
**Retrieval run:** `RR_861400a826be9e9aa4a2d0d0`

## Verified

- all 9 frozen candidates load without running retrieval;
- stable passage, document, role, rank, score, and stage-ledger metadata are displayed;
- all 9 candidates resolve through the frozen source authority to hash-verified local PDFs;
- every candidate opens the correct one-based physical PDF page;
- all 9 candidates expose exact geometry and visible highlight regions;
- page images render from the authoritative PDFs, not copied preview files;
- the real degraded-geometry control remains `RESOLVED` at `PAGE_TEXT` precision
  with `SOURCE_GEOMETRY_UNAVAILABLE` and no fabricated highlight;
- unknown candidates and out-of-binding pages fail closed without fuzzy substitution.

## Verification scope and limitations

Task 3 owner review is `ACCEPTED_LOCALLY`; repository custody requires the
commit/push checkpoint. The `PASS` above describes local verification only.
Gate C remains `NOT_YET_PASS` pending persistent human dispositions and
an evidence/audit export.

- `EXACT_GEOMETRY` and `PAGE_TEXT`: real-corpus verified.
- `PAGE_ONLY`: contract path only; not real-corpus verified.
- Candidate universe: `RETURNED_RETAINED_CANDIDATES_ONLY`. This run does not
  reconstruct historical pre-ranking losses or establish retrieval recall.
- Browser interaction checks are product QA, not human adjudication. Opening
  a source does not set `HUMAN_VERIFIED`.

## Known non-blocking issue

The installed FastAPI/Starlette `TestClient` emits an `httpx` compatibility
deprecation warning. This is limited to the test harness and does not affect
the Uvicorn workbench runtime. Track it for a later dependency refresh; it is
not a reason to change Task 3 behavior or dependencies now.

## Boundaries

```text
Qwen = off
retrieval executed = false
human disposition persistence = not implemented
broader search = not implemented
retrieval tuning = false
new embeddings = false
Ray = off
```

Task 3 establishes the reviewer surface from `CandidateEvidence` through the
authoritative original PDF and correct source location. It does not yet record
human decisions or create broader-search runs.
