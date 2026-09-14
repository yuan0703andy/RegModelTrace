"""Direct and Ray execution of frozen SCALE-1 M3.6 microbatches."""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import importlib.metadata
import json
import os
from pathlib import Path
import platform
import socket
import subprocess
import sys
import time
import uuid
from collections import Counter


def canonical(x):
    return json.dumps(x, sort_keys=True, ensure_ascii=False, separators=(",", ":"))


def sha(x):
    return hashlib.sha256(x.encode() if isinstance(x, str) else x).hexdigest()


def now():
    return dt.datetime.now(dt.timezone.utc).isoformat()


def load(path):
    return json.loads(Path(path).read_text())


def jsonl(path):
    return [json.loads(s) for s in Path(path).read_text().splitlines()]


def durable_write(path, obj):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_name(path.name + ".tmp-" + uuid.uuid4().hex)
    with temp.open("w") as f:
        f.write(json.dumps(obj, indent=2, ensure_ascii=False) + "\n")
        f.flush()
        os.fsync(f.fileno())
    os.replace(temp, path)


def durable_write_new(path, obj):
    path = Path(path)
    if path.exists():
        raise FileExistsError("APPEND_ONLY_ATTEMPT_COLLISION:" + str(path))
    durable_write(path, obj)


def append(path, obj):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a") as f:
        f.write(canonical(obj) + "\n")
        f.flush()
        os.fsync(f.fileno())


def parse_label(text, ontology):
    def unique(pairs):
        out = {}
        for key, value in pairs:
            if key in out:
                raise ValueError("duplicate")
            out[key] = value
        return out
    try:
        value = json.loads(text, object_pairs_hook=unique)
    except (ValueError, TypeError):
        return None, "INVALID_JSON"
    if not isinstance(value, dict) or set(value) != {"evidence_type"}:
        return None, "INVALID_KEYS"
    if not isinstance(value["evidence_type"], str) or value["evidence_type"] not in ontology:
        return None, "INVALID_LABEL"
    return value["evidence_type"], "PASS"


def install_read_guard():
    forbidden = ("/data/gold/", "/data/evaluation/", "/scale-1-validation-d/", "/scale-1-sealed-test-e/")
    def guard(event, args):
        if event == "open" and args and isinstance(args[0], (str, bytes, os.PathLike)):
            path = os.path.abspath(os.fsdecode(args[0])).replace("\\", "/")
            if any(part in path for part in forbidden):
                raise PermissionError("SCALE1_WORKER_FORBIDDEN_READ:" + path)
    sys.addaudithook(guard)


def gpu_identity():
    visible = os.getenv("CUDA_VISIBLE_DEVICES")
    try:
        lines = subprocess.check_output(
            ["nvidia-smi", "--query-gpu=index,name,uuid,memory.total", "--format=csv,noheader,nounits"],
            text=True,
        ).strip().splitlines()
        rows = []
        for line in lines:
            index, name, gpu_uuid, memory = [x.strip() for x in line.split(",", 3)]
            rows.append({"physical_index": index, "name": name, "uuid": gpu_uuid,
                         "memory_mib": int(memory)})
        requested = set((visible or "").split(",")) - {""}
        selected = [x for x in rows if x["physical_index"] in requested or x["uuid"] in requested]
        detail = selected if selected else rows
    except Exception as exc:
        detail = [{"error": "UNAVAILABLE:" + type(exc).__name__}]
    try:
        import torch
        logical = [{"logical_index": i, "name": torch.cuda.get_device_name(i),
                    "total_memory_bytes": torch.cuda.get_device_properties(i).total_memory}
                   for i in range(torch.cuda.device_count())]
    except Exception as exc:
        logical = [{"error": "UNAVAILABLE:" + type(exc).__name__}]
    return {"cuda_visible_devices": visible, "physical_devices": detail, "logical_devices": logical}


