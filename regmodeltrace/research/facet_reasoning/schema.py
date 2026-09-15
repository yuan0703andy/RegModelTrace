"""Strict schemas for the FT-1 research track.

The frozen release does not import this module.  It deliberately keeps host-owned
identity and provenance outside the model output contract.
"""

from __future__ import annotations

from enum import StrEnum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, model_validator


class FacetState(StrEnum):
    DEMONSTRATED = "DEMONSTRATED"
    NOT_DEMONSTRATED = "NOT_DEMONSTRATED"
    CONTRADICTED = "CONTRADICTED"
    NOT_APPLICABLE = "NOT_APPLICABLE"


class EvidenceSufficiency(StrEnum):
    SUFFICIENT = "SUFFICIENT"
    INSUFFICIENT = "INSUFFICIENT"
    NOT_APPLICABLE = "NOT_APPLICABLE"


class Relation(StrEnum):
    ALIGNED = "ALIGNED"
    PARTIALLY_ALIGNED = "PARTIALLY_ALIGNED"
    CONFLICT = "CONFLICT"


class FacetDefinition(BaseModel):
    model_config = ConfigDict(extra="forbid")

    facet_id: str = Field(min_length=1)
    text: str = Field(min_length=1)
    logic_group: str = "AND"
    state: FacetState | None = None
    supporting_proposition_ids: list[str] = Field(default_factory=list)
    limiting_proposition_ids: list[str] = Field(default_factory=list)
    annotation_status: str = "UNADJUDICATED"


class EvidenceProposition(BaseModel):
    model_config = ConfigDict(extra="forbid")

    proposition_id: str
    actor_role: str
    text: str
    document_id: str
    pages: list[int]
    evidence_role: str | None = None


class FacetCase(BaseModel):
    model_config = ConfigDict(extra="forbid")

    case_id: str
    comparison_id: str
    corpus_id: str
    requirement_id: str
    requirement_text: str
    constraint_status: str
    facets: list[FacetDefinition]
    evidence: list[EvidenceProposition]
    evidence_sufficiency: EvidenceSufficiency | None = None
    relation: Relation | None = None
    vendor_group: str
    model_version_group: str
    requirement_family: str
    regulator_text_group: str
    source_group_ids: list[str]
    revision_ancestry: str
    review_ancestry: str
    leakage_group: str | None = None
    truth_status: str = "UNADJUDICATED"

    @model_validator(mode="after")
    def validate_truth_boundary(self) -> "FacetCase":
        if self.evidence_sufficiency != EvidenceSufficiency.SUFFICIENT and self.relation is not None:
            raise ValueError("Relation is defined only for truth-sufficient comparisons")
        if self.truth_status == "FROZEN_HUMAN_FACET_TRUTH":
            if not self.facets or any(facet.state is None for facet in self.facets):
                raise ValueError("Frozen facet truth requires a state for every facet")
        return self


class FacetPrediction(BaseModel):
    """Condition C output: the model predicts states only."""

    model_config = ConfigDict(extra="forbid")
    facets: dict[str, FacetState]


class FacetAndRelationPrediction(FacetPrediction):
    """Condition B output: facet states and an overall relation."""

    overall_relation: Relation | None


def json_schema_bundle() -> dict[str, Any]:
    return {
        "facet_case": FacetCase.model_json_schema(),
        "condition_b_output": FacetAndRelationPrediction.model_json_schema(),
        "condition_c_output": FacetPrediction.model_json_schema(),
    }
