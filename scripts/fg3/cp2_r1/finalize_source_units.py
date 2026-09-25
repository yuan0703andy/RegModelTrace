"""Source-only CP2-R1 boundary decisions for the 37 repaired leads.

This is not human truth for FG-3 semantic questions. It certifies exact source
units and preserves unresolved/excluded leads rather than shifting anchors.
"""

from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
BASE = ROOT / "experiments/fg3_natural_boundary"
OUT = BASE / "checkpoint2_r1"

DECISIONS = {
    "FG3L_790bc4c0e7c53a42": ("SOURCE_UNIT_UNRESOLVED", "The general form/table instruction lacks a source-verified parent heading in the current extraction."),
    "FG3L_890ac5146ded6275": ("SOURCE_UNIT_UNRESOLVED", "The column-heading instruction lacks a source-verified parent heading in the current extraction."),
    "FG3L_464684973341bd4c": ("TERMINAL_EXCLUDED_FIXED_ANCHOR_CAPTION", "The selected phrase is a Figure 20 caption, not a substantive vendor change statement."),
    "FG3L_199e296b691cc21d": ("TERMINAL_EXCLUDED_KNOWN_EXPOSURE", "The 2023 reviewer physical page 7 was already recorded as developer-inspected in the frozen exposure ledger."),
}


def read(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text().splitlines()]


def raw_offset(page: str, normalized_offset: int) -> int:
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
    return positions[normalized_offset]


def pdf_pages(pdf: Path) -> list[str]:
    result = subprocess.run(
        ["pdftotext", "-layout", "-enc", "UTF-8", str(pdf), "-"],
        capture_output=True,
        text=True,
        check=True,
    )
    pages = result.stdout.split("\f")
    if pages and not pages[-1].strip():
        pages.pop()
    return pages


def main() -> None:
    units = read(OUT / "repaired_source_unit_candidates.jsonl")
    leads = {row["lead_id"]: row for row in read(BASE / "checkpoint2/lead_source_dossiers.jsonl")}
    assert set(DECISIONS).issubset({row["lead_id"] for row in units})
    docs = {}
    canonical = []
    dispositions = []
    for unit in units:
        lead = leads[unit["lead_id"]]
        if unit["document_id"] not in docs:
            pdf = ROOT / lead["source_path"]
            assert hashlib.sha256(pdf.read_bytes()).hexdigest() == lead["source_sha256"]
            docs[unit["document_id"]] = pdf_pages(pdf)
        pages = docs[unit["document_id"]]
        first_page = pages[lead["physical_page"] - 1]
        anchor = raw_offset(first_page, lead["anchor_start_in_normalized_page"])
        if not any(
            ref["physical_page"] == lead["physical_page"] and ref["start"] <= anchor < ref["end"]
            for ref in unit["source_refs"]
        ):
            raise ValueError(f"repaired unit does not contain exact fixed anchor: {unit['lead_id']}")
        for ref in unit["source_refs"]:
            page = pages[ref["physical_page"] - 1]
            if page[ref["start"] : ref["end"]] != ref["text"]:
                raise ValueError(f"source span drift: {unit['lead_id']}")
        parent = unit["parent_heading_source_ref"]
        if parent:
            page = pages[parent["physical_page"] - 1]
            if page[parent["start"] : parent["end"]] != parent["text"]:
                raise ValueError(f"parent heading drift: {unit['lead_id']}")
        status, rationale = DECISIONS.get(
            unit["lead_id"],
            ("CANONICAL_SOURCE_UNIT", "Source text, fixed anchor, complete local subsection/paragraph boundary, and printed parent heading were checked against the PDF extraction."),
        )
        if unit["lead_id"] == "FG3L_2b40fc1569aee3c3":
            rationale = (
                "Numbered M-3 Audit 2 runs across physical pages 20-21 and discusses one "
                "storm-track-selection/generator object; its discussed/reviewed sentences "
                "are attached details. Unlike excluded CI-4 Audit 6, it does not switch to "
                "a separate vulnerability-matrix code-count object. This is a source-unit "
                "decision, not a scrutiny/challenge gold label."
            )
        if status == "CANONICAL_SOURCE_UNIT" and not parent:
            raise ValueError(f"canonical unit lacks parent heading: {unit['lead_id']}")
        pages_used = unit["physical_page_end"] - unit["physical_page_start"] + 1
        words = len(unit["unit_text"].split())
        if status == "CANONICAL_SOURCE_UNIT" and (pages_used > 2 or words > 3000):
            status = "CONTEXT_OVERFLOW"
            rationale = "The frozen two-physical-page or 3000-word source-unit limit is exceeded."
        identity = (
            f"{unit['document_id']}|"
            + "|".join(f"{ref['physical_page']}:{ref['start']}:{ref['end']}" for ref in unit["source_refs"])
        )
        new_id = "FG3R1U_" + hashlib.sha256(identity.encode()).hexdigest()[:20]
        record = {
            **unit,
            "unit_id": new_id,
            "boundary_verification": status,
            "boundary_review_rationale": rationale,
            "source_word_count": words,
            "source_physical_page_count": pages_used,
            "fixed_anchor_raw_offset": anchor,
            "primary_eligible": False,
        }
        dispositions.append(
            {
                "lead_id": unit["lead_id"],
                "unit_id": new_id,
                "status": status,
                "rationale": rationale,
                "legacy_source_unit_id": unit["legacy_source_unit_id"],
            }
        )
        if status == "CANONICAL_SOURCE_UNIT":
            canonical.append(record)
    (OUT / "canonical_source_units.jsonl").write_text(
        "".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in canonical)
    )
    (OUT / "source_unit_dispositions.jsonl").write_text(
        "".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in dispositions)
    )
    print(f"canonical source units: {len(canonical)}; total source-unit dispositions: {len(dispositions)}")


if __name__ == "__main__":
    main()
