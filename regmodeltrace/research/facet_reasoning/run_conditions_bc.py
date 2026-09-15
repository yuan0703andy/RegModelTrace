"""Run frozen FT-1 Conditions B/C on a DCC GPU compute node.

The runner can read model requests and runtime configuration only. Truth and
human-adjudication artifacts are denied by an audit hook.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.metadata
import json
import os
import socket
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

os.environ["VLLM_ENABLE_V1_MULTIPROCESSING"] = "0"


FORBIDDEN = {
    "truth.json",
    "agreement_report.json",
    "adjudicator_a_return.json",
    "adjudicator_b_return.json",
    "resolution_return.json",
}


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_new(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def deny_truth_reads(frozen: Path) -> dict[str, int]:
    forbidden = {(frozen / name).resolve() for name in FORBIDDEN}
    reads = {"count": 0}

    def guard(event: str, args: tuple[Any, ...]) -> None:
        if event != "open" or not args or not isinstance(args[0], (str, bytes, os.PathLike)):
            return
        if Path(os.fsdecode(args[0])).resolve() in forbidden:
            reads["count"] += 1
            raise PermissionError("Inference process cannot read evaluator truth")

    sys.addaudithook(guard)
    return reads


def validate_prediction(parsed: dict[str, Any], request: dict[str, Any]) -> None:
    allowed = {"DEMONSTRATED", "NOT_DEMONSTRATED", "CONTRADICTED", "NOT_APPLICABLE"}
    expected_facets = set(request["input"]["requirement"]["facets"][i]["facet_id"] for i in range(len(request["input"]["requirement"]["facets"])))
    if set(parsed) != ({"facets", "overall_relation"} if request["condition"] == "B" else {"facets"}):
        raise ValueError("Unexpected output fields")
    if set(parsed["facets"]) != expected_facets or not set(parsed["facets"].values()) <= allowed:
        raise ValueError("Facet identities or states do not match the frozen request")
    if request["condition"] == "B" and parsed["overall_relation"] not in {
        "ALIGNED", "PARTIALLY_ALIGNED", "CONFLICT", None
    }:
        raise ValueError("Invalid Condition B relation")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--frozen", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if "login" in socket.gethostname().lower():
        raise RuntimeError("FT-1 inference requires a DCC GPU compute node")
    if args.output.exists():
        raise RuntimeError("Refusing an implicit FT-1 rerun")
    frozen = args.frozen.resolve()
    lock = load(frozen / "freeze.json")
    if lock.get("status") != "FROZEN_BEFORE_INFERENCE":
        raise ValueError("FT-1 fixture is not frozen")
    for name, expected in lock["files"].items():
        if sha(frozen / name) != expected:
            raise ValueError(f"Frozen input hash mismatch: {name}")

    config = load(frozen / "model_config.json")
    if config["semantic_retries"] != 0 or config["enable_prefix_caching"] is not False:
        raise ValueError("FT-1 decoding contract changed")
    request_lines = (frozen / "model_requests.jsonl").read_text(encoding="utf-8").splitlines()
    requests = [json.loads(line) for line in request_lines if line]
    for request in requests:
        serialized_input = json.dumps(request["input"], sort_keys=True)
        if any(value in serialized_input for value in request["host_bindings"].values()):
            raise ValueError("Host-owned proposition identity leaked into model input")

    args.output.mkdir(parents=True)
    manifest = {
        "version": "ft1-conditions-bc-run-1.0",
        "status": "RUNNING",
        "started_utc": now(),
        "hostname": socket.gethostname(),
        "gpu": subprocess.check_output(
            ["nvidia-smi", "--query-gpu=name,uuid,memory.total", "--format=csv,noheader"], text=True
        ).strip(),
        "freeze_sha256": sha(frozen / "freeze.json"),
        "model_requests_sha256": sha(frozen / "model_requests.jsonl"),
        "model": config["model"],
        "model_revision": config["model_revision"],
        "conditions": ["B", "C"],
        "condition_d": "NOT_AUTHORIZED",
        "evaluator_reads": 0,
    }
    write_new(args.output / "run_manifest.json", manifest)
    reads = deny_truth_reads(frozen)

    from vllm import LLM, SamplingParams
    from vllm.sampling_params import StructuredOutputsParams

    if importlib.metadata.version("vllm") != config["vllm_version"]:
        raise ValueError("Changed vLLM version")
    llm = LLM(
        model=config["model_path"],
        tokenizer=config["model_path"],
        dtype=config["dtype"],
        max_model_len=config["max_model_len"],
        gpu_memory_utilization=config["gpu_memory_utilization"],
        tensor_parallel_size=1,
        seed=config["seed"],
        enforce_eager=True,
        max_num_seqs=config["max_num_seqs"],
        enable_prefix_caching=False,
        disable_log_stats=True,
    )
    messages, sampling = [], []
    tokenizer = llm.get_tokenizer()
    for request in requests:
        user = json.dumps({"input": request["input"]}, ensure_ascii=False, sort_keys=True)
        conversation = [
            {"role": "system", "content": request["system"]},
            {"role": "user", "content": user},
        ]
        token_count = len(tokenizer.apply_chat_template(conversation, tokenize=True, add_generation_prompt=True))
        if token_count + config["max_output_tokens"] > config["max_model_len"]:
            raise ValueError(f"Context truncation forbidden: {request['request_id']}")
        messages.append(conversation)
        sampling.append(
            SamplingParams(
                temperature=config["temperature"],
                seed=config["seed"],
                max_tokens=config["max_output_tokens"],
                structured_outputs=StructuredOutputsParams(json=request["output_schema"]),
            )
        )
    generated = llm.chat(messages, sampling, use_tqdm=False)
    raw_persisted = now()
    raw_paths = []
    for index, output in enumerate(generated):
        response = output.outputs[0]
        raw = {
            "request_index": index,
            "request_id": requests[index]["request_id"],
            "engine_request_id": output.request_id,
            "text": response.text,
            "finish_reason": response.finish_reason,
            "output_token_ids": list(response.token_ids),
        }
        path = args.output / "raw" / f"response-{index:03d}.json"
        write_new(path, raw)
        raw_paths.append(path)

    results = []
    for request, path in zip(requests, raw_paths):
        raw = load(path)
        try:
            parsed = json.loads(raw["text"])
            validate_prediction(parsed, request)
            status, error = "PASS", None
        except Exception as exc:
            parsed, status, error = None, "FAIL", f"{type(exc).__name__}: {exc}"
        results.append(
            {
                "request_id": request["request_id"],
                "case_id": request["case_id"],
                "condition": request["condition"],
                "parse_status": status,
                "error": error,
                "prediction": parsed,
                "host_bindings": request["host_bindings"],
                "raw_response": str(path.relative_to(args.output)),
                "raw_response_sha256": sha(path),
                "raw_persisted_utc": raw_persisted,
            }
        )
    write_new(args.output / "results.json", results)
    manifest.update(
        {
            "status": "COMPLETE" if all(item["parse_status"] == "PASS" for item in results) else "COMPLETE_WITH_FAILURES",
            "completed_utc": now(),
            "requests": len(results),
            "valid_outputs": sum(item["parse_status"] == "PASS" for item in results),
            "results_sha256": sha(args.output / "results.json"),
            "raw_persisted_utc": raw_persisted,
            "evaluator_reads": reads["count"],
        }
    )
    write_new(args.output / "run_manifest.json", manifest)


if __name__ == "__main__":
    main()
