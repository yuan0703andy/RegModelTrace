# Task 4 — Human disposition persistence

Status: PASS. The owner-requested structured reason-code contract is applied.
Repository custody for the implementation is verified at
`6bf7a70bb11d1d86025d849e11065a92a9e2f9e4`.

Implemented a local SQLite review store, session/history API, and a minimal
review form in the existing workbench. ACCEPTED / REJECTED / UNRESOLVED refer
to candidate usefulness for the question, not regulatory compliance. A structured
reason code and human rationale are required and stored separately from the
decision. Revisions append events, identical retries reuse the saved event,
and stale writes fail with a conflict. Host owns source and run identities.
Frozen candidate packets and their stage ledgers remain unchanged.

Verification: 74 tests passed; targeted Ruff, Python compile, JavaScript syntax,
and OpenSpec strict validation passed. A browser smoke test opened a frozen
candidate, created and restored a session, persisted an initial decision and a
revision across reloads, and showed a visible conflict for a stale second-tab
write. The included persistence receipt uses a
real frozen candidate but an explicitly synthetic QA decision in a temporary
database. All browser and persistence events are explicitly labeled product QA;
they do not establish human verification.

Runtime: launch `python -m uvicorn regmodeltrace.workbench_server:app --host
127.0.0.1 --port 8765` from the repository. The default database is
`~/.local/share/regmodeltrace/reviews.sqlite3`; RMT_REVIEW_DB overrides its path.
Sessions resume using browser local storage. Reviewer identity is self-declared,
not authenticated. This is a local single-user deployment, not a public service.
The database is mutable by its filesystem owner; append-only guarantees are
application/SQLite controls, not cryptographic tamper evidence.

The pre-existing TestClient deprecation warning remains non-blocking.
Task 3 precision and candidate-universe limitations remain unchanged.
No Qwen, retrieval execution/tuning, embeddings, Ray, broader search, or export
was added. Gate C remains NOT_YET_PASS: evidence/audit export is still absent.
