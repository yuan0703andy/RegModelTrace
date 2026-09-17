# VS-1 Design

## 1. Identity model

Separate immutable corpus identity from rebuildable retrieval identity.

### CorpusSnapshot

Identifies authoritative source/canonical content:

```text
source manifest
parser identity
canonical passage inventory
```

It excludes retrieval-artifact build hashes.

### IndexBuildManifest

Identifies one retrieval representation built over a corpus:

```text
embedding model / revision
embedding artifacts
FTS artifacts
retrieval config
```

Every `RetrievalRun` binds both.

## 2. Provenance resolver

One authoritative resolver maps:

```text
assertion / passage / source span
→ document hash
→ physical page
→ canonical quote
→ source geometry when available
```

Terminal failures invalidate authoritative binding.

Geometry absence is a warning, not failure:

```json
{
  "status": "RESOLVED",
  "location_precision": "PAGE_TEXT",
  "warnings": ["SOURCE_GEOMETRY_UNAVAILABLE"]
}
```

## 3. Stage semantics

Stages use:

```text
NOT_REACHED
YES
NO
```

This prevents retrieval-only mode from being mislabeled as model failure.

A model-related `NO` is valid only if the model stage actually executed.

## 4. Reviewer workflow

```text
Case
→ RetrievalRun
→ CandidateEvidence[]
→ resolver
→ original PDF
→ ReviewDisposition[]
→ evidence packet
```

Qwen is not required for this path.

## 5. Persistence

Human dispositions are append-only events.

Broader search creates a new `RetrievalRun` with a parent pointer.

## 6. PDF navigation

Priority:

```text
exact geometry
→ page-text navigation
→ page-only navigation
```

Display the actual precision.

## 7. Retrieval fixtures

Ordinary product questions may validly have no relevant evidence in one or more roles.

Therefore the three-role acceptance test uses a predeclared frozen fixture known to contain relevant passages in all three roles.

## 8. Boundaries

No new retriever/model optimization is part of VS-1.

## Task 4 — Persistent reviewer decisions

Use a local SQLite store, separate from frozen artifacts. Sessions bind a
self-declared reviewer to the frozen run/corpus/index. Candidate decisions use
ACCEPTED, REJECTED, or UNRESOLVED. Each event also stores one structured reason
code (`RELEVANT_SUPPORT`, `IRRELEVANT`, `INSUFFICIENT_EVIDENCE`,
`MISSING_QUALIFICATION`, `WRONG_SOURCE`, `WRONG_VERSION`,
`NEED_BROADER_SEARCH`, or `OTHER`) and a required rationale. Each revision is
an append-only event; a caller event ID makes retries idempotent. A previous
event ID provides optimistic concurrency protection. Source resolution must
succeed before a decision is saved. Host supplies all provenance bindings.
Session history survives restarts. No frozen ledger is rewritten; these are
reviewer assertions, not independent certification or authenticated identity.
Local deployment only; no multi-user authentication is added in this task.

## Task 5 — Evidence and audit export

Export one review session into three host-generated representations:

```text
evidence_packet.json  machine-readable complete packet
evidence_packet.md    human-readable review packet
audit_record.jsonl    append-ordered session and disposition events
```

The JSON packet binds the frozen corpus snapshot, index build, retrieval run,
candidate identities, exact source resolution, retrieval metadata, unchanged
stage ledgers, review session, and append-only disposition history. The latest
event is exposed separately as a convenience view without deleting history.

Export re-resolves each candidate against source authority and fails closed on
identity, quote, document, or session-binding mismatch. For fixed packet and
review database state, repeated export is byte-identical. Export never executes
retrieval, invokes a model, or mutates the review database or frozen packet.

Human disposition state remains separate from the frozen retrieval-stage ledger.
An `ACCEPTED` candidate means useful for the displayed question; export SHALL NOT
rewrite `HUMAN_VERIFIED` or infer regulatory compliance. The packet SHALL state
that its universe is `RETURNED_RETAINED_CANDIDATES_ONLY` and cannot establish
historical retrieval recall or fixed-corpus absence.
