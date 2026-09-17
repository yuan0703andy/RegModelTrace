# VS-1 Task 5 — Evidence and audit export

Status: `PASS`; repository custody verified at
`b4329467b179b860756520741f58980c420a5a96`.

The frozen Florida case exported 9 candidates and
3 explicitly QA-only review events to JSON,
Markdown, and append-ordered JSONL. All candidates were re-resolved against the
authoritative corpus before export. Frozen retrieval-stage ledgers were preserved
exactly; human decisions remain a separate event layer. Repeating export against
the same database state produced byte-identical outputs.

A real browser smoke created a QA review session, persisted a disposition,
displayed JSON/Markdown/JSONL export links, and downloaded the JSON evidence
packet through the workbench. The browser events are separate synthetic QA data;
they are not included in the checked-in deterministic export fixture.

Export ID: `EP_e1bf36bdbc19c84d499fa22f`
Packet SHA-256: `e1bf36bdbc19c84d499fa22fbc520200abd7a72dd3585972a762ec6d862f349c`

No Qwen, retrieval execution/tuning, embedding rebuild, Ray, broader search, or
statistical research ran. The artifacts demonstrate product plumbing, not human
evidence truth. The bounded Gate C acceptance step also passed with declared
limitations.
