# Assertion classification

## Purpose

Classify complete deterministic source assertions with host-owned identity. Accepted M3.6 scope is ASSERTION_CLASSIFICATION_ON_FIXED_16; the final receipt is regmodeltrace/data/evaluation/m3_classification_freeze.json.

## Requirements

### Requirement: Host-owned identity
The model SHALL predict only evidence_type. The host SHALL supply the assertion ID, source wording and provenance and SHALL verify request-response binding before attaching a label.

#### Scenario: Correct role without a generated identifier
- **WHEN** a valid single-field result is bound to the originating request
- **THEN** its identifier is taken from the host request
- **AND** source wording, actor and location remain deterministic

### Requirement: Frozen acceptance scope
Two independent fixed-configuration executions SHALL each yield sixteen valid and correct primary labels with identical host-bound critical fields before M3 freezes.

#### Scenario: Both runs pass
- **WHEN** first and repeat independently pass with stable critical fields
- **THEN** M3 is frozen and extraction tuning stops
- **AND** retrieval and relations remain separately evaluated in M4 and M5
