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

## Source-only pilot rebuild (2026-09-15)

The owner authorized continuing preparation and recording issues. All 19 historical
fixture-derived bundles are excluded from independent adjudication. Rebuild a
separate 24-case development audit pack using retained original Impact/Verisk PDFs
and outcome-free parser products. Select two full standards per discipline
(G, M, S, V, A, CI) by a fixed SHA-256 order over regulator-only standard identities;
use the same 12 requirements for each vendor. Freeze this selection before reading
vendor/reviewer parser products. No known class, model failure, or old evidence
membership may influence selection. Existing regulator dimension locks remain
lineage references, not inherited human facet decisions.

Evidence selection is a mechanical navigation aid: include blocks under matching
standard structure and explicit standard references, with page context. Keep the
full raw PDFs and outcome-free source pools available for material facet and
reversal searches. Record tables, alignment warnings, unlinked cross-references,
and missing dependencies instead of silently interpreting them. A proposed pack
is not certified blinded merely because a deterministic builder produced it:
independent source-scope verification and two actual human returns remain required.

Do not delete existing packs or sources. Store raw/large artifacts outside public
Git with checksum receipts and a preserved local review package. No inference,
training, historical KCC rerun, or historical truth modification is authorized by
preparation alone. Historical A results on different bundles remain reference-only;
a controlled A/B/C comparison requires a matched prospective A protocol before
compute. The current B/C implementation cannot alone identify an A-to-B improvement
on rebuilt inputs.
