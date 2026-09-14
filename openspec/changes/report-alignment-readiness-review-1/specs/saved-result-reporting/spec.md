## ADDED Requirements

### Requirement: Saved-result metrics are identity-bound and read-only

The reporting workflow SHALL derive every certified metric from persisted truth, predictions, and frozen scorer outputs joined by corpus and case identity. It SHALL NOT execute inference, change semantic truth, or mutate historical artifacts.

#### Scenario: Complete saved fixture

- **WHEN** frozen truth, model results, and scorer rows contain the same unique case identities
- **THEN** the reporter produces separate primary and adverse-control metrics and records the hashes of all certified inputs

#### Scenario: Identity mismatch

- **WHEN** a case is missing, duplicated, or mismatched across truth, predictions, and scores
- **THEN** the affected metric fails certification instead of being joined by row order or approximate text

### Requirement: Classification metrics conserve failures and undefined values

The reporting workflow SHALL retain invalid outputs in terminal accounting, condition relation scoring on human-truth sufficiency, and serialize undefined class metrics as null with an explicit reason.

#### Scenario: Unsupported relation class

- **WHEN** a relation class has neither truth support nor predictions
- **THEN** precision, recall, and F1 are reported as untested and undefined rather than successful

#### Scenario: Sufficiency undercall

- **WHEN** truth is sufficient but the model predicts insufficient
- **THEN** the case remains in the conditional relation denominator and is separately counted as a sufficiency-stage joint loss

### Requirement: Storage inventory is read-only and scope-aware

The reporting workflow SHALL inspect SQLite through read-only immutable connections and SHALL distinguish SQL rows, file artifacts, logical documents, physical PDF copies, unique content hashes, machine candidates, and human-adjudicated comparisons.

#### Scenario: FTS shadow tables

- **WHEN** an SQLite store contains FTS5 virtual and shadow tables
- **THEN** shadow-table rows are excluded from evidence-record counts

### Requirement: Future designs grant no implementation authority

The LoRA, identified-vendor ingestion, and sequential-audit outputs SHALL remain design documents and SHALL preserve the closed release and zero-training boundary.

#### Scenario: REVIEW-1 closes

- **WHEN** reports, inventories, designs, and integrity checks pass with documented limitations
- **THEN** closure records `REPORTING_ONLY = TRUE`, `NEW_INFERENCE_RUNS = 0`, `TRAINING_AUTHORIZATION = NONE`, and `NEXT_RELEASE_IMPLEMENTATION = NOT_AUTHORIZED`
