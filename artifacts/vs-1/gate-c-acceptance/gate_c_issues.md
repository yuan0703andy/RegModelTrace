# VS-1 Gate C issue ledger

No blocking failure remains in the bounded retrieval-only vertical slice.

Open limitations:

- The historical candidate universe contains returned/retained candidates only.
- Product-QA dispositions prove workflow behavior, not evidence truth.
- Reviewer identity is self-declared and the SQLite file is not cryptographically tamper-evident.
- `PAGE_ONLY` lacks a real-corpus example; `PAGE_TEXT` and exact geometry are verified.
- Broader search remains deferred and no child retrieval run is created.
- Existing TestClient/httpx and restricted-macOS CPU-info warnings remain non-blocking.
- The in-app browser requires attachment download through the workbench link;
  direct attachment navigation is client-blocked but does not affect export.

These limitations constrain claims and future deployment; none invalidates the
local, single-user, retrieval-only Gate C contract.
