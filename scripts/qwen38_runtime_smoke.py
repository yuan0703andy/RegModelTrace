"""Bounded candidate-model runtime check; never reads documentary truth."""

from __future__ import annotations

import argparse
import hashlib
import importlib.metadata
import json
import os
import socket
import subprocess
import time
from datetime import datetime, timezone
from pathlib import Path


MODEL = "Qwen/Qwen3.8-27B-FP8"
REVISION = "017b9c7af6b5689d5dd426a76e0bc077eb5ca20a"


def persist(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model-path", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--tensor-parallel-size", type=int, default=1)
    parser.add_argument("--max-model-len", type=int, default=8192)
    args = parser.parse_args()
    hostname = socket.gethostname()
    if "login" in hostname.lower():
        raise RuntimeError("Inference is forbidden on a login node")
    if args.model_path.name != REVISION:
        raise ValueError("Checkpoint path must identify the pinned revision")
    if not (args.model_path / "config.json").is_file():
        raise FileNotFoundError("Pinned checkpoint is not ready")
    if args.tensor_parallel_size not in {1, 2}:
        raise ValueError("This smoke supports one 48GB GPU or two 32GB GPUs")
    args.output.mkdir(parents=True, exist_ok=False)
    manifest = {
        "status": "STARTED",
        "purpose": "SYNTHETIC_RUNTIME_SMOKE_ONLY",
        "started_utc": datetime.now(timezone.utc).isoformat(),
        "hostname": hostname,
        "slurm_job_id": os.environ.get("SLURM_JOB_ID"),
        "model": MODEL,
        "revision": REVISION,
        "model_path": str(args.model_path),
        "tensor_parallel_size": args.tensor_parallel_size,
        "max_model_len": args.max_model_len,
        "max_num_seqs": 1,
        "max_output_tokens": 128,
        "temperature": 0.0,
        "enable_thinking": False,
        "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "config_sha256": hashlib.sha256(
            (args.model_path / "config.json").read_bytes()
        ).hexdigest(),
        "runtime": {
            name: importlib.metadata.version(name)
            for name in ("vllm", "torch", "transformers", "huggingface-hub")
        },
        "gpu_inventory": subprocess.check_output(
            ["nvidia-smi", "--query-gpu=name,uuid,memory.total,driver_version",
             "--format=csv,noheader"], text=True
        ).strip(),
        "semantic_evaluation": "NOT_RUN",
    }
    persist(args.output / "manifest.json", manifest)
    try:
        import torch
        from vllm import LLM, SamplingParams
        from vllm.sampling_params import StructuredOutputsParams

        if torch.cuda.device_count() < args.tensor_parallel_size:
            raise RuntimeError("Fewer visible GPUs than the requested parallelism")
        for index in range(args.tensor_parallel_size):
            props = torch.cuda.get_device_properties(index)
            minimum_gib = 40 if args.tensor_parallel_size == 1 else 30
            if props.total_memory < minimum_gib * 1024**3:
                raise RuntimeError(f"GPU {index} has insufficient memory for this attempt")
            if torch.cuda.get_device_capability(index) < (8, 9):
                raise RuntimeError(f"GPU {index} does not meet the Ada-or-newer target")

        conversation = [
            {"role": "system", "content": (
                "Classify the supplied synthetic source. Reviewed means scrutiny; "
                "it does not imply a challenge. Return only a JSON object with "
                "evidence_type. Do not add explanations."
            )},
            {"role": "user", "content": (
                "Synthetic source: The Professional Team reviewed the methodology "
                "for landfall updates by gate and by category."
            )},
        ]
        schema = {
            "type": "object",
            "properties": {"evidence_type": {
                "type": "string",
                "enum": ["REVIEWER_SCRUTINY", "REVIEWER_CHALLENGE"],
            }},
            "required": ["evidence_type"],
            "additionalProperties": False,
        }
        persist(args.output / "request.json", {
            "messages": conversation, "schema": schema,
            "chat_template_kwargs": {"enable_thinking": False},
        })
        started = time.monotonic()
        llm = LLM(
            model=str(args.model_path), tokenizer=str(args.model_path),
            tensor_parallel_size=args.tensor_parallel_size,
            distributed_executor_backend="mp", dtype="auto",
            max_model_len=args.max_model_len, max_num_seqs=1,
            gpu_memory_utilization=0.85,
            enforce_eager=True, enable_prefix_caching=False,
            seed=1847,
        )
        manifest["load_seconds"] = time.monotonic() - started
        persist(args.output / "manifest.json", manifest)
        started = time.monotonic()
        generated = llm.chat(
            [conversation],
            SamplingParams(
                temperature=0.0, max_tokens=128, seed=1847,
                structured_outputs=StructuredOutputsParams(json=schema),
            ),
            chat_template_kwargs={"enable_thinking": False}, use_tqdm=False,
        )
        manifest["generation_seconds"] = time.monotonic() - started
        response = generated[0].outputs[0]
        raw = {
            "text": response.text,
            "finish_reason": response.finish_reason,
            "token_ids": list(response.token_ids),
        }
        raw_path = args.output / "raw_response.json"
        persist(raw_path, raw)
        manifest["raw_response_sha256"] = hashlib.sha256(raw_path.read_bytes()).hexdigest()
        parsed = json.loads(response.text)
        valid = (
            isinstance(parsed, dict)
            and set(parsed) == {"evidence_type"}
            and parsed["evidence_type"] in schema["properties"]["evidence_type"]["enum"]
        )
        expected = valid and parsed["evidence_type"] == "REVIEWER_SCRUTINY"
        product_schema = {
            "type": "object",
            "properties": {
                "claims": {"type": "array", "minItems": 1, "maxItems": 2, "items": {
                    "type": "object",
                    "properties": {
                        "text": {"type": "string", "minLength": 1},
                        "evidence_refs": {"type": "array", "minItems": 1,
                                          "items": {"type": "string", "enum": ["E01"]}},
                    },
                    "required": ["text", "evidence_refs"],
                    "additionalProperties": False,
                }},
                "evidence_status": {"type": "string", "enum": [
                    "SUPPORTED", "PARTIALLY_SUPPORTED",
                    "UNRESOLVED_FROM_RETRIEVED_EVIDENCE",
                ]},
            },
            "required": ["claims", "evidence_status"],
            "additionalProperties": False,
        }
        product_messages = [
            {"role": "system", "content": (
                "Answer only from the supplied synthetic evidence. Return JSON with "
                "claims and evidence_status. Every claim must cite E01. "
                "Review does not imply a challenge."
            )},
            {"role": "user", "content": (
                "Question: What did the team do? Evidence E01: The Professional "
                "Team reviewed the methodology for landfall updates."
            )},
        ]
        persist(args.output / "product_request.json", {
            "messages": product_messages, "schema": product_schema,
            "chat_template_kwargs": {"enable_thinking": False},
        })
        product_started = time.monotonic()
        product_generated = llm.chat(
            [product_messages],
            SamplingParams(
                temperature=0.0, max_tokens=128, seed=1847,
                structured_outputs=StructuredOutputsParams(json=product_schema),
            ),
            chat_template_kwargs={"enable_thinking": False}, use_tqdm=False,
        )
        manifest["product_generation_seconds"] = time.monotonic() - product_started
        product_response = product_generated[0].outputs[0]
        product_raw_path = args.output / "product_raw_response.json"
        persist(product_raw_path, {
            "text": product_response.text,
            "finish_reason": product_response.finish_reason,
            "token_ids": list(product_response.token_ids),
        })
        manifest["product_raw_response_sha256"] = hashlib.sha256(
            product_raw_path.read_bytes()
        ).hexdigest()
        product_parsed = json.loads(product_response.text)
        product_valid = (
            isinstance(product_parsed, dict)
            and set(product_parsed) == {"claims", "evidence_status"}
            and product_parsed["evidence_status"] in product_schema["properties"]
            ["evidence_status"]["enum"]
            and isinstance(product_parsed["claims"], list)
            and 1 <= len(product_parsed["claims"]) <= 2
            and all(
                isinstance(claim, dict)
                and set(claim) == {"text", "evidence_refs"}
                and isinstance(claim["text"], str)
                and claim["text"].strip()
                and claim["evidence_refs"] == ["E01"]
                for claim in product_parsed["claims"]
            )
        )
        persist(args.output / "validation.json", {
            "structurally_valid": valid, "synthetic_label_correct": expected,
            "product_contract_valid": product_valid,
            "parsed": parsed, "product_parsed": product_parsed,
            "quality_generalization": "NOT_ASSESSED",
        })
        manifest["status"] = (
            "RUNTIME_SMOKE_PASS" if expected and product_valid
            else "SYNTHETIC_CHECK_FAIL"
        )
        if not expected or not product_valid:
            raise ValueError("Synthetic response failed validation; raw output preserved")
    except Exception as exc:
        if manifest["status"] != "SYNTHETIC_CHECK_FAIL":
            manifest["status"] = "RUNTIME_SMOKE_FAIL"
        manifest["error"] = f"{type(exc).__name__}: {exc}"
        raise
    finally:
        manifest["ended_utc"] = datetime.now(timezone.utc).isoformat()
        persist(args.output / "manifest.json", manifest)


if __name__ == "__main__":
    main()
