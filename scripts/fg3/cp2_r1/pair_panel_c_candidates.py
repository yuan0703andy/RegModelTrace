"""Source-key-first Panel C counterpart candidate audit.

This is intentionally a search audit, not a same-object/causation decision.
All typed first-tier hits are kept; subsection and paragraph boundaries still
need source-only review before any pair is considered formed.
"""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

from .pair_panel_a_sections import extract_pages, paragraphs
from .sections import section_candidates
from .typed_keys import EXPLICIT, normalized_id

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "experiments/fg3_natural_boundary/checkpoint2_r1"


def explicit_typed_in_paragraph(paragraph: str) -> set[str]:
    result = set()
    for match in EXPLICIT.finditer(paragraph):
        kind = "FORM" if match.group(1).casefold().startswith("form") else "STANDARD"
        result.add(f"{kind}:{normalized_id(match.group(2))}")
    return result


def collect_sections(pages: list[str], key: str, doc: str, sha: str) -> tuple[list[dict], list[dict]]:
    sections = section_candidates(pages, key)
    candidates = []
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
                if not re.search(r"[A-Za-z]", match.group()):
                    continue
                candidates.append(
                    {
                        "document_id": doc,
                        "source_sha256": sha,
                        "physical_page": page_number,
                        "start": start + match.start(),
                        "end": start + match.end(),
                        "text": match.group(),
                        "matched_key": key,
                        "match_route": "TYPED_SECTION_MEMBER",
                    }
                )
    return sections, candidates


def main() -> None:
    plans = [json.loads(line) for line in (OUT / "source_only_typed_key_plans.jsonl").read_text().splitlines()]
    docs = {}
    records = []
    for plan in plans:
        if plan["panel"] != "C":
            continue
        role = "review" if plan["document_id"].endswith("submission") else "submission"
        doc = f"florida_public_{plan['cycle']}_fphlm_{role}"
        if doc not in docs:
            path = ROOT / "regmodeltrace/data/corpus/scale-1/raw" / f"{doc}.pdf"
            docs[doc] = (hashlib.sha256(path.read_bytes()).hexdigest(), extract_pages(path))
        sha, pages = docs[doc]
        keys = sorted(set(x["normalized_key"] for x in plan["tiers"]["tier1"]))
        sections = []
        matches = []
        for key in keys:
            found_sections, found_members = collect_sections(pages, key, doc, sha)
            sections.extend(found_sections)
            matches.extend(found_members)
        for page_number, page in enumerate(pages, 1):
            for match in paragraphs(page):
                printed = explicit_typed_in_paragraph(match.group())
                for key in keys:
                    if key in printed:
                        matches.append(
                            {
                                "document_id": doc,
                                "source_sha256": sha,
                                "physical_page": page_number,
                                "start": match.start(),
                                "end": match.end(),
                                "text": match.group(),
                                "matched_key": key,
                                "match_route": "EXPLICIT_TYPED_REFERENCE",
                            }
                        )
        unique = {
            (x["physical_page"], x["start"], x["end"], x["matched_key"]): x
            for x in matches
        }
        matches = list(unique.values())
        words = sum(len(x["text"].split()) for x in matches)
        records.append(
            {
                "lead_id": plan["lead_id"],
                "source_only_plan_sha256": plan["source_only_plan_sha256"],
                "counterpart_document_id": doc,
                "counterpart_source_sha256": sha,
                "typed_keys": keys,
                "first_tier_attempted": "TIER1_TYPED_IDENTIFIER",
                "section_candidates": sections,
                "literal_candidate_count": len(matches),
                "literal_candidate_words": words,
                "literal_candidates": matches,
                "preliminary_limit_exceeded": len(matches) > 20 or words > 3000,
                "pairing_status": "COUNTERPART_UNIT_AND_SAME_OBJECT_REVIEW_PENDING" if matches else "LOWER_TIER_SEARCH_PENDING",
                "permanently_secondary": plan["permanently_secondary"],
                "primary_eligible": False,
            }
        )
    (OUT / "panel_c_typed_counterpart_candidates.jsonl").write_text(
        "".join(json.dumps(x, sort_keys=True, ensure_ascii=False) + "\n" for x in records)
    )
    print([(x["lead_id"], x["literal_candidate_count"], x["preliminary_limit_exceeded"]) for x in records])


if __name__ == "__main__":
    main()
