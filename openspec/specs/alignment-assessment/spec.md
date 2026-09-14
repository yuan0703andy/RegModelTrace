# alignment-assessment Specification

## Purpose

Define documentary comparison between applicable regulatory requirements, vendor demonstration, and reviewer coverage.

## Requirements

### Requirement: sufficiency precedes relation

The system SHALL decide whether the request-scoped vendor evidence is sufficient before assigning an alignment relation.

#### Scenario: vendor evidence is incomplete

- **WHEN** a required facet is not demonstrated by the bounded vendor evidence
- **THEN** reviewer verification does not automatically fill that facet
- **AND** insufficient evidence is not labeled as conflict

### Requirement: applicable facets preserve normative logic

The system SHALL retain AND facets, OR alternatives, applicability conditions, exceptions, and version/time scope.

#### Scenario: regulation permits an alternative method

- **WHEN** the requirement permits either of two evidence bases
- **THEN** the vendor is not required to demonstrate both alternatives

### Requirement: relation classes remain distinct

The substantive relation SHALL use `ALIGNED`, `PARTIALLY_ALIGNED`, or `CONFLICT` only when the evidence is sufficient and the dimension is prescribed.

#### Scenario: implementation method is not prescribed

- **WHEN** a vendor uses a different method while demonstrating the prescribed output requirement
- **THEN** method difference alone does not establish partial alignment or conflict

### Requirement: model confidence does not establish compliance

Forced-choice token scores SHALL be reported as interface outputs rather than calibrated epistemic probabilities.

#### Scenario: candidate score is near one

- **WHEN** one candidate receives a near-unit normalized token score
- **THEN** the result remains bounded by the evidence, task contract, and human truth process

