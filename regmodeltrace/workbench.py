"""Read-only reviewer workbench over the frozen VS-1 candidate packet."""

from __future__ import annotations

import hashlib
import subprocess
import tempfile
from functools import lru_cache
from pathlib import Path
from typing import Any

from .retrieval_packet import replay_candidate_packet
from .source_authority import FrozenCorpusAuthority, file_sha256


class WorkbenchError(ValueError):
    """Raised when the workbench cannot preserve authoritative identity."""


def navigation_from_resolution(
    resolution: dict[str, Any], pages: dict[tuple[str, int], dict[str, Any]]
) -> dict[str, Any]:
    """Convert one authoritative resolution into page and region navigation."""

    if resolution.get("status") != "RESOLVED":
        raise WorkbenchError("Authoritative source resolution failed")
    assertions = resolution.get("assertions") or [resolution]
    spans = [span for assertion in assertions for span in assertion.get("source_spans", [])]
    page_views = []
    for physical_page in resolution["pages"]:
        page = pages.get((resolution["document_id"], int(physical_page)))
        if page is None:
            raise WorkbenchError(f"Canonical page missing: {physical_page}")
        width = float(page["width"])
        height = float(page["height"])
        if width <= 0 or height <= 0:
            raise WorkbenchError(f"Invalid canonical page dimensions: {physical_page}")
        regions = []
        for span in spans:
            if int(span["physical_page_index"]) != int(physical_page) or span.get("bbox") is None:
                continue
            x0, top, x1, bottom = [float(value) for value in span["bbox"]]
            if not (0 <= x0 <= x1 <= width and 0 <= top <= bottom <= height):
                raise WorkbenchError(f"Source geometry outside canonical page: {physical_page}")
            regions.append(
                {
                    "bbox": [x0, top, x1, bottom],
                    "left_percent": 100 * x0 / width,
                    "top_percent": 100 * top / height,
                    "width_percent": 100 * (x1 - x0) / width,
                    "height_percent": 100 * (bottom - top) / height,
                }
            )
        page_views.append(
            {
                "physical_page": int(physical_page),
                "pdf_page_index_zero_based": int(physical_page) - 1,
                "printed_page_label": page.get("printed_page_label"),
                "page_width": width,
                "page_height": height,
                "regions": regions,
            }
        )
    return {
        "status": "RESOLVED",
        "document_id": resolution["document_id"],
        "document_role": resolution["document_role"],
        "location_precision": resolution["location_precision"],
        "warnings": list(resolution.get("warnings", [])),
        "page_views": page_views,
        "fuzzy_substitution_used": False,
    }


