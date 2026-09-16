"""Persistent, replayable retrieval evidence packets for VS-1.

This module serializes retrieval results that already exist. It does not run,
modify, or tune retrieval and it has no model dependency.
"""

from __future__ import annotations

import hashlib
import json
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .source_authority import FrozenCorpusAuthority, canonical_json, file_sha256


STAGES = (
    "SEARCHABLE",
    "RETRIEVED",
    "RETAINED_AFTER_RANKING",
    "INCLUDED_IN_MODEL_CONTEXT",
    "MODEL_SELECTED",
    "HOST_RESOLVED",
    "DELIVERED_TO_HUMAN",
    "HUMAN_VERIFIED",
)
STAGE_STATES = {"NOT_REACHED", "YES", "NO"}


class RetrievalPacketError(ValueError):
    """Raised when a retrieval packet violates its frozen contract."""


def _digest(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def make_stage_ledger(states: dict[str, str]) -> dict[str, dict[str, str]]:
    """Build and validate the complete eight-stage tri-state ledger."""

    if set(states) != set(STAGES):
        missing = sorted(set(STAGES) - set(states))
        extra = sorted(set(states) - set(STAGES))
        raise RetrievalPacketError(f"Stage inventory mismatch: missing={missing}, extra={extra}")

    ledger: dict[str, dict[str, str]] = {}
    prior_blocked = False
    for stage in STAGES:
        state = states[stage]
        if state not in STAGE_STATES:
            raise RetrievalPacketError(f"Invalid state for {stage}: {state}")
        if prior_blocked and state != "NOT_REACHED":
            raise RetrievalPacketError(
                f"Stage {stage} must be NOT_REACHED after an earlier NO/NOT_REACHED"
            )
        ledger[stage] = {"state": state}
        prior_blocked = state in {"NO", "NOT_REACHED"}
    return ledger


def retrieval_only_ledger() -> dict[str, dict[str, str]]:
    """Ledger for a candidate returned and retained by retrieval only."""

    return make_stage_ledger(
        {
            "SEARCHABLE": "YES",
            "RETRIEVED": "YES",
            "RETAINED_AFTER_RANKING": "YES",
            "INCLUDED_IN_MODEL_CONTEXT": "NOT_REACHED",
            "MODEL_SELECTED": "NOT_REACHED",
            "HOST_RESOLVED": "NOT_REACHED",
            "DELIVERED_TO_HUMAN": "NOT_REACHED",
            "HUMAN_VERIFIED": "NOT_REACHED",
        }
    )


def classify_stage_loss(ledger: dict[str, dict[str, str]]) -> str | None:
    """Classify the first executed loss without inventing unexecuted failures."""

    states = {stage: ledger[stage]["state"] for stage in STAGES}
    make_stage_ledger(states)
    loss_by_stage = {
        "RETRIEVED": "RETRIEVAL_MISS",
        "RETAINED_AFTER_RANKING": "RANKING_LOSS",
        "INCLUDED_IN_MODEL_CONTEXT": "CONTEXT_PACKING_LOSS",
        "MODEL_SELECTED": "MODEL_NON_SELECTION",
    }
    for stage in STAGES:
        state = states[stage]
        if state == "NOT_REACHED":
            return None
        if state == "NO":
            return loss_by_stage.get(stage)
    return None


def _candidate_id(
    *, corpus_snapshot_id: str, index_build_id: str, question_sha256: str, passage_id: str
) -> str:
    identity = [corpus_snapshot_id, index_build_id, question_sha256, passage_id]
    return "CE_" + _digest(identity)[:24]


def build_saved_retrieval_packet(
    *,
    repository_root: Path,
    source_authority_dir: Path,
    retrieval_bundles_path: Path,
    retrieval_manifest_path: Path,
    question_id: str,
) -> dict[str, Any]:
    """Convert a saved retrieval result into a source-verified candidate packet."""

    root = Path(repository_root).resolve()
    bundles_path = Path(retrieval_bundles_path).resolve()
    manifest_path = Path(retrieval_manifest_path).resolve()
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    bundles_sha = file_sha256(bundles_path)
    declared = manifest.get("outputs", {}).get(bundles_path.name)
    if declared != bundles_sha:
        raise RetrievalPacketError("Saved retrieval bundle hash does not match its manifest")

    authority = FrozenCorpusAuthority(root, Path(source_authority_dir))
    index_manifest = authority.index_build
    passage_artifact = next(
        row for row in index_manifest["artifacts"] if row["artifact_role"] == "passage_inventory"
    )
    if manifest.get("passage_index_sha256") != passage_artifact["sha256"]:
        raise RetrievalPacketError("Saved retrieval run targets a different passage inventory")

    saved = json.loads(bundles_path.read_text(encoding="utf-8"))
    matches = [row for row in saved["questions"] if row["question_id"] == question_id]
    if len(matches) != 1:
        raise RetrievalPacketError(f"Expected one saved question for {question_id}")
    question_row = matches[0]
    question = question_row["question"]
    question_sha = hashlib.sha256(question.encode("utf-8")).hexdigest()
    run_id = "RR_" + _digest(
        [
            authority.snapshot["corpus_snapshot_id"],
            authority.index_build["index_build_id"],
            question_id,
            question_sha,
            bundles_sha,
        ]
    )[:24]

    candidates = []
    seen_candidate_ids: set[str] = set()
    seen_passages: set[str] = set()
    for section in question_row["sections"]:
        role = section["document_role"]
        for passage in section["passages"]:
            passage_id = passage["passage_id"]
            if passage_id in seen_passages:
                raise RetrievalPacketError(f"Duplicate passage in saved result: {passage_id}")
            resolution = authority.resolve_source(passage_id)
            if resolution["status"] != "RESOLVED":
                raise RetrievalPacketError(f"Passage failed source resolution: {passage_id}")
            if resolution["document_role"] != role:
                raise RetrievalPacketError(f"Document-role mismatch for {passage_id}")
            assertion_ids = [row["assertion_id"] for row in passage["assertions"]]
            resolved_ids = [row["assertion_id"] for row in resolution["assertions"]]
            if assertion_ids != resolved_ids:
                raise RetrievalPacketError(f"Assertion membership mismatch for {passage_id}")

            candidate_id = _candidate_id(
                corpus_snapshot_id=authority.snapshot["corpus_snapshot_id"],
                index_build_id=authority.index_build["index_build_id"],
                question_sha256=question_sha,
                passage_id=passage_id,
            )
            if candidate_id in seen_candidate_ids:
                raise RetrievalPacketError(f"Duplicate candidate identity: {candidate_id}")
            seen_candidate_ids.add(candidate_id)
            seen_passages.add(passage_id)
            candidates.append(
                {
                    "schema_version": "candidate-evidence-1.0",
                    "candidate_id": candidate_id,
                    "retrieval_run_id": run_id,
                    "corpus_snapshot_id": authority.snapshot["corpus_snapshot_id"],
                    "index_build_id": authority.index_build["index_build_id"],
                    "passage_id": passage_id,
                    "assertion_ids": assertion_ids,
                    "document_id": resolution["document_id"],
                    "document_role": role,
                    "pages": resolution["pages"],
                    "text": resolution["quote"],
                    "scores": {
                        "bm25_rank": passage.get("bm25_rank"),
                        "dense_rank": passage.get("dense_rank"),
                        "rrf_score": passage.get("score"),
                        "role_rank": passage.get("role_rank", passage.get("rank")),
                    },
                    "stage_ledger": retrieval_only_ledger(),
                    "loss_classification": None,
                    "source_resolution": resolution,
                }
            )

    retrieval_run = {
        "schema_version": "retrieval-run-1.0",
        "retrieval_run_id": run_id,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "corpus_snapshot_id": authority.snapshot["corpus_snapshot_id"],
        "index_build_id": authority.index_build["index_build_id"],
        "question_id": question_id,
        "question": question,
        "question_sha256": question_sha,
        "mode": "RETRIEVAL_ONLY",
        "execution_origin": "SAVED_RESULT_REPLAY",
        "retrieval_executed_in_this_task": False,
        "source_bundle": str(bundles_path.relative_to(root)),
        "source_bundle_sha256": bundles_sha,
        "source_manifest": str(manifest_path.relative_to(root)),
        "source_manifest_sha256": file_sha256(manifest_path),
        "candidate_universe_scope": "RETURNED_RETAINED_CANDIDATES_ONLY",
        "candidate_count": len(candidates),
        "document_roles": sorted({row["document_role"] for row in candidates}),
    }
    return {
        "schema_version": "retrieval-candidate-packet-1.0",
        "retrieval_run": retrieval_run,
        "candidates": candidates,
    }


def validate_candidate_packet(packet: dict[str, Any]) -> None:
    """Validate identities, bindings, and tri-state semantics for replay."""

    run = packet["retrieval_run"]
    candidates = packet["candidates"]
    if run["candidate_count"] != len(candidates):
        raise RetrievalPacketError("Candidate count mismatch")
    candidate_ids: set[str] = set()
    passage_ids: set[str] = set()
    for candidate in candidates:
        if candidate["retrieval_run_id"] != run["retrieval_run_id"]:
            raise RetrievalPacketError("Candidate retrieval-run binding mismatch")
        for key in ("corpus_snapshot_id", "index_build_id"):
            if candidate[key] != run[key]:
                raise RetrievalPacketError(f"Candidate {key} binding mismatch")
        expected = _candidate_id(
            corpus_snapshot_id=run["corpus_snapshot_id"],
            index_build_id=run["index_build_id"],
            question_sha256=run["question_sha256"],
            passage_id=candidate["passage_id"],
        )
        if candidate["candidate_id"] != expected:
            raise RetrievalPacketError("Candidate stable identity mismatch")
        if candidate["candidate_id"] in candidate_ids or candidate["passage_id"] in passage_ids:
            raise RetrievalPacketError("Duplicate candidate or passage identity")
        candidate_ids.add(candidate["candidate_id"])
        passage_ids.add(candidate["passage_id"])
        states = {
            stage: candidate["stage_ledger"][stage]["state"] for stage in STAGES
        }
        make_stage_ledger(states)
        if classify_stage_loss(candidate["stage_ledger"]) != candidate["loss_classification"]:
            raise RetrievalPacketError("Stage-loss classification mismatch")


def replay_candidate_packet(path: Path) -> dict[str, Any]:
    """Load and validate a packet without retrieval, embedding, or model execution."""

    packet = json.loads(Path(path).read_text(encoding="utf-8"))
    validate_candidate_packet(packet)
    return deepcopy(packet)
