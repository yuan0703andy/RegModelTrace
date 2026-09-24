"""Score preserved Qwen3.8 synthetic raw responses after inference has ended."""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path

from qwen38_boundary_diagnostic import LABELS, load_cases


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def score(cases_path: Path, oracle_path: Path, run_dir: Path) -> dict:
    cases = load_cases(cases_path)
    oracle = json.loads(oracle_path.read_text(encoding="utf-8"))
    expected = oracle["expected"]
    ids = [case["case_id"] for case in cases]
    if oracle["version"] != "qwen38-synthetic-boundary-1" or set(expected) != set(ids):
        raise ValueError("Oracle IDs or version do not match the frozen cases")
    manifest = json.loads((run_dir / "manifest.json").read_text(encoding="utf-8"))
    raw_path = run_dir / "raw_responses.jsonl"
    if manifest["status"] != "RAW_OUTPUT_COMPLETE_UNSCORED":
        raise ValueError("Refusing to score an incomplete or failed inference run")
    if manifest["cases_sha256"] != sha256(cases_path):
        raise ValueError("Case bytes changed after inference")
    if manifest["raw_responses_sha256"] != sha256(raw_path):
        raise ValueError("Raw response hash mismatch")
    rows = [json.loads(line) for line in raw_path.read_text(encoding="utf-8").splitlines()]
    if [row["case_id"] for row in rows] != ids:
        raise ValueError("Missing, duplicate, or reordered raw responses")
    results = []
    for case, row in zip(cases, rows):
        if row["panel"] != case["panel"]:
            raise ValueError("Panel mismatch")
        parsed = None
        try:
            parsed = json.loads(row["text"])
        except (ValueError, TypeError):
            pass
        valid = (
            isinstance(parsed, dict)
            and set(parsed) == {"evidence_type"}
            and parsed["evidence_type"] in LABELS[case["panel"]]
            and row["finish_reason"] == "stop"
        )
        observed = parsed["evidence_type"] if valid else None
        results.append({
            "case_id": case["case_id"], "panel": case["panel"],
            "source": case["source"], "expected": expected[case["case_id"]],
            "observed": observed, "structurally_valid": valid,
            "correct": valid and observed == expected[case["case_id"]],
        })
    by_panel = {}
    for panel in LABELS:
        subset = [row for row in results if row["panel"] == panel]
        by_panel[panel] = {
            "correct": sum(row["correct"] for row in subset),
            "valid": sum(row["structurally_valid"] for row in subset),
            "total": len(subset),
            "errors_by_expected": dict(Counter(
                row["expected"] for row in subset if not row["correct"]
            )),
        }
    return {
        "kind": "SYNTHETIC_BOUNDARY_DIAGNOSTIC_ONLY",
        "model": manifest["model"], "revision": manifest["revision"],
        "slurm_job_id": manifest["slurm_job_id"],
        "cases_sha256": sha256(cases_path), "oracle_sha256": sha256(oracle_path),
        "raw_responses_sha256": sha256(raw_path),
        "by_panel": by_panel,
        "original_case_repeat_identical": results[0]["observed"] == results[1]["observed"],
        "results": results,
        "natural_domain_accuracy": "NOT_ASSESSED",
        "active_default_change": "NONE",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cases", type=Path, required=True)
    parser.add_argument("--oracle", type=Path, required=True)
    parser.add_argument("--run-dir", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = score(args.cases, args.oracle, args.run_dir)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result["by_panel"], sort_keys=True))


if __name__ == "__main__":
    main()
