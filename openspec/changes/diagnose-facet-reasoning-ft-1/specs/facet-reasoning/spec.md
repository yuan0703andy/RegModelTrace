# facet-reasoning Specification

## Purpose

Separate multi-facet task representation, facet classification, and relation aggregation before considering weight adaptation.

## ADDED Requirements

### Requirement: atomic facet states

The research pipeline SHALL represent each applicable regulatory facet as `DEMONSTRATED`, `NOT_DEMONSTRATED`, `CONTRADICTED`, or `NOT_APPLICABLE`.

#### Scenario: vendor evidence omits one required facet

- **WHEN** bounded vendor evidence demonstrates one required facet but does not establish another
- **THEN** the omitted facet is `NOT_DEMONSTRATED`
- **AND** it is not called `CONTRADICTED` without conflicting evidence

### Requirement: actor functions remain separate

Reviewer scrutiny or verification SHALL NOT substitute for vendor demonstration.

#### Scenario: reviewer verifies a broad standard

- **WHEN** reviewer evidence covers the standard but vendor evidence omits one facet
- **THEN** that vendor facet remains `NOT_DEMONSTRATED`

### Requirement: host aggregation is prospective

The host SHALL aggregate frozen facet states using a rule fixed before model inference.

#### Scenario: mixed facet states

- **WHEN** evidence is sufficient, at least one required facet is `DEMONSTRATED`, and at least one is `NOT_DEMONSTRATED`
- **THEN** the host relation is `PARTIALLY_ALIGNED`

### Requirement: human truth precedes model evaluation

Facet truth SHALL be independently human adjudicated and frozen before Conditions B/C outputs are inspected.

#### Scenario: second human adjudication is unavailable

- **WHEN** only one or zero independent human return files exist
- **THEN** B/C evaluation remains blocked
- **AND** the FT-1 decision is `EVIDENCE_INCONCLUSIVE`

### Requirement: no training authorization by default

Condition D SHALL remain unauthorized unless Condition C retains meaningful, repeated facet-level model errors after all data gates pass.

#### Scenario: deterministic aggregation repairs the target failure

- **WHEN** Condition C sufficiently reduces false-`ALIGNED` errors without a safety regression
- **THEN** fine-tuning is not needed
