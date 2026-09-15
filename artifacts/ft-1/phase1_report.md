# RegModelTrace FT-1 Phase 1 Status

Date: 2026-09-15  
Decision: `EVIDENCE_INCONCLUSIVE`  
LoRA authorization: **No**

## Boundary preserved

The completed release remains closed at Git commit `9b0c0d29f3970613e14b5411041a8a88e2e22f93`. Test E was not reopened, no historical truth or score was edited, no retrieval/Ray/model change was made, and no inference or training run occurred.

## Implemented

- Prospective four-state facet ontology and human annotation guide.
- Prospective deterministic aggregation rule and decision thresholds.
- Separate research-only schemas, dataset builder, Condition B/C contracts, GPU runner, scorer, and agreement checker.
- Hash inventory of five external frozen v2.2 fixtures.
- Leakage metadata for vendor lineage, version, requirement family, regulator text, source passage, revision ancestry, and review ancestry.
- A 19-case historical candidate pack excluding CoreLogic, now retired for independent adjudication following the source-scope audit.
- Saved Condition A import and summary; the closed fixtures were not rerun.

## Current data audit

| Item | Count |
|---|---:|
| Historical comparison truth records | 32 |
| Model-evaluable primary cases | 30 |
| `ALIGNED` | 24 |
| `PARTIALLY_ALIGNED` | 5 |
| `INSUFFICIENT` | 1 |
| `NOT_PRESCRIBED` | 2 |
| Cases with complete canonical human facet truth | 8 |
| Cases still requiring facet adjudication | 22 |
| Canonical explicit facet states | 37 `DEMONSTRATED` |
| Legacy composite states requiring re-adjudication | 4 |

The current canonical facet truth has no `NOT_DEMONSTRATED`, `CONTRADICTED`, or `NOT_APPLICABLE` examples. Running B/C on those eight cases would therefore avoid the target failure rather than diagnose it.

All 30 model-evaluable historical cases fall into one conservative connected leakage group once shared regulator text, vendor/version lineage, and source ancestry are honored. Random row splitting would be invalid. Future training data needs independent vendor-years and requirement families that break this dependency graph.

## Condition A, saved historical results

| Metric | Saved result |
|---|---:|
| Evidence-sufficiency correctness | 23/30 |
| Joint two-stage correctness | 18/30 |
| Truth `PARTIALLY_ALIGNED` recall | 0/5 |
| Truth `ALIGNED` recall | 21/24 |
| `ALIGNED` precision | 21/26 = 80.77% |
| False-`ALIGNED` rate on partial/conflict truth | 5/5 = 100% |
| Natural `CONFLICT` support | 0 |

These figures justify the diagnostic, but they do not identify whether representation or weights caused the failures.

## Human gate

The specification requires independent double adjudication. No second human has supplied a signed facet-level return, and most historical cases never had atomic facet truth. An AI-generated second opinion would not satisfy this requirement.

Therefore:

```text
Condition A = IMPORTED_SAVED_RESULTS
Condition B = BLOCKED_HUMAN_GATE
Condition C = BLOCKED_HUMAN_GATE
Condition D = NOT_AUTHORIZED
TRAINING_DATA_READY = NO
DECISION = EVIDENCE_INCONCLUSIVE
```

The next valid action is to verify or newly establish outcome-independent evidence scopes for other cases, complete the 20–30-case pilot, and then obtain two independent human facet adjudications, resolution, and prospective truth freeze. Historical fixture membership alone does not certify blindness. Only then may the DCC B/C runner execute.

## Verification

- Offline tests: 16 passed.
- Deterministic source-scope audit rerun and retained regulator-metadata copy hashes: passed.
- OpenSpec strict validation: 7/7 items passed.
- DCC archive presence and compute-node routing: passed.
- Qwen inference: not run, by gate.
- Blank-return fail-closed check: passed; freeze creation stopped before writing output.
- LoRA/QLoRA: not run and not authorized.

## Project-owner scope update

```text
CORELOGIC_SOURCE_ONLY_REAUDIT = SKIPPED
Reason = original blinded package unavailable after cleanup
Do not reconstruct from adjudicated fixture
Historical CoreLogic judgment = ERROR_ANALYSIS_ONLY
```

Five CoreLogic entries were removed from the pilot and return templates. The remaining 19 historical candidates are provisional: they require clean source-scope verification or replacement by new independently established cases. No class labels or known model outcomes are used to backfill the pilot. The 20–30-case pilot target and independent human gate remain unchanged.

## Completed source-scope audit

All 19 current fixture-derived bundles are EXCLUDE for independent adjudication. Nine original Impact/Verisk regulator/source seeds are KEEP for fresh scope construction; ten seeds are UNRESOLVED. Independent pilot ready: 0. Existing return templates are retired. B/C remain blocked; no inference or training occurred. See [the eligibility report](source_scope_audit/eligibility_report.md). Historical A is reference-only when rebuilt bundles differ; matched A/B/C inputs remain a prerequisite.

## Source-only preparation completed

A separate 24-case development candidate pack is prepared for Impact and Verisk (12 full standards per vendor). Dimensions were selected from regulator-only structure using two hash-ordered standards per discipline and locked before vendor/reviewer input reads. No class balance, historical membership, alignment labels, or model output influenced the rebuild.

All source text blocks reconstruct from canonical page spans, and five original PDF hashes match the archive. Geometry alignment and unsupported table-header warnings remain explicit. The broad 7,846 block references are navigation context, not Gold evidence or a recall denominator. Mechanical subsection proposals still require human atomic splitting and OR/condition review.

The self-contained review package and checksum inventory are preserved outside Git. Preparation is COMPLETE; independent scope verification, two actual human adjudications, disagreement resolution, prospective truth freeze, and a matched A/B/C reference are NOT COMPLETE. No model inference or training occurred. FT-1 remains EVIDENCE_INCONCLUSIVE.

## Corrected context-budget diagnostic

The first CPU tokenizer diagnostic was invalid because len(mapping) counted fields, not token IDs. Its raw receipt is preserved under an explicitly invalid v1 filename. Corrected token-ID counting found 19/24 broad navigation prototypes over the frozen budget (input-token range 6,186–29,985). This is not a final B/C context assessment. Scope finalization and exact-template preflight remain required; no truncation or inference occurred. The same generic counting defect was fixed in the research runner before any run.
