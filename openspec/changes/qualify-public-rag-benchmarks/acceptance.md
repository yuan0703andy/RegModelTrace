# Acceptance

A0 passes when each candidate benchmark has an official source and pinned byte-level artifact, documented row count/schema/task, split status, source/evidence annotation status, scoring availability, and explicit limitations. The matrix must not imply that a method is runnable on a benchmark solely because both are called RAG.

A1 remains blocked until open qualification items relevant to a comparison are resolved, a model/configuration is frozen, and official versus project-defined partitions are distinguished. Failure to reproduce a published method is `REPRODUCTION_NOT_QUALIFIED`, not evidence of poor method quality.

No Track A result may be presented as FG-3 natural-domain validity. No Track B result may be used to tune Track A. No pooled benchmark score or semantic-quality claim is accepted from A0.

`TIMELY_BEST_ALPHA` is oracle-only because it uses per-query gold positive IDs. The deployable TimelyRAG candidate uses `TIMELY_AUTO_ALPHA`. VersionQA is end-to-end QA-only until evidence IDs are independently annotated. A faithful LIT-RAGBench run must use the official combined shuffled context and explicit full-task scope; a positive/negative contrast has a different run label and frozen case-specific ordering. A0 planning acceptance does not authorize A1 execution.
