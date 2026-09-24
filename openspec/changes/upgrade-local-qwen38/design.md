# Design

Pin `Qwen/Qwen3.8-27B-FP8` at revision
`017b9c7af6b5689d5dd426a76e0bc077eb5ca20a`. Store weights under the
existing group-filesystem Hugging Face cache; never download 30GB of weights to
the DCC login node or repository. Preserve the prior checkpoints and frozen
FG-2, alignment, and KCC artifacts.

Run two bounded synthetic JSON requests on typed Ada GPUs in a
Slurm compute allocation. Use the installed vLLM environment first. Record the
runtime version, physical GPU, checkpoint hash, request, raw output, and
validation separately. One request checks a reviewer-scrutiny label; the other
checks the active product's claim and citation schema. Disable model thinking
explicitly both when estimating
prompt length and when generating. If the current runtime cannot load the
checkpoint, diagnose the incompatibility before changing the active product
config; any runtime upgrade must use an isolated environment and a new receipt.
Match the active tensor-parallel setting to the GPU configuration actually
verified by the smoke.

After smoke success, update only the active service model snapshot and runtime
settings. The host retains question, source, and citation identity. The model
continues to produce bounded answers under the existing citation validator.
No corpus, retrieval, prompt, scorer, or historical model configuration changes.

Runtime readiness is not evidence of better alignment classification or RAG
answer quality. Any later semantic comparison needs its own predeclared natural
case evaluation, kept separate from this deployment change.
