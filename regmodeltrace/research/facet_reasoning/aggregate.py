"""Prospective deterministic aggregation for FT-1 Condition C."""

from __future__ import annotations

from collections.abc import Iterable

from .schema import EvidenceSufficiency, FacetState, Relation


AGGREGATION_RULE_VERSION = "ft1-aggregation-1.0"


def aggregate_relation(
    *,
    constraint_status: str,
    evidence_sufficiency: EvidenceSufficiency | str,
    facet_states: Iterable[FacetState | str],
) -> Relation | None:
    """Aggregate atomic facet states without consulting model relation output.

    OR alternatives must be resolved during human facet construction: an unused
    permitted alternative is `NOT_APPLICABLE`, not `NOT_DEMONSTRATED`.
    """

    if constraint_status == "NOT_PRESCRIBED":
        return None
    sufficiency = EvidenceSufficiency(evidence_sufficiency)
    if sufficiency != EvidenceSufficiency.SUFFICIENT:
        return None

    states = [FacetState(state) for state in facet_states]
    applicable = [state for state in states if state != FacetState.NOT_APPLICABLE]
    if not applicable:
        return None
    if FacetState.CONTRADICTED in applicable:
        return Relation.CONFLICT
    if all(state == FacetState.DEMONSTRATED for state in applicable):
        return Relation.ALIGNED
    if (
        FacetState.DEMONSTRATED in applicable
        and FacetState.NOT_DEMONSTRATED in applicable
    ):
        return Relation.PARTIALLY_ALIGNED
    return None
