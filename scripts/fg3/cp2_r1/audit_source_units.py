"""Fail-closed structural audit of legacy FG-3 source-unit drafts.

This does not infer missing headings or repair a unit by selecting another span.
"""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
BASE = ROOT / "experiments/fg3_natural_boundary"
OUT = BASE / "checkpoint2_r1"
HEADING = re.compile(
    r"(?m)^[ \t]{0,8}((?:Form\s+[A-Z]{1,2}[-‐‑‒–—―−﹣－]\d+(?:\.\d+)?\s*:[^\n]{4,110})|(?:[A-Z]{1,2}[-‐‑‒–—―−﹣－]\d+(?:\.\d+)?\s+[A-Z][^\n]{4,110}))",
    re.I,
)
NUMBERED = re.compile(r"^\s*(\d+)[.]\s")
LETTERED = re.compile(r"^\s*([A-Z]|[a-z])[.]\s")


def read(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text().splitlines()]


def pdf_pages(path: Path) -> list[str]:
    result = subprocess.run(
        ["pdftotext", "-layout", "-enc", "UTF-8", str(path), "-"],
        capture_output=True,
        text=True,
        check=True,
    )
    pages = result.stdout.split("\f")
    if pages and not pages[-1].strip():
        pages.pop()
    return pages


def heading_candidates(pages: list[str], page: int, offset: int) -> list[dict]:
    candidates = []
    for page_number in range(1, page + 1):
        content = pages[page_number - 1]
        end = offset if page_number == page else len(content)
        for match in HEADING.finditer(content[:end]):
            printed = match.group(1).strip()
            if "...." in printed or len(printed) > 120:
                continue
            start = match.start(1)
            candidates.append(
                {
                    "physical_page": page_number,
                    "start": start,
                    "end": match.end(1),
                    "text": content[start : match.end(1)],
                    "heading_family": "FORM"
                    if printed.casefold().startswith("form ")
                    else "STANDARD",
                }
            )
    return candidates[-4:]


def boundary_evidence(unit: dict, pages: list[str]) -> dict:
    first, last = unit["source_refs"][0], unit["source_refs"][-1]
    first_page = pages[first["physical_page"] - 1]
    last_page = pages[last["physical_page"] - 1]
    before = first_page[max(0, first["start"] - 180) : first["start"]]
    after = last_page[last["end"] : last["end"] + 180]
    first_line = first["text"].splitlines()[0].strip() if first["text"].splitlines() else ""
    first_number = NUMBERED.match(first_line)
    first_letter = LETTERED.match(first_line)
    after_stripped = after.lstrip()
    end_kind = "UNVERIFIED"
    if first_number and re.match(r"^\d+[.]\s", after_stripped):
        end_kind = "NEXT_NUMBERED_ITEM"
    elif first_letter and re.match(r"^[A-Za-z][.]\s", after_stripped):
        end_kind = "NEXT_LETTERED_ITEM"
    elif after.startswith("\n\n") or after.startswith("\n   \n"):
        end_kind = "BLANK_PARAGRAPH_BOUNDARY"
    elif not after.strip():
        end_kind = "PHYSICAL_PAGE_END_UNRESOLVED_CONTINUATION"
    return {
        "first_line": first_line,
        "preceding_text": before,
        "following_text": after,
        "start_at_printed_marker": bool(
            first_number or first_letter or unit["boundary_rule"] == "CONTAINING_LAYOUT_PARAGRAPH"
        ),
        "end_kind": end_kind,
        "physical_page_start": first["physical_page"],
        "physical_page_end": last["physical_page"],
        "raw_start": first["start"],
        "raw_end": last["end"],
    }


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    units = read(BASE / "checkpoint2/source_unit_drafts.jsonl")
    leads = {x["lead_id"]: x for x in read(BASE / "checkpoint2/lead_source_dossiers.jsonl")}
    documents = {}
    results = []
    for unit in units:
        lead = leads[unit["lead_id"]]
        document_id = unit["document_id"]
        if document_id not in documents:
            pdf = ROOT / lead["source_path"]
            if hashlib.sha256(pdf.read_bytes()).hexdigest() != lead["source_sha256"]:
                raise ValueError("source PDF hash drift")
            documents[document_id] = pdf_pages(pdf)
        pages = documents[document_id]
        for ref in unit["source_refs"]:
            page = pages[ref["physical_page"] - 1]
            if page[ref["start"] : ref["end"]] != ref["text"]:
                raise ValueError(f"source ref mismatch: {unit['lead_id']}")
        first = unit["source_refs"][0]
        candidates = heading_candidates(pages, first["physical_page"], first["start"])
        evidence = boundary_evidence(unit, pages)
        parent = candidates[-1] if candidates else None
        # Candidate headings and boundaries are audit material; neither is silently certified.
        results.append(
            {
                "lead_id": unit["lead_id"],
                "source_unit_id": unit["source_unit_id"],
                "document_id": document_id,
                "source_sha256": unit["source_sha256"],
                "source_refs": unit["source_refs"],
                "unit_text": unit["unit_text"],
                "anchor_query_id": unit["anchor_query_id"],
                "parent_heading_candidate": parent,
                "other_nearby_heading_candidates": candidates[:-1],
                "boundary_rule": unit["boundary_rule"],
                "boundary_evidence": evidence,
                "canonical_status": "REQUIRES_SOURCE_BOUNDARY_AND_HEADING_CONFIRMATION",
                "primary_eligible": False,
            }
        )
    path = OUT / "source_unit_boundary_audit.jsonl"
    path.write_text(
        "".join(json.dumps(x, ensure_ascii=False, sort_keys=True) + "\n" for x in results)
    )
    print(f"Audited {len(results)} source-unit drafts; none silently certified")


if __name__ == "__main__":
    main()
