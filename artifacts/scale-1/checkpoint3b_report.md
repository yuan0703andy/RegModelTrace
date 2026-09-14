# SCALE-1 Checkpoint 3B — bounded determinism characterization

**Diagnostic status: COMPLETE**  
**Classification: `ENVIRONMENT_DIFFERENCE`**  
**Ray lane: `PASS_WITH_GENERATIVE_NONDETERMINISM_LIMITATION`**  
**Historical Checkpoint 3 status remains: `PARITY_GATE_FAIL`**

Checkpoint 3B replayed only request `R58c78cfaeaafd1fff8218aea` / assertion `Bcdafcbb88d295b51ac33` in isolation and in its unchanged original 16-request microbatch. No 4,096-request rerun, semantic adjudication, Validation D, Sealed Test E, prompt change, model change, or tuning occurred.

## A. Input identity

The input layer is **PASS**. Frozen prompt bytes and token IDs, request and payload bindings, sampling parameters, model/tokenizer revision, M3.6 configuration, execution configuration, and environment-lock hashes were checked. All controlled actors reconstructed all sixteen prompt-token sequences exactly: **True**.

## B. Runtime

The controlled Direct, Ray-1, and two Ray-2 actors ran on the same node: `dcc-core-gpu-ferc-s-aa32-1`. Package identities were equal across controlled processes: **True**. Historical Direct/Ray-1 ran on `dcc-core-gpu-ferc-s-aa32-9`, while historical Ray-2 ran on `dcc-core-gpu-ferc-s-aa32-1` and reported a different visible-memory configuration. Complete driver, CUDA, GPU UUID, kernel, CPU, and package fingerprints are preserved in the machine receipt.

## C. Free-form outputs

| Actor | Node | Logical GPU bytes | Isolated labels (3) | Original-microbatch labels (3) |
|---|---|---:|---|---|
| direct.actor0 | dcc-core-gpu-ferc-s-aa32-1 | 33824571392 | VENDOR_METHODOLOGY, VENDOR_METHODOLOGY, VENDOR_METHODOLOGY | VENDOR_METHODOLOGY, VENDOR_METHODOLOGY, VENDOR_METHODOLOGY |
| ray1.actor0 | dcc-core-gpu-ferc-s-aa32-1 | 33824571392 | VENDOR_METHODOLOGY, VENDOR_METHODOLOGY, VENDOR_METHODOLOGY | VENDOR_METHODOLOGY, VENDOR_METHODOLOGY, VENDOR_METHODOLOGY |
| ray2.actor0 | dcc-core-gpu-ferc-s-aa32-1 | 33824571392 | VENDOR_METHODOLOGY, VENDOR_METHODOLOGY, VENDOR_METHODOLOGY | VENDOR_METHODOLOGY, VENDOR_METHODOLOGY, VENDOR_METHODOLOGY |
| ray2.actor1 | dcc-core-gpu-ferc-s-aa32-1 | 33824571392 | VENDOR_METHODOLOGY, VENDOR_METHODOLOGY, VENDOR_METHODOLOGY | VENDOR_METHODOLOGY, VENDOR_METHODOLOGY, VENDOR_METHODOLOGY |

Repeated-output variation: **False**. Isolated-versus-original-microbatch sensitivity: **False**. Controlled actor/backend difference: **False**.

The preserved Direct result from failed wrapper job `55352343` supplies an auxiliary environment contrast: on 30,712 MiB node `dcc-core-gpu-ferc-s-aa32-5`, its three isolated observations were `VENDOR_METHODOLOGY` and its three original-microbatch observations were `REGULATORY_REQUIREMENT`. The wrapper failed only afterward, before Ray-1, because `SLURM_TMPDIR` was unset. This partial result is retained as supporting context and is not counted as the complete controlled matrix.

## D. Competing-label margin

Positive margin favors `REGULATORY_REQUIREMENT`; negative margin favors `VENDOR_METHODOLOGY`. The frozen near-boundary threshold is an absolute difference no larger than `0.25` natural-log units.

| Actor | Context | JSON prefix | Mean R-minus-V logprob | Minimum absolute delta | Maximum absolute delta |
|---|---|---|---:|---:|---:|
| direct.actor0 | ISOLATED | COMPACT | 0.218750 | 0.218750 | 0.218750 |
| direct.actor0 | ISOLATED | SPACE_AFTER_COLON | -0.875000 | 0.875000 | 0.875000 |
| direct.actor0 | ORIGINAL_MICROBATCH | COMPACT | 0.187500 | 0.187500 | 0.187500 |
| direct.actor0 | ORIGINAL_MICROBATCH | SPACE_AFTER_COLON | -0.875000 | 0.875000 | 0.875000 |
| ray1.actor0 | ISOLATED | COMPACT | 0.218750 | 0.218750 | 0.218750 |
| ray1.actor0 | ISOLATED | SPACE_AFTER_COLON | -0.875000 | 0.875000 | 0.875000 |
| ray1.actor0 | ORIGINAL_MICROBATCH | COMPACT | 0.187500 | 0.187500 | 0.187500 |
| ray1.actor0 | ORIGINAL_MICROBATCH | SPACE_AFTER_COLON | -0.875000 | 0.875000 | 0.875000 |
| ray2.actor0 | ISOLATED | COMPACT | 0.218750 | 0.218750 | 0.218750 |
| ray2.actor0 | ISOLATED | SPACE_AFTER_COLON | -0.875000 | 0.875000 | 0.875000 |
| ray2.actor0 | ORIGINAL_MICROBATCH | COMPACT | 0.187500 | 0.187500 | 0.187500 |
| ray2.actor0 | ORIGINAL_MICROBATCH | SPACE_AFTER_COLON | -0.875000 | 0.875000 | 0.875000 |
| ray2.actor1 | ISOLATED | COMPACT | 0.218750 | 0.218750 | 0.218750 |
| ray2.actor1 | ISOLATED | SPACE_AFTER_COLON | -0.875000 | 0.875000 | 0.875000 |
| ray2.actor1 | ORIGINAL_MICROBATCH | COMPACT | 0.187500 | 0.187500 | 0.187500 |
| ray2.actor1 | ORIGINAL_MICROBATCH | SPACE_AFTER_COLON | -0.875000 | 0.875000 | 0.875000 |

Near-boundary observation: **True**.

## Attribution

`ENVIRONMENT_DIFFERENCE`: The historical outputs differ across recorded runtime environments, while the same-node controlled replay is stable across backends and contexts.

This classification identifies an environment-associated change, not the exact low-level property responsible. The historical jobs did not retain enough runtime detail to separate visible-memory/KV-cache capacity, physical GPU instance, driver state, node state, or lower-level numerical kernels.

Checkpoint 3B used **0.548889 allocated GPU-hours** across the completed matrix and two retained infrastructure failures. One failed wrapper preserved a complete Direct probe before stopping; the 6000 Ada attempt failed at NVML initialization before inference. A duplicate pending job was cancelled before allocation.

This bounded characterization supports `PASS_WITH_GENERATIVE_NONDETERMINISM_LIMITATION` only within the tested M3.6 execution contract. It does not erase the prospective exact-parity failure, establish which label is semantically correct, or claim bitwise determinism for arbitrary models, GPUs, prompts, or workloads.
