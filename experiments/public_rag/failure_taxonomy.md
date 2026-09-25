# Track A failure taxonomy — prospective, not observed results

The unit of analysis is a benchmark question under a pinned retrieval/context/generation run. Categories are non-exclusive. Record both the eligible-case denominator and the actual context delivered to the generator. A missing annotation is `NOT_ASSESSABLE`, never a negative finding.

| Code | Failure | Minimum evidence needed to assign it |
|---|---|---|
| R1 | Candidate retrieval miss | Relevant source IDs exist and are absent from the retrieval candidate pool. |
| R2 | Wrong version or time | Version/effective-time truth exists and retrieved source is incompatible with query time/version. Publication time alone is insufficient. |
| R3 | Incomplete evidence set | Independently established required evidence set exists and delivered context lacks at least one required element. |
| R4 | Relevant-noise interference | Paired same-question/evidence conditions differ only by added distractors, and judgment changes. |
| C1 | Context packing loss | Required evidence was retrieved but removed before model input. |
| G1 | Sufficient context, wrong answer | Context sufficiency was independently established and output is incorrect under a qualified scorer. |
| G2 | Proposition or scope mismatch | Output applies a source proposition to the wrong requirement, entity, time, or method/output dimension. |
| G3 | Unsupported claim or overclaim | A substantive answer claim is not supported by the actual delivered context. |
| G4 | Unnecessary abstention | Sufficient evidence exists in delivered context and a determinate answer was expected, but model abstains. |
| G5 | Citation or evidence localization error | Cited source ID/span does not support the attached claim. |
| J1 | Scorer uncertainty | Reference answer or LLM judge cannot reliably distinguish the case; requires human audit or alternate scoring. |

Do not infer R1–R3 from VersionQA's answer-only CSV or infer retrieval quality from LIT-RAGBench supplied chunks. Do not label a generator error from retrieval output alone. A controlled `gold-only` versus `gold+distractor` contrast estimates an effect under that constructed context condition; it does not prove the source of errors in an unaltered end-to-end run.

The first strong objection to the proposed cross-benchmark study is construct mismatch: Korean temporal retrieval, small versioned-document QA, and fictional supplied-context generation have distinct targets. They can triangulate mechanisms, but a pooled score would have no coherent estimand. A second concern is public-test adaptation: absent official development splits, repeated tuning would destroy confirmation value. Both are protocol gates, not reasons to abandon the study.
