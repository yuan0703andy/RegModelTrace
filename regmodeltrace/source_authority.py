"""Frozen-corpus identity, retrieval-build binding, and real-source resolution.

This module binds the recovered VS-1 artifacts without copying or rebuilding
them.  Original PDFs and the existing canonical stores remain authoritative.
"""

from __future__ import annotations

import hashlib
import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


class SourceAuthorityError(RuntimeError):
    """Raised when an authoritative source or retrieval binding fails closed."""

    def __init__(self, code: str, detail: str | None = None):
        self.code = code
        self.detail = detail
        super().__init__(code if detail is None else f"{code}: {detail}")


def canonical_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def digest_json(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _read_json(path: Path) -> Any:
    return json.loads(path.read_text())


def _write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n")


def _sqlite_quick_check(path: Path) -> None:
    with sqlite3.connect(path.resolve().as_uri() + "?mode=ro", uri=True) as database:
        result = database.execute("PRAGMA quick_check").fetchone()[0]
    if result != "ok":
        raise SourceAuthorityError("SQLITE_INTEGRITY_FAILED", f"{path}: {result}")


def _document_role(document_type: str) -> str:
    roles = {
        "standard": "STANDARDS",
        "vendor_submission": "VENDOR_SUBMISSION",
        "professional_team_report": "PROFESSIONAL_TEAM_REPORT",
    }
    return roles.get(document_type, "OTHER")


def build_task1_source_authority(
    repository_root: Path,
    output_dir: Path,
    *,
    created_at: str | None = None,
    retrieval_config_override: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Freeze the three-document corpus and bind recovered retrieval assets."""

    repository_root = repository_root.resolve()
    package_root = repository_root / "regmodeltrace"
    created_at = created_at or datetime.now(timezone.utc).isoformat()

    document_manifest_path = package_root / "data/document_manifest.json"
    parser_manifest_path = package_root / "data/processed/parser_run_manifest.json"
    passage_path = package_root / "data/retrieval/m4c-v1/passages.jsonl"
    passage_db = package_root / "data/retrieval/m4c-v1/passages.sqlite"
    records_db = package_root / "data/retrieval/m4-foundation-v1.sqlite"
    embedding_dir = package_root / "data/retrieval/m4c-v1/embedding-run"
    embedding_manifest_path = embedding_dir / "manifest.json"
    system_config_path = package_root / "config/system_v1.json"
    source_pages_path = package_root / "data/processed/source_pages.parquet"

    required = [
        document_manifest_path,
        parser_manifest_path,
        passage_path,
        passage_db,
        records_db,
        embedding_manifest_path,
        system_config_path,
        source_pages_path,
    ]
    missing = [str(path) for path in required if not path.is_file()]
    if missing:
        raise SourceAuthorityError("REQUIRED_ARTIFACT_MISSING", ", ".join(missing))

    documents_raw = _read_json(document_manifest_path)
    parser_manifest = _read_json(parser_manifest_path)
    parser_sources = {item["document_id"]: item for item in parser_manifest["source_pdfs"]}
    if set(parser_sources) != {item["document_id"] for item in documents_raw}:
        raise SourceAuthorityError("PARSER_DOCUMENT_SET_MISMATCH")

    documents: list[dict[str, Any]] = []
    for item in sorted(documents_raw, key=lambda row: row["document_id"]):
        relative = Path("regmodeltrace") / item["local_path"]
        source_path = repository_root / relative
        if not source_path.is_file():
            raise SourceAuthorityError("SOURCE_FILE_MISSING", str(relative))
        actual_hash = file_sha256(source_path)
        if actual_hash != item["sha256"]:
            raise SourceAuthorityError("SOURCE_HASH_MISMATCH", item["document_id"])
        parser_source = parser_sources[item["document_id"]]
        if parser_source["sha256"] != actual_hash:
            raise SourceAuthorityError("PARSER_SOURCE_HASH_MISMATCH", item["document_id"])
        if int(parser_source["num_pages"]) != int(item["num_pages"]):
            raise SourceAuthorityError("PARSER_SOURCE_PAGE_COUNT_MISMATCH", item["document_id"])
        documents.append(
            {
                "document_id": item["document_id"],
                "document_sha256": actual_hash,
                "title": item["title"],
                "document_role": _document_role(item["document_type"]),
                "organization": item["author"],
                "source_url": item.get("source_url"),
                "local_original_path": relative.as_posix(),
                "mime_type": "application/pdf",
                "standard_cycle": str(item["standards_year"])
                if item.get("standards_year") is not None
                else None,
                "model_version": item.get("model_version"),
                "document_version_label": item.get("model_version")
                or str(item.get("standards_year") or "")
                or None,
                "physical_page_count": int(item["num_pages"]),
            }
        )

    source_manifest_sha256 = digest_json(documents)
    passage_inventory_sha256 = file_sha256(passage_path)
    snapshot_basis = {
        "schema_version": "corpus-snapshot-1.0",
        "document_identities": [
            {"document_id": row["document_id"], "document_sha256": row["document_sha256"]}
            for row in documents
        ],
        "source_manifest_sha256": source_manifest_sha256,
        "parser_version": parser_manifest["parser_version"],
        "parser_config_sha256": parser_manifest["config_sha256"],
        "parser_canonical_output_sha256": parser_manifest["canonical_output_sha256"],
        "passage_inventory_sha256": passage_inventory_sha256,
    }
    corpus_snapshot_id = "CS_" + digest_json(snapshot_basis)[:24]
    corpus_snapshot = {
        **snapshot_basis,
        "corpus_snapshot_id": corpus_snapshot_id,
        "created_at": created_at,
        "document_ids": [row["document_id"] for row in documents],
        "status": "VALID",
        "notes": "VS-1 three-document RMS 21.0 / 2019 Standards corpus.",
    }

    _sqlite_quick_check(passage_db)
    _sqlite_quick_check(records_db)
    embedding_manifest = _read_json(embedding_manifest_path)
    if embedding_manifest["passages_sha256"] != passage_inventory_sha256:
        raise SourceAuthorityError("EMBEDDING_PASSAGE_IDENTITY_MISMATCH")
    for name, expected in embedding_manifest["output_sha256"].items():
        artifact = embedding_dir / name
        if not artifact.is_file():
            raise SourceAuthorityError("EMBEDDING_OUTPUT_MISSING", name)
        if file_sha256(artifact) != expected:
            raise SourceAuthorityError("EMBEDDING_OUTPUT_HASH_MISMATCH", name)

    config = _read_json(system_config_path)
    retrieval_config = retrieval_config_override or {
        "retrieval": config["retrieval"],
        "embedding": config["embedding"],
    }
    artifact_paths = {
        "passage_inventory": passage_path,
        "passage_fts_database": passage_db,
        "records_database": records_db,
        "source_pages": source_pages_path,
        "embedding_manifest": embedding_manifest_path,
        "passage_matrix": embedding_dir / "passages.npy",
        "passage_ids": embedding_dir / "passage_ids.json",
    }
    artifacts = []
    for role, path in sorted(artifact_paths.items()):
        artifacts.append(
            {
                "artifact_role": role,
                "path": path.relative_to(repository_root).as_posix(),
                "sha256": file_sha256(path),
                "bytes": path.stat().st_size,
            }
        )
    artifact_manifest_sha256 = digest_json(artifacts)
    index_basis = {
        "schema_version": "index-build-manifest-1.0",
        "corpus_snapshot_id": corpus_snapshot_id,
        "retrieval_artifact_manifest_sha256": artifact_manifest_sha256,
        "embedding_model_id": embedding_manifest["model_id"],
        "embedding_model_revision": embedding_manifest["model_revision"],
        "retrieval_config_sha256": digest_json(retrieval_config),
    }
    index_build_id = "IB_" + digest_json(index_basis)[:24]
    index_build_manifest = {
        **index_basis,
        "index_build_id": index_build_id,
        "created_at": created_at,
        "artifacts": artifacts,
        "passage_count": int(embedding_manifest["passage_count"]),
        "embedding_dimension": int(embedding_manifest["dimension"]),
        "status": "VALID",
    }
    runtime_binding = {
        "schema_version": "vs1-source-authority-binding-1.0",
        "corpus_snapshot_id": corpus_snapshot_id,
        "index_build_id": index_build_id,
        "source_documents_file": "source_documents.json",
        "corpus_snapshot_file": "corpus_snapshot.json",
        "index_build_manifest_file": "index_build_manifest.json",
        "path_base": "REPOSITORY_ROOT",
    }

    _write_json(output_dir / "source_documents.json", documents)
    _write_json(output_dir / "corpus_snapshot.json", corpus_snapshot)
    _write_json(output_dir / "index_build_manifest.json", index_build_manifest)
    _write_json(output_dir / "runtime_binding.json", runtime_binding)
    return {
        "source_documents": documents,
        "corpus_snapshot": corpus_snapshot,
        "index_build_manifest": index_build_manifest,
        "runtime_binding": runtime_binding,
    }


def _union_bbox(regions: list[list[float]]) -> list[float] | None:
    if not regions:
        return None
    return [
        min(region[0] for region in regions),
        min(region[1] for region in regions),
        max(region[2] for region in regions),
        max(region[3] for region in regions),
    ]


class FrozenCorpusAuthority:
    """Resolve existing real-corpus identities without fuzzy substitution."""

    def __init__(self, repository_root: Path, authority_dir: Path):
        self.repository_root = repository_root.resolve()
        self.authority_dir = authority_dir.resolve()
        self.snapshot = _read_json(self.authority_dir / "corpus_snapshot.json")
        self.index_build = _read_json(self.authority_dir / "index_build_manifest.json")
        self.documents = {
            item["document_id"]: item
            for item in _read_json(self.authority_dir / "source_documents.json")
        }
        if self.snapshot["status"] != "VALID":
            raise SourceAuthorityError("CORPUS_SNAPSHOT_INVALID")
        if self.index_build["status"] != "VALID":
            raise SourceAuthorityError("INDEX_BUILD_INVALID")
        if self.index_build["corpus_snapshot_id"] != self.snapshot["corpus_snapshot_id"]:
            raise SourceAuthorityError("INDEX_CORPUS_BINDING_MISMATCH")
        if digest_json(list(self.documents.values())) != self.snapshot["source_manifest_sha256"]:
            raise SourceAuthorityError("SOURCE_MANIFEST_HASH_MISMATCH")
        if sorted(self.documents) != sorted(self.snapshot["document_ids"]):
            raise SourceAuthorityError("SOURCE_DOCUMENT_SET_MISMATCH")

        artifacts = {
            item["artifact_role"]: self.repository_root / item["path"]
            for item in self.index_build["artifacts"]
        }
        for item in self.index_build["artifacts"]:
            path = self.repository_root / item["path"]
            if not path.is_file() or file_sha256(path) != item["sha256"]:
                raise SourceAuthorityError("INDEX_ARTIFACT_HASH_MISMATCH", item["artifact_role"])

        self.passages = {}
        for line in artifacts["passage_inventory"].read_text().splitlines():
            passage = json.loads(line)
            self.passages[passage["passage_id"]] = passage

        with sqlite3.connect(
            artifacts["records_database"].resolve().as_uri() + "?mode=ro", uri=True
        ) as database:
            self.records = {
                key: json.loads(payload)
                for key, payload in database.execute("SELECT record_id,payload FROM records")
            }
            self.blocks = {
                key: json.loads(payload)
                for key, payload in database.execute("SELECT block_id,payload FROM blocks")
            }

        try:
            import pyarrow.parquet as pq
        except ImportError as exc:
            raise SourceAuthorityError("PYARROW_REQUIRED_FOR_CANONICAL_PAGES") from exc
        page_table = pq.read_table(artifacts["source_pages"])
        self.pages = {
            (row["document_id"], int(row["page"])): row for row in page_table.to_pylist()
        }
        self._document_hash_cache: dict[str, str] = {}
        self._span_index: dict[str, tuple[str, int, str]] = {}
        for assertion_id, record in self.records.items():
            for raw_index, raw_span in enumerate(record.get("source_spans") or []):
                for block_id in raw_span.get("source_block_ids") or []:
                    source_span_id = self._source_span_id(assertion_id, raw_index, block_id)
                    self._span_index[source_span_id] = (assertion_id, raw_index, block_id)

    @staticmethod
    def _source_span_id(assertion_id: str, raw_index: int, block_id: str) -> str:
        return "SS_" + digest_json([assertion_id, raw_index, block_id])[:24]

    def _failed(self, identifier: str, code: str, detail: str | None = None) -> dict[str, Any]:
        return {
            "status": "FAILED",
            "corpus_snapshot_id": self.snapshot["corpus_snapshot_id"],
            "index_build_id": self.index_build["index_build_id"],
            "requested_id": identifier,
            "error": code,
            "detail": detail,
            "fuzzy_substitution_used": False,
        }

    def _verified_document(self, document_id: str) -> tuple[dict[str, Any], Path]:
        document = self.documents.get(document_id)
        if document is None or document_id not in self.snapshot["document_ids"]:
            raise SourceAuthorityError("ID_NOT_IN_SNAPSHOT", document_id)
        path = self.repository_root / document["local_original_path"]
        if not path.is_file():
            raise SourceAuthorityError("SOURCE_FILE_MISSING", document_id)
        actual_hash = self._document_hash_cache.get(document_id)
        if actual_hash is None:
            actual_hash = file_sha256(path)
            self._document_hash_cache[document_id] = actual_hash
        if actual_hash != document["document_sha256"]:
            raise SourceAuthorityError("SOURCE_HASH_MISMATCH", document_id)
        return document, path

    def _map_block_range(
        self,
        block: dict[str, Any],
        selected_start: int,
        selected_end: int,
    ) -> list[dict[str, Any]]:
        block_text = block["text"]
        if selected_start < 0 or selected_end < selected_start or selected_end > len(block_text):
            raise SourceAuthorityError("INVALID_SOURCE_SPAN", block["block_id"])
        selected_text = block_text[selected_start:selected_end]
        block_spans = block.get("source_spans") or []
        pieces = []
        for span in block_spans:
            page_key = (block["document_id"], int(span["page"]))
            page = self.pages.get(page_key)
            if page is None:
                raise SourceAuthorityError("UNKNOWN_CANONICAL_PAGE", str(page_key))
            if page["page_text_sha256"] != span["page_text_sha256"]:
                raise SourceAuthorityError("PAGE_TEXT_HASH_MISMATCH", str(page_key))
            text = page["text"][int(span["start"]):int(span["end"])]
            pieces.append({"span": span, "page": page, "text": text})

        separators = ["", "\n", " "]
        separator = next(
            (candidate for candidate in separators if candidate.join(x["text"] for x in pieces) == block_text),
            None,
        )
        if separator is None:
            raise SourceAuthorityError("BLOCK_CANONICAL_TEXT_MISMATCH", block["block_id"])

        mapped = []
        cursor = 0
        for index, piece in enumerate(pieces):
            piece_start = cursor
            piece_end = cursor + len(piece["text"])
            overlap_start = max(selected_start, piece_start)
            overlap_end = min(selected_end, piece_end)
            if overlap_start < overlap_end:
                page_start = int(piece["span"]["start"]) + overlap_start - piece_start
                page_end = int(piece["span"]["start"]) + overlap_end - piece_start
                page_text = piece["page"]["text"][page_start:page_end]
                line_geometry = []
                for line in block.get("line_geometry") or []:
                    if int(line["start"]) < page_end and int(line["end"]) > page_start:
                        line_geometry.append(line)
                regions = [line["bbox"] for line in line_geometry if line.get("bbox")]
                mapped.append(
                    {
                        "physical_page_index": int(piece["span"]["page"]),
                        "pdf_page_index_zero_based": int(piece["span"]["page"]) - 1,
                        "printed_page_label": block.get("printed_page_label"),
                        "page_text_sha256": piece["page"]["page_text_sha256"],
                        "char_start": page_start,
                        "char_end": page_end,
                        "quote": page_text,
                        "quote_sha256": hashlib.sha256(page_text.encode("utf-8")).hexdigest(),
                        "bbox": _union_bbox(regions),
                        "line_geometry": line_geometry,
                        "alignment_status": "ALIGNED" if regions else "ALIGNMENT_FAILED",
                    }
                )
            cursor = piece_end
            if index < len(pieces) - 1:
                cursor += len(separator)
        if "".join(item["quote"] for item in mapped) != selected_text:
            raise SourceAuthorityError("SOURCE_SPAN_TEXT_MISMATCH", block["block_id"])
        return mapped

    def _resolve_assertion(self, assertion_id: str) -> dict[str, Any]:
        record = self.records.get(assertion_id)
        if record is None:
            raise SourceAuthorityError("UNKNOWN_ASSERTION_ID", assertion_id)
        document_id = record["document_id"]
        document, source_path = self._verified_document(document_id)
        if record.get("document_sha256") != document["document_sha256"]:
            raise SourceAuthorityError("ASSERTION_DOCUMENT_HASH_MISMATCH", assertion_id)

        resolved_spans = []
        raw_quotes = []
        for raw_index, raw_span in enumerate(record.get("source_spans") or []):
            block_ids = raw_span.get("source_block_ids") or []
            if len(block_ids) != 1:
                raise SourceAuthorityError("MULTIBLOCK_SOURCE_SPAN_UNSUPPORTED", assertion_id)
            block_id = block_ids[0]
            block = self.blocks.get(block_id)
            if block is None:
                raise SourceAuthorityError("UNKNOWN_SOURCE_BLOCK", block_id)
            if block["document_id"] != document_id:
                raise SourceAuthorityError("BLOCK_DOCUMENT_MISMATCH", block_id)
            start = int(raw_span.get("block_char_start", 0))
            end = int(raw_span.get("block_char_end", len(block["text"])))
            selected = block["text"][start:end]
            if selected != raw_span.get("quote"):
                raise SourceAuthorityError("ASSERTION_BLOCK_QUOTE_MISMATCH", assertion_id)
            raw_quotes.append(selected)
            mapped = self._map_block_range(block, start, end)
            source_span_id = self._source_span_id(assertion_id, raw_index, block_id)
            for item in mapped:
                resolved_spans.append(
                    {
                        **item,
                        "source_span_id": source_span_id,
                        "source_block_id": block_id,
                    }
                )

        record_text = record.get("text")
        joins = {"".join(raw_quotes), " ".join(raw_quotes), "\n".join(raw_quotes)}
        if record_text not in joins:
            raise SourceAuthorityError("ASSERTION_TEXT_RECONSTRUCTION_MISMATCH", assertion_id)
        warnings = []
        if any(item["bbox"] is None for item in resolved_spans):
            warnings.append("SOURCE_GEOMETRY_UNAVAILABLE")
        if all(item["bbox"] is not None for item in resolved_spans):
            precision = "EXACT_GEOMETRY"
        elif resolved_spans:
            precision = "PAGE_TEXT"
        else:
            precision = "PAGE_ONLY"
        return {
            "status": "RESOLVED",
            "corpus_snapshot_id": self.snapshot["corpus_snapshot_id"],
            "index_build_id": self.index_build["index_build_id"],
            "requested_type": "ASSERTION",
            "requested_id": assertion_id,
            "assertion_id": assertion_id,
            "document_id": document_id,
            "document_sha256": document["document_sha256"],
            "document_title": document["title"],
            "document_role": document["document_role"],
            "local_original_path": source_path.relative_to(self.repository_root).as_posix(),
            "source_file_hash_verified": True,
            "quote": record_text,
            "quote_sha256": hashlib.sha256(record_text.encode("utf-8")).hexdigest(),
            "pages": sorted({item["physical_page_index"] for item in resolved_spans}),
            "source_spans": resolved_spans,
            "location_precision": precision,
            "warnings": warnings,
            "fuzzy_substitution_used": False,
        }

    def resolve_source(self, identifier: str) -> dict[str, Any]:
        try:
            if identifier in self.passages:
                passage = self.passages[identifier]
                assertions = [self._resolve_assertion(item) for item in passage["assertion_ids"]]
                if not assertions:
                    raise SourceAuthorityError("PASSAGE_HAS_NO_ASSERTIONS", identifier)
                if {item["document_id"] for item in assertions} != {passage["document_id"]}:
                    raise SourceAuthorityError("PASSAGE_DOCUMENT_MISMATCH", identifier)
                reconstructed = {
                    " ".join(item["quote"] for item in assertions),
                    "\n".join(item["quote"] for item in assertions),
                }
                if passage["text"] not in reconstructed:
                    raise SourceAuthorityError("PASSAGE_TEXT_RECONSTRUCTION_MISMATCH", identifier)
                warnings = sorted({warning for item in assertions for warning in item["warnings"]})
                return {
                    "status": "RESOLVED",
                    "corpus_snapshot_id": self.snapshot["corpus_snapshot_id"],
                    "index_build_id": self.index_build["index_build_id"],
                    "requested_type": "PASSAGE",
                    "requested_id": identifier,
                    "passage_id": identifier,
                    "document_id": passage["document_id"],
                    "document_role": passage["document_role"],
                    "quote": passage["text"],
                    "pages": passage["pages"],
                    "assertions": assertions,
                    "location_precision": "EXACT_GEOMETRY"
                    if all(item["location_precision"] == "EXACT_GEOMETRY" for item in assertions)
                    else "PAGE_TEXT",
                    "warnings": warnings,
                    "fuzzy_substitution_used": False,
                }
            if identifier in self.records:
                return self._resolve_assertion(identifier)
            if identifier in self._span_index:
                assertion_id, _, _ = self._span_index[identifier]
                assertion = self._resolve_assertion(assertion_id)
                spans = [
                    item for item in assertion["source_spans"] if item["source_span_id"] == identifier
                ]
                if not spans:
                    raise SourceAuthorityError("UNKNOWN_SOURCE_SPAN_ID", identifier)
                return {
                    **assertion,
                    "requested_type": "SOURCE_SPAN",
                    "requested_id": identifier,
                    "source_span_id": identifier,
                    "source_spans": spans,
                    "pages": sorted({item["physical_page_index"] for item in spans}),
                }
            return self._failed(identifier, "ID_NOT_IN_SNAPSHOT")
        except SourceAuthorityError as exc:
            return self._failed(identifier, exc.code, exc.detail)
