# Design

Freeze 18 source-only synthetic requests and a separate expected-label file
before GPU execution. Twelve requests distinguish `REVIEWER_SCRUTINY` from
`REVIEWER_CHALLENGE`; two of those requests repeat the exact earlier failing
sentence to assess within-run stability. Six requests distinguish an explicit
review-to-modification link from mere temporal co-occurrence. The reviewer
panel reuses the exact system instruction, JSON schema, thinking mode, and
sampling configuration from the earlier smoke. The causal panel uses a fixed
task instruction frozen with this change.

The runner reads only the source-only cases. It writes a manifest and raw
responses, including token IDs, before any score is computed. A separate
scorer reads the expected-label file after the run. Report case-level errors
and group counts without tuning the fixture or inferring domain accuracy.

Use the same pinned checkpoint revision, vLLM environment, two RTX 5000 Ada
GPUs, tensor parallelism 2, thinking disabled, temperature 0, and seed 1847.
Preserve input and code hashes, GPU/runtime metadata, Slurm logs, and the
original failed smoke. Any failure is reported as observed; the active model
does not change as a result of this diagnostic alone.
