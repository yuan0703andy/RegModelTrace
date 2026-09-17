# source-authority Specification

## Purpose
TBD - created by archiving change vs-1. Update Purpose after archive.
## Requirements
### Requirement: Corpus identity is independent of retrieval-build identity

The system SHALL identify a frozen source/canonical corpus with a
`CorpusSnapshot` and SHALL identify each rebuildable retrieval representation
with a separate `IndexBuildManifest` bound to that snapshot.

#### Scenario: Retrieval representation changes

- **WHEN** retrieval artifacts or retrieval configuration change without changing source files, parser identity, or canonical passage inventory
- **THEN** the `index_build_id` changes and the `corpus_snapshot_id` remains unchanged

#### Scenario: Source universe changes

- **WHEN** a source PDF, verified source hash, parser identity, or canonical passage inventory changes
- **THEN** the system creates a different `corpus_snapshot_id`

### Requirement: Source documents are hash-verified within the snapshot

Every `SourceDocument` in a valid snapshot SHALL resolve to an existing local
original whose SHA-256 equals the frozen document hash.

#### Scenario: Frozen source is intact

- **WHEN** the snapshot is verified
- **THEN** every declared local original exists and matches its recorded SHA-256

#### Scenario: Frozen source hash differs

- **WHEN** a declared original does not match its recorded SHA-256
- **THEN** snapshot verification fails closed and the document cannot be rendered as authoritative evidence

### Requirement: Recovered retrieval assets are explicitly bound

The system SHALL bind the recovered passage inventory, FTS database, record
store, embedding manifest, passage matrix, and passage-ID inventory to one
`IndexBuildManifest` without copying them into ambiguous legacy paths.

#### Scenario: Runtime build is verified

- **WHEN** an index-build manifest is created
- **THEN** every required artifact exists, its content hash is recorded, and the embedding manifest's declared passage and output hashes match the bound files

### Requirement: Provenance resolution returns to the authoritative PDF

The system SHALL resolve a passage, assertion, or source-span identity through
the canonical record and page text to the frozen original PDF and SHALL verify
the original file hash before reporting a successful authoritative resolution.

#### Scenario: Real-corpus passage round trip

- **WHEN** a known passage identity from the frozen Florida corpus is resolved
- **THEN** its assertion text, source span, canonical page text, physical page, document identity, and verified original-PDF hash agree

#### Scenario: Invalid or mismatched identity

- **WHEN** an identifier is absent from the snapshot or its source binding does not match
- **THEN** resolution fails closed and no fuzzy text substitute is used

### Requirement: Missing geometry degrades precision without invalidating text provenance

The system SHALL treat geometry as optional localization metadata. Valid
document, page, hash, and text binding remains resolved when exact geometry is
unavailable.

#### Scenario: Text provenance succeeds without geometry

- **WHEN** document hash, canonical page text, and source offsets verify but no exact regions are available
- **THEN** resolution returns `RESOLVED`, reports `PAGE_TEXT` or `PAGE_ONLY` precision as applicable, and includes `SOURCE_GEOMETRY_UNAVAILABLE` as a warning

### Requirement: Retrieval results persist as bound candidate packets

The system SHALL serialize every returned passage as stable `CandidateEvidence`
and SHALL bind one `RetrievalRun` to both the frozen `corpus_snapshot_id` and
the frozen `index_build_id`.

#### Scenario: Existing retrieval result is serialized

- **WHEN** a saved retrieval result is converted into a candidate packet
- **THEN** each candidate retains its passage, document, role, ranks, scores,
  source resolution, corpus snapshot, and index-build identity

#### Scenario: Packet is replayed

- **WHEN** a persisted candidate packet is loaded later
- **THEN** its identities and stage states validate without rerunning retrieval

### Requirement: Evidence stages use explicit tri-state semantics

Every candidate SHALL record `NOT_REACHED`, `YES`, or `NO` for `SEARCHABLE`,
`RETRIEVED`, `RETAINED_AFTER_RANKING`, `INCLUDED_IN_MODEL_CONTEXT`,
`MODEL_SELECTED`, `HOST_RESOLVED`, `DELIVERED_TO_HUMAN`, and `HUMAN_VERIFIED`.

#### Scenario: Retrieval-only execution

- **WHEN** retrieval completes but context packing and model execution do not run
- **THEN** all model and downstream stages are `NOT_REACHED`, not `NO`

#### Scenario: Executed stage loses evidence

- **WHEN** a reached stage records `NO`
- **THEN** the system attributes the loss to that stage and leaves later stages
  `NOT_REACHED`

### Requirement: Frozen candidates open authoritative source locations

The retrieval-only workbench SHALL load the frozen candidate packet and SHALL
resolve every displayed candidate through the frozen source authority before
displaying its original PDF or page preview.

#### Scenario: Candidate has exact geometry

- **WHEN** the reviewer selects a candidate whose source spans have verified
  geometry
- **THEN** the workbench opens the correct one-based physical PDF page and
  displays the exact source region as a highlight

#### Scenario: Candidate lacks exact geometry

- **WHEN** document, hash, page, and text provenance verify but source geometry
  is unavailable
- **THEN** the candidate remains `RESOLVED`, the workbench visibly reports
  `PAGE_TEXT` or `PAGE_ONLY`, and no exact highlight is fabricated

#### Scenario: Candidate identity is not authoritative

- **WHEN** a requested candidate, passage, document, or page falls outside its
  frozen binding
- **THEN** navigation fails closed without fuzzy source substitution

### Requirement: Workbench replay does not execute retrieval or a model

The first workbench fixture SHALL replay `RR_861400a826be9e9aa4a2d0d0`
without rerunning retrieval, changing rankings, or invoking Qwen.

#### Scenario: Reviewer opens the frozen case

- **WHEN** the workbench loads the Task 2 packet
- **THEN** it displays all 9 candidates and preserves their stable identity,
  retrieval metadata, tri-state ledger, corpus snapshot, and index build

### Requirement: Human dispositions persist without mutating frozen evidence

The workbench SHALL store review sessions and append-only candidate dispositions
separately from the frozen packet, with host-owned provenance, a structured
reason code, and required rationale. Decision outcome, reason code, and human
explanation SHALL remain separate fields.

#### Scenario: Reviewer revises a disposition

- **WHEN** a reviewer submits a decision with the current previous event identity
- **THEN** a new event is appended and the prior event remains readable

#### Scenario: Retry or stale edit

- **WHEN** an identical event is retried or a stale previous identity is submitted
- **THEN** the retry returns the saved event without duplication and the stale edit is rejected

### Requirement: Audit export preserves evidence and review boundaries

The system SHALL export frozen candidate evidence, authoritative provenance, and
append-only review events in machine-readable, human-readable, and event-stream
formats without changing source, retrieval, or review state.

#### Scenario: Export a reviewed frozen case

- **WHEN** a bound review session is exported
- **THEN** JSON, Markdown, and JSONL outputs preserve corpus, index, run,
  candidate, source, and disposition identities and state the candidate-universe
  limitation

#### Scenario: Review decision and retrieval ledger differ

- **WHEN** a candidate has a human review event but its frozen `HUMAN_VERIFIED`
  stage is `NOT_REACHED`
- **THEN** export preserves both facts separately and does not rewrite the ledger

#### Scenario: Authority changed after retrieval

- **WHEN** a candidate no longer resolves to its frozen source identity or quote
- **THEN** export fails closed and emits no completed packet