class VLLMReplica:
    def __init__(self, config, prompt, output_root, backend):
        os.environ["VLLM_ENABLE_V1_MULTIPROCESSING"] = "0"
        self.config = config
        self.prompt = prompt
        self.output_root = Path(output_root)
        self.backend = backend
        install_read_guard()
        from vllm import LLM, SamplingParams
        self.SamplingParams = SamplingParams
        local = config["local"]
        started = time.monotonic()
        self.llm = LLM(
            model=local["model_path"], tokenizer=local["model_path"], dtype=local["dtype"],
            max_model_len=local["max_model_len"], gpu_memory_utilization=local["gpu_memory_utilization"],
            tensor_parallel_size=1, seed=local["seed"], enforce_eager=True,
            max_num_seqs=local["max_num_seqs"], enable_prefix_caching=False, disable_log_stats=True,
        )
        self.tokenizer = self.llm.get_tokenizer()
        self.system = prompt + "\nAllowed evidence types and definitions:\n" + canonical(config["ontology"])
        self.actor_id = self._actor_id()
        self.initialized_at = now()
        self.initialization_seconds = time.monotonic() - started
        durable_write(self.output_root / "actor_initializations" / (self.actor_id + ".json"), {
            "actor_id": self.actor_id, "backend": backend, "hostname": socket.gethostname(),
            "pid": os.getpid(), "gpu": gpu_identity(), "initialized_at_utc": self.initialized_at,
            "initialization_seconds": self.initialization_seconds,
        })

    def _actor_id(self):
        if self.backend == "ray":
            try:
                import ray
                return str(ray.get_runtime_context().get_actor_id())
            except Exception:
                pass
        return "direct-" + socket.gethostname() + "-" + str(os.getpid())

    def run(self, microbatch, request_map):
        attempt_id = uuid.uuid4().hex
        started_at = now()
        started = time.monotonic()
        members = [request_map[x] for x in microbatch["semantic_request_ids"]]
        messages = []
        actual_tokens = []
        for item, expected in zip(members, microbatch["members"]):
            user = canonical({k: item[k] for k in ["document", "focal_assertion", "context_before", "context_after"]})
            request = [{"role": "system", "content": self.system}, {"role": "user", "content": user}]
            rendered = self.tokenizer.apply_chat_template(request, tokenize=False, add_generation_prompt=True)
            tokens = self.tokenizer.encode(rendered, add_special_tokens=False)
            if tokens != expected["prompt_token_ids"]:
                raise ValueError("PROMPT_TOKEN_ID_MISMATCH:" + item["semantic_request_id"])
            messages.append(request)
            actual_tokens.append(tokens)
        sampling = self.SamplingParams(
            temperature=self.config["temperature"], seed=self.config["local"]["seed"],
            max_tokens=self.config["max_output_tokens"],
        )
        outputs = self.llm.chat(messages, sampling, use_tqdm=False)
        raw = []
        for index, (item, expected, generated, tokens) in enumerate(zip(members, microbatch["members"], outputs, actual_tokens)):
            choice = generated.outputs[0]
            raw.append({
                "position_in_microbatch": index,
                "semantic_request_id": item["semantic_request_id"],
                "source_request_sha256": expected["source_request_sha256"],
                "payload_sha256": expected["payload_sha256"],
                "prompt_token_ids": list(generated.prompt_token_ids),
                "expected_prompt_token_ids": tokens,
                "engine_request_id": generated.request_id,
                "text": choice.text,
                "finish_reason": choice.finish_reason,
                "output_token_ids": list(choice.token_ids),
            })
        shard = {
            "version": "scale-1-raw-attempt-1.0", "attempt_id": attempt_id,
            "microbatch_id": microbatch["microbatch_id"], "microbatch_index": microbatch["microbatch_index"],
            "backend": self.backend, "actor_id": self.actor_id, "hostname": socket.gethostname(),
            "pid": os.getpid(), "gpu": gpu_identity(), "started_at_utc": started_at,
            "completed_at_utc": now(), "elapsed_seconds": time.monotonic() - started, "responses": raw,
        }
        path = self.output_root / "attempts" / f'{microbatch["microbatch_id"]}-{attempt_id}.json'
        durable_write_new(path, shard)
        return {"microbatch_id": microbatch["microbatch_id"], "attempt_id": attempt_id,
                "shard_path": str(path), "shard_sha256": sha(path.read_bytes()),
                "actor_id": self.actor_id, "gpu": shard["gpu"], "elapsed_seconds": shard["elapsed_seconds"]}


