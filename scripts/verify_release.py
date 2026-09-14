#!/usr/bin/env python3
"""Offline structural checks for the compact GitHub release."""

from __future__ import annotations

import json
import hashlib
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    required = [
        "README.md",
        "LICENSE",
        "pyproject.toml",
        "demo/index.html",
        "demo/data/demo.json",
        "docs/architecture.md",
        "docs/final-metrics.md",
        "docs/limitations.md",
        "artifacts/review-1/closure_receipt.json",
        "artifacts/test-e/project_closure_receipt.json",
        "artifacts/scale-1/systems_lane_closure.json",
        "artifacts/release_manifest.json",
        "regmodeltrace/service.py",
        "regmodeltrace/tests/test_system_v1.py",
    ]
    missing = [name for name in required if not (ROOT / name).is_file()]

    forbidden = [
        ".soilwater-revision-20260914",
        "outputs",
        "reviews",
        "tmp",
        "regmodeltrace/data",
        "regmodeltrace-ui",
    ]
    present_forbidden = [name for name in forbidden if (ROOT / name).exists()]

    nested_git = [str(path.relative_to(ROOT)) for path in ROOT.rglob(".git") if path != ROOT / ".git"]
    oversized = [
        {"path": str(path.relative_to(ROOT)), "bytes": path.stat().st_size}
        for path in ROOT.rglob("*")
        if path.is_file() and ".git" not in path.parts and path.stat().st_size > 25 * 2**20
    ]

    for path in ROOT.rglob("*.json"):
        if ".git" not in path.parts:
            json.loads(path.read_text())

    readme = (ROOT / "README.md").read_text()
    required_boundaries = [
        "PARTIALLY_ALIGNED",
        "CONFLICT",
        "FAIL_TABLE_IDENTITY",
        "PASS_WITH_GENERATIVE_NONDETERMINISM_LIMITATION",
        "cannot replay the historical GPU runs",
    ]
    missing_boundaries = [value for value in required_boundaries if value not in readme]

    local_links = re.findall(r"\[[^\]]+\]\((?!https?://|#)([^)]+)\)", readme)
    missing_links = [link for link in local_links if not (ROOT / link).exists()]

    secret_patterns = {
        "github_token": re.compile(r"gh[oprsu]_[A-Za-z0-9]{20,}"),
        "private_key": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
        "aws_access_key": re.compile(r"AKIA[0-9A-Z]{16}"),
    }
    secret_hits = []
    for path in ROOT.rglob("*"):
        if not path.is_file() or ".git" in path.parts or path.suffix.lower() in {".png", ".jpg", ".ico"}:
            continue
        try:
            text = path.read_text(errors="ignore")
        except OSError:
            continue
        for name, pattern in secret_patterns.items():
            if pattern.search(text):
                secret_hits.append({"path": str(path.relative_to(ROOT)), "pattern": name})

    release_manifest = json.loads((ROOT / "artifacts/release_manifest.json").read_text()) if not missing else {"files": {}}
    manifest_mismatches = []
    for relative, expected in release_manifest.get("files", {}).items():
        path = ROOT / relative
        actual = hashlib.sha256(path.read_bytes()).hexdigest() if path.is_file() else None
        if actual != expected:
            manifest_mismatches.append(relative)

    checks = {
        "required_files": not missing,
        "forbidden_paths_absent": not present_forbidden,
        "no_nested_git": not nested_git,
        "no_file_over_25_mib": not oversized,
        "claim_boundaries_present": not missing_boundaries,
        "readme_local_links_resolve": not missing_links,
        "release_manifest_hashes": not manifest_mismatches,
        "basic_secret_scan": not secret_hits,
    }
    detail = {
        "missing": missing,
        "present_forbidden": present_forbidden,
        "nested_git": nested_git,
        "oversized": oversized,
        "missing_boundaries": missing_boundaries,
        "missing_links": missing_links,
        "manifest_mismatches": manifest_mismatches,
        "secret_hits": secret_hits,
    }
    status = "PASS" if all(checks.values()) else "FAIL"
    print(json.dumps({"status": status, "checks": checks, "detail": detail}, indent=2))
    raise SystemExit(0 if status == "PASS" else 1)


if __name__ == "__main__":
    main()
