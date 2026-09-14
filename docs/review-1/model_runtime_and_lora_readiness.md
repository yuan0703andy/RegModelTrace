# REVIEW-1 — model/runtime decision and LoRA readiness

## Decision

The closed release retains the frozen `Qwen/Qwen2.5-32B-Instruct-AWQ` model at revision `5c7cb76a268fc6cfbb9c4777eb24ba6e27f9ee6c`, served with vLLM 0.29.0 through the v2.2 alignment interface. This choice preserves an evaluated and reproducible deployment. It does not establish that this model or runtime is superior to every current alternative.

```text
RELEASE_TRAINING_DECISION = NO_TRAINING_THIS_RELEASE
NEXT_RELEASE_RESEARCH_OPTION = ADAPTER_COMPARISON_PROPOSED
TRAINING_AUTHORIZATION = NONE
```

The strongest objection to training now is not that adapters cannot help. It is that the available labels do not yet support a clean estimate of what an adapter would learn or whether it would generalize. The pooled primary set contains five truth-`PARTIALLY_ALIGNED` cases, zero truth-`CONFLICT` cases, and one naturally truth-insufficient case. All five partial cases were predicted `ALIGNED`, which identifies a serious observed weakness, but this small and selected set cannot distinguish a stable model mechanism from requirement-family and annotation effects.

## Architecture decision record

| Component | Responsibility in RegModelTrace |
|---|---|
| Qwen | Model architecture and weights that supply predictions |
| vLLM | Inference runtime that loads and executes Qwen under the frozen contract |
| Ollama | Alternative model-management and inference runtime that can also run Qwen |
| Ray | Scheduler for independent persistent inference replicas; it does not change Qwen's learned semantics |
| RAG | Workflow that retrieves source evidence and conditions answer generation on it |
| LoRA | Potential trainable low-rank weight adaptation for a future experiment; it is not a runtime |

“Qwen versus Ollama” is therefore a category error: Qwen identifies the model, whereas Ollama identifies one possible way to run it. REVIEW-1 does not benchmark runtimes or verify current Ollama scoring interfaces. The Ray lane remains closed as `PASS_WITH_GENERATIVE_NONDETERMINISM_LIMITATION`; the historical Checkpoint 3 exact-parity gate remains `PARITY_GATE_FAIL`.

## Observed error families

The saved rows verify the following primary relation errors:

| Evidence status | Frozen cases | Observation | Limitation |
|---|---|---|---|
| Independent pre-Test-E evidence | Impact G-4; CoreLogic M-2 and CI-5 | Human truth was `PARTIALLY_ALIGNED`; the model predicted `ALIGNED` | Three cases across two independent corpora supported the historical candidate family `MULTI_FACET_OVERALIGNMENT`, below the project's predeclared three-corpus trigger |
| Development-only counterdirection | RMS/ARA M-3.B ARA | Human truth was `ALIGNED`; the model predicted `PARTIALLY_ALIGNED` and undercalled sufficiency | Consistent with requirement/method scope conflation, but it was not an independent validation corpus |
| Post-final-test motivation | KCC V-2 and CI-6 | Human truth was `PARTIALLY_ALIGNED`; the model predicted `ALIGNED` | KCC results were exposed only after the no-training decision; they cannot retroactively satisfy the closed release's trigger or serve as a future untouched test |

Verisk had no truth-`PARTIALLY_ALIGNED` primary case. Its absence of this error supplies no positive evidence that the model can recognize that class. The recurrence table also does not identify why the errors occurred. `VENDOR_REVIEWER_EVIDENCE_COLLAPSE`, missing-facet overstatement, and generic bias toward `ALIGNED` remain candidate explanations rather than established internal mechanisms.

## Annotation and evidence readiness

A future training example is usable only when the inference input contained the evidence needed for the human label, its propositions remain source-grounded, and the disagreement is not explained by interface failure or known adjudication sensitivity. The present archive does not yet establish that condition consistently for a sufficiently varied training set.

The most consequential convention that must be stabilized prospectively is the distinction between:

1. an explicitly demonstrated implementation that omits an applicable required facet; and
2. a document bundle that simply does not demonstrate the facet.

The first may support `PARTIALLY_ALIGNED` or `CONFLICT`, depending on the requirement logic. The second ordinarily supports an evidence-sufficiency judgment rather than a substantive relation. REVIEW-1 records this possible contract sensitivity and does not alter any frozen truth.

Any future dataset also needs counterexamples that prevent an adapter from learning universal pessimism: fully aligned multi-facet cases, legitimate OR alternatives, non-prescribed method choices, truth-insufficient cases, and genuine conflicts. Vendor lineage, shared passages, related model versions, and requirement families are leakage groups, not independent rows. Train, development, and test partitions must separate those groups.

## Proposed next-release experiment

A separately authorized release could compare three fixed conditions on identical frozen evidence:

1. unchanged base Qwen under the established evidence interface;
2. a non-training baseline that explicitly evaluates each applicable facet before aggregating the relation; and
3. a LoRA-adapted model trained for facet completeness and actor/evidence separation.

The comparison should measure false `ALIGNED` judgments, excessive `INSUFFICIENT` or `PARTIALLY_ALIGNED` judgments, class-specific metrics, and source-boundary safety. Any gain must be attributed separately to representation/prompt changes and to weight adaptation. A more conservative output distribution is not sufficient evidence of improvement.

KCC may be used only as exposed diagnostic material, never as a new untouched final test. A future test requires a new independently frozen evaluation arrangement. No training file is materialized by REVIEW-1.

QLoRA feasibility also remains unverified. The deployed AWQ artifact must not be assumed to be the training base. A future technical proposal must identify the compatible base checkpoint, training quantization, tokenizer and chat template, memory envelope, adapter format, and vLLM serving compatibility before allocating GPUs.

## Sources

- Qwen Team. *Run Qwen with Ollama*. Qwen documentation. https://qwen.readthedocs.io/en/latest/run_locally/ollama.html
- Tim Dettmers et al. *QLoRA: Efficient Finetuning of Quantized LLMs*. 2023. NeurIPS / arXiv. https://arxiv.org/abs/2305.14314
- Hugging Face. *PEFT Quantization Guide*. https://huggingface.co/docs/peft/main/en/developer_guides/quantization

