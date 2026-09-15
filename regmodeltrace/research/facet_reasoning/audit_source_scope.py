"""Audit FT-1 input lineage without reading alignment truth or predictions.

Verdicts concern the CURRENT candidate-pack version. Separately, a KEEP source
seed identifies retained raw PDFs and a pre-adjudication regulator lock; it does
not approve existing fixture memberships or establish blinded human truth.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path
from typing import Any


FIXTURE_BY_CORPUS = {
    "impact-forecasting-2023": "alignment-impact-2023-v2-2-1.0",
    "verisk-2023-validation-d": "alignment-verisk-2023-v2-2-1.0",
    "rms-ara-2019-development": "alignment-v2-2-pilot-1.0",
    "kcc-2023-exposed-test-e": "alignment-kcc-2023-test-e-v2-2-1.0",
}
FORBIDDEN_NAMES = {
    "comparison_truth.json", "truth.json", "human_adjudication.json",
    "comparison_records.json", "results.json", "scores.json",
    "condition_a_saved_predictions.json", "facet_case_inventory.json",
}


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_json(path: Path, reads: list[dict[str, str]]) -> Any:
    if path.name in FORBIDDEN_NAMES:
        raise PermissionError("Eligibility audit cannot read truth or model outputs")
    reads.append({"file": path.name, "sha256": sha(path)})
    return json.loads(path.read_text(encoding="utf-8"))


def inspect_cases(
    pilot: list[dict[str, Any]], historical: Path, pretruth: Path,
    remote_hashes: dict[str, list[str]], reads: list[dict[str, str]],
) -> list[dict[str, Any]]:
    catalog = {}
    models = {}
    for corpus in sorted({case["corpus_id"] for case in pilot}):
        fixture = historical / FIXTURE_BY_CORPUS[corpus]
        models[corpus] = {
            item["case_id"]: item
            for item in read_json(fixture / "model_cases.json", reads)
        }
        catalog[corpus] = {
            item["assertion_id"]: item
            for item in read_json(fixture / "source_assertions.json", reads)
        }

    regulators = {}
    for corpus, group, filename in [
        ("impact-forecasting-2023", "impact", "dimension_selection.json"),
        ("verisk-2023-validation-d", "verisk", "validation_d_dimension_selection.json"),
    ]:
        selection_path = pretruth / group / filename
        lock_path = pretruth / group / "dimension_lock.json"
        selection = read_json(selection_path, reads)
        lock = read_json(lock_path, reads)
        if sha(selection_path) != lock["dimension_selection_sha256"]:
            raise ValueError("Pretruth dimension lock hash mismatch")
        if "FROZEN_BEFORE" not in lock["status"]:
            raise ValueError("Regulator dimensions are not locked before paired adjudication")
        regulators[corpus] = {
            "dimensions": {d["dimension_id"]: d for d in selection["dimensions"]},
            "selection_sha256": sha(selection_path),
            "lock_sha256": sha(lock_path),
            "lock_status": lock["status"],
        }

    rows = []
    for case in pilot:
        corpus = case["corpus_id"]
        original = models[corpus][case["case_id"]]
        current_ids = [e["proposition_id"] for e in case["evidence"]]
        fixture_ids = [e["assertion_id"] for e in original["evidence"]]
        if current_ids != fixture_ids:
            raise ValueError("Current candidate lineage does not match the recorded builder")
        documents: dict[str, set[str]] = {}
        for prop_id in current_ids:
            proposition = catalog[corpus][prop_id]
            document_id = proposition["document_id"]
            documents.setdefault(document_id, set()).update(
                span["document_sha256"] for span in proposition["source_spans"]
                if span.get("document_sha256")
            )
        sources = [
            {
                "document_id": doc,
                "expected_sha256": sorted(hashes),
                "matching_raw_paths": sorted({
                    path for h in hashes for path in remote_hashes.get(h, [])
                    if path.endswith(".pdf")
                }),
            }
            for doc, hashes in sorted(documents.items())
        ]
        source_verified = bool(sources) and all(
            hashes and all(
                any(path.endswith(".pdf") for path in remote_hashes.get(digest, []))
                for digest in hashes
            )
            for hashes in documents.values()
        )
        regulator = regulators.get(corpus)
        dimension = regulator["dimensions"].get(case["requirement_id"]) if regulator else None
        block_ids = []
        if dimension:
            block_ids = dimension.get("regulatory_source_block_ids") or [
                item["block_id"] for item in dimension.get("regulator_sources", [])
            ]
        seed = "KEEP" if source_verified and dimension and block_ids else "UNRESOLVED"
        reasons = ["EVIDENCE_MEMBERSHIP_FROM_ADJUDICATED_FIXTURE"]
        if corpus in {"verisk-2023-validation-d", "kcc-2023-exposed-test-e"}:
            reasons.append("FACET_BOUNDARIES_IMPORTED_FROM_HISTORICAL_HUMAN_DECISIONS")
        else:
            reasons.append("FACET_DEFINITIONS_READ_FROM_ADJUDICATED_COMPARISON_RECORD")
        rows.append({
            "case_id": case["case_id"], "corpus_id": corpus,
            "requirement_id": case["requirement_id"],
            "current_candidate_verdict": "EXCLUDE",
            "source_scope_status": "EXCLUDED_CURRENT_FIXTURE_SCOPE",
            "evidence_scope_frozen_without_truth": False,
            "reason_codes": reasons,
            "evidence_membership_exactly_matches_fixture": True,
            "source_seed_verdict": seed,
            "pretruth_regulator_dimension": {
                "verified": bool(dimension and block_ids),
                "source_block_ids": block_ids,
                "selection_sha256": regulator["selection_sha256"] if regulator else None,
                "lock_sha256": regulator["lock_sha256"] if regulator else None,
                "lock_status": regulator["lock_status"] if regulator else None,
            },
            "source_documents": sources,
            "unresolved_dependencies": (
                [] if seed == "KEEP" else
                (["Original pre-adjudication regulator dimension lock not located"] if not dimension else [])
                + (["One or more exact raw PDFs not located in checked archive paths"] if not source_verified else [])
            ),
            "next_action": (
                "Retain the regulator dimension seed; establish a new evidence scope from raw sources without fixture memberships or prior truth."
                if seed == "KEEP" else
                "Resolve source/lock dependencies independently or replace with a new case. Do not use the current fixture bundle."
            ),
        })
    return rows


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--pilot", type=Path, required=True)
    parser.add_argument("--historical", type=Path, required=True)
    parser.add_argument("--pretruth", type=Path, required=True)
    parser.add_argument("--dcc-hashes", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    reads: list[dict[str, str]] = []
    pilot = read_json(args.pilot, reads)
    hashes: dict[str, list[str]] = {}
    for line in args.dcc_hashes.read_text().splitlines():
        digest, path = line.split(None, 1)
        hashes.setdefault(digest, []).append(path)
    rows = inspect_cases(pilot, args.historical, args.pretruth, hashes, reads)
    report = {
        "version": "ft1-source-scope-eligibility-audit-1.0",
        "status": "COMPLETE", "unit": "CURRENT_CANDIDATE_PACK_VERSION",
        "candidate_counts": dict(Counter(row["current_candidate_verdict"] for row in rows)),
        "source_seed_counts": dict(Counter(row["source_seed_verdict"] for row in rows)),
        "independent_pilot_ready": 0,
        "corelogic": "SKIPPED_DO_NOT_RECONSTRUCT_FROM_ADJUDICATED_FIXTURE",
        "alignment_labels_used": False, "model_predictions_used": False,
        "model_inference_runs": 0, "reads": reads, "cases": rows,
        "scope_caveats": [
            "KEEP source seeds are not KEEP fixture bundles and not frozen facet truth.",
            "Historical sources are exposed development data; use independent annotators who have not seen their judgments.",
            "A new evidence bundle cannot be causally compared against a saved A prediction on a different bundle. Pair A/B/C only on identical prospectively frozen evidence; closed Test E reruns remain prohibited.",
            "No missing path is treated as corpus-wide source absence.",
        ],
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")


if __name__ == "__main__":
    main()
