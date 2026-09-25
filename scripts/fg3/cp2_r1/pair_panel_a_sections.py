"""Rebuild Panel A typed-section candidate sets; no substantive pairing claim.

The source-only key plans must already exist in a prior commit. Heading and
section ends remain candidates until visually/source reviewed.
"""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
from pathlib import Path

from .sections import section_candidates

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "experiments/fg3_natural_boundary/checkpoint2_r1"


def paragraphs(text: str):
    yield from re.finditer(r"[^\n]+(?:\n(?!\s*\n)[^\n]+)*", text)


def extract_pages(path: Path) -> list[str]:
    output = subprocess.run(
        ["pdftotext", "-layout", "-enc", "UTF-8", str(path), "-"],
        capture_output=True,
        text=True,
        check=True,
    ).stdout.split("\f")
    if output and not output[-1].strip():
        output.pop()
    return output


def main() -> None:
    plans = [json.loads(line) for line in (OUT / "source_only_typed_key_plans.jsonl").read_text().splitlines()]
    records = []
    docs = {}
    for plan in plans:
        if plan["panel"] != "A":
            continue
        document_id = f"florida_public_{plan['cycle']}_fphlm_submission"
        if document_id not in docs:
            path = ROOT / "regmodeltrace/data/corpus/scale-1/raw" / f"{document_id}.pdf"
            docs[document_id] = (hashlib.sha256(path.read_bytes()).hexdigest(), extract_pages(path))
        pdf_sha, pages = docs[document_id]
        keys = sorted(set(x["normalized_key"] for x in plan["tiers"]["tier1"]))
        sections = []
        for key in keys:
            sections.extend(section_candidates(pages, key))
        matches = []
        for section in sections:
            heading = section["heading"]
            boundary = section["end_boundary"]
            if boundary is None:
                continue
            for page_number in range(heading["physical_page"], boundary["physical_page"] + 1):
                page = pages[page_number - 1]
                start = heading["end"] if page_number == heading["physical_page"] else 0
                end = boundary["start"] if page_number == boundary["physical_page"] else len(page)
                if end <= start:
                    continue
                for match in paragraphs(page[start:end]):
                    text = match.group().strip()
                    if not text or re.fullmatch(r"\d+", text):
                        continue
                    matches.append(
                        {
                            "document_id": document_id,
                            "source_sha256": pdf_sha,
                            "physical_page": page_number,
                            "start": start + match.start(),
                            "end": start + match.end(),
                            "text": match.group(),
                            "source_key": heading["normalized_key"],
                            "substantive_status": "NOT_YET_REVIEWED",
                        }
                    )
        words = sum(len(x["text"].split()) for x in matches)
        records.append(
            {
                "lead_id": plan["lead_id"],
                "source_only_plan_sha256": plan["source_only_plan_sha256"],
                "source_only_plan_frozen_before_this_search": True,
                "counterpart_document_id": document_id,
                "counterpart_pdf_sha256": pdf_sha,
                "first_tier_attempted": "TIER1_TYPED_SECTION",
                "typed_keys": keys,
                "section_candidates": sections,
                "paragraph_candidates": matches,
                "candidate_paragraph_count": len(matches),
                "candidate_words": words,
                "preliminary_limit_exceeded": len(matches) > 20 or words > 3000,
                "pairing_status": "SECTION_BOUNDARY_AND_SUBSTANTIVE_REVIEW_PENDING" if sections else "LOWER_TIER_SEARCH_PENDING",
                "primary_eligible": False,
            }
        )
    (OUT / "panel_a_typed_section_candidates.jsonl").write_text(
        "".join(json.dumps(x, sort_keys=True, ensure_ascii=False) + "\n" for x in records)
    )
    print([(x["lead_id"], len(x["section_candidates"]), x["candidate_paragraph_count"], x["candidate_words"]) for x in records])


if __name__ == "__main__":
    main()
