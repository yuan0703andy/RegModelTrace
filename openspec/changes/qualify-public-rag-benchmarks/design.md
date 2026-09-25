# Design

Track A uses three benchmark-specific adapters: TimelyQABench for temporal retrieval, VersionQA for version-aware QA, and LIT-RAGBench for generation from supplied context. Scores remain within benchmark and task strata. Cross-benchmark synthesis compares failure mechanisms, not a pooled accuracy.

A0 pins official repository commits, locally preserves byte-identical source archives outside Git, records SHA-256, inspects schemas and release/evaluation code, and lists unknowns. Raw archives are never modified. An official split remains authoritative; where absent, a development/confirmation partition must be frozen before model outputs are inspected. Any derived partition must be labeled as project-defined.

Baseline qualification is prospective. A faithful published-method reproduction retains its original model/runtime and records deviations. A controlled-component comparison fixes common components only where that is technically meaningful. These are distinct estimands. Gold-context controls are allowed only when evidence labels are actually present or independently adjudicated; reference answers are not automatically sufficient evidence.

The Track B FG-3 protocol is unchanged and cannot supply development cases, labels, or thresholds to Track A. FG-2 synthetic results may motivate failure categories, but not public-benchmark performance claims.
