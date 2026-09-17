import json
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from regmodeltrace.workbench import (
    RetrievalOnlyWorkbench,
    WorkbenchError,
    navigation_from_resolution,
)


ROOT = Path(__file__).resolve().parents[2]
BASELINE = "842e404f0cbb1301c0940314f10a37e2c0f808e0"


@pytest.fixture(scope="module")
def workbench():
    return RetrievalOnlyWorkbench(
        ROOT,
        baseline_commit=BASELINE,
        expected_run_id="RR_861400a826be9e9aa4a2d0d0",
        expected_corpus_snapshot_id="CS_815122cca84bcfd9c1637df6",
        expected_index_build_id="IB_e922be7973b49bb13e2b340a",
    )


def test_frozen_case_loads_all_nine_candidates(workbench):
    payload = workbench.case_payload()
    assert payload["baseline_commit"] == BASELINE
    assert payload["candidate_count"] == 9
    assert payload["candidate_universe_scope"] == "RETURNED_RETAINED_CANDIDATES_ONLY"
    assert {row["document_role"] for row in payload["candidates"]} == {
        "STANDARDS",
        "PROFESSIONAL_TEAM_REPORT",
        "VENDOR_SUBMISSION",
    }


def test_every_candidate_round_trips_to_pdf_page_and_geometry(workbench):
    for candidate_id in workbench.candidates:
        detail = workbench.candidate_payload(candidate_id)
        receipt = workbench.navigation_receipt(candidate_id)
        assert detail["source_status"] == "RESOLVED"
        assert receipt["fuzzy_substitution_used"] is False
        assert receipt["location_precision"] == "EXACT_GEOMETRY"
        assert receipt["page_views"]
        assert all(page["physical_page"] >= 1 for page in receipt["page_views"])
        assert all(page["regions"] for page in receipt["page_views"])
        assert (ROOT / receipt["authoritative_pdf_path"]).is_file()


def test_rendered_page_is_png(workbench):
    candidate_id = next(iter(workbench.candidates))
    page = workbench.candidate_payload(candidate_id)["pages"][0]
    payload = workbench.render_page_png(candidate_id, page, dpi=72)
    assert payload.startswith(b"\x89PNG\r\n\x1a\n")
    assert len(payload) > 10_000


def test_wrong_candidate_or_page_fails_without_substitution(workbench):
    with pytest.raises(KeyError):
        workbench.candidate_payload("CE_UNKNOWN")
    candidate_id = next(iter(workbench.candidates))
    with pytest.raises(WorkbenchError):
        workbench.render_page_png(candidate_id, 9999)


def test_real_geometry_failure_degrades_visibly(workbench):
    task1 = json.loads(
        (ROOT / "artifacts/vs-1/source-authority/task1_verification.json").read_text()
    )
    resolution = task1["degraded_geometry_control"]
    navigation = navigation_from_resolution(resolution, workbench.authority.pages)
    assert navigation["status"] == "RESOLVED"
    assert navigation["location_precision"] == "PAGE_TEXT"
    assert "SOURCE_GEOMETRY_UNAVAILABLE" in navigation["warnings"]
    assert all(not page["regions"] for page in navigation["page_views"])


def test_workbench_static_surface_has_required_panels():
    html = (ROOT / "workbench/index.html").read_text()
    for marker in ("case-header", "candidate-panel", "source-viewer", "trace-panel"):
        assert marker in html


def test_workbench_http_surface_serves_case_source_pdf_and_page_png():
    from regmodeltrace.workbench_server import app

    client = TestClient(app)
    case = client.get("/api/case")
    assert case.status_code == 200
    assert case.json()["candidate_count"] == 9
    candidate_id = case.json()["candidates"][0]["candidate_id"]
    detail = client.get(f"/api/candidates/{candidate_id}")
    assert detail.status_code == 200
    page = detail.json()["pages"][0]
    image = client.get(f"/api/candidates/{candidate_id}/pages/{page}.png")
    assert image.status_code == 200
    assert image.headers["content-type"] == "image/png"
    assert image.content.startswith(b"\x89PNG\r\n\x1a\n")
    pdf = client.get(f"/api/candidates/{candidate_id}/original.pdf")
    assert pdf.status_code == 200
    assert pdf.headers["content-type"] == "application/pdf"
    assert pdf.content.startswith(b"%PDF-")
    assert client.get("/api/candidates/CE_UNKNOWN").status_code == 404
