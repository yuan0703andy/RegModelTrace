"""Persistent deterministic three-role hybrid retrieval for RegModelTrace v1."""

import hashlib
import json
import os
import re
import sqlite3
from pathlib import Path

import numpy as np


def _load(path):
    return json.loads(Path(path).read_text())


def _sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


class TransformersQueryEncoder:
    """Pinned MiniLM query encoder. Passage vectors remain precomputed."""

    def __init__(self, model_path, model_files, max_length=256, device="cpu"):
        self.model_path = Path(model_path)
        self.max_length = int(max_length)
        self.device = device
        for name, expected in model_files.items():
            if _sha(self.model_path / name) != expected:
                raise ValueError("Changed embedding model file: " + name)

        import torch
        from transformers import AutoModel, AutoTokenizer

        self.torch = torch
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_path, local_files_only=True)
        self.model = AutoModel.from_pretrained(self.model_path, local_files_only=True).to(device).eval()

    def encode(self, texts):
        encoded = self.tokenizer(
            list(texts),
            padding=True,
            truncation=True,
            max_length=self.max_length,
            return_tensors="pt",
        )
        encoded = {key: value.to(self.device) for key, value in encoded.items()}
        with self.torch.inference_mode():
            hidden = self.model(**encoded).last_hidden_state
        mask = encoded["attention_mask"].unsqueeze(-1).expand(hidden.size()).float()
        pooled = (hidden * mask).sum(1) / mask.sum(1).clamp(min=1e-9)
        pooled = self.torch.nn.functional.normalize(pooled, p=2, dim=1)
        return pooled.cpu().numpy().astype("float32")


