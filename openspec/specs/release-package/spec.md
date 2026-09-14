# release-package Specification

## Purpose

Define the compact public project snapshot and the evidence boundaries it must preserve.

## Requirements

### Requirement: public release preserves final limitations

The release SHALL report partial-class failure, untested conflict detection, table-portability limits, probabilistic-readout limits, and Ray nondeterminism beside its successful results.

#### Scenario: final metrics are presented

- **WHEN** a reader reviews project outcomes
- **THEN** raw denominators and relevant limitations are visible without requiring the omitted research archive

### Requirement: large historical artifacts remain external

The release SHALL exclude raw PDFs, model weights, retrieval indexes, embeddings, and cluster logs from Git history.

#### Scenario: a reviewer clones the repository

- **WHEN** external artifacts are absent
- **THEN** the README states that historical GPU evaluations cannot be replayed from the compact snapshot alone

### Requirement: offline review remains possible

The release SHALL provide contract tests, a release verifier, final receipts, and a static evidence demo.

#### Scenario: no GPU is available

- **WHEN** a reviewer runs the offline checks
- **THEN** host-citation and output-contract tests execute without loading model weights
