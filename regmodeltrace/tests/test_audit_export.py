import json

import pytest

from regmodeltrace.audit_export import AuditExportError, EvidenceAuditExporter, verify_packet
from regmodeltrace.review_store import ReviewStore


@pytest.fixture
def reviewed_export(tmp_path):
    from regmodeltrace.workbench_server import WORKBENCH

    store = ReviewStore(tmp_path / "reviews.sqlite3", WORKBENCH)
    session = store.create_session("AUTOMATED_PRODUCT_QA_NOT_HUMAN_ADJUDICATION")
    by_role = {}
    for candidate_id, candidate in WORKBENCH.candidates.items():
        by_role.setdefault(candidate["document_role"], candidate_id)
    events = [
        ("qa-standards", by_role["STANDARDS"], "ACCEPTED", "RELEVANT_SUPPORT"),
        ("qa-team", by_role["PROFESSIONAL_TEAM_REPORT"], "REJECTED", "WRONG_SOURCE"),
        ("qa-vendor", by_role["VENDOR_SUBMISSION"], "UNRESOLVED", "NEED_BROADER_SEARCH"),
    ]
    for event_id, candidate_id, decision, reason_code in events:
        store.append(
            session["session_id"],
            candidate_id,
            event_id=event_id,
            decision=decision,
            reason_code=reason_code,
            rationale="Product QA only; no substantive adjudication.",
        )
    return EvidenceAuditExporter(WORKBENCH, store), session["session_id"]


def test_export_is_complete_deterministic_and_replayable(reviewed_export, tmp_path):
    exporter, session_id = reviewed_export
    first = exporter.render(session_id)
    second = exporter.render(session_id)
    assert first == second
    assert set(first) == {"evidence_packet.json", "evidence_packet.md", "audit_record.jsonl"}

    packet = json.loads(first["evidence_packet.json"])
    verify_packet(packet)
    assert packet["candidate_count"] == 9
    assert packet["review_event_count"] == 3
    assert sum(row["review"]["event_count"] == 0 for row in packet["candidates"]) == 6
    assert packet["export_semantics"]["candidate_universe_scope"] == (
        "RETURNED_RETAINED_CANDIDATES_ONLY"
    )
    assert packet["export_semantics"]["frozen_stage_ledger_mutated"] is False
    for exported, frozen in zip(packet["candidates"], exporter.workbench.packet["candidates"]):
        assert exported["frozen_stage_ledger"] == frozen["stage_ledger"]
        assert exported["source_resolution"] == frozen["source_resolution"]

    records = [json.loads(line) for line in first["audit_record.jsonl"].splitlines()]
    assert [row["record_type"] for row in records].count("CANDIDATE_EVIDENCE") == 9
    assert [row["record_type"] for row in records].count("REVIEW_DISPOSITION") == 3
    assert records[0]["record_type"] == "EXPORT_HEADER"
    assert records[-1]["record_type"] == "EXPORT_TRAILER"
    assert b"historical retrieval recall" in first["evidence_packet.md"]

    output = tmp_path / "export"
    hashes = exporter.write(session_id, output)
    assert set(hashes) == set(first)
    assert all((output / name).read_bytes() == payload for name, payload in first.items())
    with pytest.raises(AuditExportError, match="absent or empty"):
        exporter.write(session_id, output)


def test_packet_tampering_and_source_drift_fail_closed(reviewed_export, tmp_path, monkeypatch):
    exporter, session_id = reviewed_export
    packet = json.loads(exporter.render(session_id)["evidence_packet.json"])
    packet["candidates"][0]["text"] = "tampered"
    with pytest.raises(AuditExportError, match="content hash"):
        verify_packet(packet)

    original = exporter.workbench.authority.resolve_source

    def changed_source(source_id):
        result = original(source_id)
        if result.get("status") == "RESOLVED":
            result = {**result, "quote": result["quote"] + " altered"}
        return result

    monkeypatch.setattr(exporter.workbench.authority, "resolve_source", changed_source)
    output = tmp_path / "must-not-exist"
    with pytest.raises(AuditExportError, match="resolution failed|changed"):
        exporter.write(session_id, output)
    assert not output.exists()
