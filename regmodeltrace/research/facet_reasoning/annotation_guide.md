# FT-1 Human Facet Annotation Guide

Version: `1.0-prospective`  
Model outputs visible to annotators: **No**  
Historical whole-case labels visible during independent annotation: **No**

## Unit of judgment

A facet is one atomic regulatory proposition whose satisfaction can be judged without also deciding a second conjunction. Split `A and B` when either part could be demonstrated independently. Preserve regulator-defined OR alternatives and conditions; do not turn an unused permitted alternative into a missing obligation.

Annotate what the request-scoped documents demonstrate. Do not adjudicate the underlying model by outside knowledge.

## Facet states

- `DEMONSTRATED`: bounded vendor evidence directly establishes the applicable facet.
- `NOT_DEMONSTRATED`: the bounded vendor evidence does not establish the facet. This is a documentary gap, not proof of noncompliance.
- `CONTRADICTED`: bounded evidence explicitly conflicts with the facet. Silence, ambiguity, or a different non-prescribed method is insufficient.
- `NOT_APPLICABLE`: regulator wording makes the facet conditional or an unused OR alternative, and the condition does not apply.

Reviewer evidence is recorded separately. A reviewer statement such as “reviewed” or “verified” cannot change an unsupported vendor facet to `DEMONSTRATED`.

## Comparison-level evidence sufficiency

Use `INSUFFICIENT` when the bounded material does not permit a reliable facet-level comparison, such as vendor evidence consisting only of copied requirements, reviewer-only evidence, future review, wrong-scope material, or evidence too incomplete to determine even which facets are demonstrated.

Use `SUFFICIENT` when the bounded material permits a documentary comparison across the applicable facets. It may show all facets, a mixture of demonstrated and not demonstrated facets, or an explicit contradiction. Thus `SUFFICIENT` does not imply alignment.

Use `NOT_APPLICABLE` only when the dimension is not prescribed or the regulator's scope excludes the comparison.

## Overall relation

Do not choose an overall relation when evidence is `INSUFFICIENT` or the requirement is not prescribed.

- `ALIGNED`: every applicable required facet is `DEMONSTRATED`.
- `PARTIALLY_ALIGNED`: at least one applicable facet is `DEMONSTRATED` and at least one is `NOT_DEMONSTRATED`.
- `CONFLICT`: at least one applicable required facet is `CONTRADICTED`, under the prospective host rule.

The host recomputes this relation. Annotators still provide it so disagreement in human aggregation can be measured.

## OR requirements

Represent mutually permitted alternatives in one logic group. Once one qualifying alternative is demonstrated, mark unused alternatives `NOT_APPLICABLE`; do not penalize the vendor for selecting a permitted method. If the regulation requires a conjunction within the chosen alternative, split and assess its conjuncts.

## Reviewer statements

Record reviewer propositions and coverage, but judge vendor facets only from vendor evidence. Reviewer scrutiny is not a challenge. Reviewer verification is not vendor implementation evidence. A later reviewer disposition cannot by itself prove an earlier vendor state.

## Revisions and time

Adjudicate the document state named by the case. A corrected final state may be aligned even if an earlier defect existed. Preserve earlier defects and revision evidence as limitations. Do not infer that review caused a model or method change without an explicit link. A future review is not completed review.

## Supporting and limiting propositions

For each facet, list exact supporting proposition IDs. List propositions that narrow scope, expose missing proof, or conflict as limiting IDs. A retrieval or shortlist miss is not corpus absence.

## Independent pilot procedure

1. Work from the blinded pack and one blank return file.
2. Do not inspect historical labels, prior Qwen outputs, or the other adjudicator's file.
3. Confirm or revise the proposed atomic facet boundaries.
4. Assign applicability, evidence sufficiency, facet states, relation, support IDs, limitation IDs, and a short rationale.
5. Sign the return with adjudicator identity and date.
6. Agreement is computed only after both files are locked. Disagreements inform guide clarification, not label balancing.