class RayBatchActor:
    def __init__(self, config_json, prompt, output_root, microbatch_json, requests_json):
        import numpy as np
        self.np = np
        config = json.loads(config_json)
        self.microbatches = {x["microbatch_id"]: x for x in json.loads(microbatch_json)["batches"]}
        requests = [json.loads(x) for x in requests_json.splitlines()]
        self.requests = {x["semantic_request_id"]: x for x in requests}
        self.replica = VLLMReplica(config, prompt, output_root, "ray")

    def __call__(self, batch):
        results = []
        for microbatch_id in batch["microbatch_id"]:
            if isinstance(microbatch_id, bytes):
                microbatch_id = microbatch_id.decode()
            results.append(self.replica.run(self.microbatches[str(microbatch_id)], self.requests))
        return {
            "microbatch_id": self.np.array([x["microbatch_id"] for x in results]),
            "attempt_id": self.np.array([x["attempt_id"] for x in results]),
            "shard_path": self.np.array([x["shard_path"] for x in results]),
            "shard_sha256": self.np.array([x["shard_sha256"] for x in results]),
            "actor_id": self.np.array([x["actor_id"] for x in results]),
            "gpu_json": self.np.array([canonical(x["gpu"]) for x in results]),
            "elapsed_seconds": self.np.array([x["elapsed_seconds"] for x in results]),
        }


def validate_inputs(args):
    config = load(args.config)
    execution = load(args.execution)
    micro = load(args.microbatches)
    if not (sha(args.requests.read_bytes()) == execution["request_manifest_sha256"] == micro["request_manifest_sha256"]):
        raise ValueError("REQUEST_MANIFEST_HASH_MISMATCH")
    if sha(args.config.read_bytes()) != micro["m3_config_sha256"]:
        raise ValueError("M3_CONFIG_HASH_MISMATCH")
    if sha(args.prompt.read_bytes()) != micro["prompt_sha256"]:
        raise ValueError("PROMPT_HASH_MISMATCH")
    if sha(args.execution.read_bytes()) != micro["execution_config_sha256"]:
        raise ValueError("EXECUTION_CONFIG_HASH_MISMATCH")
    if sha(args.environment_lock.read_bytes()) != execution["environment_lock_sha256"]:
        raise ValueError("ENVIRONMENT_LOCK_HASH_MISMATCH")
    if sha(args.checkpoint1.read_bytes()) != execution["checkpoint1_verification_sha256"]:
        raise ValueError("CHECKPOINT1_VERIFICATION_HASH_MISMATCH")
    if sha(args.config.read_bytes()) != execution["m3_config_sha256"]:
        raise ValueError("FROZEN_M3_CONFIG_HASH_MISMATCH")
    if sha(args.prompt.read_bytes()) != execution["prompt_sha256"]:
        raise ValueError("FROZEN_PROMPT_HASH_MISMATCH")
    requests = jsonl(args.requests)
    if len(requests) != micro["request_count"] or len(micro["batches"]) != execution["microbatch_count"]:
        raise ValueError("INVENTORY_MISMATCH")
    if {x["partition"] for x in requests} - set(execution["allowed_partitions"]):
        raise ValueError("PROTECTED_PARTITION_IN_WORKLOAD")
    return config, execution, micro, requests


