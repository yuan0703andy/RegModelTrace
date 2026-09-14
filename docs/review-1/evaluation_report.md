# RegModelTrace REVIEW-1 — saved-result evaluation report

## Scope and release boundary

This report recomputes classification summaries from saved, identity-bound v2.2 score rows. It does not re-run inference, re-adjudicate truth, tune a threshold, or alter a historical score. The closed release remains `PROJECT_TECHNICAL_DEVELOPMENT = CLOSED`, `TEST_E = CLOSED`, and `VALIDATION_D = CLOSED`.

The five v2.2 fixtures contain 52 cases: 30 primary comparisons and 22 deliberately constructed adverse controls. These cases share requirements, source documents, and organization lineages. Pooled counts are therefore descriptive accounting, not an independent-sample performance estimate.

## Per-corpus results

Relation accuracy is conditional on **human-truth sufficiency**, regardless of the model's sufficiency prediction. Joint correctness requires a correct sufficiency decision and, when truth is sufficient, a correct relation decision.

| Corpus | Primary cases | Primary sufficiency | Conditional relation | Primary joint | Adverse-control sufficiency |
|---|---:|---:|---:|---:|---:|
| RMS/ARA development | 8 | 6/8 | 7/8 | 6/8 | 6/6 |
| Impact Forecasting 2023 | 4 | 2/4 | 2/4 | 1/4 | 3/4 |
| CoreLogic/Cotality 2023 | 6 | 5/6 | 3/5 | 3/6 | not present |
| Verisk Validation D | 6 | 5/6 | 5/6 | 5/6 | 6/6 |
| KCC final Test E | 6 | 5/6 | 4/6 | 3/6 | 6/6 |

CoreLogic's one truth-insufficient primary case is outside the relation denominator. Impact's adverse set includes one truth-sufficient missing-facet variant; it is therefore not interchangeable with the truth-insufficient boundary controls in the other fixtures.

## Descriptive pooled accounting

Across primary comparisons, the sufficiency matrix is:

| Human truth \ Model | SUFFICIENT | INSUFFICIENT | INVALID |
|---|---:|---:|---:|
| SUFFICIENT | 23 | 6 | 0 |
| INSUFFICIENT | 1 | 0 | 0 |

For `SUFFICIENT`, precision is 23/24 = 95.83%, recall is 23/29 = 79.31%, and F1 is 46/53 = 86.79%. The sole truth-insufficient primary case was predicted sufficient, so the primary set does not demonstrate successful discrimination of naturally insufficient evidence.

Across the 29 truth-sufficient primary comparisons, the relation matrix is:

| Human truth \ Model | ALIGNED | PARTIALLY_ALIGNED | CONFLICT | INVALID |
|---|---:|---:|---:|---:|
| ALIGNED | 21 | 3 | 0 | 0 |
| PARTIALLY_ALIGNED | 5 | 0 | 0 | 0 |
| CONFLICT | 0 | 0 | 0 | 0 |

`ALIGNED` precision is 21/26 = 80.77%, recall is 21/24 = 87.50%, and F1 is 84.00%. `PARTIALLY_ALIGNED` precision is 0/3 = 0%, recall is 0/5 = 0%, and F1 is 0%. `CONFLICT` has neither truth support nor predictions; precision, recall, and F1 are undefined and untested. Primary joint correctness is 18/30 = 60.00%, with seven losses at sufficiency and five at relation.

The model did not merely predict `ALIGNED` on every case: it assigned `PARTIALLY_ALIGNED` to three truth-`ALIGNED` cases while assigning `ALIGNED` to all five truth-`PARTIALLY_ALIGNED` cases. The saved fixtures therefore show poor partial-class discrimination in both directions. They do not identify the internal mechanism.

## KCC reconciliation

The saved KCC artifacts exactly reproduce the predeclared reconciliation target:

