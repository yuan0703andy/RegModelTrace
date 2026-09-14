"""Unified RegModelTrace v1 retrieval, synthesis, validation, and citation service."""

import json
import os
import threading
from pathlib import Path

from .contracts import ContractError, model_output_schema, parse_model_output, validate_question


PACKAGE_ROOT = Path(__file__).resolve().parent
DEFAULT_CONFIG = PACKAGE_ROOT / "config/system_v1.json"
_DEFAULT_SYSTEM = None
_DEFAULT_LOCK = threading.Lock()


def _canonical(value):
    return json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(",", ":"))


class RegModelTrace:
    """Long-lived local RAG application. Construct once, then call ask repeatedly."""

    def __init__(self, config_path=None, retriever=None, backend=None):
        self.config_path = Path(config_path or os.environ.get("REGMODELTRACE_CONFIG", DEFAULT_CONFIG))
        self.config = json.loads(self.config_path.read_text())
        self.root = PACKAGE_ROOT
        self.prompt = (self.root / self.config["paths"]["prompt"]).read_text()
        if retriever is None:
            from .retrieval import HybridPassageRetriever

            retriever = HybridPassageRetriever(self.root, self.config)
        if backend is None:
            from .generation import VLLMGenerationBackend

            backend = VLLMGenerationBackend(self.config["generation"])
        self.retriever = retriever
        self.backend = backend
        self.initialization_count = 1

    def _resolve(self, parsed, bundle):
        by_ref = {item["evidence_ref"]: item for item in bundle["references"]}
        public_ids = {}
        public_evidence = []
        answer_parts = []
        resolved_claims = []
        for claim_index, claim in enumerate(parsed["claims"], 1):
            claim_ids = []
            claim_sources = []
            for evidence_ref in claim["evidence_refs"]:
                if evidence_ref not in by_ref:
                    raise ContractError("UNRESOLVED_EVIDENCE_REF")
                source = by_ref[evidence_ref]
                assertion_id = source["assertion_id"]
                if assertion_id not in public_ids:
                    public_id = str(len(public_ids) + 1)
                    public_ids[assertion_id] = public_id
                    public_evidence.append(
                        {
                            "id": public_id,
                            "document": source["document"],
                            "document_role": source["document_role"],
                            "page": source["pages"][0],
                            "pages": source["pages"],
                            "quote": source["text"],
                            "url": source["source_links"][0],
                            "section_path": source["section_path"],
                            "assertion_id": assertion_id,
                            "source_spans": source["source_spans"],
                        }
                    )
                claim_ids.append(public_ids[assertion_id])
                claim_sources.append(source)
            marker = "[" + ", ".join(claim_ids) + "]"
            answer_parts.append(claim["text"] + " " + marker)
            resolved_claims.append(
                {
                    "claim_index": claim_index,
                    "text": claim["text"],
                    "model_evidence_refs": claim["evidence_refs"],
                    "public_evidence_ids": claim_ids,
                    "sources": claim_sources,
                }
            )
        return (
            {
                "answer": "\n\n".join(answer_parts),
                "status": parsed["evidence_status"],
                "evidence": public_evidence,
            },
            resolved_claims,
        )

    def ask(self, question):
        responses, _ = self.ask_many_with_trace([question])
        return responses[0]

    def ask_many(self, questions):
        responses, _ = self.ask_many_with_trace(questions)
        return responses

    def ask_many_with_trace(self, questions):
        questions = [validate_question(question) for question in questions]
        if not questions:
            raise ContractError("AT_LEAST_ONE_QUESTION_REQUIRED")
        maximum = int(self.config["service"]["max_batch_questions"])
        if len(questions) > maximum:
            raise ContractError("BATCH_TOO_LARGE")

        bundles = [self.retriever.retrieve(question) for question in questions]
        conversations = []
        schemas = []
        valid_refs_by_request = []
        for bundle in bundles:
            payload = _canonical(
                {"question": bundle["question"], "evidence_sections": bundle["evidence_sections"]}
            )
            conversations.append(
                [{"role": "system", "content": self.prompt}, {"role": "user", "content": payload}]
            )
            valid_refs = [item["evidence_ref"] for item in bundle["references"]]
            valid_refs_by_request.append(valid_refs)
            schemas.append(model_output_schema(valid_refs))

        generated = self.backend.generate(conversations, schemas)
        if len(generated) != len(questions):
            raise ContractError("REQUEST_RESPONSE_COUNT_MISMATCH")

        responses = []
        traces = []
        for question, bundle, output, valid_refs in zip(questions, bundles, generated, valid_refs_by_request):
            parsed = parse_model_output(output["text"], valid_refs)
            response, claims = self._resolve(parsed, bundle)
            responses.append(response)
            traces.append(
                {
                    "question": question,
                    "selected_passage_ids": bundle["selected_passage_ids"],
                    "retrieval_sections": bundle["sections"],
                    "raw_model_output": output["text"],
                    "validated_model_output": parsed,
                    "resolved_claims": claims,
                    "usage": {
                        "input_tokens": output.get("input_tokens"),
                        "output_tokens": output.get("output_tokens"),
                    },
                }
            )
        return responses, traces


def get_default_system():
    global _DEFAULT_SYSTEM
    if _DEFAULT_SYSTEM is None:
        with _DEFAULT_LOCK:
            if _DEFAULT_SYSTEM is None:
                _DEFAULT_SYSTEM = RegModelTrace()
    return _DEFAULT_SYSTEM


def default_system_ready():
    return _DEFAULT_SYSTEM is not None


def ask(question):
    return get_default_system().ask(question)
