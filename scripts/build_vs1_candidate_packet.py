#!/usr/bin/env python3
"""Build the VS-1 Task 2 packet from an existing saved retrieval result."""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from regmodeltrace.retrieval_packet import (  # noqa: E402
    STAGES,
    build_saved_retrieval_packet,
    classify_stage_loss,
    make_stage_ledger,
    replay_candidate_packet,
    validate_candidate_packet,
)
from regmodeltrace.source_authority import canonical_json, file_sha256  # noqa: E402


OUTPUT = ROOT / "artifacts/vs-1/task-2-candidate-packet"


def _write_json(path: Path, value) -> None:
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def _write_jsonl(path: Path, rows) -> None:
    path.write_text(
        "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows),
        encoding="utf-8",
    )


def _loss_fixture() -> dict:
    def ledger(**overrides):
        states = {stage: "NOT_REACHED" for stage in STAGES}
        states.update(overrides)
        return make_stage_ledger(states)

    cases = [
        {
            "case_id": "RETRIEVAL_MISS",
            "ledger": ledger(SEARCHABLE="YES", RETRIEVED="NO"),
            "expected": "RETRIEVAL_MISS",
        },
        {
            "case_id": "RANKING_LOSS",
            "ledger": ledger(
                SEARCHABLE="YES", RETRIEVED="YES", RETAINED_AFTER_RANKING="NO"
            ),
            "expected": "RANKING_LOSS",
        },
        {
            "case_id": "CONTEXT_PACKING_LOSS",
            "ledger": ledger(
                SEARCHABLE="YES",
                RETRIEVED="YES",
                RETAINED_AFTER_RANKING="YES",
                INCLUDED_IN_MODEL_CONTEXT="NO",
            ),
            "expected": "CONTEXT_PACKING_LOSS",
        },
        {
            "case_id": "MODEL_NON_SELECTION",
            "ledger": ledger(
                SEARCHABLE="YES",
                RETRIEVED="YES",
                RETAINED_AFTER_RANKING="YES",
                INCLUDED_IN_MODEL_CONTEXT="YES",
                MODEL_SELECTED="NO",
            ),
            "expected": "MODEL_NON_SELECTION",
        },
        {
            "case_id": "RETRIEVAL_ONLY_NOT_REACHED",
            "ledger": ledger(
                SEARCHABLE="YES",
                RETRIEVED="YES",
                RETAINED_AFTER_RANKING="YES",
            ),
            "expected": None,
        },
    ]
    for case in cases:
        observed = classify_stage_loss(case["ledger"])
        if observed != case["expected"]:
            raise RuntimeError(f"Stage-loss fixture failed: {case['case_id']}")
        case["observed"] = observed
    return {"schema_version": "vs1-stage-loss-fixture-1.0", "cases": cases}


