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
The live default remains unchanged until the GPU smoke passes. The new model
is configured to run with thinking explicitly disabled for bounded JSON output;
the host still owns evidence IDs, source resolution, and citations. The model
path must resolve to the pinned revision, or startup fails.

**Runtime smoke:** PENDING, Slurm job `56256759`.

**Domain quality:** NOT ASSESSED. Newer published general benchmarks do not
establish improved judgment of regulatory evidence, especially partial
alignment and multi-facet requirements. A fair comparison needs newly frozen
natural cases with the same source evidence and human truth. Historical FG-2
scores remain attached to Qwen3.5 and cannot be relabeled as Qwen3.8 results.

On DCC, set `REGMODELTRACE_MODEL_PATH` to the verified snapshot before running
the active service. The model weights are external to GitHub. The compact
checkout currently lacks the full production retrieval assets, so the runtime
smoke alone is not an end-to-end RAG demonstration.
