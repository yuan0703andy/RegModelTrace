"""Panel C tier-1 typed-ID-bearing paragraph candidates.

The historical broad-section diagnostic is preserved separately. An exact
identifier-bearing paragraph is only an anchor for natural-unit expansion,
not a completed counterpart pair or a same-object judgment.
"""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

from .pair_panel_a_sections import extract_pages, paragraphs
from .sections import headings
from .typed_keys import EXPLICIT, NUMBERED_COMMENT_TARGET, normalized_id

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "experiments/fg3_natural_boundary/checkpoint2_r1"


def typed_id_occurrences(text: str, reviewer_document: bool) -> list[dict]:
    """Return only printed, syntactically typed IDs with offsets in *text*."""
    found = []
    for match in EXPLICIT.finditer(text):
        kind = "FORM" if match.group(1).casefold().startswith("form") else "STANDARD"
        found.append(
            {
                "normalized_key": f"{kind}:{normalized_id(match.group(2))}",
                "start": match.start(),
                "end": match.end(),
                "printed": match.group(),
                "derivation": "EXPLICIT_FORM_OR_STANDARD_REFERENCE",
            }
        )
    if reviewer_document:
        match = NUMBERED_COMMENT_TARGET.match(text)
        if match:
            found.append(
                {
                    "normalized_key": f"STANDARD:{normalized_id(match.group(1))}",
                    "start": match.start(1),
                    "end": match.end(1),
                    "printed": match.group(1),
                    "derivation": "PRINTED_NUMBERED_REVIEW_COMMENT_TARGET",
                }
            )
    return found


def candidate_records(
    pages: list[str], document_id: str, document_sha256: str, frozen_keys: set[str]
) -> tuple[list[dict], list[dict]]:
    reviewer = document_id.endswith("_review")
    heading_spans = {
        (h.physical_page, h.start, h.end)
        for h in headings(pages)
    }
    result = []
    rejected = []
    for page_number, page in enumerate(pages, 1):
        toc_page = bool(re.search(r"(?im)^\s*Table of Contents\s*$", page[:500])) or len(
            re.findall(r"\.{5,}\s*\d+\s*$", page, re.M)
        ) >= 3
        for paragraph in paragraphs(page):
            start, end = paragraph.start(), paragraph.end()
            heading_only = (page_number, start, end) in heading_spans
            for occurrence in typed_id_occurrences(paragraph.group(), reviewer):
                if occurrence["normalized_key"] not in frozen_keys:
                    continue
                identifier_ref = {
                    "document_id": document_id,
                    "physical_page": page_number,
                    "start": start + occurrence["start"],
                    "end": start + occurrence["end"],
                    "text": occurrence["printed"],
                }
                record = {
                        "document_id": document_id,
                        "source_sha256": document_sha256,
                        "physical_page": page_number,
                        "start": start,
                        "end": end,
                        "text": paragraph.group(),
                        "matched_key": occurrence["normalized_key"],
                        "identifier_source_ref": identifier_ref,
                        "match_derivation": occurrence["derivation"],
                        "counterpart_natural_unit_status": "BOUNDARY_REVIEW_PENDING",
                        "source_role_review_status": "NOT_REVIEWED",
                    }
                if toc_page or heading_only:
                    record["rejection_reason"] = "TABLE_OF_CONTENTS_PAGE" if toc_page else "HEADING_ONLY_CONTEXT"
                    rejected.append(record)
                else:
                    result.append(record)
    return result, rejected


def main() -> None:
    plans = [json.loads(line) for line in (OUT / "source_only_typed_key_plans.jsonl").read_text().splitlines()]
    receipt = json.loads((OUT / "panel_c_tier1_clarification_receipt.json").read_text())
    for item in receipt["files"]:
        assert hashlib.sha256((ROOT / item["path"]).read_bytes()).hexdigest() == item["sha256"]
    docs = {}
    records = []
    for plan in plans:
        if plan["panel"] != "C":
            continue
        counterpart_role = "review" if plan["document_id"].endswith("submission") else "submission"
        document_id = f"florida_public_{plan['cycle']}_fphlm_{counterpart_role}"
        if document_id not in docs:
            path = ROOT / "regmodeltrace/data/corpus/scale-1/raw" / f"{document_id}.pdf"
            docs[document_id] = (hashlib.sha256(path.read_bytes()).hexdigest(), extract_pages(path))
        sha, pages = docs[document_id]
        keys = {item["normalized_key"] for item in plan["tiers"]["tier1"]}
        matches, rejected = candidate_records(pages, document_id, sha, keys)
        records.append(
            {
                "lead_id": plan["lead_id"],
                "source_only_plan_sha256": plan["source_only_plan_sha256"],
                "counterpart_document_id": document_id,
                "counterpart_source_sha256": sha,
                "typed_keys": sorted(keys),
                "first_tier_attempted": "TIER1_EXPLICIT_TYPED_ID_BEARING_NATURAL_UNIT",
                "identifier_occurrence_count": len(matches),
                "distinct_candidate_paragraph_count": len({(m["physical_page"], m["start"], m["end"]) for m in matches}),
                "identifier_bearing_paragraph_candidates": matches,
                "rejected_search_matches": rejected,
                "match_limit_status": "NOT_EVALUATED_UNTIL_NATURAL_UNIT_EXPANSION",
                "pairing_status": "COUNTERPART_NATURAL_UNIT_REVIEW_PENDING" if matches else "LOWER_TIER_SEARCH_PENDING",
                "permanently_secondary": plan["permanently_secondary"],
                "primary_eligible": False,
            }
        )
    (OUT / "panel_c_tier1_explicit_unit_candidates.jsonl").write_text(
        "".join(json.dumps(item, ensure_ascii=False, sort_keys=True) + "\n" for item in records)
    )
    print([(item["lead_id"], item["identifier_occurrence_count"]) for item in records])


if __name__ == "__main__":
    main()
