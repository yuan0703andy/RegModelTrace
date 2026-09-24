# Tasks

- [x] Verify the official model identity, license, and pinned revision.
- [x] Download the exact revision on a DCC compute node and verify its local files.
- [ ] Run two bounded synthetic structured-output requests on typed Ada GPUs.
- [x] Update active model selection and explicit thinking-mode handling; retain
  a fail-closed pending-runtime status until the smoke passes.
- [ ] Run local checks, strict OpenSpec validation, and record a runtime receipt.

Download receipt: `artifacts/model-smoke/qwen38-upgrade-20260924/download_receipt.json`.
All 81 Hub files, including 66 safetensors files, passed exact size and SHA-256
checks on DCC compute allocation 56252522. The typed-GPU smoke is pending in
Slurm job 56256759; active configuration selects Qwen3.8 but operational
readiness remains unverified while that job is pending.
- [ ] Report runtime status and semantic-quality status separately.
