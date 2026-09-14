# Final metrics

## Held-out KCC Test E

| Task | Raw result |
|---|---:|
| Evidence sufficiency, primary cases | 5/6 |
| Conditional relation, truth-sufficient primary cases | 4/6 |
| Joint two-stage correctness, primary cases | 3/6 |
| Truth `ALIGNED` relation recall | 4/4 |
| Truth `PARTIALLY_ALIGNED` relation recall | 0/2 |
| Constructed insufficient-evidence controls | 6/6 |

KCC `SUFFICIENT` precision/recall/F1 were 100% / 83.33% / 90.91%. KCC `ALIGNED` precision/recall/F1 were 66.67% / 100% / 80%. `PARTIALLY_ALIGNED` precision was undefined because the model never predicted the class; recall and F1 were zero.

## Five-fixture descriptive accounting

The five v2.2 fixtures contain 30 primary comparisons and 22 adverse controls. They share requirements, documents, and organization lineages.

### Evidence sufficiency, primary cases

| Human truth \ Model | `SUFFICIENT` | `INSUFFICIENT` |
|---|---:|---:|
| `SUFFICIENT` | 23 | 6 |
| `INSUFFICIENT` | 1 | 0 |

### Relation, 29 truth-sufficient primary cases

| Human truth \ Model | `ALIGNED` | `PARTIALLY_ALIGNED` | `CONFLICT` |
|---|---:|---:|---:|
| `ALIGNED` | 21 | 3 | 0 |
| `PARTIALLY_ALIGNED` | 5 | 0 | 0 |
| `CONFLICT` | 0 | 0 | 0 |

Primary joint correctness was 18/30. `ALIGNED` precision/recall/F1 were 80.77% / 87.50% / 84.00%. `PARTIALLY_ALIGNED` precision/recall/F1 were 0% / 0% / 0%. `CONFLICT` was untested.

These totals describe the archive; they are not an independent cross-vendor performance estimate or a calibration study. The complete denominators and frozen proper scores are in [REVIEW-1](review-1/evaluation_report.md).

## RAG

| Audit | Result |
|---|---|
| RAG v0.2 traceability | 16/16 substantive claims resolved to source assertions |
| RAG v0.2 bounded causal safety | 8/8 questions passed |
| Same-corpus unseen structure | 20/20 valid responses and host bindings |
| Same-corpus unseen usefulness | 14 pass, 5 partial, 1 fail |
| Same-corpus unseen unsupported claims | 6 claims across 3 questions |
| Unsupported causal attributions | 0 observed |

Valid citation IDs and spans establish traceability, not semantic entailment. Claim precision is not computable because the audit did not freeze the total number of substantive claims.

## Ray/vLLM systems result

| Result | Outcome |
|---|---:|
| Frozen workload | 4,096 unique requests |
| Valid/invalid outputs per large run | 4,078 / 18 |
| Ray 2-GPU versus Ray 1-GPU throughput | 2.004× |
| Actor split | 2,048 / 2,048 |
| Direct versus Ray 2-GPU exact output parity | 4,095 / 4,096 |
| Infrastructure retries | 0 |

The single changed label was not repaired or regraded. Checkpoint 3 exact parity remained failed; the Ray lane closed with a generative nondeterminism limitation.

## Parser boundary

The original Gold Core passed nine parser gates for source-span recoverability, provenance, hierarchy, continuation, margin separation, table integrity, determinism, and transparent failure. KCC later exposed `FAIL_TABLE_IDENTITY` on four table panels with 140 duplicate row/column identities. The final semantic evaluation excluded those panels and used reconstructable narrative propositions.

