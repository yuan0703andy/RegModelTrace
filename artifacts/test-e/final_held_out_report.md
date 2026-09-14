# KCC 2023 Sealed Test E — final held-out evaluation

Status: **COMPLETE_WITH_MODEL_ERRORS**

Test E: **CLOSED**  
RegModelTrace technical development: **CLOSED**

## Held-out result

| Measure | Result |
|---|---:|
| Valid cases | 12/12 |
| Valid forced-choice decisions | 24/24 |
| Evidence sufficiency, all cases | 11/12 |
| Evidence sufficiency, primary comparisons | 5/6 |
| Evidence sufficiency, adverse controls | 6/6 |
| Conditional relation classification | 4/6 |
| ALIGNED classification | 4/4 |
| PARTIALLY_ALIGNED classification | 0/2 |
| CONFLICT classification | not tested |
| Provenance/interface integrity | PASS |

## Case results

| Case | Truth evidence | P(sufficient) | Evidence argmax | Truth relation | Relation argmax | Attribution |
|---|---|---:|---|---|---|---|
| `FC-TE23-G2` | SUFFICIENT | 0.999997 | SUFFICIENT | ALIGNED | ALIGNED | PASS |
| `FC-TE23-M3` | SUFFICIENT | 0.982558 | SUFFICIENT | ALIGNED | ALIGNED | PASS |
| `FC-TE23-S2` | SUFFICIENT | 0.092688 | INSUFFICIENT | ALIGNED | ALIGNED | EVIDENCE_SUFFICIENCY_UNDERCALL, SCOPE_APPLICABILITY_UNDERCALL |
| `FC-TE23-V2` | SUFFICIENT | 0.999995 | SUFFICIENT | PARTIALLY_ALIGNED | ALIGNED | MULTI_FACET_OVERALIGNMENT |
| `FC-TE23-A2` | SUFFICIENT | 0.999851 | SUFFICIENT | ALIGNED | ALIGNED | PASS |
| `FC-TE23-CI6` | SUFFICIENT | 0.999992 | SUFFICIENT | PARTIALLY_ALIGNED | ALIGNED | MULTI_FACET_OVERALIGNMENT |
| `ADV-TE23-G2-COPIED-REQUIREMENT` | INSUFFICIENT | 0.000000 | INSUFFICIENT | null | not scored | PASS |
| `ADV-TE23-M3-FUTURE-REVIEW` | INSUFFICIENT | 0.000000 | INSUFFICIENT | null | not scored | PASS |
| `ADV-TE23-S2-REVIEWER-ONLY` | INSUFFICIENT | 0.000000 | INSUFFICIENT | null | not scored | PASS |
| `ADV-TE23-V2-COPIED-REQUIREMENT` | INSUFFICIENT | 0.000000 | INSUFFICIENT | null | not scored | PASS |
| `ADV-TE23-A2-REVISION-HISTORY-ONLY` | INSUFFICIENT | 0.000000 | INSUFFICIENT | null | not scored | PASS |
| `ADV-TE23-CI6-FUTURE-REVIEW` | INSUFFICIENT | 0.000000 | INSUFFICIENT | null | not scored | PASS |

## Proper scores

- Binary Brier: `0.06862664357058956`
- Binary natural-log score: `0.1996899799191357`
- Conditional multiclass Brier: `0.6666716833485092`
- Conditional multiclass natural-log score: `8.735031717150793`

The relation loss is dominated by extreme confidence in `ALIGNED` for both frozen `PARTIALLY_ALIGNED` cases. These scores are descriptive for this held-out fixture and are not a calibration claim.

## Error attribution

- `FC-TE23-S2`: evidence-sufficiency undercall. The model assigned only 0.092688 to sufficient evidence even though the frozen adjudication treats hourly loss-cost analysis as inapplicable when no hourly loss-cost output exists.
- `FC-TE23-V2`: multi-facet overalignment. The model predicted `ALIGNED` although the frozen vendor evidence does not clearly establish claims data as a direct development basis for V-2.A.
- `FC-TE23-CI6`: multi-facet overalignment. The model predicted `ALIGNED` although the vendor evidence does not fully demonstrate that options are unique, explicit, and distinctly emphasized.
- All six adverse controls passed. No interface, provenance, actor-binding, copied-requirement, future-tense, reviewer-only, or revision-history sufficiency error occurred.

The v2.2 interface has no causal-output field, so unsupported causal inference is not directly measurable in this test. The adverse controls support the narrower finding that bounded review or revision evidence was not treated as sufficient vendor implementation evidence. A retrieval miss or bounded-bundle miss must not be read as corpus absence.

## Parser limitation

KCC whole-document parser portability remains `FAIL_TABLE_IDENTITY`: four panels on submission PDF pages 184–185 produced 140 duplicate row/column identities. All truth-supporting narrative propositions reconstruct exactly, and the affected tables were excluded. The system must not be described as fully parser-portable on KCC.

## Closure

This was the only authorized Base-Qwen run on KCC Test E. No rerun, prompt/scorer/model change, fine-tuning, or additional semantic development is authorized. Test E and RegModelTrace technical development are closed; remaining work is product packaging and documentation.