- sufficiency: 5 true-sufficient predicted sufficient, 1 true-sufficient predicted insufficient, 0 true-insufficient predicted sufficient, and 6 true-insufficient predicted insufficient;
- relation: all 4 truth-`ALIGNED` cases predicted `ALIGNED`; both truth-`PARTIALLY_ALIGNED` cases predicted `ALIGNED`;
- primary joint correctness: 3/6;
- conditional relation accuracy: 4/6, equal on this fixture to an always-`ALIGNED` reporting baseline.

KCC `SUFFICIENT` precision is 100%, recall is 83.33%, and F1 is 90.91%. KCC `ALIGNED` precision is 66.67%, recall is 100%, and F1 is 80%. `PARTIALLY_ALIGNED` precision is undefined because there were no such predictions; recall and F1 are zero.

## Proper scores

Frozen Brier and natural-log scores were carried forward with their original denominators. Recomputed Brier values agree with every frozen scorer output without clipping or a new threshold.

| Corpus | Binary Brier | Binary log | Relation Brier | Relation log | Denominators binary/relation |
|---|---:|---:|---:|---:|---:|
| RMS/ARA development | 0.093088 | 1.280197 | 0.248741 | 2.043603 | 14 / 8 |
| Impact Forecasting 2023 | 0.375296 | 3.438704 | 1.222291 | 10.668305 | 8 / 5 |
| CoreLogic/Cotality 2023 | 0.140336 | 0.427814 | 0.800000 | 9.796910 | 6 / 5 |
| Verisk Validation D | 0.083331 | 0.916964 | 0.332002 | 1.052449 | 12 / 6 |
| KCC final Test E | 0.068627 | 0.199690 | 0.666672 | 8.735032 | 12 / 6 |

These are candidate-renormalized next-token scores under fixed prompts, token order, verbalizers, tokenizer, and decoding. They are not established epistemic posteriors or evidence of global calibration. Class support is selected and incomplete, especially for `CONFLICT`.

## RAG results remain a separate task

The saved M4A BM25 experiment reports a 9,750-candidate pool, macro Recall@5 18.75%, macro Recall@10 25.00%, micro Recall@5 12.50%, micro Recall@10 18.75%, and MRR 0.1972. M4B did not improve the key recall measures with its tested dense/hybrid variants. M4C's oracle passage bundle reached 56.25% micro required-record coverage and 68.75% macro bundle coverage, but that target bundled analytical records rather than only answer-sufficient facts.

The eight-question RAG v0.2 development run bound 16/16 substantive claims to source assertions and passed its bounded causal and corpus-absence safety audits. This establishes ID/span traceability, not complete semantic entailment. Its per-question notes identify citation relevance defects, but there is no complete claim-level semantic-support denominator, so claim precision is not computable.

The twenty-question same-corpus unseen audit produced 20/20 structurally valid responses and host bindings, with 14 useful answers, 5 partial answers, 1 failure, and 6 unsupported claims across 3 questions. Because the total number of substantive claims was not frozen, “six unsupported claims” remains a count rather than a rate. Issue/gap recall is also not computable because there is no independent complete issue inventory.

The RAG audits observed zero unsupported causal attributions in their audited outputs. The v2.2 alignment interface has no causal field and therefore does not measure causal-language safety.

## Product interpretation and limitations

The strongest demonstrated capabilities are deterministic provenance, valid forced-choice output, reliable rejection of most constructed insufficient boundary bundles, and accurate recognition of many fully aligned cases. The principal saved weakness is failure to identify `PARTIALLY_ALIGNED`, accompanied by occasional conservative sufficiency undercalls and one naturally insufficient primary overclaim.

The system evaluates prepared evidence bundles against owner-adjudicated documentary truth. It does not observe hidden production implementation, and its joint score is not end-to-end PDF-to-alignment accuracy. Reviewer findings, vendor documentation, and deployed behavior remain separate evidence objects. KCC table portability remains `FAIL_TABLE_IDENTITY`; affected panels were excluded rather than repaired.

All certified rows, matrices, undefined-value reasons, and input hashes are in `regmodeltrace/data/reporting/review-1/`.

