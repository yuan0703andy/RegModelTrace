## ADDED Requirements

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
