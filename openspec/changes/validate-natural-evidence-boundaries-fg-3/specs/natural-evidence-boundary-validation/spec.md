## ADDED Requirements

### Requirement: Prospective source-only discovery
FG-3 SHALL freeze the documents, deterministic search queries, inclusion rules, deduplication, candidate cap, and stopping condition before natural source screening. Candidate discovery SHALL NOT use model correctness or expected difficulty.

#### Scenario: Search reaches the predeclared stop
- **WHEN** all frozen panel queries have been executed on the frozen document set
- **THEN** discovery closes under the predeclared rule even if the selected leads contain few or no difficult cases

### Requirement: Exact-context human sufficiency
FG-3 SHALL admit a natural case to primary semantic evaluation only when independent adjudicators can derive the frozen judgment from the identical evidence packet that the model will receive.

#### Scenario: Human needs omitted context
- **WHEN** an adjudicator requires source material outside the model-facing packet to reach the proposed judgment
- **THEN** the case is marked `HUMAN_CONTEXT_INSUFFICIENT` and excluded from the primary semantic analysis

### Requirement: Predeclared natural-case pairing
FG-3 SHALL freeze a source-unit and cross-document pairing rule before interpreting selected page leads. The rule SHALL preserve all candidates at the first applicable pairing tier and group repeated or substantially equivalent source claims into dependency clusters.

#### Scenario: Reviewer and vendor passages share only a broad topic
- **WHEN** a reviewer action and vendor revision both mention a hurricane model but lack a confirmed shared substantive object
- **THEN** the record is marked `UNRESOLVED` or `NOT_SAME_OBJECT` for pairing and cannot establish review-caused model modification

#### Scenario: Two standards cycles repeat one requirement
- **WHEN** 2021 and 2023 cases derive from an exact or substantially equivalent clause
- **THEN** they share a case dependency cluster and are not counted as independent replications

### Requirement: Auditable model correctness
FG-3 SHALL report verdict agreement, evidence localization, and joint auditable correctness separately. A correct verdict with a citation that does not support it SHALL fail the joint metric.

#### Scenario: Challenge label cites neutral review
- **WHEN** a model predicts `CHALLENGE_ESTABLISHED` but cites only a passage documenting ordinary scrutiny
- **THEN** label agreement may be true while joint auditable correctness is false

### Requirement: Frozen repeatability and blinded mechanism coding
FG-3 SHALL qualify repeated-run stability on exposed synthetic inputs before natural inference and SHALL blind checkpoint identity during dual-human post-hoc failure-mode coding.

#### Scenario: Identical synthetic request produces a label flip
- **WHEN** the pre-natural repeatability qualification detects a semantic flip
- **THEN** the natural repetition and aggregation rule is frozen before any natural outcome is inspected
