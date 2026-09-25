"""Verify the bounded Panel C reinterpretation without promoting case status."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from .pair_panel_a_sections import extract_pages

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "experiments/fg3_natural_boundary/checkpoint2_r1"


def read(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text().splitlines()]


def main() -> None:
    receipt = json.loads((OUT / "panel_c_tier1_clarification_receipt.json").read_text())
    assert receipt["status"] == "FROZEN_BEFORE_PANEL_C_TIER1_REGENERATION"
    for item in receipt["files"]:
        assert hashlib.sha256((ROOT / item["path"]).read_bytes()).hexdigest() == item["sha256"]
    prior = {x["lead_id"]: x for x in read(OUT / "panel_c_typed_counterpart_candidates.jsonl")}
    current = read(OUT / "panel_c_tier1_explicit_unit_candidates.jsonl")
    plans = {x["lead_id"]: x for x in read(OUT / "source_only_typed_key_plans.jsonl")}
    assert len(prior) == len(current) == 27
    assert sum(x["preliminary_limit_exceeded"] for x in prior.values()) == 16
    docs = {}
    total_kept = total_rejected = 0
    for row in current:
        plan = plans[row["lead_id"]]
        assert plan["panel"] == "C"
        assert row["source_only_plan_sha256"] == plan["source_only_plan_sha256"]
        assert row["permanently_secondary"] == plan["permanently_secondary"]
        assert row["primary_eligible"] is False
        assert row["match_limit_status"] == "NOT_EVALUATED_UNTIL_NATURAL_UNIT_EXPANSION"
        document_id = row["counterpart_document_id"]
        if document_id not in docs:
            pdf = ROOT / "regmodeltrace/data/corpus/scale-1/raw" / f"{document_id}.pdf"
            sha = hashlib.sha256(pdf.read_bytes()).hexdigest()
            docs[document_id] = (sha, extract_pages(pdf))
        sha, pages = docs[document_id]
        assert sha == row["counterpart_source_sha256"]
        allowed = set(row["typed_keys"])
        for candidate in row["identifier_bearing_paragraph_candidates"] + row["rejected_search_matches"]:
            assert candidate["matched_key"] in allowed
            assert candidate["document_id"] == document_id
            assert candidate["source_sha256"] == sha
            page = pages[candidate["physical_page"] - 1]
            assert page[candidate["start"] : candidate["end"]] == candidate["text"]
            ref = candidate["identifier_source_ref"]
            assert ref["document_id"] == document_id
            assert ref["physical_page"] == candidate["physical_page"]
            assert candidate["start"] <= ref["start"] < ref["end"] <= candidate["end"]
            assert page[ref["start"] : ref["end"]] == ref["text"]
            assert candidate["match_derivation"] in {
                "EXPLICIT_FORM_OR_STANDARD_REFERENCE",
                "PRINTED_NUMBERED_REVIEW_COMMENT_TARGET",
            }
        total_kept += len(row["identifier_bearing_paragraph_candidates"])
        total_rejected += len(row["rejected_search_matches"])
    result = {
        "status": "PASS_FOR_EXACT_ID_BEARING_CANDIDATE_INTEGRITY_ONLY",
        "fg3_checkpoint_2": "NOT_PASS",
        "panel_c_plans": 27,
        "old_broad_section_preliminary_over_limit": 16,
        "new_id_bearing_occurrences": total_kept,
        "rejected_toc_or_heading_occurrences": total_rejected,
        "plans_with_at_least_one_id_bearing_candidate": sum(bool(x["identifier_bearing_paragraph_candidates"]) for x in current),
        "plans_requiring_lower_tier_search": sum(not x["identifier_bearing_paragraph_candidates"] for x in current),
        "natural_unit_expansion": "PENDING",
        "final_overflow_dispositions": 0,
        "same_object_adjudication": "NOT_STARTED",
        "human_gold_count": 0,
        "model_inference_count": 0,
    }
    (OUT / "panel_c_clarification_verification.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
