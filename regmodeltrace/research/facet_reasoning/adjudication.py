"""Validate independent human returns and compute raw agreement."""

from __future__ import annotations

from collections import Counter
from typing import Any

from .schema import EvidenceSufficiency, FacetState, Relation


def cohen_kappa(pairs: list[tuple[Any, Any]]) -> float | None:
    if not pairs:
        return None
    observed = sum(left == right for left, right in pairs) / len(pairs)
    left_counts = Counter(left for left, _ in pairs)
    right_counts = Counter(right for _, right in pairs)
    labels = set(left_counts) | set(right_counts)
    expected = sum(
        left_counts[label] / len(pairs) * right_counts[label] / len(pairs)
        for label in labels
    )
    if expected == 1:
        return 1.0 if observed == 1 else None
    return (observed - expected) / (1 - expected)


def validate_return(value: dict[str, Any]) -> None:
    required_header = ["adjudicator_name", "adjudication_date", "attestation"]
    if any(not value.get(field) for field in required_header):
        raise ValueError("Human return is unsigned or incomplete")
    cases = value.get("cases", [])
    if not cases or len({case["case_id"] for case in cases}) != len(cases):
        raise ValueError("Human return requires nonempty, unique case identities")
    for case in cases:
        if case.get("constraint_status") not in {"PRESCRIBED", "NOT_PRESCRIBED"}:
            raise ValueError("Every comparison needs an applicability decision")
        if case.get("review_coverage") not in {"DIRECT", "PARTIAL", "NOT_FOUND", "NOT_ASSESSED"}:
            raise ValueError("Every comparison needs an independent review-coverage decision")
        if not case.get("case_rationale") or not case.get("facets"):
            raise ValueError("Every comparison needs a rationale and resolved facets")
        if len({facet["facet_id"] for facet in case["facets"]}) != len(case["facets"]):
            raise ValueError("Duplicate facet identity")
        if case["constraint_status"] == "NOT_PRESCRIBED" and (
            case["evidence_sufficiency"] != "NOT_APPLICABLE"
            or case.get("overall_relation") is not None
        ):
            raise ValueError("Not-prescribed comparison must exit the relation simplex")
        EvidenceSufficiency(case["evidence_sufficiency"])
        if case["evidence_sufficiency"] == "SUFFICIENT":
            Relation(case["overall_relation"])
        elif case.get("overall_relation") is not None:
            raise ValueError("Relation must be null when evidence is not sufficient")
        for facet in case.get("facets", []):
            FacetState(facet["state"])
            if not facet.get("rationale"):
                raise ValueError("Every facet needs a human rationale")


def agreement(left: dict[str, Any], right: dict[str, Any]) -> dict[str, Any]:
    validate_return(left)
    validate_return(right)
    if left["adjudicator_name"].strip().casefold() == right["adjudicator_name"].strip().casefold():
        raise ValueError("Independent returns require two distinct human adjudicators")
    left_cases = {case["case_id"]: case for case in left["cases"]}
    right_cases = {case["case_id"]: case for case in right["cases"]}
    if set(left_cases) != set(right_cases):
        raise ValueError("Adjudicators returned different case sets")

    counts = Counter()
    pairs: dict[str, list[tuple[Any, Any]]] = {
        "constraint_status": [],
        "evidence_sufficiency": [],
        "overall_relation": [],
        "review_coverage": [],
        "facet_state": [],
    }
    disagreements = []
    for case_id in sorted(left_cases):
        a, b = left_cases[case_id], right_cases[case_id]
        for field in ["constraint_status", "evidence_sufficiency", "overall_relation", "review_coverage"]:
            pairs[field].append((a.get(field), b.get(field)))
            counts[f"{field}_total"] += 1
            if a.get(field) == b.get(field):
                counts[f"{field}_agree"] += 1
            else:
                disagreements.append({"case_id": case_id, "field": field, "a": a.get(field), "b": b.get(field)})
        af = {item["facet_id"]: item for item in a["facets"]}
        bf = {item["facet_id"]: item for item in b["facets"]}
        if set(af) != set(bf):
            disagreements.append({"case_id": case_id, "field": "facet_boundaries", "a": sorted(af), "b": sorted(bf)})
            continue
        for facet_id in sorted(af):
            pairs["facet_state"].append((af[facet_id]["state"], bf[facet_id]["state"]))
            counts["facet_state_total"] += 1
            if af[facet_id]["state"] == bf[facet_id]["state"]:
                counts["facet_state_agree"] += 1
            else:
                disagreements.append({"case_id": case_id, "facet_id": facet_id, "field": "facet_state", "a": af[facet_id]["state"], "b": bf[facet_id]["state"]})
    rates = {
        key.removesuffix("_agree"): counts[key] / counts[key.replace("_agree", "_total")]
        for key in counts
        if key.endswith("_agree") and counts[key.replace("_agree", "_total")]
    }
    return {
        "raw_agreement": rates,
        "cohen_kappa": {field: cohen_kappa(values) for field, values in pairs.items()},
        "counts": dict(counts),
        "disagreements": disagreements,
    }
