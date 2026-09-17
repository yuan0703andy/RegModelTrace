"""Verify the complete retrieval-only VS-1 vertical slice and emit Gate C receipts."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from regmodeltrace.audit_export import verify_packet  # noqa: E402
from regmodeltrace.retrieval_packet import replay_candidate_packet  # noqa: E402


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_json(path: Path):
    return json.loads(path.read_text())


def verify_manifest(directory: Path, manifest_name: str) -> int:
    manifest = load_json(directory / manifest_name)
    files = manifest.get("files", manifest.get("artifacts"))
    if not isinstance(files, dict) or not files:
        raise ValueError(f"No artifact hashes in {directory / manifest_name}")
    for name, expected in files.items():
        path = directory / name
        if not path.is_file() or file_sha256(path) != expected:
            raise ValueError(f"Artifact manifest mismatch: {path}")
    return len(files)


def write_json(path: Path, value) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tests-passed", type=int, required=True)
    parser.add_argument(
        "--output", type=Path, default=ROOT / "artifacts/vs-1/gate-c-acceptance"
    )
    args = parser.parse_args()
    output = args.output.resolve()
    if output.exists() and any(output.iterdir()):
        raise SystemExit(f"Refusing to overwrite non-empty Gate C directory: {output}")
    output.mkdir(parents=True, exist_ok=True)

    artifact_sets = [
        (ROOT / "artifacts/vs-1/source-authority", "task1_manifest.json"),
        (ROOT / "artifacts/vs-1/task-2-candidate-packet", "task2_manifest.json"),
        (ROOT / "artifacts/vs-1/task-3-workbench", "task3_manifest.json"),
        (ROOT / "artifacts/vs-1/task-4-dispositions", "task4_manifest.json"),
        (ROOT / "artifacts/vs-1/task-5-export", "task5_manifest.json"),
    ]
    manifest_file_count = sum(verify_manifest(*item) for item in artifact_sets)

    task1 = load_json(ROOT / "artifacts/vs-1/source-authority/task1_verification.json")
    task2 = load_json(
        ROOT / "artifacts/vs-1/task-2-candidate-packet/task2_verification.json"
    )
    task3 = load_json(ROOT / "artifacts/vs-1/task-3-workbench/task3_verification.json")
    task4 = load_json(ROOT / "artifacts/vs-1/task-4-dispositions/task4_verification.json")
    task5 = load_json(ROOT / "artifacts/vs-1/task-5-export/task5_verification.json")
    task5_browser = load_json(
        ROOT / "artifacts/vs-1/task-5-export/task5_browser_smoke.json"
    )
    if [task1["status"], task2["status"], task3["status"], task4["status"], task5["status"]] != [
        "PASS",
        "PASS",
        "PASS",
        "PASS",
        "PASS",
    ]:
        raise ValueError("A prerequisite VS-1 task has not passed its expected gate")

    candidate_packet = replay_candidate_packet(
        ROOT / "artifacts/vs-1/task-2-candidate-packet/candidate_packet.json"
    )
    evidence_packet = load_json(ROOT / "artifacts/vs-1/task-5-export/evidence_packet.json")
    verify_packet(evidence_packet)
    run = candidate_packet["retrieval_run"]
    exported_run = evidence_packet["retrieval_run"]
    identity_keys = ("retrieval_run_id", "corpus_snapshot_id", "index_build_id")
    if any(run[key] != exported_run[key] for key in identity_keys):
        raise ValueError("Task 2 and Task 5 runtime identities differ")

    frozen_candidates = candidate_packet["candidates"]
    exported_candidates = evidence_packet["candidates"]
    if [row["candidate_id"] for row in frozen_candidates] != [
        row["candidate_id"] for row in exported_candidates
    ]:
        raise ValueError("Candidate order or identities changed during export")
    for frozen, exported in zip(frozen_candidates, exported_candidates):
        if frozen["stage_ledger"] != exported["frozen_stage_ledger"]:
            raise ValueError(f"Frozen stage ledger changed: {frozen['candidate_id']}")
        if frozen["source_resolution"] != exported["source_resolution"]:
            raise ValueError(f"Frozen source resolution changed: {frozen['candidate_id']}")

    role_counts = Counter(row["document_role"] for row in exported_candidates)
    expected_roles = {
        "STANDARDS": 3,
        "PROFESSIONAL_TEAM_REPORT": 3,
        "VENDOR_SUBMISSION": 3,
    }
    if dict(role_counts) != expected_roles:
        raise ValueError(f"Frozen three-role fixture changed: {dict(role_counts)}")
    if not task4["browser_smoke"]["stale_second_tab_write_rejected"]:
        raise ValueError("Task 4 browser conflict protection was not verified")
    if not task5["deterministic_repeat"] or not task5["saved_packet_replay_verified"]:
        raise ValueError("Task 5 export is not deterministic/replayable")
    if task5["retrieval_executed"] or task5["qwen_runs"]:
        raise ValueError("Task 5 crossed the retrieval/model boundary")
    if task5_browser["status"] != "PASS" or task5_browser["qa_only"] is not True:
        raise ValueError("Task 5 browser export smoke is not a QA-only PASS")
    if task5_browser["json_packet_download_from_ui"] != "PASS":
        raise ValueError("Task 5 JSON packet was not downloaded from the workbench")

    verification = {
        "schema_version": "vs1-gate-c-verification-1.0",
        "status": "PASS_WITH_DECLARED_LIMITATIONS",
        "gate": "GATE_C_RETRIEVAL_ONLY_REVIEWER_WORKFLOW",
        "retrieval_run_id": run["retrieval_run_id"],
        "corpus_snapshot_id": run["corpus_snapshot_id"],
        "index_build_id": run["index_build_id"],
        "candidate_count": len(exported_candidates),
        "role_counts": expected_roles,
        "review_event_count": evidence_packet["review_event_count"],
        "manifest_files_verified": manifest_file_count,
        "tests_passed": args.tests_passed,
        "vertical_slice": {
            "frozen_corpus_selected": True,
            "saved_role_aware_retrieval_replayed": True,
            "retrieval_trace_preserved": True,
            "authoritative_pdf_navigation_verified": True,
            "review_disposition_persisted": True,
            "audit_packet_exported": True,
        },
        "frozen_stage_ledgers_exact": True,
        "authoritative_source_resolutions_exact": True,
        "export_replay_verified": True,
        "browser_export_smoke_verified": True,
        "qa_only": True,
        "human_adjudication_claimed": False,
        "retrieval_executed_in_gate_c": False,
        "qwen_runs": 0,
        "known_limitations": [
            "RETURNED_RETAINED_CANDIDATES_ONLY",
            "PAGE_ONLY_NOT_REAL_CORPUS_VERIFIED",
            "SELF_DECLARED_REVIEWER_IDENTITY",
            "NO_CRYPTOGRAPHIC_TAMPER_EVIDENCE",
            "BROADER_SEARCH_DEFERRED",
            "PRODUCT_QA_NOT_HUMAN_ADJUDICATION",
            "TESTCLIENT_HTTPX_DEPRECATION_WARNING",
            "RESTRICTED_MACOS_CPU_INFO_WARNING",
        ],
        "next_authorized_state": "QWEN_RECONNECTION_REQUIRES_SEPARATE_OWNER_DECISION",
        "repository_custody": "PENDING",
    }
    write_json(output / "gate_c_verification.json", verification)
    (output / "gate_c_issues.md").write_text(
        """# VS-1 Gate C issue ledger

