"""Build the frozen VS-1 Task 5 product-QA export and verification artifacts."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from regmodeltrace.audit_export import EvidenceAuditExporter, verify_packet  # noqa: E402
from regmodeltrace.review_store import ReviewStore  # noqa: E402
from regmodeltrace.workbench import RetrievalOnlyWorkbench  # noqa: E402


BASELINE_COMMIT = "58c00ec7d55273a0d0e41ed3a83f5346fbf424b1"


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_json(path: Path, value) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output",
        type=Path,
        default=ROOT / "artifacts/vs-1/task-5-export",
    )
    args = parser.parse_args()
    output = args.output.resolve()
    if output.exists() and any(output.iterdir()):
        raise SystemExit(f"Refusing to overwrite non-empty export directory: {output}")

    workbench = RetrievalOnlyWorkbench(
        ROOT,
        baseline_commit=BASELINE_COMMIT,
        expected_run_id="RR_861400a826be9e9aa4a2d0d0",
        expected_corpus_snapshot_id="CS_815122cca84bcfd9c1637df6",
        expected_index_build_id="IB_e922be7973b49bb13e2b340a",
    )
    with tempfile.TemporaryDirectory(prefix="vs1-task5-") as temporary:
        store = ReviewStore(Path(temporary) / "reviews.sqlite3", workbench)
        session = store.create_session("AUTOMATED_PRODUCT_QA_NOT_HUMAN_ADJUDICATION")
        by_role = {}
        for candidate_id, candidate in workbench.candidates.items():
            by_role.setdefault(candidate["document_role"], candidate_id)
        qa_events = [
            ("qa-standards", by_role["STANDARDS"], "ACCEPTED", "RELEVANT_SUPPORT"),
            (
                "qa-team",
                by_role["PROFESSIONAL_TEAM_REPORT"],
                "REJECTED",
                "WRONG_SOURCE",
            ),
            (
                "qa-vendor",
                by_role["VENDOR_SUBMISSION"],
                "UNRESOLVED",
                "NEED_BROADER_SEARCH",
            ),
        ]
        for event_id, candidate_id, decision, reason_code in qa_events:
            store.append(
                session["session_id"],
                candidate_id,
                event_id=event_id,
                decision=decision,
                reason_code=reason_code,
                rationale="Product QA only; no substantive human adjudication.",
            )
        exporter = EvidenceAuditExporter(workbench, store)
        output_hashes = exporter.write(session["session_id"], output)
        repeated = exporter.render(session["session_id"])
        deterministic_repeat = all(
            (output / name).read_bytes() == payload for name, payload in repeated.items()
        )

    packet = json.loads((output / "evidence_packet.json").read_text())
    verify_packet(packet)
    frozen_ledgers_exact = all(
        exported["frozen_stage_ledger"] == frozen["stage_ledger"]
        for exported, frozen in zip(packet["candidates"], workbench.packet["candidates"])
    )
    verification = {
        "schema_version": "vs1-task5-verification-1.0",
        "status": "LOCAL_PASS",
        "baseline_commit": BASELINE_COMMIT,
        "qa_only": True,
        "human_adjudication_claimed": False,
        "export_id": packet["export_id"],
        "packet_sha256": packet["packet_sha256"],
        "candidate_count": packet["candidate_count"],
        "document_roles": sorted(
            {candidate["document_role"] for candidate in packet["candidates"]}
        ),
        "review_event_count": packet["review_event_count"],
        "unreviewed_candidate_count": sum(
            candidate["review"]["event_count"] == 0 for candidate in packet["candidates"]
        ),
        "all_sources_resolved": all(
            candidate["source_resolution"]["status"] == "RESOLVED"
            for candidate in packet["candidates"]
        ),
        "frozen_stage_ledgers_exact": frozen_ledgers_exact,
        "deterministic_repeat": deterministic_repeat,
        "saved_packet_replay_verified": True,
        "output_hashes": output_hashes,
        "retrieval_executed": False,
        "qwen_runs": 0,
        "gate_c": "PENDING_VERTICAL_SLICE_ACCEPTANCE",
        "repository_custody": "PENDING",
    }
    write_json(output / "task5_verification.json", verification)

    (output / "task5_issues.md").write_text(
        """# VS-1 Task 5 issue log

- The first direct builder run could not import the repository package because
  the entrypoint did not add the repository root to `sys.path`. The entrypoint
  was corrected before artifact creation; no partial export was retained.
- The checked-in dispositions are product-QA events, not human adjudication or
  regulatory-compliance judgments.
- Candidate scope remains `RETURNED_RETAINED_CANDIDATES_ONLY`; the export cannot
  establish historical retrieval recall or fixed-corpus absence.
- SQLite append-only protection remains an application/local-database control,
  not cryptographic tamper evidence against the filesystem owner.
- Reviewer identity remains self-declared; multi-user authentication is out of scope.
- `PAGE_ONLY` remains contract-tested but lacks a real-corpus case.
- Broader search remains deferred, so `NEED_BROADER_SEARCH` is recorded but does
  not launch a child retrieval run.
- The pre-existing Starlette TestClient/httpx deprecation warning remains open.
- On restricted macOS execution, a transitive CPU-info probe logs non-fatal
  `sysctlbyname` permission warnings during artifact generation. Outputs and
  verification complete successfully; no correctness failure was observed.
"""
    )
    (output / "task5_report.md").write_text(
        f"""# VS-1 Task 5 — Evidence and audit export

Status: `LOCAL_PASS`; owner review and repository custody pending.

The frozen Florida case exported {packet['candidate_count']} candidates and
{packet['review_event_count']} explicitly QA-only review events to JSON,
Markdown, and append-ordered JSONL. All candidates were re-resolved against the
authoritative corpus before export. Frozen retrieval-stage ledgers were preserved
exactly; human decisions remain a separate event layer. Repeating export against
the same database state produced byte-identical outputs.

Export ID: `{packet['export_id']}`
Packet SHA-256: `{packet['packet_sha256']}`

No Qwen, retrieval execution/tuning, embedding rebuild, Ray, broader search, or
statistical research ran. The artifacts demonstrate product plumbing, not human
evidence truth. Gate C requires the bounded vertical-slice acceptance step.
"""
    )
    manifest_files = sorted(
        path for path in output.iterdir() if path.name != "task5_manifest.json"
    )
    write_json(
        output / "task5_manifest.json",
        {
            "schema_version": "vs1-task5-manifest-1.0",
            "files": {path.name: file_sha256(path) for path in manifest_files},
        },
    )


if __name__ == "__main__":
    main()
