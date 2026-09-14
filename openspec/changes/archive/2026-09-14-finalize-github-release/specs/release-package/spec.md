## ADDED Requirements

### Requirement: Public release package preserves evidence boundaries

The public package SHALL preserve final metrics, known failures, provenance design, and release status while excluding large local research artifacts.

#### Scenario: Historical data is omitted

- **WHEN** raw PDFs, model outputs, or cluster logs are not included on GitHub
- **THEN** the README identifies the omission and does not claim that the compact repository alone reproduces the historical inference runs

### Requirement: Public release is executable without hidden evaluation data

The package SHALL provide offline contract tests and a static evidence demo that do not require private paths, model weights, or cluster access.

#### Scenario: Reviewer checks the repository

- **WHEN** a reviewer installs the lightweight development dependencies
- **THEN** contract tests run locally and the demo can be served as static files

### Requirement: Publication retains adverse results

The release narrative SHALL include partial-class failure, untested conflict detection, KCC table-portability failure, probability limitations, and Ray nondeterminism.

#### Scenario: Portfolio summary is rendered

- **WHEN** the system's achievements are summarized
- **THEN** limitations appear beside the corresponding claims rather than only in an inaccessible archive
