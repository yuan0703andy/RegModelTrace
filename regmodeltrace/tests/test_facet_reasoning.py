from __future__ import annotations

import pytest

from regmodeltrace.research.facet_reasoning.adjudication import agreement
from regmodeltrace.research.facet_reasoning.aggregate import aggregate_relation
from regmodeltrace.research.facet_reasoning.baselines import build_request
from regmodeltrace.research.facet_reasoning.schema import (
    EvidenceSufficiency,
    FacetCase,
    FacetDefinition,
    FacetState,
    Relation,
)


def test_aggregation_separates_missing_proof_from_conflict() -> None:
    assert aggregate_relation(
        constraint_status="PRESCRIBED",
        evidence_sufficiency=EvidenceSufficiency.SUFFICIENT,
        facet_states=[FacetState.DEMONSTRATED, FacetState.NOT_DEMONSTRATED],
    ) == Relation.PARTIALLY_ALIGNED
    assert aggregate_relation(
        constraint_status="PRESCRIBED",
        evidence_sufficiency=EvidenceSufficiency.SUFFICIENT,
        facet_states=[FacetState.DEMONSTRATED, FacetState.CONTRADICTED],
    ) == Relation.CONFLICT


def test_insufficient_has_no_relation() -> None:
    assert aggregate_relation(
        constraint_status="PRESCRIBED",
        evidence_sufficiency=EvidenceSufficiency.INSUFFICIENT,
        facet_states=[FacetState.DEMONSTRATED],
    ) is None


def test_condition_c_output_excludes_relation_and_host_identity() -> None:
    case = FacetCase(
        case_id="C1",
        comparison_id="CMP1",
        corpus_id="corpus",
        requirement_id="G-1",
        requirement_text="A requirement",
        constraint_status="PRESCRIBED",
        facets=[FacetDefinition(facet_id="F1", text="A facet")],
        evidence=[],
        vendor_group="vendor",
        model_version_group="version",
        requirement_family="G",
        regulator_text_group="hash",
        source_group_ids=[],
        revision_ancestry="revision",
        review_ancestry="review",
    )
    request = build_request(case, "C")
    properties = request["output_schema"]["properties"]
    assert set(properties) == {"facets"}
    assert properties["facets"]["additionalProperties"] is False
    assert request["request_id"] == "FT1-C-C1"


def test_agreement_rejects_unsigned_machine_like_returns() -> None:
    value = {"adjudicator_name": None, "adjudication_date": None, "attestation": None, "cases": []}
    with pytest.raises(ValueError, match="unsigned"):
        agreement(value, value)
