"""Fetch and verify the pinned Qwen3.8 checkpoint on a DCC compute node."""

from __future__ import annotations

import hashlib
import json
import os
import socket
from datetime import datetime, timezone
from pathlib import Path

from huggingface_hub import HfApi, snapshot_download

MODEL = "Qwen/Qwen3.8-27B-FP8"
REVISION = "017b9c7af6b5689d5dd426a76e0bc077eb5ca20a"


def persist(path: Path, data: dict) -> None:
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(8 * 1024 * 1024), b""):
            value.update(chunk)
    return value.hexdigest()


def main() -> None:
    hostname = socket.gethostname()
    if "login" in hostname.lower():
        raise RuntimeError("Model download is forbidden on the DCC login node")
    receipt_dir = Path(os.environ["RMT_QWEN38_RECEIPT_DIR"])
    receipt_dir.mkdir(parents=True, exist_ok=False)
    receipt = {
        "model": MODEL,
        "revision": REVISION,
        "hostname": hostname,
        "slurm_job_id": os.environ.get("SLURM_JOB_ID"),
        "started_utc": datetime.now(timezone.utc).isoformat(),
        "status": "STARTED",
    }
    persist(receipt_dir / "download_receipt.json", receipt)
    try:
        info = HfApi().model_info(MODEL, revision=REVISION, files_metadata=True)
        if info.sha != REVISION:
            raise ValueError(f"Hub resolved unexpected revision: {info.sha}")
        snapshot = Path(snapshot_download(
            repo_id=MODEL, revision=REVISION,
            cache_dir=os.environ["RMT_QWEN38_CACHE_DIR"], max_workers=4,
        ))
        if snapshot.name != REVISION:
            raise ValueError("Downloaded snapshot does not have the pinned revision")
        files = []
        for sibling in info.siblings:
            path = snapshot / sibling.rfilename
            if not path.is_file():
                raise FileNotFoundError(f"Missing Hub file: {sibling.rfilename}")
            actual_size = path.stat().st_size
            if sibling.size is not None and actual_size != sibling.size:
                raise ValueError(f"Size mismatch: {sibling.rfilename}")
            actual_sha = digest(path)
            expected_sha = sibling.lfs.get("sha256") if sibling.lfs else None
            if expected_sha and actual_sha != expected_sha:
                raise ValueError(f"Hash mismatch: {sibling.rfilename}")
            files.append({"path": sibling.rfilename, "size": actual_size,
                          "sha256": actual_sha, "hub_sha256": expected_sha})
        persist(receipt_dir / "files.json", {"files": files})
        receipt.update({
            "status": "DOWNLOAD_VERIFIED", "snapshot": str(snapshot),
            "files": len(files),
            "safetensors_files": sum(x["path"].endswith(".safetensors") for x in files),
            "total_bytes": sum(x["size"] for x in files),
        })
    except Exception as exc:
        receipt["status"] = "DOWNLOAD_FAILED"
        receipt["error"] = f"{type(exc).__name__}: {exc}"
        raise
    finally:
        receipt["ended_utc"] = datetime.now(timezone.utc).isoformat()
        persist(receipt_dir / "download_receipt.json", receipt)


if __name__ == "__main__":
    main()
