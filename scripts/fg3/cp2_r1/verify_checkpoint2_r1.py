"""Fail-closed integrity verification of the CP2-R1 implementation checkpoint.

Integrity PASS here is deliberately separate from the FG-3 Checkpoint 2 gate.
"""

from __future__ import annotations

import hashlib
import json
import subprocess
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
BASE = ROOT / "experiments/fg3_natural_boundary"
OUT = BASE / "checkpoint2_r1"


def rows(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text().splitlines()]


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def pdf_pages(path: Path) -> list[str]:
    value = subprocess.run(
        ["pdftotext", "-layout", "-enc", "UTF-8", str(path), "-"],
        capture_output=True,
        text=True,
        check=True,
    ).stdout.split("\f")
    if value and not value[-1].strip():
        value.pop()
    return value


def main() -> None:
    leads = {x["lead_id"]: x for x in rows(BASE / "checkpoint2/lead_source_dossiers.jsonl")}
    source_paths = {}
    for lead in leads.values():
        source_paths.setdefault(lead["document_id"], lead["source_path"])
        assert source_paths[lead["document_id"]] == lead["source_path"]
    units = rows(OUT / "canonical_source_units.jsonl")
    decisions = rows(OUT / "source_unit_dispositions.jsonl")
    plans = rows(OUT / "source_only_typed_key_plans.jsonl")
    excluded = rows(OUT / "fixed_anchor_exclusion_recheck.jsonl")
    exposure = rows(OUT / "source_exact_exposure_candidates.jsonl")
    a_pairs = rows(OUT / "panel_a_typed_section_candidates.jsonl")
    c_pairs = rows(OUT / "panel_c_typed_counterpart_candidates.jsonl")
    raw = rows(OUT / "raw_mode_verification_v2.jsonl")
    assert len(leads) == 85 and len(raw) == 85
    assert len(decisions) == 37 and len(units) == len(plans) == len(exposure) == 33
    assert len(excluded) == 45 and len(a_pairs) == 5 and len(c_pairs) == 27
    assert len({x["lead_id"] for x in decisions + excluded}) == 82
    assert len({x["lead_id"] for x in plans}) == 33
    assert set(x["lead_id"] for x in plans) == set(x["lead_id"] for x in exposure)
    assert sum(x["permanently_secondary"] for x in plans) == 19
    assert all(x["primary_eligible"] is False for x in units + plans + exposure + a_pairs + c_pairs)
    docs = {}

    def check_ref(document_id: str, pdf_sha: str, ref: dict) -> None:
        if document_id not in docs:
            path = ROOT / source_paths[document_id]
            docs[document_id] = (digest(path), pdf_pages(path))
        current_sha, pages = docs[document_id]
        assert current_sha == pdf_sha
        assert pages[ref["physical_page"] - 1][ref["start"] : ref["end"]] == ref["text"]

    for unit in units:
        lead = leads[unit["lead_id"]]
        assert lead["document_id"] == unit["document_id"]
        assert lead["source_sha256"] == unit["source_sha256"]
        for ref in unit["source_refs"]:
            check_ref(unit["document_id"], unit["source_sha256"], ref)
        check_ref(unit["document_id"], unit["source_sha256"], unit["parent_heading_source_ref"])
    for plan in plans:
        lead = leads[plan["lead_id"]]
        for tier in plan["tiers"].values():
            for key in tier:
                ref = key["source_ref"]
                assert ref["document_id"] == lead["document_id"]
                _, pages = docs[lead["document_id"]]
                assert pages[ref["physical_page"] - 1][ref["start"] : ref["end"]] == key["key_text"]
                if key.get("normalized_key"):
                    assert key["normalized_key"].startswith(("FORM:", "STANDARD:"))
    plan_by_lead = {x["lead_id"]: x for x in plans}
    for pair in a_pairs + c_pairs:
        assert pair["source_only_plan_sha256"] == plan_by_lead[pair["lead_id"]]["source_only_plan_sha256"]
        doc = pair["counterpart_document_id"]
        sha = pair.get("counterpart_pdf_sha256") or pair.get("counterpart_source_sha256")
        if doc not in docs:
            path = ROOT / source_paths[doc]
            docs[doc] = (digest(path), pdf_pages(path))
        assert docs[doc][0] == sha
        for candidate in pair.get("paragraph_candidates", pair.get("literal_candidates", [])):
            check_ref(doc, sha, candidate)
    manifest = json.loads((BASE / "protocol/known_exposure_file_manifest_v1.json").read_text())
    assert len(manifest["files"]) == 347
    assert all(digest(ROOT / item["path"]) == item["sha256"] for item in manifest["files"])
    assert all(x["exposure_status"] != "CLEAR" for x in exposure)
    result = {
        "cp2_r1_integrity": "PASS_FOR_RECORDED_ARTIFACTS_ONLY",
        "fg3_checkpoint_2": "NOT_PASS_REPAIR_AND_SOURCE_REVIEW_INCOMPLETE",
        "frozen_leads": 85,
        "source_unit_dispositions": dict(Counter(x["status"] for x in decisions)),
        "canonical_source_units": len(units),
        "source_only_key_plans": len(plans),
        "panel_a_typed_candidate_sets": len(a_pairs),
        "panel_c_typed_candidate_sets": len(c_pairs),
        "reopened_fixed_anchor_exclusions": sum(x["r1_status"].startswith("REOPEN") for x in excluded),
        "source_exact_overlap_candidate_units": sum(bool(x["exact_overlap_candidates"]) for x in exposure),
        "source_exposure_parse_failure_units": sum(bool(x["parse_failures"]) for x in exposure),
        "known_exposure_manifest_files_verified": len(manifest["files"]),
        "human_gold_count": 0,
        "model_inference_count": 0,
        "primary_eligible_count": 0,
        "limits": [
            "Counterpart headings, section boundaries, substantive paragraphs, and same-object pairs are candidates only.",
            "Lower-tier search is incomplete for no-first-tier cases.",
            "Exact nonmatch does not clear substantial exposure; one frozen binary ledger file cannot be text-decoded.",
            "Five prior fixed-anchor exits require canonical source-unit review; other retained exits await PDF-level confirmation.",
        ],
    }
    (OUT / "cp2_r1_integrity_verification.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
