"""FastAPI surface for the VS-1 retrieval-only reviewer workbench."""

from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI, HTTPException, Response
from fastapi.responses import FileResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles

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
