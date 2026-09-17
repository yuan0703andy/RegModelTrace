"""Deterministic, source-verified evidence and audit export for VS-1."""

from __future__ import annotations

import hashlib
import html
import json
import tempfile
from copy import deepcopy
from pathlib import Path
from typing import Any

from .review_store import ReviewConflict, ReviewStore
from .retrieval_packet import STAGES, make_stage_ledger
from .source_authority import canonical_json
from .workbench import RetrievalOnlyWorkbench, WorkbenchError


class AuditExportError(ValueError):
    """Raised when a complete authoritative export cannot be produced."""


def _sha256(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def _pretty_json(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode()


def _markdown_text(value: Any) -> str:
    return html.escape(str(value), quote=False).replace("|", "\\|")


class EvidenceAuditExporter:
    """Export a frozen retrieval case plus one append-only review session."""

    def __init__(self, workbench: RetrievalOnlyWorkbench, review_store: ReviewStore):
        self.workbench = workbench
        self.review_store = review_store

    def build_packet(self, session_id: str) -> dict[str, Any]:
        try:
            session, events = self.review_store.snapshot(session_id)
        except (KeyError, ReviewConflict) as exc:
            raise AuditExportError(str(exc)) from exc

        case = self.workbench.case_payload()
        binding = {
            key: case[key]
            for key in ("retrieval_run_id", "corpus_snapshot_id", "index_build_id")
        }
        if any(session[key] != value for key, value in binding.items()):
            raise AuditExportError("Review session does not match the frozen case")

        histories: dict[str, list[dict[str, Any]]] = {
            candidate_id: [] for candidate_id in self.workbench.candidates
        }
        for event in events:
            candidate = self.workbench.candidates[event["candidate_id"]]
            expected = {
                "passage_id": candidate["passage_id"],
                "document_id": candidate["document_id"],
                **binding,
            }
            if any(event[key] != value for key, value in expected.items()):
                raise AuditExportError(f"Review event binding mismatch: {event['event_id']}")
            histories[event["candidate_id"]].append(event)

        candidates = []
        for frozen in self.workbench.packet["candidates"]:
            candidate_id = frozen["candidate_id"]
            try:
                detail = self.workbench.candidate_payload(candidate_id)
                resolution = self.workbench.authority.resolve_source(frozen["passage_id"])
                navigation = self.workbench.navigation_receipt(candidate_id)
            except (KeyError, WorkbenchError) as exc:
                raise AuditExportError(
                    f"Authoritative export resolution failed for {candidate_id}: {exc}"
                ) from exc
            if resolution.get("status") != "RESOLVED":
                raise AuditExportError(f"Source no longer resolves: {candidate_id}")
            if canonical_json(resolution) != canonical_json(frozen["source_resolution"]):
                raise AuditExportError(f"Frozen source resolution changed: {candidate_id}")
            if resolution.get("quote") != frozen["text"]:
                raise AuditExportError(f"Frozen quote mismatch: {candidate_id}")
            if resolution.get("document_id") != frozen["document_id"]:
                raise AuditExportError(f"Frozen document mismatch: {candidate_id}")

            history = deepcopy(histories[candidate_id])
            candidates.append(
                {
                    "candidate_id": candidate_id,
                    "retrieval_run_id": frozen["retrieval_run_id"],
                    "corpus_snapshot_id": frozen["corpus_snapshot_id"],
                    "index_build_id": frozen["index_build_id"],
                    "passage_id": frozen["passage_id"],
                    "assertion_ids": deepcopy(frozen["assertion_ids"]),
                    "document_id": frozen["document_id"],
                    "document_role": frozen["document_role"],
                    "document_title": detail["document_title"],
                    "pages": deepcopy(frozen["pages"]),
                    "text": frozen["text"],
                    "scores": deepcopy(frozen["scores"]),
                    "frozen_stage_ledger": deepcopy(frozen["stage_ledger"]),
                    "loss_classification": frozen["loss_classification"],
                    "source_resolution": resolution,
                    "source_navigation": navigation,
                    "review": {
                        "event_count": len(history),
                        "history": history,
                        "latest_event": deepcopy(history[-1]) if history else None,
                    },
                }
            )

        body = {
            "schema_version": "vs1-evidence-packet-1.0",
            "export_semantics": {
                "candidate_decision": "USEFULNESS_FOR_DISPLAYED_QUESTION",
                "regulatory_compliance_inferred": False,
                "frozen_stage_ledger_mutated": False,
                "candidate_universe_scope": case["candidate_universe_scope"],
                "historical_retrieval_recall_established": False,
                "fixed_corpus_absence_established": False,
                "independent_human_adjudication_established_by_export": False,
            },
            "source_authority": {
                "corpus_snapshot": deepcopy(self.workbench.authority.snapshot),
                "index_build": deepcopy(self.workbench.authority.index_build),
            },
            "retrieval_run": deepcopy(self.workbench.packet["retrieval_run"]),
            "review_session": session,
            "review_events": deepcopy(events),
            "candidate_count": len(candidates),
            "review_event_count": len(events),
            "candidates": candidates,
        }
        packet_hash = _sha256(body)
        packet = {**body, "packet_sha256": packet_hash, "export_id": f"EP_{packet_hash[:24]}"}
        verify_packet(packet)
        return packet

    @staticmethod
    def render_markdown(packet: dict[str, Any]) -> bytes:
        run = packet["retrieval_run"]
        session = packet["review_session"]
        lines = [
            "# RegModelTrace Evidence Packet",
            "",
            f"- Export: `{packet['export_id']}`",
            f"- Packet SHA-256: `{packet['packet_sha256']}`",
            f"- Question: {_markdown_text(run['question'])}",
            f"- Retrieval run: `{run['retrieval_run_id']}`",
            f"- Corpus snapshot: `{run['corpus_snapshot_id']}`",
            f"- Index build: `{run['index_build_id']}`",
            f"- Review session: `{session['session_id']}`",
            f"- Reviewer: {_markdown_text(session['reviewer'])}",
            "",
            "## Scope and interpretation",
            "",
            "This export covers returned and retained candidates only. It does not establish",
            "historical retrieval recall, fixed-corpus absence, or regulatory compliance.",
            "Candidate decisions record usefulness for the displayed question. Frozen stage",
            "ledgers are reproduced unchanged and remain separate from review events.",
            "",
        ]
        for candidate in packet["candidates"]:
            latest = candidate["review"]["latest_event"]
            lines.extend(
                [
                    f"## {candidate['document_role']} — {candidate['candidate_id']}",
                    "",
                    f"- Document: {_markdown_text(candidate['document_title'])}",
                    f"- Document ID: `{candidate['document_id']}`",
                    f"- Passage ID: `{candidate['passage_id']}`",
                    f"- Physical pages: {', '.join(map(str, candidate['pages']))}",
                    f"- Precision: `{candidate['source_navigation']['location_precision']}`",
                    f"- Review events: {candidate['review']['event_count']}",
                    "",
                    "> " + _markdown_text(candidate["text"]).replace("\n", "\n> "),
                    "",
                ]
            )
            if latest is None:
                lines.extend(["Latest decision: **UNREVIEWED**", ""])
            else:
                lines.extend(
                    [
                        f"Latest decision: **{latest['decision']}**",
                        "",
                        f"Reason: `{latest['reason_code']}`",
                        "",
                        "Rationale:",
                        "",
                        "> " + _markdown_text(latest["rationale"]).replace("\n", "\n> "),
                        "",
                    ]
                )
        return ("\n".join(lines).rstrip() + "\n").encode()

    @staticmethod
    def render_jsonl(packet: dict[str, Any]) -> bytes:
        records = [
            {
                "record_type": "EXPORT_HEADER",
                "export_id": packet["export_id"],
                "packet_sha256": packet["packet_sha256"],
                "retrieval_run": packet["retrieval_run"],
                "review_session": packet["review_session"],
                "export_semantics": packet["export_semantics"],
            }
        ]
        for candidate in packet["candidates"]:
            records.append(
                {
                    "record_type": "CANDIDATE_EVIDENCE",
                    "export_id": packet["export_id"],
                    "candidate_id": candidate["candidate_id"],
                    "passage_id": candidate["passage_id"],
                    "document_id": candidate["document_id"],
                    "document_role": candidate["document_role"],
                    "pages": candidate["pages"],
                    "source_status": candidate["source_resolution"]["status"],
                    "location_precision": candidate["source_navigation"]["location_precision"],
                    "authoritative_pdf_sha256": candidate["source_navigation"][
                        "authoritative_pdf_sha256"
                    ],
                    "frozen_stage_ledger": candidate["frozen_stage_ledger"],
                }
            )
        for event in packet["review_events"]:
            records.append(
                {"record_type": "REVIEW_DISPOSITION", "export_id": packet["export_id"], **event}
            )
        records.append(
            {
                "record_type": "EXPORT_TRAILER",
                "export_id": packet["export_id"],
                "packet_sha256": packet["packet_sha256"],
                "candidate_count": packet["candidate_count"],
                "review_event_count": packet["review_event_count"],
            }
        )
        return b"".join(
            (json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n").encode()
            for record in records
        )

    def render(self, session_id: str) -> dict[str, bytes]:
        packet = self.build_packet(session_id)
        return {
            "evidence_packet.json": _pretty_json(packet),
            "evidence_packet.md": self.render_markdown(packet),
            "audit_record.jsonl": self.render_jsonl(packet),
        }

    def write(self, session_id: str, output_dir: Path) -> dict[str, str]:
        rendered = self.render(session_id)
        output_dir = Path(output_dir)
        if output_dir.exists() and any(output_dir.iterdir()):
            raise AuditExportError("Export directory must be absent or empty")
        output_dir.parent.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(prefix="vs1-export-", dir=output_dir.parent) as tmp:
            temporary = Path(tmp)
            for name, payload in rendered.items():
                (temporary / name).write_bytes(payload)
            output_dir.mkdir(parents=True, exist_ok=True)
            for name in rendered:
                (temporary / name).replace(output_dir / name)
        return {name: hashlib.sha256(payload).hexdigest() for name, payload in rendered.items()}


def verify_packet(packet: dict[str, Any]) -> None:
    """Validate a saved packet without consulting mutable runtime state."""

    if packet.get("schema_version") != "vs1-evidence-packet-1.0":
        raise AuditExportError("Unsupported evidence packet schema")
    body = {key: value for key, value in packet.items() if key not in {"packet_sha256", "export_id"}}
    expected_hash = _sha256(body)
    if packet.get("packet_sha256") != expected_hash:
        raise AuditExportError("Evidence packet content hash mismatch")
    if packet.get("export_id") != f"EP_{expected_hash[:24]}":
        raise AuditExportError("Evidence packet identity mismatch")

    run = packet["retrieval_run"]
    session = packet["review_session"]
    binding = {
        key: run[key] for key in ("retrieval_run_id", "corpus_snapshot_id", "index_build_id")
    }
    if any(session[key] != value for key, value in binding.items()):
        raise AuditExportError("Review-session binding mismatch")
    if packet["source_authority"]["corpus_snapshot"]["corpus_snapshot_id"] != binding[
        "corpus_snapshot_id"
    ]:
        raise AuditExportError("Corpus-snapshot binding mismatch")
    if packet["source_authority"]["index_build"]["index_build_id"] != binding[
        "index_build_id"
    ]:
        raise AuditExportError("Index-build binding mismatch")

    candidates = packet["candidates"]
    if packet["candidate_count"] != len(candidates):
        raise AuditExportError("Candidate count mismatch")
    candidate_ids = [candidate["candidate_id"] for candidate in candidates]
    if len(candidate_ids) != len(set(candidate_ids)):
        raise AuditExportError("Duplicate candidate identity in export")
    candidate_map = {candidate["candidate_id"]: candidate for candidate in candidates}
    histories: dict[str, list[dict[str, Any]]] = {}
    for candidate in candidates:
        if any(candidate[key] != value for key, value in binding.items()):
            raise AuditExportError(f"Candidate binding mismatch: {candidate['candidate_id']}")
        ledger_states = {
            stage: candidate["frozen_stage_ledger"][stage]["state"] for stage in STAGES
        }
        make_stage_ledger(ledger_states)
        if candidate["source_resolution"].get("status") != "RESOLVED":
            raise AuditExportError(f"Unresolved source in export: {candidate['candidate_id']}")
        if candidate["source_resolution"].get("requested_id") != candidate["passage_id"]:
            raise AuditExportError(f"Source identity mismatch: {candidate['candidate_id']}")
        if candidate["source_resolution"].get("quote") != candidate["text"]:
            raise AuditExportError(f"Source quote mismatch: {candidate['candidate_id']}")
        history = candidate["review"]["history"]
        if candidate["review"]["event_count"] != len(history):
            raise AuditExportError(f"Review-event count mismatch: {candidate['candidate_id']}")
        latest = history[-1] if history else None
        if candidate["review"]["latest_event"] != latest:
            raise AuditExportError(f"Latest review event mismatch: {candidate['candidate_id']}")
        histories[candidate["candidate_id"]] = history

    events = packet["review_events"]
    if packet["review_event_count"] != len(events):
        raise AuditExportError("Review event count mismatch")
    event_ids = [event["event_id"] for event in events]
    if len(event_ids) != len(set(event_ids)):
        raise AuditExportError("Duplicate review event identity")
    for event in events:
        candidate = candidate_map.get(event["candidate_id"])
        if candidate is None or event not in histories[event["candidate_id"]]:
            raise AuditExportError(f"Orphan review event: {event['event_id']}")
        expected = {
            "passage_id": candidate["passage_id"],
            "document_id": candidate["document_id"],
            **binding,
        }
        if any(event[key] != value for key, value in expected.items()):
            raise AuditExportError(f"Review-event binding mismatch: {event['event_id']}")

    semantics = packet["export_semantics"]
    if semantics.get("frozen_stage_ledger_mutated") is not False:
        raise AuditExportError("Export does not preserve the frozen stage ledger")
    if semantics.get("candidate_universe_scope") != "RETURNED_RETAINED_CANDIDATES_ONLY":
        raise AuditExportError("Unexpected candidate-universe scope")
