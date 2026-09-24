# Tasks

- [x] Verify the official model identity, license, and pinned revision.
- [x] Download the exact revision on a DCC compute node and verify its local files.
- [x] Run two bounded synthetic structured-output requests on typed Ada GPUs.
- [x] Preserve exact thinking-mode handling and pinned candidate configuration.
- [x] Restore the previous active default after the synthetic meaning check
  fails; do not promote a schema-valid response to product readiness.
- [x] Run local checks, strict OpenSpec validation, and record a runtime receipt.

Download receipt: `artifacts/model-smoke/qwen38-upgrade-20260924/download_receipt.json`.
All 81 Hub files, including 66 safetensors files, passed exact size and SHA-256
checks on DCC compute allocation 56252522. Job 56256759 failed on a preflight
threshold that exceeded the 5000 Ada's reported memory by about 8 MiB. After
that threshold was corrected, job 56262873 loaded Qwen3.8 and emitted both
valid structured responses, but the reviewer-scrutiny synthetic check failed.
The raw outputs are preserved. No historical FG-2 result or frozen prompt was
changed. The active default is restored to system-v1.
- [x] Report runtime status and semantic-quality status separately.