def reduce_attempts(output, micro, requests, config):
    expected = {x["semantic_request_id"]: x for x in requests}
    member = {m["semantic_request_id"]: (batch, m) for batch in micro["batches"] for m in batch["members"]}
    attempts = sorted((output / "attempts").glob("*.json"))
    by_request = {}
    for path in attempts:
        shard = load(path)
        for raw in shard["responses"]:
            rid = raw["semantic_request_id"]
            if rid not in expected or rid not in member:
                raise ValueError("UNKNOWN_REQUEST_IN_ATTEMPT")
            batch, plan = member[rid]
            if raw["source_request_sha256"] != plan["source_request_sha256"] or raw["payload_sha256"] != plan["payload_sha256"]:
                raise ValueError("SOURCE_BINDING_MISMATCH:" + rid)
            if raw["prompt_token_ids"] != plan["prompt_token_ids"] or raw["expected_prompt_token_ids"] != plan["prompt_token_ids"]:
                raise ValueError("PROMPT_BINDING_MISMATCH:" + rid)
            by_request.setdefault(rid, []).append((shard, raw, path))
    records = []
    conflicts = []
    for request_index, item in enumerate(requests):
        rid = item["semantic_request_id"]
        found = by_request.get(rid, [])
        if not found:
            record = {"semantic_request_id": rid, "request_index": request_index,
                      "terminal_disposition": "INFRASTRUCTURE_FAILURE", "reason": "NO_DURABLE_RAW_ATTEMPT"}
        else:
            signatures = {canonical({k: raw[k] for k in ["text", "finish_reason", "output_token_ids", "prompt_token_ids"]}) for _, raw, _ in found}
            if len(signatures) != 1:
                conflicts.append(rid)
                record = {"semantic_request_id": rid, "request_index": request_index,
                          "terminal_disposition": "INFRASTRUCTURE_FAILURE", "reason": "DUPLICATE_RESULT_CONFLICT",
                          "attempt_ids": [s["attempt_id"] for s, _, _ in found]}
            else:
                shard, raw, path = found[0]
                label, parse_status = parse_label(raw["text"], config["ontology"])
                disposition = "VALID_OUTPUT" if parse_status == "PASS" and raw["finish_reason"] != "length" else "INVALID_MODEL_OUTPUT"
                if raw["finish_reason"] == "length":
                    parse_status = "OUTPUT_TOKEN_LIMIT"
                    label = None
                record = {
                    "semantic_request_id": rid, "assertion_id": item["assertion_id"], "request_index": request_index,
                    "source_request_sha256": member[rid][1]["source_request_sha256"],
                    "source_binding_sha256": sha(canonical({k: item[k] for k in ["unit_id", "candidate_ids", "pages", "source_spans"]})),
                    "microbatch_id": member[rid][0]["microbatch_id"], "terminal_disposition": disposition,
                    "parse_status": parse_status, "normalized_label": label, "raw_model_text": raw["text"],
                    "output_token_ids": raw["output_token_ids"], "prompt_token_ids_sha256": sha(canonical(raw["prompt_token_ids"])),
                    "actor_id": shard["actor_id"], "gpu": shard["gpu"], "attempt_id": shard["attempt_id"],
                    "raw_attempt_path": str(path), "raw_attempt_sha256": sha(path.read_bytes()),
                }
        canonical_path = output / "canonical" / (rid + ".json")
        if canonical_path.exists():
            prior = load(canonical_path)
            if canonical(prior) != canonical(record):
                raise ValueError("STALE_OR_CONFLICTING_CANONICAL_RESULT:" + rid)
        else:
            durable_write(canonical_path, record)
            append(output / "canonical_journal.jsonl", record)
        records.append(record)
    durable_write(output / "results.json", records)
    return records, conflicts, attempts


