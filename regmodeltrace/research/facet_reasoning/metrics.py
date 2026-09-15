"""Evaluation metrics for Conditions A/B/C without calibration claims."""

from __future__ import annotations

import math
from collections import Counter
from typing import Any


RELATIONS = ("ALIGNED", "PARTIALLY_ALIGNED", "CONFLICT")


def safe_ratio(numerator: int, denominator: int) -> float | None:
    return numerator / denominator if denominator else None


def classification_metrics(rows: list[dict[str, Any]]) -> dict[str, Any]:
    eligible = [row for row in rows if row.get("truth") in RELATIONS and row.get("prediction") in RELATIONS]
    matrix = {truth: {pred: 0 for pred in RELATIONS} for truth in RELATIONS}
    for row in eligible:
        matrix[row["truth"]][row["prediction"]] += 1
    per_class = {}
    f1_values = []
    recalls = []
    for label in RELATIONS:
        tp = matrix[label][label]
        fp = sum(matrix[other][label] for other in RELATIONS if other != label)
        fn = sum(matrix[label][other] for other in RELATIONS if other != label)
        precision = safe_ratio(tp, tp + fp)
        recall = safe_ratio(tp, tp + fn)
        f1 = None if precision is None or recall is None or precision + recall == 0 else 2 * precision * recall / (precision + recall)
        per_class[label] = {"precision": precision, "recall": recall, "f1": f1, "support": tp + fn}
        if f1 is not None:
            f1_values.append(f1)
        if recall is not None:
            recalls.append(recall)
    risky_truth = [row for row in eligible if row["truth"] in {"PARTIALLY_ALIGNED", "CONFLICT"}]
    false_aligned = sum(row["prediction"] == "ALIGNED" for row in risky_truth)
    return {
        "n": len(eligible),
        "confusion_matrix": matrix,
        "per_class": per_class,
        "macro_f1_observed_classes": sum(f1_values) / len(f1_values) if f1_values else None,
        "balanced_accuracy_observed_classes": sum(recalls) / len(recalls) if recalls else None,
        "partial_recall": per_class["PARTIALLY_ALIGNED"]["recall"],
        "aligned_precision": per_class["ALIGNED"]["precision"],
        "false_aligned_rate": safe_ratio(false_aligned, len(risky_truth)),
    }


def proper_scores(rows: list[dict[str, Any]]) -> dict[str, float | int | None]:
    scored = [row for row in rows if row.get("truth") in RELATIONS and row.get("probabilities")]
    if not scored:
        return {"n": 0, "brier": None, "log_score": None}
    brier = 0.0
    log_score = 0.0
    for row in scored:
        probs = row["probabilities"]
        brier += sum((float(probs[label]) - float(label == row["truth"])) ** 2 for label in RELATIONS)
        log_score -= math.log(max(float(probs[row["truth"]]), 1e-300))
    return {"n": len(scored), "brier": brier / len(scored), "log_score": log_score / len(scored)}


def facet_metrics(rows: list[dict[str, str]]) -> dict[str, Any]:
    labels = ("DEMONSTRATED", "NOT_DEMONSTRATED", "CONTRADICTED", "NOT_APPLICABLE")
    valid = [row for row in rows if row.get("truth") in labels and row.get("prediction") in labels]
    correct = sum(row["truth"] == row["prediction"] for row in valid)
    supports = Counter(row["truth"] for row in valid)
    f1s = []
    per_class = {}
    for label in labels:
        tp = sum(row["truth"] == label and row["prediction"] == label for row in valid)
        fp = sum(row["truth"] != label and row["prediction"] == label for row in valid)
        fn = sum(row["truth"] == label and row["prediction"] != label for row in valid)
        p, r = safe_ratio(tp, tp + fp), safe_ratio(tp, tp + fn)
        f1 = None if p is None or r is None or p + r == 0 else 2 * p * r / (p + r)
        per_class[label] = {"precision": p, "recall": r, "f1": f1, "support": supports[label]}
        if f1 is not None:
            f1s.append(f1)
    return {"n": len(valid), "accuracy": safe_ratio(correct, len(valid)), "macro_f1_observed_classes": sum(f1s) / len(f1s) if f1s else None, "per_class": per_class}
