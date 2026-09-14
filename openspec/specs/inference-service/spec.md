# inference-service Specification

## Purpose
Define the stable local RAG application contract, runtime reuse, citation ownership, and bounded uncertainty behavior.
## Requirements
### Requirement: one callable application contract

The system SHALL expose a stable `ask(question)` operation that returns an answer, evidence status, and host-resolved evidence.

#### Scenario: a valid question is answered

- **WHEN** a caller submits a nonempty question
- **THEN** the system returns only the public answer contract
- **AND** every evidence item includes document identity, role, page, exact quote, and source URL

### Requirement: long-lived runtime components

The system SHALL reuse loaded retrieval indexes, query encoder, and generation engine across calls on one instance.

#### Scenario: two questions are asked sequentially

- **WHEN** the second call begins
- **THEN** the passage index and models are not initialized again

### Requirement: host-owned citation identity

The model SHALL select only request-scoped evidence handles, and the host SHALL create all public citation markers and source metadata.

#### Scenario: a model returns an unknown evidence handle

- **WHEN** strict output validation encounters the handle
- **THEN** the call fails explicitly
- **AND** no public answer is produced

### Requirement: bundle-scoped uncertainty

The system SHALL preserve the distinction between evidence missing from a retrieved bundle and evidence absent from the corpus.

#### Scenario: a requested link is not established

- **WHEN** the supplied evidence does not establish the link
- **THEN** the response may use `UNRESOLVED_FROM_RETRIEVED_EVIDENCE`
- **AND** it SHALL NOT claim corpus absence or nonoccurrence

### Requirement: locally deployable service

The system SHALL expose the same application contract through Python and a local HTTP endpoint without requiring an external model API.

#### Scenario: the service is ready

- **WHEN** the local model and retrieval components have initialized
- **THEN** `GET /health` reports readiness
- **AND** `POST /ask` returns the Python contract shape