def recoverable_microbatch_ids(output, micro):
    """Return batches with a complete durable raw shard from an earlier driver attempt."""
    expected = {x["microbatch_id"]: set(x["semantic_request_ids"]) for x in micro["batches"]}
    recovered = set()
    for path in sorted((output / "attempts").glob("*.json")):
        shard = load(path)
        batch_id = shard.get("microbatch_id")
        response_ids = {x.get("semantic_request_id") for x in shard.get("responses", [])}
        if batch_id in expected and response_ids == expected[batch_id]:
            recovered.add(batch_id)
    return recovered


def installed_versions(names):
    out = {}
    for name in names:
        try:
            out[name] = importlib.metadata.version(name)
        except importlib.metadata.PackageNotFoundError:
            out[name] = "NOT_INSTALLED"
    return out


def main():
    p = argparse.ArgumentParser()
    for name in ["requests", "microbatches", "config", "prompt", "execution", "environment-lock", "checkpoint1", "output"]:
        p.add_argument("--" + name, type=Path, required=True)
    p.add_argument("--backend", choices=["direct", "ray"], required=True)
    p.add_argument("--replicas", type=int, required=True)
    p.add_argument("--resume", action="store_true")
    a = p.parse_args()
    config, execution, micro, requests = validate_inputs(a)
    if a.backend == "direct" and a.replicas != 1:
        raise ValueError("DIRECT_REQUIRES_ONE_REPLICA")
    if a.output.exists() and not a.resume:
        raise ValueError("OUTPUT_EXISTS_USE_EXPLICIT_RESUME")
    a.output.mkdir(parents=True, exist_ok=True)
    started = now()
    start = time.monotonic()
    request_map = {x["semantic_request_id"]: x for x in requests}
    committed = {p.stem for p in (a.output / "canonical").glob("*.json")}
    recoverable = recoverable_microbatch_ids(a.output, micro)
    pending = [b for b in micro["batches"]
               if not set(b["semantic_request_ids"]) <= committed and b["microbatch_id"] not in recoverable]
    if any(set(b["semantic_request_ids"]) & committed and not set(b["semantic_request_ids"]) <= committed for b in micro["batches"]):
        raise ValueError("PARTIAL_MICROBATCH_COMMIT_REQUIRES_MANUAL_AUDIT")
    run = {
        "version": "scale-1-batch-run-1.0", "status": "RUNNING", "backend": a.backend,
        "replicas": a.replicas, "started_at_utc": started, "hostname": socket.gethostname(),
        "python": platform.python_version(), "input_sha256": {name: sha(getattr(a, name).read_bytes()) for name in ["requests", "microbatches", "config", "prompt", "execution", "environment_lock", "checkpoint1"]},
        "request_count": len(requests), "microbatch_count": len(micro["batches"]),
        "pending_microbatches": len(pending), "resume": a.resume, "semantic_retries": 0,
        "recovered_raw_microbatches": sorted(recoverable),
        "microbatch_order": [x["microbatch_id"] for x in micro["batches"]],
        "package_versions": installed_versions(load(a.environment_lock)["packages"]),
        "slurm_job_id": os.getenv("SLURM_JOB_ID"),
    }
    durable_write(a.output / "run_manifest.json", run)
    summaries = []
    if pending:
        if a.backend == "direct":
            actor = VLLMReplica(config, a.prompt.read_text(), str(a.output), "direct")
            for batch in pending:
                last = None
                for attempt in range(execution["infrastructure_retries_per_microbatch"] + 1):
                    try:
                        summaries.append(actor.run(batch, request_map)); last = None; break
                    except Exception as exc:
                        last = exc
                        append(a.output / "infrastructure_failures.jsonl", {"microbatch_id": batch["microbatch_id"], "attempt": attempt + 1, "error_type": type(exc).__name__, "message": str(exc), "at_utc": now()})
                if last is not None:
                    continue
        else:
            import ray
            import ray.data
            scratch = os.getenv("RAY_TMPDIR") or os.getenv("SLURM_TMPDIR")
            if not scratch:
                raise RuntimeError("RAY_REQUIRES_NODE_LOCAL_RAY_TMPDIR")
            Path(scratch).mkdir(parents=True, exist_ok=True)
            allocated_cpus = int(os.getenv("SLURM_CPUS_PER_TASK", "1"))
            visible_gpus = [x for x in (os.getenv("CUDA_VISIBLE_DEVICES") or "").split(",") if x]
            if len(visible_gpus) < a.replicas:
                raise RuntimeError(f"INSUFFICIENT_SLURM_GPUS:{len(visible_gpus)}<{a.replicas}")
            run["ray_resources_registered"] = {
                "num_cpus": allocated_cpus, "num_gpus": len(visible_gpus),
                "cuda_visible_devices": visible_gpus,
            }
            durable_write(a.output / "run_manifest.json", run)
            ray.init(_temp_dir=scratch, include_dashboard=False, log_to_driver=True,
                     num_cpus=allocated_cpus, num_gpus=len(visible_gpus))
            rows = [{"microbatch_id": b["microbatch_id"]} for b in pending]
            dataset = ray.data.from_items(rows).repartition(len(rows))
            result = dataset.map_batches(
                RayBatchActor, batch_size=1, batch_format="numpy",
                compute=ray.data.ActorPoolStrategy(size=a.replicas), num_gpus=1,
                fn_constructor_kwargs={"config_json": canonical(config), "prompt": a.prompt.read_text(),
                    "output_root": str(a.output), "microbatch_json": canonical(micro),
                    "requests_json": a.requests.read_text()},
                max_restarts=1, max_task_retries=execution["infrastructure_retries_per_microbatch"],
            )
            summaries = result.take_all()
            ray.shutdown()
    durable_write(a.output / "dispatch_results.json", summaries)
    records, conflicts, attempts = reduce_attempts(a.output, micro, requests, config)
    terminal = Counter(r["terminal_disposition"] for r in records)
    actors = sorted({r.get("actor_id") for r in records if r.get("actor_id")})
    gpus = sorted({canonical(r.get("gpu")) for r in records if r.get("gpu")})
    attempt_counts = Counter()
    for path in attempts:
        for raw in load(path)["responses"]:
            attempt_counts[raw["semantic_request_id"]] += 1
    equivalent_duplicates = sum(max(0, count - 1) for count in attempt_counts.values())
    run.update({
        "status": "COMPLETE" if len(records) == len(requests) and not conflicts and terminal.get("INFRASTRUCTURE_FAILURE", 0) == 0 else "COMPLETE_WITH_FAILURES",
        "completed_at_utc": now(), "elapsed_seconds": time.monotonic() - start,
        "terminal_dispositions": dict(terminal), "canonical_records": len(records),
        "raw_attempt_shards": len(attempts), "duplicate_conflicts": conflicts,
        "duplicate_equivalent_attempts": equivalent_duplicates,
        "actor_ids": actors, "actor_count": len(actors), "gpu_identities": [json.loads(x) for x in gpus],
        "results_sha256": sha((a.output / "results.json").read_bytes()),
        "canonical_journal_sha256": sha((a.output / "canonical_journal.jsonl").read_bytes()),
        "dispatch_results_sha256": sha((a.output / "dispatch_results.json").read_bytes()),
        "model_id": config["local"]["model"], "model_revision": config["local"]["model_revision"],
        "decoding": {"temperature": config["temperature"], "seed": config["local"]["seed"], "max_output_tokens": config["max_output_tokens"]},
        "truth_reads": 0, "protected_corpus_reads": 0,
    })
    durable_write(a.output / "run_manifest.json", run)
    print(json.dumps({k: run[k] for k in ["status", "backend", "replicas", "elapsed_seconds", "terminal_dispositions", "actor_count", "gpu_identities"]}, indent=2))


if __name__ == "__main__":
    main()
