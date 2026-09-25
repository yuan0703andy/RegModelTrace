"""Verify custody and internal consistency of FG-3 Checkpoint 2 audit drafts.

A successful verification is not scientific eligibility or Checkpoint 2 PASS.
"""

from __future__ import annotations

from collections import Counter
import hashlib
import json
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT / "experiments/fg3_natural_boundary"
OUT = BASE / "checkpoint2"


def read(name: str):
    return [json.loads(line) for line in (OUT / name).read_text().splitlines()]


def normalize(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip().casefold()


def raw_anchor_offset(page: str, offset: int) -> int:
    positions = []
    previous_space = False
    for index, char in enumerate(page):
        if char.isspace():
            if positions and not previous_space:
                positions.append(index)
            previous_space = True
        else:
            positions.extend([index] * len(char.casefold()))
            previous_space = False
    return positions[offset]


def main() -> None:
    leads = read("lead_source_dossiers.jsonl")
    screens = read("lead_screening.jsonl")
    raw_checks = read("pdf_text_verification.jsonl")
    units = read("source_unit_drafts.jsonl")
    plans = read("pair_search_inputs.jsonl")
    audits = read("pairing_literal_audit.jsonl")
    unit_exposure = read("unit_exact_exposure_matches.jsonl")
    paired_exposure = read("counterpart_exact_exposure_matches.jsonl")
    lexical = read("exposure_similarity_candidates.jsonl")
    assert len(leads) == len(screens) == len(raw_checks) == 85
    assert len({r["lead_id"] for r in leads}) == 85
    assert {r["lead_id"] for r in leads} == {r["lead_id"] for r in screens}
    assert {r["lead_id"] for r in leads} == {r["lead_id"] for r in raw_checks}
    review_required = sum(
        row["source_context_screening_status"] == "SOURCE_UNIT_AND_PAIRING_REVIEW_REQUIRED"
        for row in screens
    )
    assert len(units) == len(unit_exposure) == len(lexical) == review_required
    assert len(plans) == len(audits) == len(paired_exposure) == 36
    assert {r["lead_id"] for r in units} == {r["lead_id"] for r in unit_exposure}
    assert {r["lead_id"] for r in plans} == {r["lead_id"] for r in audits}
    lead_by_id = {r["lead_id"]: r for r in leads}
    pages_by_document = {}
    for lead in leads:
        doc = lead["document_id"]
        if doc not in pages_by_document:
            pdf = ROOT / lead["source_path"]
            assert hashlib.sha256(pdf.read_bytes()).hexdigest() == lead["source_sha256"]
            result = subprocess.run(
                ["pdftotext", "-layout", "-enc", "UTF-8", str(pdf), "-"],
                capture_output=True,
                text=True,
                check=True,
            )
            pages = result.stdout.split("\f")
            if pages and not pages[-1].strip():
                pages.pop()
            pages_by_document[doc] = pages
        page = pages_by_document[doc][lead["physical_page"] - 1]
        assert hashlib.sha256(page.encode()).hexdigest() == lead["page_text_sha256"]
        assert page == lead["page_text"]
        offset = lead["anchor_start_in_normalized_page"]
        assert (
            normalize(page)[offset : offset + len(lead["anchor_text"])]
            == lead["anchor_text"].casefold()
        )

    for unit in units:
        lead = lead_by_id[unit["lead_id"]]
        assert lead["document_id"] == unit["document_id"]
        assert lead["source_sha256"] == unit["source_sha256"]
        anchor_raw = raw_anchor_offset(
            pages_by_document[unit["document_id"]][lead["physical_page"] - 1],
            lead["anchor_start_in_normalized_page"],
        )
        assert any(
            ref["physical_page"] == lead["physical_page"]
            and ref["start"] <= anchor_raw < ref["end"]
            for ref in unit["source_refs"]
        ), f"source unit misses fixed anchor: {unit['lead_id']}"
        for ref in unit["source_refs"]:
            page = pages_by_document[unit["document_id"]][ref["physical_page"] - 1]
            assert page[ref["start"] : ref["end"]] == ref["text"]
    for audit in audits:
        doc = audit["counterpart_document_id"]
        if doc not in pages_by_document:
            pdf = ROOT / "regmodeltrace/data/corpus/scale-1/raw" / f"{doc}.pdf"
            assert (
                hashlib.sha256(pdf.read_bytes()).hexdigest() == audit["counterpart_source_sha256"]
            )
            result = subprocess.run(
                ["pdftotext", "-layout", "-enc", "UTF-8", str(pdf), "-"],
                capture_output=True,
                text=True,
                check=True,
            )
            pages = result.stdout.split("\f")
            if pages and not pages[-1].strip():
                pages.pop()
            pages_by_document[doc] = pages
        for candidate in audit["literal_candidates"]:
            page = pages_by_document[doc][candidate["physical_page"] - 1]
            assert page[candidate["start"] : candidate["end"]] == candidate["text"]
            assert candidate["source_sha256"] == audit["counterpart_source_sha256"]
    report = {
        "status": "AUDIT_INTEGRITY_VERIFIED_NOT_CHECKPOINT_PASS",
        "frozen_leads": len(leads),
        "pdf_anchor_text_verified": len(leads),
        "draft_source_units_with_anchor_and_exact_spans": len(units),
        "literal_pairing_audits": len(audits),
        "source_screening": dict(Counter(x["source_context_screening_status"] for x in screens)),
        "literal_pairing_status": dict(Counter(x["pairing_audit_status"] for x in audits)),
        "unit_exact_overlap_candidate_count": sum(
            bool(x["exact_12_token_match_files"]) for x in unit_exposure
        ),
        "pairing_audits_with_exact_overlap_candidates": sum(
            bool(x["counterpart_exact_matches"]) for x in paired_exposure
        ),
        "primary_eligible_cases": 0,
        "human_truth_records": 0,
        "model_runs": 0,
    }
    (OUT / "audit_integrity_verification.json").write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n"
    )
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
