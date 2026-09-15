"""Score saved Condition A and one frozen B/C run after raw persistence."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any

from .aggregate import aggregate_relation
from .metrics import classification_metrics, facet_metrics


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write(path: Path, value: Any) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def evaluate_condition(
    condition: str,
    truth: dict[str, dict[str, Any]],
    predictions: dict[tuple[str, str], dict[str, Any]],
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    relation_rows, facet_rows, residuals = [], [], []
    for case_id, case in truth.items():
        result = predictions.get((case_id, condition))
        if not result or result["parse_status"] != "PASS":
            residuals.append({"case_id": case_id, "kind": "OUTPUT_INTERFACE_ERROR"})
            continue
        pred = result["prediction"]
        truth_facets = {item["facet_id"]: item["state"] for item in case["facets"]}
        for facet_id, expected in truth_facets.items():
            actual = pred["facets"][facet_id]
            facet_rows.append({"case_id": case_id, "facet_id": facet_id, "truth": expected, "prediction": actual})
            if actual != expected:
                residuals.append(
                    {
                        "case_id": case_id,
                        "corpus_id": case["corpus_id"],
                        "requirement_family": case["requirement_family"],
                        "facet_id": facet_id,
                        "kind": "FACET_STATE_ERROR",
                        "truth": expected,
                        "prediction": actual,
                    }
                )
        relation = pred.get("overall_relation")
        if condition == "C":
            relation = aggregate_relation(
                constraint_status=case["constraint_status"],
                evidence_sufficiency=case["evidence_sufficiency"],
                facet_states=pred["facets"].values(),
            )
            relation = relation.value if relation is not None else None
        if case.get("relation") is not None:
            relation_rows.append({"case_id": case_id, "truth": case["relation"], "prediction": relation})
    metrics = classification_metrics(relation_rows)
    metrics["facet_metrics"] = facet_metrics(facet_rows)
    metrics["structured_output_validity"] = {
        "valid": sum(predictions.get((case_id, condition), {}).get("parse_status") == "PASS" for case_id in truth),
        "total": len(truth),
    }
    return metrics, residuals


def saved_condition_a(path: Path, eligible: set[str]) -> dict[str, Any]:
    rows = list(csv.DictReader(path.open(encoding="utf-8")))
    relation_rows = [
        {"case_id": row["case_id"], "truth": row["truth_relation"], "prediction": row["relation_prediction"]}
        for row in rows
        if row["case_kind"] == "PRIMARY" and row["case_id"] in eligible and row["truth_relation"]
    ]
    primary = [row for row in rows if row["case_kind"] == "PRIMARY" and row["case_id"] in eligible]
    suff_correct = sum(row["binary_prediction_correct"] == "True" for row in primary)
    metrics = classification_metrics(relation_rows)
    metrics["evidence_sufficiency_accuracy"] = suff_correct / len(primary) if primary else None
    metrics["evidence_sufficiency_n"] = len(primary)
    return metrics


def decide(a: dict[str, Any], c: dict[str, Any], residuals: list[dict[str, Any]], rule: dict[str, Any], safety_violations: int, *, matched_condition_a: bool = False) -> str:
    if not matched_condition_a:
        return "EVIDENCE_INCONCLUSIVE"
    partial_support = c["per_class"]["PARTIALLY_ALIGNED"]["support"]
    aligned_support = c["per_class"]["ALIGNED"]["support"]
    if partial_support < rule["minimum_partial_truth_cases"] or aligned_support < rule["minimum_aligned_truth_cases"]:
        return "EVIDENCE_INCONCLUSIVE"
    dominant = rule["representation_problem_dominant"]
    c_partial, a_partial = c["partial_recall"], a["partial_recall"]
    c_far, a_far = c["false_aligned_rate"], a["false_aligned_rate"]
    c_precision, a_precision = c["aligned_precision"], a["aligned_precision"]
    facet_macro = c["facet_metrics"]["macro_f1_observed_classes"]
    if None not in {c_partial, a_partial, c_far, a_far, c_precision, a_precision, facet_macro}:
        if (
            c_partial - a_partial >= dominant["minimum_condition_c_partial_recall_gain_over_a"]
            and a_far - c_far >= dominant["minimum_condition_c_false_aligned_rate_reduction_from_a"]
            and facet_macro >= dominant["minimum_condition_c_facet_macro_f1"]
            and a_precision - c_precision <= dominant["maximum_aligned_precision_regression"]
            and safety_violations <= dominant["maximum_new_safety_violations"]
        ):
            return "REPRESENTATION_PROBLEM_DOMINANT"
    weight = rule["weight_adaptation_still_justified"]
    error_corpora = {row.get("corpus_id") for row in residuals if row.get("kind") == "FACET_STATE_ERROR"}
    error_families = {row.get("requirement_family") for row in residuals if row.get("kind") == "FACET_STATE_ERROR"}
    if (
        c_partial is not None
        and c_far is not None
        and c_partial <= weight["maximum_condition_c_partial_recall"]
        and c_far >= weight["minimum_condition_c_false_aligned_rate"]
        and len(error_corpora - {None}) >= weight["minimum_residual_error_corpora"]
        and len(error_families - {None}) >= weight["minimum_residual_error_requirement_families"]
    ):
        return "WEIGHT_ADAPTATION_STILL_JUSTIFIED"
    return "EVIDENCE_INCONCLUSIVE"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--frozen", type=Path, required=True)
    parser.add_argument("--run", type=Path, required=True)
    parser.add_argument("--condition-a-csv", type=Path, required=True)
    parser.add_argument("--safety-violations", type=int, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    manifest = load(args.run / "run_manifest.json")
    if manifest.get("raw_persisted_utc") is None:
        raise ValueError("Raw outputs were not persisted before scoring")
    truth_list = load(args.frozen / "truth.json")
    truth = {case["case_id"]: case for case in truth_list}
    predictions = {(item["case_id"], item["condition"]): item for item in load(args.run / "results.json")}
    a = saved_condition_a(args.condition_a_csv, set(truth))
    b, b_residuals = evaluate_condition("B", truth, predictions)
    c, c_residuals = evaluate_condition("C", truth, predictions)
    rule = load(args.frozen / "decision_rule.json")
    decision = decide(a, c, c_residuals, rule, args.safety_violations)
    report = {
        "matched_condition_a": False,
        "comparative_decision_limitation": "Saved historical A does not certify identical prospectively frozen evidence. A matched-reference protocol is pending.",
        "condition_a": a,
        "condition_b": b,
        "condition_c": c,
        "condition_d": "NOT_RUN",
        "condition_b_residuals": b_residuals,
        "condition_c_residuals": c_residuals,
        "new_safety_violations": args.safety_violations,
        "probability_metrics": {
            "condition_a": "CARRY_FORWARD_SAVED_V2_2_SCORES",
            "condition_b": "NOT_AVAILABLE_FROM_STRUCTURED_MULTI_TOKEN_OUTPUT",
            "condition_c": "NOT_AVAILABLE_FROM_STRUCTURED_MULTI_TOKEN_OUTPUT",
            "calibration_claim": "NOT_AUTHORIZED",
        },
        "decision": decision,
        "lora_authorized": False,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    write(args.output, report)


if __name__ == "__main__":
    main()
