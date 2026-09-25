"""Verify pinned official benchmark archives and write an acquisition receipt."""

from __future__ import annotations

import argparse
import hashlib
import json
import urllib.request
import zipfile
from datetime import datetime, timezone
from io import BytesIO
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PUBLIC_RAG = ROOT / "experiments" / "public_rag"
INVENTORY = PUBLIC_RAG / "public_benchmark_inventory.json"
RECEIPT = PUBLIC_RAG / "benchmark_acquisition_receipt.json"


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def inner_member(archive: zipfile.ZipFile, suffix: str) -> bytes:
    matches = [name for name in archive.namelist() if name.endswith(suffix)]
    if len(matches) != 1:
        raise ValueError(f"Expected exactly one {suffix!r} member, got {matches!r}")
    return archive.read(matches[0])


def verify(verify_remote: bool) -> dict:
    inventory = json.loads(INVENTORY.read_text())
    records = []
    for item in inventory["benchmarks"]:
        archive_path = PUBLIC_RAG / item["archive_path"]
        local_bytes = archive_path.read_bytes()
        if len(local_bytes) != item["archive_bytes"] or sha256(local_bytes) != item["archive_sha256"]:
            raise ValueError(f"Local archive does not match pin: {item['id']}")

        source_url = (
            item["official_repository"].replace("https://github.com/", "https://codeload.github.com/")
            + "/zip/"
            + item["repository_revision"]
        )
        remote_observed_at = None
        if verify_remote:
            request = urllib.request.Request(source_url, headers={"User-Agent": "RegModelTrace-A0"})
            with urllib.request.urlopen(request, timeout=60) as response:
                remote_bytes = response.read()
            remote_observed_at = datetime.now(timezone.utc).isoformat(timespec="seconds")
            if remote_bytes != local_bytes:
                raise ValueError(f"Official remote bytes differ from local archive: {item['id']}")

        with zipfile.ZipFile(BytesIO(local_bytes)) as archive:
            if archive.testzip() is not None:
                raise ValueError(f"Archive integrity failed: {item['id']}")
            if item["id"] == "TimelyQABench":
                inner = {"datasets.zip": sha256(inner_member(archive, "datasets.zip"))}
                expected = {"datasets.zip": item["inner_dataset_sha256"]}
            elif item["id"] == "VersionQA":
                inner = {"data/test/evaluation_set.csv": sha256(inner_member(archive, "data/test/evaluation_set.csv"))}
                expected = {"data/test/evaluation_set.csv": item["evaluation_file_sha256"]}
            else:
                inner = {"datasets/en.jsonl": sha256(inner_member(archive, "datasets/en.jsonl"))}
                expected = {"datasets/en.jsonl": item["english_dataset_sha256"]}
            if inner != expected:
                raise ValueError(f"Inner data hash differs from inventory: {item['id']}")

        records.append(
            {
                "benchmark": item["id"],
                "source_url": source_url,
                "repository_commit": item["repository_revision"],
                "local_archive_path": str(archive_path),
                "archive_bytes": len(local_bytes),
                "archive_sha256": sha256(local_bytes),
                "inner_data_sha256": inner,
                "remote_retrieved_at_utc": remote_observed_at,
                "verification_status": "PASS_REMOTE_AND_LOCAL" if verify_remote else "PASS_LOCAL_ONLY",
            }
        )

    return {
        "receipt_version": "track-a-a0-2026-09-25",
        "verified_at_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "verification_command": "python scripts/public_rag/verify_benchmark_acquisition.py --verify-remote",
        "original_acquisition_timestamp_status": "NOT_CAPTURED_IN_INITIAL_A0_DOWNLOAD; remote_retrieved_at_utc records this independent re-fetch",
        "raw_archives_in_git_or_handoff_zip": False,
        "records": records,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--verify-remote", action="store_true")
    args = parser.parse_args()
    receipt = verify(args.verify_remote)
    RECEIPT.write_text(json.dumps(receipt, indent=2, ensure_ascii=False) + "\n")
    print(f"Verified {len(receipt['records'])} official archives; receipt: {RECEIPT}")


if __name__ == "__main__":
    main()
