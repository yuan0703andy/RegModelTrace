# Design

## Inputs

The research workspace reads copies of the five frozen historical v2.2 fixtures from the DCC archive. A hash manifest binds every input. The public repository retains only compact derived metadata, code, protocol documents, and audit templates; raw PDFs and historical run stores remain external.

## Facet representation

Each case contains atomic prescribed facets and bounded regulator, vendor, reviewer, supporting, and limiting proposition memberships. A facet state is exactly one of `DEMONSTRATED`, `NOT_DEMONSTRATED`, `CONTRADICTED`, or `NOT_APPLICABLE`. Reviewer evidence is represented separately and cannot demonstrate a vendor facet.

Comparison evidence sufficiency is independent of facet state. Missing documentary proof may yield comparison-level `INSUFFICIENT`; sufficiently bounded evidence showing a mix of demonstrated and not-demonstrated facets may yield `PARTIALLY_ALIGNED`. The annotation guide fixes this boundary before inference.

## Conditions

- Condition A reads saved whole-bundle predictions; it never reruns a closed fixture.
- Condition B presents the same bounded bundle with explicit facets and asks Base Qwen for facet states and an overall relation.
- Condition C uses the same facet-state predictions but computes the relation with the frozen host aggregator.

Conditions B/C are blocked until the selected 20–30-case pilot has two independent human adjudications, disagreements are resolved without model outputs, and facet truth is frozen. Condition D is outside this change.

## Leakage control

Each case records vendor lineage, model year/version, requirement family, shared regulator text, source passages, revision ancestry, and review ancestry. Connected cases form one leakage group and may not cross a future train/dev/test boundary.

## Decision rule

The Phase 1 report returns `REPRESENTATION_PROBLEM_DOMINANT`, `WEIGHT_ADAPTATION_STILL_JUSTIFIED`, or `EVIDENCE_INCONCLUSIVE`. Missing independent human adjudication necessarily yields `EVIDENCE_INCONCLUSIVE`; it never authorizes training.

## Owner-approved CoreLogic exclusion

`CORELOGIC_SOURCE_ONLY_REAUDIT = SKIPPED` because the original blinded package is unavailable after cleanup. Do not reconstruct it from an adjudicated fixture. Historical CoreLogic judgments remain error-analysis evidence only and are excluded from this independent pilot. Other historical fixture candidates require outcome-independent source-scope verification; hidden labels alone do not make an evidence pool blind. Clean/new cases may complete the pilot before human adjudication, disagreement resolution, truth freeze, and B/C inference.
