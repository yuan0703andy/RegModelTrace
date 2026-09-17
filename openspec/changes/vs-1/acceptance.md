# VS-1 Acceptance

## Gate A — Inventory

Pass when:

- inventory files exist;
- every capability has a formal status;
- every `IMPLEMENTED*` claim is grounded in actual repo/artifact evidence;
- recovered/public state conflicts are documented.

Until Gate A passes:

```text
NO CODE CHANGES
NO INFERENCE
NO RETRIEVAL TUNING
NO UI-ARCHITECTURE CHANGES
```

## Gate B — Source authority

Pass when:

- a frozen `CorpusSnapshot` exists;
- source hashes verify;
- `IndexBuildManifest` is separate;
- authoritative provenance round trip passes;
- missing geometry returns `RESOLVED` with warning/downgraded precision.

## Gate C — Retrieval-only reviewer workflow

Pass when:

- retrieval candidates serialize;
- tri-state stage trace is correct;
- frozen three-role fixture passes;
- original PDF opens at correct page/location precision;
- human dispositions persist;
- evidence/audit export works.

## Gate D — Qwen reconnection

Pass only after Gate C.

Requirements:

- only host-provided evidence refs accepted;
- source/page/hash fields remain host-owned;
- reviewer can reject semantically unsupported generated claims.

---

## Acceptance tests

### Identity
- corpus rebuild-independent identity test;
- retrieval rebuild produces new `index_build_id` without changing corpus identity.

### Provenance
- exact source round trip;
- hash mismatch fails closed;
- geometry unavailable is warning, not failure;
- invalid ID never triggers fuzzy substitution.

### Stage trace
- retrieval-only model stages are `NOT_REACHED`;
- true stage loss is recorded at correct reached stage.

### Role-aware retrieval
- use a frozen fixture known in advance to contain relevant passages in all three roles;
- require expected role preservation only on that fixture;
- ordinary no-hit roles are allowed.

### Review/export
- review events are append-only and survive reload;
- broader search creates a child retrieval run;
- export binds corpus + index build + retrieval runs + provenance + dispositions.

## Final vertical-slice criterion

VS-1 eventually passes when one frozen Florida case can complete:

```text
select frozen corpus
→ ask one regulatory question
→ retrieve role-aware candidates
→ inspect retrieval trace
→ open candidates in authoritative PDFs
→ record human disposition
→ persist state
→ export audit packet
```

without requiring a new model, retrieval tuning, Ray optimization, or statistical research.

## Task 4 bounded acceptance

Verify persistence after reopening the store, append-only revisions, identical
retry deduplication, conflicting retries and stale revisions rejected, unknown
session/candidate rejected, required reviewer/reason code/rationale validated, and exact
host-owned run/corpus/index/passage bindings. Source failure prevents writes.
Read-only navigation must create no disposition. Test data is product QA, not
human adjudication. Gate C remains pending evidence/audit export.
