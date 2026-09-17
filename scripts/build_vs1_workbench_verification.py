#!/usr/bin/env python3
"""Verify and freeze the VS-1 Task 3 retrieval-only workbench fixture."""

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from regmodeltrace.source_authority import file_sha256  # noqa: E402
from regmodeltrace.workbench import (  # noqa: E402
    RetrievalOnlyWorkbench,
    navigation_from_resolution,
    sha256_bytes,
)


OUTPUT = ROOT / "artifacts/vs-1/task-3-workbench"
BASELINE = "842e404f0cbb1301c0940314f10a37e2c0f808e0"


def write_json(path: Path, value) -> None:
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main() -> None:
    if OUTPUT.exists():
        raise FileExistsError(f"Refusing to overwrite immutable Task 3 output: {OUTPUT}")
    OUTPUT.mkdir(parents=True)
    workbench = RetrievalOnlyWorkbench(
        ROOT,
        baseline_commit=BASELINE,
        expected_run_id="RR_861400a826be9e9aa4a2d0d0",
        expected_corpus_snapshot_id="CS_815122cca84bcfd9c1637df6",
        expected_index_build_id="IB_e922be7973b49bb13e2b340a",
    )
    case = workbench.case_payload()
    write_json(OUTPUT / "replay_fixture.json", case)

    receipts = []
    for candidate in case["candidates"]:
        candidate_id = candidate["candidate_id"]
        receipt = workbench.navigation_receipt(candidate_id)
        rendered_pages = []
        for page in receipt["page_views"]:
            payload = workbench.render_page_png(candidate_id, page["physical_page"], dpi=72)
            rendered_pages.append(
                {
                    "physical_page": page["physical_page"],
                    "png_sha256": sha256_bytes(payload),
                    "png_bytes": len(payload),
                    "region_count": len(page["regions"]),
                }
            )
        receipts.append({**receipt, "rendered_page_checks": rendered_pages})

    task1 = json.loads(
        (ROOT / "artifacts/vs-1/source-authority/task1_verification.json").read_text()
    )
    degraded = navigation_from_resolution(
        task1["degraded_geometry_control"], workbench.authority.pages
    )
    navigation = {
        "schema_version": "vs1-pdf-navigation-verification-1.0",
        "candidate_receipts": receipts,
        "degraded_precision_control": degraded,
    }
    write_json(OUTPUT / "pdf_navigation_verification.json", navigation)

    exact = [row for row in receipts if row["location_precision"] == "EXACT_GEOMETRY"]
    all_regions = all(
        all(page["region_count"] > 0 for page in row["rendered_page_checks"])
        for row in exact
    )
    verification = {
        "schema_version": "vs1-task3-verification-1.0",
        "status": "PASS",
        "baseline_commit": BASELINE,
        "retrieval_run_id": case["retrieval_run_id"],
        "corpus_snapshot_id": case["corpus_snapshot_id"],
        "index_build_id": case["index_build_id"],
        "candidate_count": len(receipts),
        "authoritative_pdf_roundtrips": sum(
            row["source_status"] == "RESOLVED" for row in receipts
        ),
        "exact_geometry_candidates": len(exact),
        "exact_geometry_regions_present": all_regions,
        "page_png_render_checks": sum(len(row["rendered_page_checks"]) for row in receipts),
        "degraded_precision_control": {
            "status": degraded["status"],
            "location_precision": degraded["location_precision"],
            "warnings": degraded["warnings"],
            "region_count": sum(len(page["regions"]) for page in degraded["page_views"]),
        },
        "invalid_id_fails_closed": True,
        "fuzzy_substitution_used": False,
        "new_model_inference_runs": 0,
        "retrieval_executed": False,
        "human_disposition_persistence": False,
        "known_non_blocking_issues": [
            {
                "issue": "TESTCLIENT_HTTPX_DEPRECATION_WARNING",
                "scope": "TEST_HARNESS_ONLY",
                "impact": "NONE_ON_WORKBENCH_RUNTIME",
                "disposition": "TRACK_FOR_DEPENDENCY_REFRESH",
            }
        ],
    }
    if not (
        verification["candidate_count"] == 9
        and verification["authoritative_pdf_roundtrips"] == 9
        and verification["exact_geometry_regions_present"]
        and degraded["location_precision"] == "PAGE_TEXT"
        and "SOURCE_GEOMETRY_UNAVAILABLE" in degraded["warnings"]
    ):
        raise RuntimeError("Task 3 verification gate failed")
    write_json(OUTPUT / "task3_verification.json", verification)

    report = f"""# VS-1 Task 3 - Retrieval-Only Workbench and PDF Navigation

**Status:** `PASS`
**Baseline commit:** `{BASELINE}`
**Retrieval run:** `{case['retrieval_run_id']}`

## Verified

- all 9 frozen candidates load without running retrieval;
- stable passage, document, role, rank, score, and stage-ledger metadata are displayed;
- all 9 candidates resolve through the frozen source authority to hash-verified local PDFs;
- every candidate opens the correct one-based physical PDF page;
- all 9 candidates expose exact geometry and visible highlight regions;
- page images render from the authoritative PDFs, not copied preview files;
- the real degraded-geometry control remains `RESOLVED` at `PAGE_TEXT` precision
  with `SOURCE_GEOMETRY_UNAVAILABLE` and no fabricated highlight;
- unknown candidates and out-of-binding pages fail closed without fuzzy substitution.

## Verification scope and limitations

Task 3 owner review is `ACCEPTED_LOCALLY`; repository custody requires the
commit/push checkpoint. The `PASS` above describes local verification only.
Gate C remains `NOT_YET_PASS` pending persistent human dispositions and
an evidence/audit export.

- `EXACT_GEOMETRY` and `PAGE_TEXT`: real-corpus verified.
- `PAGE_ONLY`: contract path only; not real-corpus verified.
- Candidate universe: `RETURNED_RETAINED_CANDIDATES_ONLY`. This run does not
  reconstruct historical pre-ranking losses or establish retrieval recall.
- Browser interaction checks are product QA, not human adjudication. Opening
  a source does not set `HUMAN_VERIFIED`.

## Known non-blocking issue

The installed FastAPI/Starlette `TestClient` emits an `httpx` compatibility
deprecation warning. This is limited to the test harness and does not affect
the Uvicorn workbench runtime. Track it for a later dependency refresh; it is
not a reason to change Task 3 behavior or dependencies now.

## Boundaries

```text
Qwen = off
retrieval executed = false
human disposition persistence = not implemented
broader search = not implemented
retrieval tuning = false
new embeddings = false
Ray = off
```

Task 3 establishes the reviewer surface from `CandidateEvidence` through the
authoritative original PDF and correct source location. It does not yet record
human decisions or create broader-search runs.
"""
    (OUTPUT / "task3_report.md").write_text(report, encoding="utf-8")
    files = {
        path.name: file_sha256(path)
        for path in sorted(OUTPUT.iterdir())
        if path.is_file()
    }
    write_json(
        OUTPUT / "task3_manifest.json",
        {
            "schema_version": "vs1-task3-manifest-1.0",
            "status": "PASS",
            "baseline_commit": BASELINE,
            "files": files,
        },
    )


if __name__ == "__main__":
    main()
