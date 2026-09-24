# Qwen3.8 synthetic evidence-boundary diagnostic

**Status:** Complete, synthetic diagnostic only. The active RegModelTrace
default remains `system_v1.json` (Qwen2.5); Qwen3.8 remains an opt-in
candidate. No corpus, prompt, model weight, FG-2 result, or gold label changed.

## Fixed run

Protocol commit: `e99a20d2` (before inference). Model:
`Qwen/Qwen3.8-27B-FP8`, revision
`017b9c7af6b5689d5dd426a76e0bc077eb5ca20a`. DCC Slurm job
`56271038` completed with exit code 0 on two RTX 5000 Ada GPUs, tensor
parallelism 2, vLLM 0.29.0, thinking disabled, temperature 0, seed 1847.
The checkpoint loaded in 138.0 seconds. The runner persisted all 18 raw
responses before the independent scorer read the oracle. The source-only
cases SHA-256 is `8a7007b45fcb41659148f0abab2c07a248701ae68c8262c1576a7286982b1c06`;
the separate oracle SHA-256 is
`129c01421e47603627a526d8da31632e956952cd0e30730d948cbc39e0f7c853`.
Remote and local SHA-256 values matched for the manifest, model-facing
requests, raw responses, and Slurm log. The run manifest records physical
GPU identity, runtime versions, hashes, and execution configuration.

## Observed results

All 18 outputs were valid under the fixed one-field JSON schema. The reviewer
panel was 8/12 correct; the causal-link panel was 5/6 correct. The combined
13/18 count is descriptive of this constructed fixture, not an estimate of
accuracy on regulatory documents. R01 and R02 repeat the same source, so
those two errors are not independent examples.

| Case | Source cue | Frozen expectation | Qwen3.8 output |
| --- | --- | --- | --- |
| R01, R02 | “reviewed the methodology” | `REVIEWER_SCRUTINY` | `REVIEWER_CHALLENGE` twice |
| R03 | “examined the calculations” | `REVIEWER_SCRUTINY` | `REVIEWER_CHALLENGE` |
| R10 | “rejected ... because it did not satisfy the standard” | `REVIEWER_CHALLENGE` | `REVIEWER_SCRUTINY` |
| C05 | “In response to ... request ... RMS revised” | `EXPLICIT_REVIEW_CAUSED_MODIFICATION` | `NOT_ESTABLISHED` |

The other 13 reviewer/causal decisions were correct. In particular, all
four no-link causal controls stayed `NOT_ESTABLISHED`, and the more explicit
two-sentence response case C06 was correctly identified as a link. The
original failure is reproducible within this run under the same prompt,
schema, and sampling settings; the opposite R10 error and C05 miss show that
the issue is not simply a blanket tendency to make stronger causal claims.

## Interpretation and limits

This diagnostic establishes runtime and JSON-format compatibility but shows
several meaning errors under the currently chosen bounded, nonthinking
interface. It does not identify whether the errors arise from the checkpoint,
the fixed instruction, constrained decoding, or their interaction. It does
not measure natural-document performance, compare models on independent
cases, establish calibrated probabilities, or authorize changing the active
default. No prompt adjustment or semantic retry was made after seeing the
outputs.

Primary artifacts: `artifacts/model-smoke/qwen38-boundary-20260924/` contains
the byte-verified DCC run, raw responses, scorer output, Slurm log, and copy
receipt. The exact cases and oracle are under
`experiments/qwen38_boundary/` and remain frozen at protocol commit.
