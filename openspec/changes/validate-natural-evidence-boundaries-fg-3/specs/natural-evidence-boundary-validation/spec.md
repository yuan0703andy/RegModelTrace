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
- **THEN** the case is marked `PACKET_INSUFFICIENT` if the allowed source record contains the omitted evidence, or `SOURCE_INDETERMINATE` if it does not establish the judgment and excluded from the primary semantic analysis

### Requirement: Predeclared natural-case pairing
FG-3 SHALL freeze a source-unit and cross-document pairing rule before interpreting selected page leads. The rule SHALL preserve all candidates at the first applicable pairing tier and group repeated or substantially equivalent source claims into dependency clusters.

#### Scenario: Reviewer and vendor passages share only a broad topic
- **WHEN** a reviewer action and vendor revision both mention a hurricane model but lack a confirmed shared substantive object
- **THEN** the record is marked `UNRESOLVED` or `NOT_SAME_OBJECT` for pairing and cannot establish `EXPLICIT_REVIEW_LINK_STATED`

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

### Requirement: Gold-blind packet and known-exposure scope
FG-3 SHALL freeze the exact file scope of `KNOWN_EXPOSURE_LEDGER_V1` and construct identical, hash-bound evidence packets before human adjudication, retaining all first-tier source matches. Protected KCC Test E content SHALL remain sealed.

#### Scenario: Packet omits a needed qualification
- **WHEN** a model-blind source-scope resolver finds the qualification in the allowed source record but not the frozen packet
- **THEN** the case is `PACKET_INSUFFICIENT` and the packet is not repaired within this evaluation

#### Scenario: Prior exposure cannot be resolved
- **WHEN** exact or substantial equivalence to an in-scope prior case remains unresolved
- **THEN** the case is `MATCH_UNRESOLVED` and outside the primary prospective set

### Requirement: Documentary-link and claim boundaries
Panel C SHALL distinguish an explicit source statement linking review to same-object model modification from independent causal proof. H1 SHALL use directional dependency-cluster statuses. H2 SHALL report human-human disagreement separately from model-gold disagreement. H4 SHALL describe only the two pinned configurations.

#### Scenario: Reviewer reports response revision only
- **WHEN** the source links review to revised disclosure wording without stating a model-method or implementation modification
- **THEN** `EXPLICIT_REVIEW_LINK_STATED` is not established for the model-modification target

### Requirement: Independent future retrieval axis
FG-4 retrieval eligibility SHALL require a frozen, source-verified natural set and a separate prospective FG-4 protocol, not a threshold on FG-3 semantic performance.

#### Scenario: FG-3 semantic judgment is poor
- **WHEN** FG-3 finds semantic errors with supplied evidence
- **THEN** FG-4 remains admissible under its own protocol and both error axes may be studied
