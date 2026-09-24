## ADDED Requirements

### Requirement: Frozen synthetic boundary diagnostic

The Qwen3.8 diagnostic SHALL keep model-facing source text separate from the
expected-label oracle and SHALL persist all raw responses before scoring.

#### Scenario: A synthetic classification is wrong

- **WHEN** a valid response selects the wrong evidence label
- **THEN** the raw response and wrong label remain in the report without
  modifying the frozen request or active service default.

#### Scenario: Diagnostic results are reported

- **WHEN** all requests finish or a runtime failure occurs
- **THEN** the report separates runtime/format validity from synthetic meaning
  and does not present synthetic accuracy as natural-document performance.