class RetrievalOnlyWorkbench:
    """Load a frozen candidate packet and resolve it to authoritative PDFs."""

    def __init__(
        self,
        repository_root: Path,
        *,
        baseline_commit: str,
        expected_run_id: str,
        expected_corpus_snapshot_id: str,
        expected_index_build_id: str,
    ):
        self.root = Path(repository_root).resolve()
        self.baseline_commit = baseline_commit
        self.packet_path = (
            self.root / "artifacts/vs-1/task-2-candidate-packet/candidate_packet.json"
        )
        self.packet = replay_candidate_packet(self.packet_path)
        self.authority = FrozenCorpusAuthority(
            self.root, self.root / "artifacts/vs-1/source-authority"
        )
        run = self.packet["retrieval_run"]
        expected = {
            "retrieval_run_id": expected_run_id,
            "corpus_snapshot_id": expected_corpus_snapshot_id,
            "index_build_id": expected_index_build_id,
        }
        observed = {key: run[key] for key in expected}
        if observed != expected:
            raise WorkbenchError(f"Frozen runtime identity mismatch: {observed}")
        self.candidates = {row["candidate_id"]: row for row in self.packet["candidates"]}
        if len(self.candidates) != len(self.packet["candidates"]):
            raise WorkbenchError("Duplicate frozen candidate identity")

    def case_payload(self) -> dict[str, Any]:
        run = self.packet["retrieval_run"]
        return {
            "schema_version": "vs1-workbench-case-1.0",
            "baseline_commit": self.baseline_commit,
            "question": run["question"],
            "question_id": run["question_id"],
            "retrieval_run_id": run["retrieval_run_id"],
            "corpus_snapshot_id": run["corpus_snapshot_id"],
            "index_build_id": run["index_build_id"],
            "candidate_universe_scope": run["candidate_universe_scope"],
            "candidate_count": len(self.candidates),
            "candidates": [self._candidate_summary(row) for row in self.packet["candidates"]],
        }

    @staticmethod
    def _candidate_summary(candidate: dict[str, Any]) -> dict[str, Any]:
        resolution = candidate["source_resolution"]
        return {
            "candidate_id": candidate["candidate_id"],
            "passage_id": candidate["passage_id"],
            "assertion_ids": candidate["assertion_ids"],
            "document_id": candidate["document_id"],
            "document_role": candidate["document_role"],
            "document_title": resolution["assertions"][0]["document_title"],
            "pages": candidate["pages"],
            "text": candidate["text"],
            "scores": candidate["scores"],
            "stage_ledger": candidate["stage_ledger"],
            "source_status": resolution["status"],
            "location_precision": resolution["location_precision"],
            "warnings": resolution["warnings"],
        }

    def candidate_payload(self, candidate_id: str) -> dict[str, Any]:
        candidate = self.candidates.get(candidate_id)
        if candidate is None:
            raise KeyError(candidate_id)
        resolution = self.authority.resolve_source(candidate["passage_id"])
        if resolution["status"] != "RESOLVED":
            raise WorkbenchError(f"Authoritative ID no longer resolves: {candidate_id}")
        if resolution["requested_id"] != candidate["passage_id"]:
            raise WorkbenchError("Resolver substituted a different passage identity")
        if resolution["document_id"] != candidate["document_id"]:
            raise WorkbenchError("Resolver returned a different document identity")
        if resolution["quote"] != candidate["text"]:
            raise WorkbenchError("Resolver returned different frozen passage text")
        navigation = navigation_from_resolution(resolution, self.authority.pages)
        navigation.update(
            {
                "candidate_id": candidate_id,
                "passage_id": candidate["passage_id"],
                "pdf_url": f"/api/candidates/{candidate_id}/original.pdf",
                "page_image_url_template": (
                    f"/api/candidates/{candidate_id}/pages/{{physical_page}}.png"
                ),
            }
        )
        return {**self._candidate_summary(candidate), "navigation": navigation}

    def original_pdf_path(self, candidate_id: str) -> Path:
        candidate = self.candidates.get(candidate_id)
        if candidate is None:
            raise KeyError(candidate_id)
        document = self.authority.documents[candidate["document_id"]]
        path = self.root / document["local_original_path"]
        if not path.is_file() or file_sha256(path) != document["document_sha256"]:
            raise WorkbenchError("Authoritative PDF is missing or its hash changed")
        return path

    @lru_cache(maxsize=32)
    def render_page_png(self, candidate_id: str, physical_page: int, dpi: int = 120) -> bytes:
        detail = self.candidate_payload(candidate_id)
        allowed_pages = {row["physical_page"] for row in detail["navigation"]["page_views"]}
        if int(physical_page) not in allowed_pages:
            raise WorkbenchError("Requested page is outside the candidate source binding")
        pdf_path = self.original_pdf_path(candidate_id)
        with tempfile.TemporaryDirectory(prefix="regmodeltrace-workbench-") as directory:
            output_root = Path(directory) / "page"
            command = [
                "pdftoppm",
                "-f",
                str(physical_page),
                "-l",
                str(physical_page),
                "-singlefile",
                "-png",
                "-r",
                str(dpi),
                str(pdf_path),
                str(output_root),
            ]
            result = subprocess.run(command, capture_output=True, check=False)
            if result.returncode != 0:
                raise WorkbenchError(
                    "PDF page rendering failed: "
                    + result.stderr.decode("utf-8", errors="replace")[:400]
                )
            rendered = output_root.with_suffix(".png")
            payload = rendered.read_bytes()
        if not payload.startswith(b"\x89PNG\r\n\x1a\n"):
            raise WorkbenchError("Rendered page is not a valid PNG")
        return payload

    def navigation_receipt(self, candidate_id: str) -> dict[str, Any]:
        detail = self.candidate_payload(candidate_id)
        pdf_path = self.original_pdf_path(candidate_id)
        navigation = detail["navigation"]
        return {
            "candidate_id": candidate_id,
            "passage_id": detail["passage_id"],
            "document_id": detail["document_id"],
            "document_role": detail["document_role"],
            "authoritative_pdf_path": pdf_path.relative_to(self.root).as_posix(),
            "authoritative_pdf_sha256": file_sha256(pdf_path),
            "source_status": detail["source_status"],
            "location_precision": navigation["location_precision"],
            "warnings": navigation["warnings"],
            "page_views": navigation["page_views"],
            "fuzzy_substitution_used": False,
        }


def sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()
