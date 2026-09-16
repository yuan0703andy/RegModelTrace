import json
from pathlib import Path

import pytest

from regmodeltrace.retrieval_packet import (
    STAGES,
    RetrievalPacketError,
    build_saved_retrieval_packet,
    classify_stage_loss,
    make_stage_ledger,
    replay_candidate_packet,
    retrieval_only_ledger,
    validate_candidate_packet,
)


ROOT = Path(__file__).resolve().parents[2]


def _packet():
    return build_saved_retrieval_packet(
        repository_root=ROOT,
        source_authority_dir=ROOT / "artifacts/vs-1/source-authority",
        retrieval_bundles_path=ROOT / "regmodeltrace/data/rag/v0/retrieval_bundles.json",
        retrieval_manifest_path=ROOT / "regmodeltrace/data/rag/v0/retrieval_manifest.json",
        question_id="Q1",
    )


def test_saved_three_role_packet_is_bound_and_replayable(tmp_path):
    packet = _packet()
    validate_candidate_packet(packet)
    assert packet["retrieval_run"]["corpus_snapshot_id"] == "CS_815122cca84bcfd9c1637df6"
    assert packet["retrieval_run"]["index_build_id"] == "IB_e922be7973b49bb13e2b340a"
    assert packet["retrieval_run"]["retrieval_executed_in_this_task"] is False
    assert len(packet["candidates"]) == 9
    assert {row["document_role"] for row in packet["candidates"]} == {
        "STANDARDS",
        "PROFESSIONAL_TEAM_REPORT",
        "VENDOR_SUBMISSION",
    }
    path = tmp_path / "packet.json"
    path.write_text(json.dumps(packet), encoding="utf-8")
    replayed = replay_candidate_packet(path)
    assert replayed == packet


def test_retrieval_only_model_stages_are_not_reached():
    ledger = retrieval_only_ledger()
    assert ledger["SEARCHABLE"]["state"] == "YES"
    assert ledger["RETAINED_AFTER_RANKING"]["state"] == "YES"
    for stage in STAGES[3:]:
        assert ledger[stage]["state"] == "NOT_REACHED"
    assert classify_stage_loss(ledger) is None


def test_candidate_and_run_identities_are_stable_across_serialization_builds():
    first = _packet()
    second = _packet()
    assert first["retrieval_run"]["retrieval_run_id"] == second["retrieval_run"][
        "retrieval_run_id"
    ]
    assert [row["candidate_id"] for row in first["candidates"]] == [
        row["candidate_id"] for row in second["candidates"]
    ]


@pytest.mark.parametrize(
    ("states", "expected"),
    [
        ({"SEARCHABLE": "YES", "RETRIEVED": "NO"}, "RETRIEVAL_MISS"),
        (
            {"SEARCHABLE": "YES", "RETRIEVED": "YES", "RETAINED_AFTER_RANKING": "NO"},
            "RANKING_LOSS",
        ),
        (
            {
                "SEARCHABLE": "YES",
                "RETRIEVED": "YES",
                "RETAINED_AFTER_RANKING": "YES",
                "INCLUDED_IN_MODEL_CONTEXT": "NO",
            },
            "CONTEXT_PACKING_LOSS",
        ),
        (
            {
                "SEARCHABLE": "YES",
                "RETRIEVED": "YES",
                "RETAINED_AFTER_RANKING": "YES",
                "INCLUDED_IN_MODEL_CONTEXT": "YES",
                "MODEL_SELECTED": "NO",
            },
            "MODEL_NON_SELECTION",
        ),
    ],
)
def test_stage_loss_attribution(states, expected):
    complete = {stage: "NOT_REACHED" for stage in STAGES}
    complete.update(states)
    assert classify_stage_loss(make_stage_ledger(complete)) == expected


def test_stage_cannot_execute_after_not_reached():
    states = {stage: "NOT_REACHED" for stage in STAGES}
    states["SEARCHABLE"] = "YES"
    states["RETRIEVED"] = "NOT_REACHED"
    states["MODEL_SELECTED"] = "NO"
    with pytest.raises(RetrievalPacketError):
        make_stage_ledger(states)


def test_packet_identity_tamper_fails():
    packet = _packet()
    packet["candidates"][0]["candidate_id"] = "CE_tampered"
    with pytest.raises(RetrievalPacketError):
        validate_candidate_packet(packet)
