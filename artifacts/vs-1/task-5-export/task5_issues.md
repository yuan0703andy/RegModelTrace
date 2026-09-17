# VS-1 Task 5 issue log

- The first direct builder run could not import the repository package because
  the entrypoint did not add the repository root to `sys.path`. The entrypoint
  was corrected before artifact creation; no partial export was retained.
- The checked-in dispositions are product-QA events, not human adjudication or
  regulatory-compliance judgments.
- Candidate scope remains `RETURNED_RETAINED_CANDIDATES_ONLY`; the export cannot
  establish historical retrieval recall or fixed-corpus absence.
- SQLite append-only protection remains an application/local-database control,
  not cryptographic tamper evidence against the filesystem owner.
- Reviewer identity remains self-declared; multi-user authentication is out of scope.
- `PAGE_ONLY` remains contract-tested but lacks a real-corpus case.
- Broader search remains deferred, so `NEED_BROADER_SEARCH` is recorded but does
  not launch a child retrieval run.
- The pre-existing Starlette TestClient/httpx deprecation warning remains open.
- On restricted macOS execution, a transitive CPU-info probe logged non-fatal
  `sysctlbyname` permission warnings during artifact generation. Outputs and
  verification completed successfully; no correctness failure was observed.
- The in-app browser blocks direct navigation to the attachment response, while
  clicking the workbench export link downloads the same JSON packet successfully.
- One composite browser action timed out after its POST had already completed.
  The retry created a second append-only QA event. No event was overwritten; UI
  automation should confirm each write before retrying a composite interaction.
