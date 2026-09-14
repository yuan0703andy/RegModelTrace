# RegModelTrace System v1 — Same-Corpus Unseen-Question Audit

## Result

**The RegModelTrace v1 service contract passes. Unattended answer quality does not yet pass a reliability claim.** The system completed a single frozen run over twenty previously unused questions with one persistent retriever, embedding model, and Qwen2.5-32B-Instruct-AWQ instance. All twenty responses were structurally valid and every generated claim was bound to retrieved source assertions. Human review nevertheless found six unsupported claims across three questions, so the current release should remain a development MVP with human review.

This is a same-corpus unseen-question audit over the same three documents used during development. It is not evidence of cross-vendor, cross-year, or cross-document-family generalization.

## Frozen execution

| Item | Value |
|---|---|
| SLURM job | `55229862` |
| Compute node | `dcc-plusds-gpu-02` |
| GPU | NVIDIA RTX 5000 Ada, 32,760 MiB |
| Model | Qwen2.5-32B-Instruct-AWQ via vLLM |
| Questions | 20 |
| Valid responses | 20/20 |
| Runtime | 182.81 seconds |
| System/retriever/backend initializations | 1 / 1 / 1 |
| Evaluator or rubric reads during inference | 0 |
| Result SHA-256 | `8ca6f3aa7b0f99c430e0a6797b13bfe2661dba42303c4092e6c5daaad50e5140` |

The question fixture, rubric, runtime implementation, prompt, and configuration were hashed before inference. The run was preserved before human adjudication. No prompt, retrieval, model, question, or service change was made in response to these outputs.

## Human adjudication

| Dimension | Result |
|---|---:|
| Structurally valid responses | 20/20 |
| Claims bound to retrieved assertions | 20/20 questions |
| Answer usefulness | 14 PASS / 5 PARTIAL / 1 FAIL |
| Citation correctness | 16 PASS / 3 PARTIAL / 1 FAIL |
| Unsupported substantive claims | 6 across 3 questions |
| Unsupported causal claims | 0 |
| Retrieval miss stated as corpus absence | 0 |
| Retrieval sufficiency | 16 SUFFICIENT / 2 PARTIAL / 2 INSUFFICIENT |

Grounding and citation correctness are intentionally separate. The host guaranteed that each claim named valid retrieved assertion IDs. Human review then checked whether those exact assertions supported the claim's actor, tense, scope, and proposition.

## Material failures

`U08` was a synthesis error despite sufficient retrieval. The correct RMS submission described quarterly third-party ZIP Code updates, quality and consistency checks, and boundary and centroid alignment checks. The answer stated that correctly, then misassigned two Professional Team actions—“Reviewed” and “Discussed”—to RMS.

`U11` was the single answer-usefulness failure. Its cited audit text said the sensitivity analysis, statistical techniques, and graphical results **will be reviewed**. The answer converted all three into statements that the Team **reviewed** them. This is an unsupported tense and actuality upgrade, even though every claim had a valid source binding.

`U10` and `U13` exposed retrieval misses. The stochastic-track bundle did not retrieve the specific genesis-location mechanism. The compensating-adjustment bundle retrieved the governing G-4 standard but missed the Professional Team's actual finding. Both responses avoided inventing missing facts; `U13` remained relevant but did not answer the requested actor-specific question.

`U19` safely returned `UNRESOLVED_FROM_RETRIEVED_EVIDENCE`, but the Team citations concerned other methodologies rather than inland filling. `U20` correctly described RMS internal verification, then generalized two standard-specific Team comments into the scope of the Professional Team review as a whole.

## Safety boundary

The strongest result is narrow but important. Across all twenty questions, including causal and negative questions, the system produced:

- zero unsupported causal attributions;
- zero conversions of a retrieval miss into a claim of corpus absence;
- no inference that reviewer scrutiny itself established a challenge or required modification;
- no inference that agreement or verification meant exact numerical equality.

These observations apply to this frozen development run only. They do not establish a statistical error rate.

## Failure attribution and fine-tuning decision

The six questions below PASS split into three retrieval-side cases (`U10`, `U13`, `U19`), two synthesis-side cases (`U08`, `U11`), and one mixed case (`U20`). This is enough to locate concrete engineering limits, but it is not a coherent training distribution. Fine-tuning is therefore **not justified** by this run.

The next validation step should use a separately authored corpus or a new vendor/year before any quality claim is broadened. Fine-tuning should be reconsidered only after retrieval is shown to contain the needed evidence and repeated model-side errors form a stable behavior pattern across a materially larger human-adjudicated set.

## Release decision

`RegModelTrace.ask(question)` and the local HTTP interface are ready as a development MVP. The service is auditable, persistent across calls, strict about malformed model output, and able to resolve citations back to exact PDF spans. The answer layer still requires human review because valid citations alone did not prevent actor, tense, and scope errors.

The complete per-question judgments are in `human_adjudication.json`. Raw answers, retrieval bundles, model outputs, source bindings, and token usage remain under `data/validation/unseen-v1/run-55229862/`.
