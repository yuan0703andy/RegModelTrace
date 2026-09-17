"""FastAPI surface for the VS-1 retrieval-only reviewer workbench."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Literal

from fastapi import FastAPI, HTTPException, Response
from fastapi.responses import FileResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, ConfigDict

from .audit_export import AuditExportError, EvidenceAuditExporter
from .review_store import ReviewConflict, ReviewStore
from .workbench import RetrievalOnlyWorkbench, WorkbenchError


ROOT = Path(__file__).resolve().parents[1]
BASELINE_COMMIT = "842e404f0cbb1301c0940314f10a37e2c0f808e0"
WORKBENCH = RetrievalOnlyWorkbench(
    ROOT,
    baseline_commit=BASELINE_COMMIT,
    expected_run_id="RR_861400a826be9e9aa4a2d0d0",
    expected_corpus_snapshot_id="CS_815122cca84bcfd9c1637df6",
    expected_index_build_id="IB_e922be7973b49bb13e2b340a",
)

# Runtime review data is outside the repository and frozen artifact tree.
REVIEW_STORE = ReviewStore(
    Path(os.environ.get("RMT_REVIEW_DB", str(Path.home() / ".local/share/regmodeltrace/reviews.sqlite3"))),
    WORKBENCH,
)

app = FastAPI(title="RegModelTrace Retrieval-Only Workbench", version="vs1-task3")


@app.get("/")
def root_redirect():
    return RedirectResponse("/workbench/")


@app.get("/api/case")
def case_payload():
    return WORKBENCH.case_payload()


@app.get("/api/candidates/{candidate_id}")
def candidate_payload(candidate_id: str):
    try:
        return WORKBENCH.candidate_payload(candidate_id)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail="Unknown frozen candidate identity") from exc
    except WorkbenchError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc


@app.get("/api/candidates/{candidate_id}/original.pdf")
def original_pdf(candidate_id: str):
    try:
        path = WORKBENCH.original_pdf_path(candidate_id)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail="Unknown frozen candidate identity") from exc
    except WorkbenchError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc
    return FileResponse(path, media_type="application/pdf", filename=path.name, content_disposition_type="inline")


@app.get("/api/candidates/{candidate_id}/pages/{physical_page}.png")
def page_image(candidate_id: str, physical_page: int):
    try:
        payload = WORKBENCH.render_page_png(candidate_id, physical_page)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail="Unknown frozen candidate identity") from exc
    except WorkbenchError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc
    return Response(content=payload, media_type="image/png")


app.mount(
    "/workbench",
    StaticFiles(directory=ROOT / "workbench", html=True),
    name="workbench",
)


class SessionInput(BaseModel):
    model_config = ConfigDict(extra="forbid")
    reviewer: str


class DecisionInput(BaseModel):
    model_config = ConfigDict(extra="forbid")
    event_id: str
    decision: Literal["ACCEPTED", "REJECTED", "UNRESOLVED"]
    reason_code: Literal[
        "RELEVANT_SUPPORT",
        "IRRELEVANT",
        "INSUFFICIENT_EVIDENCE",
        "MISSING_QUALIFICATION",
        "WRONG_SOURCE",
        "WRONG_VERSION",
        "NEED_BROADER_SEARCH",
        "OTHER",
    ]
    rationale: str
    previous_event_id: str | None = None


def review_call(fn, *args, **kwargs):
    try:
        return fn(*args, **kwargs)
    except KeyError as exc:
        raise HTTPException(404, str(exc)) from exc
    except (ReviewConflict, WorkbenchError) as exc:
        raise HTTPException(409, str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(422, str(exc)) from exc


@app.post("/api/review-sessions")
def create_review_session(body: SessionInput):
    return review_call(REVIEW_STORE.create_session, body.reviewer)


@app.get("/api/review-sessions/{session_id}")
def get_review_session(session_id: str):
    return review_call(REVIEW_STORE.session, session_id)


@app.get("/api/review-sessions/{session_id}/candidates/{candidate_id}")
def review_history(session_id: str, candidate_id: str):
    return review_call(REVIEW_STORE.history, session_id, candidate_id)


@app.post("/api/review-sessions/{session_id}/candidates/{candidate_id}")
def append_review(session_id: str, candidate_id: str, body: DecisionInput):
    return review_call(REVIEW_STORE.append, session_id, candidate_id, **body.model_dump())


EXPORT_MEDIA_TYPES = {
    "evidence_packet.json": "application/json",
    "evidence_packet.md": "text/markdown; charset=utf-8",
    "audit_record.jsonl": "application/x-ndjson",
}


@app.get("/api/review-sessions/{session_id}/exports/{filename}")
def export_review_session(session_id: str, filename: str):
    if filename not in EXPORT_MEDIA_TYPES:
        raise HTTPException(404, "Unknown audit-export format")
    try:
        payload = EvidenceAuditExporter(WORKBENCH, REVIEW_STORE).render(session_id)[filename]
    except AuditExportError as exc:
        raise HTTPException(409, str(exc)) from exc
    return Response(
        content=payload,
        media_type=EXPORT_MEDIA_TYPES[filename],
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )
