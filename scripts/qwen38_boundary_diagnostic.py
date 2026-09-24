"""Run frozen synthetic Qwen3.8 diagnostics without reading their oracle."""

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


REVISION = "017b9c7af6b5689d5dd426a76e0bc077eb5ca20a"
REVIEWER_SYSTEM = (
    "Classify the supplied synthetic source. Reviewed means scrutiny; "
    "it does not imply a challenge. Return only a JSON object with "
    "evidence_type. Do not add explanations."
)
CAUSAL_SYSTEM = (
    "Decide whether the supplied synthetic source explicitly connects a "
    "review intervention to a vendor or model modification. Review and update "
    "occurring together or in sequence do not establish causation. Return "
    "only a JSON object with evidence_type. Do not add explanations."
)
LABELS = {
    "reviewer": ["REVIEWER_SCRUTINY", "REVIEWER_CHALLENGE"],
    "causal": ["NOT_ESTABLISHED", "EXPLICIT_REVIEW_CAUSED_MODIFICATION"],
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def persist(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def load_cases(path: Path) -> list[dict[str, str]]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    cases = payload["cases"]
    ids = [case["case_id"] for case in cases]
    if payload["version"] != "qwen38-synthetic-boundary-1" or len(cases) != 18:
        raise ValueError("Unexpected diagnostic fixture version or case count")
    if len(set(ids)) != len(ids):
        raise ValueError("Duplicate case ID")
    for case in cases:
        if set(case) != {"case_id", "panel", "source"}:
            raise ValueError("Model-facing cases must not contain an oracle label")
        if case["panel"] not in LABELS or not case["source"].strip():
            raise ValueError("Invalid panel or empty source")
    if cases[0]["source"] != cases[1]["source"]:
        raise ValueError("R01/R02 must repeat the original source exactly")
    return cases


def request_for(case: dict[str, str]) -> dict:
    panel = case["panel"]
    return {
        "case_id": case["case_id"],
        "panel": panel,
        "messages": [
            {"role": "system", "content": REVIEWER_SYSTEM if panel == "reviewer" else CAUSAL_SYSTEM},
            {"role": "user", "content": "Synthetic source: " + case["source"]},
        ],
        "schema": {
            "type": "object",
            "properties": {"evidence_type": {"type": "string", "enum": LABELS[panel]}},
            "required": ["evidence_type"],
            "additionalProperties": False,
        },
        "chat_template_kwargs": {"enable_thinking": False},
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cases", type=Path, required=True)
    parser.add_argument("--model-path", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--validate-only", action="store_true")
    args = parser.parse_args()
    cases = load_cases(args.cases)
    requests = [request_for(case) for case in cases]
    if args.validate_only:
        print(json.dumps({"cases": len(cases), "panels": {
            panel: sum(case["panel"] == panel for case in cases) for panel in LABELS
        }, "cases_sha256": sha256(args.cases)}, sort_keys=True))
        return

    if args.model_path is None or args.output is None:
        parser.error("--model-path and --output are required for inference")
    if "login" in socket.gethostname().lower():
        raise RuntimeError("Inference is forbidden on a login node")
    if args.model_path.name != REVISION:
        raise ValueError("Checkpoint path must identify the pinned revision")
    config_path = args.model_path / "config.json"
    if not config_path.is_file():
        raise FileNotFoundError(config_path)
    if sha256(config_path) != "74227dd615bf1ea975aa676bdf355a0379858c12f394b5365cd9dfa5fc2c70bc":
        raise ValueError("Pinned checkpoint config hash mismatch")

    args.output.mkdir(parents=True, exist_ok=False)
    persist(args.output / "requests.json", requests)
    manifest = {
        "status": "STARTED",
        "purpose": "SYNTHETIC_BOUNDARY_DIAGNOSTIC_ONLY",
        "started_utc": datetime.now(timezone.utc).isoformat(),
        "hostname": socket.gethostname(),
        "slurm_job_id": os.environ.get("SLURM_JOB_ID"),
        "model": "Qwen/Qwen3.8-27B-FP8",
        "revision": REVISION,
        "model_path": str(args.model_path),
        "config_sha256": sha256(config_path),
        "cases_sha256": sha256(args.cases),
        "runner_sha256": sha256(Path(__file__)),
        "requests_sha256": sha256(args.output / "requests.json"),
        "tensor_parallel_size": 2,
        "max_model_len": 8192,
        "max_num_seqs": 1,
        "temperature": 0.0,
        "seed": 1847,
        "enable_thinking": False,
        "runtime": {name: importlib.metadata.version(name) for name in (
            "vllm", "torch", "transformers", "huggingface-hub"
        )},
        "gpu_inventory": subprocess.check_output([
            "nvidia-smi", "--query-gpu=name,uuid,memory.total,driver_version",
            "--format=csv,noheader",
        ], text=True).strip(),
        "semantic_evaluation": "NOT_RUN_BY_INFERENCE_SCRIPT",
    }
    persist(args.output / "manifest.json", manifest)
    try:
        import torch
        from vllm import LLM, SamplingParams
        from vllm.sampling_params import StructuredOutputsParams

        if torch.cuda.device_count() < 2:
            raise RuntimeError("Two GPUs are required")
        for index in range(2):
            props = torch.cuda.get_device_properties(index)
            if props.total_memory < 29 * 1024**3:
                raise RuntimeError(f"GPU {index} has less than 29 GiB")
            if torch.cuda.get_device_capability(index) < (8, 9):
                raise RuntimeError(f"GPU {index} is older than Ada")

        started = time.monotonic()
        llm = LLM(
            model=str(args.model_path), tokenizer=str(args.model_path),
            tensor_parallel_size=2, distributed_executor_backend="mp",
            dtype="auto", max_model_len=8192, max_num_seqs=1,
            gpu_memory_utilization=0.85, enforce_eager=True,
            enable_prefix_caching=False, seed=1847,
        )
        manifest["load_seconds"] = time.monotonic() - started
        persist(args.output / "manifest.json", manifest)

        raw_path = args.output / "raw_responses.jsonl"
        with raw_path.open("w", encoding="utf-8") as raw_file:
            for request in requests:
                started = time.monotonic()
                result = llm.chat(
                    [request["messages"]],
                    SamplingParams(
                        temperature=0.0, max_tokens=128, seed=1847,
                        structured_outputs=StructuredOutputsParams(json=request["schema"]),
                    ),
                    chat_template_kwargs={"enable_thinking": False},
                    use_tqdm=False,
                )[0].outputs[0]
                record = {
                    "case_id": request["case_id"], "panel": request["panel"],
                    "text": result.text, "finish_reason": result.finish_reason,
                    "token_ids": list(result.token_ids),
                    "generation_seconds": time.monotonic() - started,
                }
                raw_file.write(json.dumps(record, sort_keys=True) + "\n")
                raw_file.flush()
                os.fsync(raw_file.fileno())
                manifest["responses_persisted"] = manifest.get("responses_persisted", 0) + 1
                persist(args.output / "manifest.json", manifest)

        manifest["raw_responses_sha256"] = sha256(raw_path)
        manifest["status"] = "RAW_OUTPUT_COMPLETE_UNSCORED"
    except Exception as exc:
        manifest["status"] = "RUNTIME_FAILURE_RAW_PRESERVED"
        manifest["error"] = f"{type(exc).__name__}: {exc}"
        raise
    finally:
        manifest["ended_utc"] = datetime.now(timezone.utc).isoformat()
        persist(args.output / "manifest.json", manifest)


if __name__ == "__main__":
    main()