No blocking failure remains in the bounded retrieval-only vertical slice.

Open limitations:

- The historical candidate universe contains returned/retained candidates only.
- Product-QA dispositions prove workflow behavior, not evidence truth.
- Reviewer identity is self-declared and the SQLite file is not cryptographically tamper-evident.
- `PAGE_ONLY` lacks a real-corpus example; `PAGE_TEXT` and exact geometry are verified.
- Broader search remains deferred and no child retrieval run is created.
- Existing TestClient/httpx and restricted-macOS CPU-info warnings remain non-blocking.
- The in-app browser requires attachment download through the workbench link;
  direct attachment navigation is client-blocked but does not affect export.

These limitations constrain claims and future deployment; none invalidates the
local, single-user, retrieval-only Gate C contract.
"""
    )
    (output / "gate_c_report.md").write_text(
        f"""# VS-1 Gate C — Retrieval-only reviewer workflow

Status: `PASS_WITH_DECLARED_LIMITATIONS`.

The frozen Florida case completed the full product path: source-authority binding,
saved three-role retrieval replay, candidate trace inspection, authoritative PDF
navigation, append-only reviewer disposition, and deterministic evidence/audit
export. {len(exported_candidates)} candidates across all three document roles and
{evidence_packet['review_event_count']} QA-only review events were preserved.

The real-browser export smoke also passed: a synthetic QA disposition persisted,
all three export links appeared, and the JSON evidence packet downloaded from
the product surface.

All prerequisite artifact manifests passed ({manifest_file_count} files), and
{args.tests_passed} repository tests passed. No model inference, retrieval
execution/tuning, embedding rebuild, Ray workload, or statistical research ran.

The result proves the bounded local product workflow, not human evidence truth,
historical retrieval recall, fixed-corpus absence, or regulatory compliance.
Qwen reconnection remains a separate owner decision after Gate C custody.
"""
    )
    files = sorted(path for path in output.iterdir() if path.name != "gate_c_manifest.json")
    write_json(
        output / "gate_c_manifest.json",
        {
            "schema_version": "vs1-gate-c-manifest-1.0",
            "status": "PASS_WITH_DECLARED_LIMITATIONS",
            "files": {path.name: file_sha256(path) for path in files},
        },
    )


if __name__ == "__main__":
    main()
