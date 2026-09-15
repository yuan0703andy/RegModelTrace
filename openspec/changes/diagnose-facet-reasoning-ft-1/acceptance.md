# Acceptance

- Historical release files and external frozen fixtures are hash-bound and unchanged.
- Facet states, evidence sufficiency, OR logic, reviewer boundaries, revisions, and aggregation are defined before inference.
- Automatically inferred facet labels are never treated as human Gold.
- The pilot contains 20–30 blinded cases and two independent human return files before agreement is computed.
- Dataset grouping prevents shared vendor lineage, regulator text, source passages, revisions, or review ancestry from crossing future splits.
- Condition A uses saved predictions; B/C use the same frozen evidence for each case.
- B/C inference runs only on DCC GPU compute nodes after the human gate passes.
- Metrics include partial recall, aligned precision, false-`ALIGNED` rate, insufficient performance, class and facet metrics, proper scores where available, and safety violations.
- The final Phase 1 decision is one of the three frozen decision values and cannot authorize LoRA unless residual model-side facet errors remain after Condition C.
- Until the human gate and B/C evaluation pass, the required decision is `EVIDENCE_INCONCLUSIVE`, `TRAINING_DATA_READY = NO`, and no training occurs.
