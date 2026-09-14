# REVIEW-1 — sequential alignment-audit design

## Objective and boundary

The proposed audit chooses the next evidence action that could resolve a consequential requirement facet at a defensible cost. It does not maximize retrieval volume or model confidence. The principal failure mode to prevent is false closure: reviewer verification, vendor prose, or a high model score must not substitute for evidence about the specific applicable facet.

Access determines what can be claimed:

| Available access | Permissible conclusion |
|---|---|
| Existing public documents | What the public record demonstrates and which evidence needs remain unresolved |
| Additional versioned vendor submissions or test reports | What those artifacts demonstrate, under their declared identity and provenance |
| Authorized execution of a fixed model/build | Behavior observed under the specified test conditions; not all deployed or future behavior |

Vendor contact, outbound requests, execution instructions, and substantive decisions require human approval. REVIEW-1 implements none of them.

## Requirement and facet representation

Each requirement must retain its logical form. `AND` facets, `OR` alternatives, applicability conditions, exceptions, and version/time scope are explicit. A rule permitting either engineering analysis or claims evidence cannot be rewritten as requiring both.

```text
facet_id
parent_requirement_id
logical_group_id and operator
applicability condition and supporting source
version and time scope
exact regulatory proposition IDs
vendor supporting and contradictory proposition IDs
reviewer propositions, stored under a separate actor role
documentary status
unresolved dependency
candidate next evidence action
```

The design-level documentary statuses are:

| Status | Meaning |
|---|---|
| `SUPPORTED` | The available, applicable evidence demonstrates the facet |
| `EXPLICITLY_CONTRADICTED` | An attributable source explicitly conflicts with the facet |
| `NOT_DEMONSTRATED` | The bounded evidence does not demonstrate the facet; this does not prove the implementation lacks it |
| `NOT_APPLICABLE` | A source-supported applicability condition or exception excludes the facet |

These statuses do not automatically relabel historical comparison truth. Aggregating facets into `ALIGNED`, `PARTIALLY_ALIGNED`, or `CONFLICT` requires a separately approved rule and human adjudication.

## Bounded action space

| Action | Required authority | Resulting evidence |
|---|---|---|
| `INSPECT_EXISTING_SOURCE` | Existing authorized corpus access | New proposition membership or explicit unresolved result within that corpus |
| `REQUEST_VENDOR_CLARIFICATION` | Human approval for outbound contact | Attributable, versioned vendor explanation; not independently observed behavior |
| `REQUEST_VERSIONED_VALIDATION_ARTIFACT` | Human approval and vendor capability | Version-bound specification, results, or validation record |
| `REQUEST_VENDOR_EXECUTED_CONFORMANCE_TEST` | Human approval, executable build access, agreed protocol | Vendor-reported or independently witnessed test result, labeled by source origin |
| `STOP_WITH_SUPPORTED_DECISION` | Human-reviewed facet and aggregation decision | Closed supported audit state |
| `STOP_UNRESOLVED` | Human acceptance of remaining uncertainty | Closed unresolved state with the missing dependency preserved |

Every action record must name the facet, missing evidence, possible observations that would support or reverse the interpretation, access requirements, estimated cost when known, and stopping condition. Unknown access or cost remains unknown.

## Illustrative conformance request

Suppose a testing requirement has applicable unit, regression, and integration/coverage facets. Existing vendor evidence demonstrates unit and regression testing but does not demonstrate integration coverage for all applicable components. The next request could be:

> For the declared model build, provide the integration-test specification and execution record mapping each applicable component to the tests actually run. Identify any component treated as not applicable and cite the governing exception.

Possible observations have distinct interpretations:

| Observation | Evidentiary update |
|---|---|
| Version-matched specification and execution records cover every applicable facet | Adds positive documentary or test support |
| Vendor explicitly states the required test was not performed | Creates potential explicit contradiction for human adjudication |
| Vendor gives a source-supported exception | Reopens applicability for that facet |
| Vendor cannot provide the record | Leaves `NOT_DEMONSTRATED`; it does not by itself prove noncompliance |
| Reviewer confirms review without supplying implementation evidence | Changes review coverage but does not fill the vendor-evidence gap |

## Coastal landfall example

For a coastal landfall-frequency requirement, the audit first identifies the prescribed output comparisons, geographic units, intensity groups, reference period, and any allowed tolerances or alternatives. It may request version-matched output comparisons and explanations for differences. It must not require a particular segmentation-based parameterization merely because a different vendor uses one. A non-prescribed implementation choice is evidence about method, not automatically evidence of alignment or conflict.

Testing whether a calibration constraint induces tuning to historical noise is a separate causal experiment. It would require controlled access to executable model or calibration variants, a fixed outcome measure, and an independent assessment protocol. Its estimand would be the effect of changing the calibration constraint on the tested build. It would not establish that regulation historically caused adoption of the method.

## Action selection and stopping

A future formal policy could select action `a` using expected reduction in decision risk minus evidence-acquisition cost:

\[
R(D_t)=\min_d \mathbb{E}[L(d,\theta)\mid D_t],
\]

\[
\mathrm{VOI}(a\mid D_t)=R(D_t)-\mathbb{E}_{Y\mid D_t,a}[R(D_t\cup\{a,Y\})]-\lambda c(a).
\]

Here `D_t` is current evidence, `theta` is a defined target state, `d` is the audit decision, `Y` is the possible observation, and `c(a)` is acquisition cost. The v2.2 forced-choice token probabilities are not a calibrated posterior over `theta` and must not be substituted into this expression. Until observation models, loss, and cost are defensible, a human-prioritized evidence queue is the honest implementation.

The audit stops when:

- all applicable required facets have sufficient evidence for a human-reviewed decision;
- an explicit contradiction warrants escalation;
- no accessible approved action can resolve the remaining facet; or
- the approved evidence budget is exhausted.

The latter two outcomes are `STOP_UNRESOLVED`. More searching or a larger language-model score does not force a conclusion.

## Future evaluation and integration

An offline study could compare a fixed evidence order with an adaptive policy over a pre-frozen evidence universe. It would measure correctly resolved facets and decisions, false clearance of incomplete cases, retained uncertainty, reviewer effort, and acquisition cost at a common budget. Leakage controls must prevent the policy from observing hidden evidence before its reveal. This evaluates sequential acquisition, not modification of a catastrophe model.

A vendor-run conformance study is a different design. It requires version attestation, executable access, an approved test specification, and clear classification of vendor-reported versus independently observed results.

The future integration point remains outside the frozen inference path:

```text
existing RAG and evidence store
  -> proposed requirement/facet ledger
  -> unresolved evidence need
  -> human-approved action
  -> versioned returned artifact or test result
  -> evidence update
  -> explicit human adjudication
```

No autonomous planner, vendor outreach, simulator execution, database migration, or model-weight change is authorized.

## Source

- Tom Rainforth et al. *Modern Bayesian Experimental Design*. 2023. arXiv. https://arxiv.org/abs/2302.14545

