# Tasks

- [x] Freeze model-facing cases, separate oracle, and their hashes.
- [x] Validate the fixture without model inference.
- [x] Run one bounded GPU job on the pinned Qwen3.8 revision.
- [x] Preserve and verify raw output and runtime metadata before scoring.
- [x] Score per case and panel; report limitations without changing the active
  default, model configuration, prompt, or historical results.
- [x] Run focused tests and strict OpenSpec validation.

Job 56271038 completed 18/18 requests with valid JSON. Reviewer labels were
8/12 correct; causal-link labels were 5/6 correct. The original reviewer
sentence was again misclassified twice. This is a synthetic diagnostic, not
an active-model promotion or natural-document quality estimate. See
`docs/qwen38_boundary_diagnostic.md` and
`artifacts/model-smoke/qwen38-boundary-20260924/score.json`.
