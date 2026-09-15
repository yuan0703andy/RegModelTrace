"""Model-facing contracts for FT-1 Conditions B and C."""

from __future__ import annotations

import json
from typing import Any

from .schema import FacetCase


SYSTEM_INSTRUCTION = """You classify documentary support for atomic regulatory facets.
Use only the bounded propositions. Vendor evidence determines vendor facet states.
Reviewer review or verification never fills missing vendor evidence. NOT_DEMONSTRATED
means not established by this evidence and does not mean noncompliance. A different
implementation method is not a defect unless the requirement prescribes that method.
Return only JSON matching the supplied schema."""


def model_payload(case: FacetCase) -> tuple[dict[str, Any], dict[str, str]]:
    bindings: dict[str, str] = {}
    grouped: dict[str, list[dict[str, str]]] = {
        "VENDOR": [],
        "REVIEWER": [],
        "REGULATOR": [],
    }
    for index, item in enumerate(case.evidence, 1):
        handle = f"E{index:02d}"
        bindings[handle] = item.proposition_id
        role = {
            "STANDARDS": "REGULATOR",
            "VENDOR_SUBMISSION": "VENDOR",
            "PROFESSIONAL_TEAM_REPORT": "REVIEWER",
        }.get(item.actor_role, item.actor_role)
        if role not in grouped:
            raise ValueError(f"Unknown provenance actor role: {item.actor_role}")
        grouped[role].append({"handle": handle, "text": item.text})
    payload = {
        "requirement": {
            "id": case.requirement_id,
            "text": case.requirement_text,
            "facets": [{"facet_id": item.facet_id, "text": item.text} for item in case.facets],
        },
        "vendor_evidence": grouped["VENDOR"],
        "reviewer_evidence": grouped["REVIEWER"],
        "regulator_evidence": grouped["REGULATOR"],
    }
    return payload, bindings


def build_request(case: FacetCase, condition: str) -> dict[str, Any]:
    if condition not in {"B", "C"}:
        raise ValueError("Condition must be B or C")
    facet_properties = {
        facet.facet_id: {"type": "string", "enum": [
            "DEMONSTRATED", "NOT_DEMONSTRATED", "CONTRADICTED", "NOT_APPLICABLE"
        ]}
        for facet in case.facets
    }
    schema: dict[str, Any] = {
        "type": "object",
        "properties": {
            "facets": {
                "type": "object",
                "properties": facet_properties,
                "required": list(facet_properties),
                "additionalProperties": False,
            }
        },
        "required": ["facets"],
        "additionalProperties": False,
    }
    if condition == "B":
        schema["properties"]["overall_relation"] = {
            "anyOf": [
                {"type": "string", "enum": ["ALIGNED", "PARTIALLY_ALIGNED", "CONFLICT"]},
                {"type": "null"},
            ]
        }
        schema["required"].append("overall_relation")
    payload, bindings = model_payload(case)
    return {
        "request_id": f"FT1-{condition}-{case.case_id}",
        "case_id": case.case_id,
        "condition": condition,
        "system": SYSTEM_INSTRUCTION,
        "input": payload,
        "host_bindings": bindings,
        "output_schema": schema,
    }


def render_prompt(request: dict[str, Any]) -> str:
    return request["system"] + "\n\n" + json.dumps(
        {"input": request["input"], "output_schema": request["output_schema"]},
        ensure_ascii=False,
        sort_keys=True,
    )
