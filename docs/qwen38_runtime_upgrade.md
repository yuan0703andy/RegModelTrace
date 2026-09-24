# Qwen3.8 active-runtime upgrade

The owner selected `Qwen/Qwen3.8-27B-FP8` for future local RegModelTrace
inference. The exact revision is
`017b9c7af6b5689d5dd426a76e0bc077eb5ca20a`.

The checkpoint was downloaded on a DCC CPU compute allocation into the group
Hugging Face cache. All 81 Hub files, including 66 safetensors files, passed
size and SHA-256 checks. The receipt and per-file hashes are in
`artifacts/model-smoke/qwen38-upgrade-20260924/`.

The prepared Qwen3.8 service configuration is separate. It leaves the frozen
Qwen2.5 system-v1 configuration and Qwen3.5 FG-2 experiment untouched.
Qwen3.8 is **not the active default**. Its bounded smoke loaded the checkpoint
and returned valid structured JSON, but failed the synthetic meaning check,
so the service default was restored to `system_v1.json`. The candidate
configuration remains available by explicit opt-in. It runs with thinking
disabled for bounded JSON output;
the host still owns evidence IDs, source resolution, and citations. The model
path must resolve to the pinned revision, or startup fails.

**Runtime smoke:** GPU attempt `56256759` failed before model load because its
preflight required 30 GiB while the allocated RTX 5000 Ada reported 30,712 MiB
(about 8 MiB short). The preflight was corrected to 29 GiB without changing
the checkpoint, prompts, or generation parameters. Attempt `56262873` loaded
the exact checkpoint in 234.8 seconds on two RTX 5000 Ada GPUs and generated
both bounded responses. Both were valid JSON under their schemas. The product
claim/citation response was valid. The classification response labeled the
synthetic sentence “The Professional Team reviewed the methodology ...” as
`REVIEWER_CHALLENGE`, although the fixed expected label was
`REVIEWER_SCRUTINY`. The smoke validator therefore recorded
`SYNTHETIC_CHECK_FAIL`; Slurm exited 1. This is a real failure of the bounded
synthetic check, not evidence of domain-wide accuracy or inaccuracy. The raw
requests, responses, validation, runtime metadata, and logs are preserved in
`artifacts/model-smoke/qwen38-upgrade-20260924/` with verified DCC-to-local
hashes. No prompt or model tuning was done to turn the result into a pass.

**Domain quality:** NOT ASSESSED. Newer published general benchmarks do not
establish improved judgment of regulatory evidence, especially partial
alignment and multi-facet requirements. A fair comparison needs newly frozen
natural cases with the same source evidence and human truth. Historical FG-2
scores remain attached to Qwen3.5 and cannot be relabeled as Qwen3.8 results.

For an explicit candidate run on DCC, set `REGMODELTRACE_CONFIG` to the
`system_qwen38.json` path and `REGMODELTRACE_MODEL_PATH` to the verified
snapshot. The model weights are external to GitHub. The compact checkout
currently lacks the full production retrieval assets, so this smoke is not an
end-to-end RAG demonstration.
