# SCALE-1 Checkpoint 3 — W2 compatibility and large-workload scaling

**Status: PARITY_GATE_FAIL**

The frozen W2 forced-choice compatibility prerequisite passed. The large benchmark then executed the same 4,096 unique M3.6 requests and 256 fixed microbatches under direct one-GPU, Ray one-GPU, and Ray two-GPU execution.

| Run | Wall seconds | Inference span | Max actor init | Requests/s | Input tokens/s | Output tokens/s | Active GPU util % | Actor-load CV | Requests by actor | Terminal dispositions |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|---|
| direct | 3231.55 | 3128.73 | 27.19 | 1.268 | 1588.3 | 16.286 | 99.4 | 0.000 | 4096 | {'VALID_OUTPUT': 4078, 'INVALID_MODEL_OUTPUT': 18} |
| ray1 | 3227.79 | 3111.70 | 23.88 | 1.269 | 1590.2 | 16.305 | 99.4 | 0.000 | 4096 | {'VALID_OUTPUT': 4078, 'INVALID_MODEL_OUTPUT': 18} |
| ray2 | 1610.89 | 1427.83 | 34.94 | 2.543 | 3186.3 | 32.673 | 99.1 | 0.000 | 2048, 2048 | {'VALID_OUTPUT': 4078, 'INVALID_MODEL_OUTPUT': 18} |

The prospective formal Ray-2/Ray-1 end-to-end throughput ratio is **2.004x** against the unchanged **1.5x** gate: **PASS**. This metric includes model and Ray startup. It is not changed or reinterpreted after observing the result.

Optional Ray four-GPU execution was **NOT_RUN_RESOURCE_AVAILABILITY**. The scheduler's test-only query predicted a next-day start, so no R4 job was submitted and it consumed zero GPU-hours.

All mandatory runs passed request conservation, explicit terminal-disposition accounting, provenance, durable-attempt, GPU-identity, telemetry, and zero-infrastructure-retry checks. Each path produced 4,078 valid outputs and the same 18 explicit `INVALID_MODEL_OUTPUT/INVALID_KEYS` dispositions. Direct and Ray one-GPU matched exactly for 4,096/4,096 requests. Direct and Ray two-GPU matched for 4095/4,096 requests. The sole differing request was `R58c78cfaeaafd1fff8218aea` / `Bcdafcbb88d295b51ac33` (Florida Public Hurricane Loss Model 2023 Standards Submission, physical page 159): direct/Ray-1 returned `REGULATORY_REQUIREMENT`, while Ray-2 returned `VENDOR_METHODOLOGY`. Its focal assertion is `56-74 75-112 >112mph >56mph 56-74 75-112 >112mph >56mph Storms Year Model Model Model Model H*Wind H*Wind H*Wind H*Wind Threshold Thresh.` The request is a source-preserved table-like narrative fragment; no semantic truth was assigned and neither label is adjudicated here.

The direct/Ray-1 node reported [30712.0] MiB total memory per RTX 5000 Ada, while the Ray-2 node reported [32760.0] MiB. The model and GPU type were unchanged, but the device-memory configuration was not identical and is retained as a measurement limitation.

Total Checkpoint 3 allocated usage, including W2 and every submitted large run, was **2.736389 GPU-hours**.

Ray spill reporting is bounded to an explicit case-insensitive scan of preserved job logs. A log with no matching event is reported as `NO_SPILL_EVENT_REPORTED_IN_JOB_LOG`, not as a measured zero-byte spill result. Full observations are retained in the machine receipt.

This report establishes bounded systems behavior only. It does not score semantic accuracy, expose Validation D or Sealed Test E, change Qwen or the frozen requests, authorize fine-tuning, or establish general production scaling.
