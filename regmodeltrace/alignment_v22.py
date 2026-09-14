"""Forced-choice alignment probability readout for the v2.2 pilot."""

from __future__ import annotations

import math
from typing import Any


EVIDENCE_LABELS = ("INSUFFICIENT", "SUFFICIENT")
RELATION_LABELS = ("ALIGNED", "PARTIALLY_ALIGNED", "CONFLICT")


def stable_softmax(log_scores: dict[str, float], labels: tuple[str, ...]) -> dict[str, float]:
    """Renormalize finite candidate log probabilities on a fixed label set."""
    if set(log_scores) != set(labels):
        raise ValueError("Candidate score labels do not match the frozen label set")
    values = [float(log_scores[label]) for label in labels]
    if not all(math.isfinite(value) for value in values):
        raise ValueError("Candidate log probabilities must be finite")
    maximum = max(values)
    weights = [math.exp(value - maximum) for value in values]
    denominator = sum(weights)
    if not math.isfinite(denominator) or denominator <= 0:
        raise ValueError("Candidate normalization failed")
    probabilities = {label: weight / denominator for label, weight in zip(labels, weights)}
    if abs(sum(probabilities.values()) - 1.0) > 1e-12:
        raise ValueError("Host-normalized probabilities do not sum to one")
    return probabilities


def choice_mapping(contract: dict[str, Any], task: str) -> tuple[tuple[str, ...], dict[str, str], dict[str, int]]:
    """Return the frozen label order and verbalizer/token mappings for one task."""
    if task not in contract["tasks"]:
        raise ValueError(f"Unknown choice task: {task}")
    entries = contract["tasks"][task]["choices"]
    labels = tuple(entry["label"] for entry in entries)
    verbalizers = {entry["label"]: entry["verbalizer"] for entry in entries}
    token_ids = {entry["label"]: int(entry["token_id"]) for entry in entries}
    if len(set(labels)) != len(labels) or len(set(verbalizers.values())) != len(labels) or len(set(token_ids.values())) != len(labels):
        raise ValueError("Choice labels, verbalizers, and token IDs must be unique")
    return labels, verbalizers, token_ids


def serialize_logprob(value: Any) -> dict[str, Any]:
    return {
        "logprob": float(value.logprob),
        "rank": value.rank,
        "decoded_token": value.decoded_token,
    }


def read_choice_scores(
    token_logprobs: dict[int, Any],
    generated_token_ids: list[int] | tuple[int, ...],
    contract: dict[str, Any],
    task: str,
) -> dict[str, Any]:
    """Resolve every frozen candidate token and normalize its returned log probability."""
    labels, verbalizers, token_ids = choice_mapping(contract, task)
    if len(generated_token_ids) != 1:
        raise ValueError("Forced-choice output must contain exactly one token")
    allowed = set(token_ids.values())
    generated_token_id = int(generated_token_ids[0])
    if generated_token_id not in allowed:
        raise ValueError("Generated token is outside the frozen candidate set")
    missing = [token_id for token_id in token_ids.values() if token_id not in token_logprobs]
    if missing:
        raise ValueError(f"Missing requested candidate log probabilities: {missing}")
    raw = {
        label: {
            "verbalizer": verbalizers[label],
            "token_id": token_ids[label],
            **serialize_logprob(token_logprobs[token_ids[label]]),
        }
        for label in labels
    }
    log_scores = {label: raw[label]["logprob"] for label in labels}
    probabilities = stable_softmax(log_scores, labels)
    generated_label = next(label for label in labels if token_ids[label] == generated_token_id)
    argmax_label = max(labels, key=lambda label: (probabilities[label], -labels.index(label)))
    return {
        "task": task,
        "generated_token_id": generated_token_id,
        "generated_label": generated_label,
        "argmax_label": argmax_label,
        "candidate_logprob_records": raw,
        "candidate_renormalized_probabilities": probabilities,
    }
