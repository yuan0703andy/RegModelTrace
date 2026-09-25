# Public RAG benchmark qualification

## ADDED Requirements

### Requirement: Independent tracks

Track A public-benchmark evaluation SHALL proceed independently of FG-3 case formation and SHALL NOT use FG-3 gold for method development or threshold selection.

#### Scenario: FG-3 has no frozen natural gold

- **WHEN** Track A benchmark artifacts are qualified
- **THEN** Track A may proceed to baseline planning without representing FG-3 as complete.

### Requirement: Benchmark-specific estimands

The study SHALL preserve retrieval, version-aware QA, and supplied-context generation as distinct tasks and SHALL NOT pool raw scores across them.

#### Scenario: LIT-RAGBench has supplied chunks

- **WHEN** LIT-RAGBench is evaluated
- **THEN** the reported result is generator behavior under supplied chunks, not retrieval performance.

### Requirement: Evidence availability

Gold-context and sufficient-context analyses SHALL require explicit evidence annotations or independent adjudication. A reference answer alone SHALL NOT count as a gold evidence set.

#### Scenario: VersionQA has only question and answer fields

- **WHEN** a gold-context control is requested
- **THEN** it remains unavailable until evidence is separately annotated.

### Requirement: Reproduction qualification

Published-method reproduction SHALL pin code, data, environment, and deviations. A reproduction that cannot meet its contract SHALL be labeled `REPRODUCTION_NOT_QUALIFIED`.

#### Scenario: Reference implementation requires unavailable services

- **WHEN** faithful execution cannot be completed
- **THEN** no negative method-performance conclusion is drawn from the incomplete run.
