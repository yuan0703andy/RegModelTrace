# SCALE-1 Checkpoint 2 — thin Ray executor

**Status: PASS**

Checkpoint 2 wraps the frozen M3.6 assertion-classification request in a thin Ray Data actor pool. The host retains request identity, prompt tokens, provenance, validation, and canonical commitment; each GPU actor loads one unchanged Qwen2.5-32B-Instruct-AWQ/vLLM replica and persists raw attempt shards before reduction.

## Final environment

The executor used Ray 2.58.0 in an isolated overlay with its Ray Data dependencies. The frozen vLLM 0.29.0, Torch 2.13.0, Transformers 5.17.0, PyArrow 21.0.0, and NumPy 2.3.5 packages were unchanged. The final environment lock SHA-256 is `c9d0300f3ee79d7bf47b4d1892972b5a0cd4a3658ab0d14205240e543e173545`.

## Valid runs

| Run | GPU replicas | Wall seconds | Requests/second | Valid outputs | Actors | Physical GPU UUIDs |
|---|---:|---:|---:|---:|---:|---|
| direct | 1 | 225.74 | 0.567 | 128/128 | 1 | GPU-9293afd7-f916-6613-8563-140b9f2f0369 |
| ray1 | 1 | 234.81 | 0.545 | 128/128 | 1 | GPU-92d29792-ef83-ab4b-0577-29d3f068ee36 |
| ray2 | 2 | 164.71 | 0.777 | 128/128 | 2 | GPU-92d29792-ef83-ab4b-0577-29d3f068ee36, GPU-eab0f052-7a0f-ee5b-a53a-123e21350e22 |

Both Ray runs match the direct reference exactly for all 128 requests across raw model text, output token IDs, normalized labels, prompt-token hashes, request IDs, source bindings, and microbatch IDs. The observed direct-to-Ray-2 wall-time ratio was 1.371x in this single bounded run; it is a descriptive measurement, not a scaling estimate. Full runner-level JSON hashes differ as expected because timestamps, actor IDs, attempt IDs, GPU UUIDs, and output paths are execution provenance.

All thirteen submitted Checkpoint 2 jobs, including failed and cancelled attempts, consumed 0.560833 allocated GPU-hours. Queue waits and per-job allocations are retained in `slurm_accounting.json`.

## Recovery and isolation

The final no-model controls passed 9/9. Synthetic reducer controls distinguished equivalent duplicates from conflicting duplicates. An actual child-process interruption after raw persistence was recovered without model inference; an actual Ray actor crash was restarted; and an actual Ray worker was denied reads under Gold, evaluation, Validation D, and Sealed Test E paths while retaining access to its allowed microbatch manifest.

The failure ledger is retained. It includes the initial control-harness defects, a missing `ninja` PATH entry, an incomplete Ray Core-only overlay that lacked Ray Data dependencies, and Ray resource over-detection before `ray.init` was bound to the SLURM allocation. These attempts produced no semantic evaluation and are included in GPU-hour accounting where applicable.

## Boundaries

This checkpoint validates transport, parity, provenance, durability, isolation, and two-GPU execution only for the 128-request M3.6 source-classification workload. It does not establish v2.2 forced-choice compatibility, semantic accuracy, calibration, large-workload throughput, Ray superiority, or readiness to expose Validation D or Sealed Test E.