def main() -> None:
    if OUTPUT.exists():
        raise FileExistsError(f"Refusing to overwrite immutable Task 2 output: {OUTPUT}")
    OUTPUT.mkdir(parents=True)
    packet = build_saved_retrieval_packet(
        repository_root=ROOT,
        source_authority_dir=ROOT / "artifacts/vs-1/source-authority",
        retrieval_bundles_path=ROOT / "regmodeltrace/data/rag/v0/retrieval_bundles.json",
        retrieval_manifest_path=ROOT / "regmodeltrace/data/rag/v0/retrieval_manifest.json",
        question_id="Q1",
    )
    validate_candidate_packet(packet)
    _write_json(OUTPUT / "retrieval_run.json", packet["retrieval_run"])
    _write_jsonl(OUTPUT / "candidate_evidence.jsonl", packet["candidates"])
    _write_json(OUTPUT / "candidate_packet.json", packet)
    _write_json(OUTPUT / "stage_loss_fixture.json", _loss_fixture())

    replayed = replay_candidate_packet(OUTPUT / "candidate_packet.json")
    canonical_sha = hashlib.sha256(canonical_json(replayed).encode("utf-8")).hexdigest()
    role_counts = {}
    for candidate in replayed["candidates"]:
        role = candidate["document_role"]
        role_counts[role] = role_counts.get(role, 0) + 1
    verification = {
        "schema_version": "vs1-task2-verification-1.0",
        "status": "PASS",
        "retrieval_run_id": replayed["retrieval_run"]["retrieval_run_id"],
        "corpus_snapshot_id": replayed["retrieval_run"]["corpus_snapshot_id"],
        "index_build_id": replayed["retrieval_run"]["index_build_id"],
        "candidate_count": len(replayed["candidates"]),
        "role_counts": role_counts,
        "candidate_packet_canonical_sha256": canonical_sha,
        "replay_without_retrieval": True,
        "stable_candidate_ids": True,
        "all_model_stages_not_reached": all(
            row["stage_ledger"]["MODEL_SELECTED"]["state"] == "NOT_REACHED"
            for row in replayed["candidates"]
        ),
        "new_model_inference_runs": 0,
        "retrieval_executed_in_task": False,
        "retrieval_behavior_changed": False,
        "embedding_rebuilt": False,
        "retrieval_tuned": False,
        "issues_observed": [
            {
                "issue": "MULTI_ASSERTION_PASSAGE_SEPARATOR_MISMATCH",
                "disposition": "FIXED_WITH_REGRESSION_TEST",
                "detail": (
                    "The source resolver accepted space-joined assertion text while some "
                    "canonical passages use newline joins. Resolution now accepts either "
                    "deterministic separator and still requires exact passage text."
                ),
            }
        ],
    }
    _write_json(OUTPUT / "task2_verification.json", verification)
    (OUTPUT / "task2_report.md").write_text(
        f"""# VS-1 Task 2 — Evidence Stage Ledger and Candidate Packet

**Status:** `PASS`
**Retrieval run:** `{verification['retrieval_run_id']}`
**Corpus snapshot:** `{verification['corpus_snapshot_id']}`
**Index build:** `{verification['index_build_id']}`

## Result

- replayed the frozen Q1 retrieval result; retrieval was not rerun;
- persisted one `RetrievalRun` and {verification['candidate_count']} `CandidateEvidence` records;
- preserved BM25 rank, dense rank, RRF score, role rank, passage identity, and source provenance;
- preserved all three document roles: `{role_counts}`;
- assigned stable candidate IDs bound to corpus, index build, question, and passage;
- recorded all eight stages with `NOT_REACHED | YES | NO` semantics;
- all model and downstream stages remain `NOT_REACHED` in retrieval-only mode;
- replayed and validated the serialized packet without retrieval;
- verified fixtures for `RETRIEVAL_MISS`, `RANKING_LOSS`,
  `CONTEXT_PACKING_LOSS`, and `MODEL_NON_SELECTION`.

## Issue found and resolved

`MULTI_ASSERTION_PASSAGE_SEPARATOR_MISMATCH`: the Task 1 resolver accepted
space-joined assertion text, while some canonical passages use newline joins.
The resolver now accepts either deterministic separator while continuing to
require an exact match to the frozen passage text. A real four-assertion
passage regression test covers the fix.

## Boundaries

```text
new model inference runs = 0
retrieval executed in Task 2 = false
retrieval behavior changed = false
embedding rebuilt = false
retrieval tuned = false
```

The saved RAG v0 artifact exposes returned/retained passages, not the complete
discarded ranking universe. The packet therefore declares
`candidate_universe_scope = RETURNED_RETAINED_CANDIDATES_ONLY` and does not
invent ranking-loss events for candidates that the saved result did not record.
""",
        encoding="utf-8",
    )
    artifact_hashes = {
        path.name: file_sha256(path)
        for path in sorted(OUTPUT.iterdir())
        if path.is_file()
    }
    _write_json(
        OUTPUT / "task2_manifest.json",
        {
            "schema_version": "vs1-task2-manifest-1.0",
            "status": "PASS",
            "artifacts": artifact_hashes,
        },
    )


if __name__ == "__main__":
    main()