class HybridPassageRetriever:
    """Load retrieval artifacts once and fan each question across three roles."""

    def __init__(self, root, config, query_encoder=None):
        self.root = Path(root)
        self.config = config
        paths = config["paths"]
        self.passages_path = self.root / paths["passages"]
        self.passages_db = self.root / paths["passages_database"]
        self.records_db = self.root / paths["records_database"]
        self.embedding_manifest_path = self.root / paths["embedding_manifest"]
        self.matrix_path = self.root / paths["passage_matrix"]
        self.passage_ids_path = self.root / paths["passage_ids"]

        manifest = _load(self.embedding_manifest_path)
        for name, expected in manifest["output_sha256"].items():
            artifact = self.embedding_manifest_path.parent / name
            if _sha(artifact) != expected:
                raise ValueError("Changed retrieval embedding artifact: " + name)
        if _sha(self.passages_path) != manifest["passages_sha256"]:
            raise ValueError("Changed deterministic passage inventory")

        self.passages = [json.loads(line) for line in self.passages_path.read_text().splitlines()]
        self.by_passage = {item["passage_id"]: item for item in self.passages}
        self.passage_ids = _load(self.passage_ids_path)
        self.passage_index = {pid: index for index, pid in enumerate(self.passage_ids)}
        self.matrix = np.load(self.matrix_path, mmap_mode="r", allow_pickle=False)
        if self.matrix.shape[0] != len(self.passage_ids):
            raise ValueError("Passage matrix and identity inventory differ")

        self.roles = tuple(config["retrieval"]["document_role_order"])
        self.role_ids = {
            role: [pid for pid in self.passage_ids if self.by_passage[pid]["document_role"] == role]
            for role in self.roles
        }
        with sqlite3.connect(self.records_db.resolve().as_uri() + "?mode=ro", uri=True) as database:
            self.records = {
                key: json.loads(payload)
                for key, payload in database.execute("SELECT record_id,payload FROM records")
            }
            self.documents = {
                key: json.loads(payload)
                for key, payload in database.execute("SELECT document_id,payload FROM documents")
            }

        if query_encoder is None:
            snapshot = _load(self.root / paths["embedding_model_snapshot"])
            model_path = os.environ.get("REGMODELTRACE_EMBEDDING_MODEL_PATH") or snapshot.get("local_path")
            if not model_path:
                raise ValueError(
                    "Set REGMODELTRACE_EMBEDDING_MODEL_PATH to the pinned MiniLM snapshot"
                )
            query_encoder = TransformersQueryEncoder(
                model_path,
                snapshot["files"],
                max_length=config["embedding"]["maximum_sequence_length"],
                device=config["embedding"]["device"],
            )
        self.query_encoder = query_encoder
        self.initialization_count = 1

    def _bm25(self, query, role):
        tokens = list(dict.fromkeys(re.findall(r"\w+", query, re.UNICODE)))[:64]
        if not tokens:
            return []
        expression = " OR ".join('"' + token + '"' for token in tokens)
        with sqlite3.connect(self.passages_db.resolve().as_uri() + "?mode=ro", uri=True) as database:
            rows = database.execute(
                """SELECT passages.passage_id,bm25(search_text,1.0,0.2) AS score
                   FROM search_text JOIN passages ON search_text.rowid=passages.rowid
                   WHERE search_text MATCH ? AND passages.document_role=?
                   ORDER BY score,passages.passage_id""",
                [expression, role],
            ).fetchall()
        return {pid: rank for rank, (pid, _) in enumerate(rows, 1)}

    def _rank_role(self, query, role, query_vector):
        ids = self.role_ids[role]
        positions = [self.passage_index[pid] for pid in ids]
        scores = np.asarray(self.matrix[positions] @ query_vector, dtype="float64")
        dense_order = sorted(
            zip(ids, scores.tolist()), key=lambda item: (-item[1], item[0])
        )
        dense_rank = {pid: rank for rank, (pid, _) in enumerate(dense_order, 1)}
        bm25_rank = self._bm25(query, role)
        rrf_k = int(self.config["retrieval"]["rrf_k"])
        rows = []
        for pid in ids:
            score = 1.0 / (rrf_k + dense_rank[pid])
            if pid in bm25_rank:
                score += 1.0 / (rrf_k + bm25_rank[pid])
            rows.append(
                {
                    "passage_id": pid,
                    "score": score,
                    "bm25_rank": bm25_rank.get(pid),
                    "dense_rank": dense_rank[pid],
                }
            )
        rows.sort(key=lambda item: (-item["score"], item["passage_id"]))
        for index, row in enumerate(rows, 1):
            row["rank"] = index
        return rows[: int(self.config["retrieval"]["passages_per_role"])]

    def retrieve(self, question):
        query_vector = self.query_encoder.encode([question])[0]
        if query_vector.shape != (self.matrix.shape[1],):
            raise ValueError("Unexpected query embedding shape")
        sections = []
        model_sections = []
        references = []
        selected = []
        for role in self.roles:
            section = {"document_role": role, "passages": []}
            model_section = {"document_role": role, "passages": []}
            for role_rank, row in enumerate(self._rank_role(question, role, query_vector), 1):
                passage = self.by_passage[row["passage_id"]]
                selected.append(row["passage_id"])
                resolved_assertions = []
                model_assertions = []
                for assertion_id in passage["assertion_ids"]:
                    record = self.records[assertion_id]
                    document = self.documents[record["document_id"]]
                    evidence_ref = "E" + str(len(references) + 1).zfill(2)
                    binding = {
                        "evidence_ref": evidence_ref,
                        "assertion_id": assertion_id,
                        "text": record["text"],
                        "document": document.get("title", record["document_id"]),
                        "document_role": role,
                        "document_id": record["document_id"],
                        "pages": record["pages"],
                        "section_path": record["section_path"],
                        "source_spans": record["source_spans"],
                        "source_links": [document["source_url"] + "#page=" + str(page) for page in record["pages"]],
                        "passage_id": row["passage_id"],
                        "role_rank": role_rank,
                    }
                    references.append(binding)
                    resolved_assertions.append(binding)
                    model_assertions.append(
                        {
                            "evidence_ref": evidence_ref,
                            "text": record["text"],
                            "document": binding["document"],
                            "pages": record["pages"],
                            "section_path": record["section_path"],
                        }
                    )
                section["passages"].append({**row, "role_rank": role_rank, "assertions": resolved_assertions})
                model_section["passages"].append(
                    {"passage_ref": role[:2] + str(role_rank), "assertions": model_assertions}
                )
            sections.append(section)
            model_sections.append(model_section)
        return {
            "question": question,
            "sections": sections,
            "evidence_sections": model_sections,
            "references": references,
            "selected_passage_ids": selected,
        }
