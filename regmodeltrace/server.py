"""Local HTTP interface for RegModelTrace v1."""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from .contracts import ContractError
from .service import ask, default_system_ready


class AskRequest(BaseModel):
    question: str = Field(min_length=1, max_length=2000)


app = FastAPI(title="RegModelTrace", version="1.0.0")


@app.get("/health")
def health():
    ready = default_system_ready()
    return {
        "status": "ready" if ready else "initializes_on_first_request",
        "ready": ready,
        "service": "regmodeltrace-v1",
    }


@app.post("/ask")
def ask_endpoint(request: AskRequest):
    try:
        return ask(request.question)
    except ContractError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail="RegModelTrace could not produce a validated answer") from exc

