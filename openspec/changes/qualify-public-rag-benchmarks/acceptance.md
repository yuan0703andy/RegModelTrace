# Acceptance

A0 passes when each candidate benchmark has an official source and pinned byte-level artifact, documented row count/schema/task, split status, source/evidence annotation status, scoring availability, and explicit limitations. The matrix must not imply that a method is runnable on a benchmark solely because both are called RAG.

A1 remains blocked until open qualification items relevant to a comparison are resolved, a model/configuration is frozen, and official versus project-defined partitions are distinguished. Failure to reproduce a published method is `REPRODUCTION_NOT_QUALIFIED`, not evidence of poor method quality.

No Track A result may be presented as FG-3 natural-domain validity. No Track B result may be used to tune Track A. No pooled benchmark score or semantic-quality claim is accepted from A0.

`TIMELY_BEST_ALPHA` is oracle-only because it uses per-query gold positive IDs. The deployable TimelyRAG candidate uses `TIMELY_AUTO_ALPHA`. VersionQA is end-to-end QA-only until evidence IDs are independently annotated. A faithful LIT-RAGBench run must use the official combined shuffled context and explicit full-task scope; a positive/negative contrast has a different run label and frozen case-specific ordering. A0 planning acceptance does not authorize A1 execution.

A0.4 accepts a prospective Timely split only if each exact document-text overlap component stays in one partition and assignments are hash-pinned before outputs. A patched Timely runner may be called a compatibility candidate after source/patch hash checks and a non-claim-bearing smoke, but paper-number parity requires the actual dependencies, candidate-pool/top-k configuration, and full run. An import-shim smoke does not satisfy that gate. LIT scorer qualification requires a fixed judge/runtime and comparison with the frozen human-audit subset after answers exist; a frozen audit plan alone is not a passed judge. Internal execution eligibility and public redistribution clearance are separate statuses. A0 remains `PASS_FOR_PLANNING_NOT_CLOSED`; A1 full execution remains unauthorized here.
