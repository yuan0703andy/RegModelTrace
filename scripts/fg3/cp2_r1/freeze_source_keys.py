"""Freeze source-only, provenance-bearing pairing plans before counterpart search.

This deliberately records unmaterializable lower tiers instead of inventing a
synonym or using counterpart text to choose a convenient phrase.
"""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

from .typed_keys import keys_from_refs

ROOT = Path(__file__).resolve().parents[3]
BASE = ROOT / "experiments/fg3_natural_boundary"
OUT = BASE / "checkpoint2_r1"
QUOTED = re.compile(r"[“\"]([^”\"]{3,100})[”\"]")
NAMED_HEADING = re.compile(r"^[A-Z][A-Za-z0-9 /–—-]{8,120}$")
EXPLICIT_DISCLOSURE = re.compile(r"\b(?:Disclosure|Response|Comment)\s+\d+[A-Z]?(?:\.\d+)?\b", re.I)


def read(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text().splitlines()]


def span_key(ref: dict, start: int, end: int, key_type: str, derivation: str, document_id: str) -> dict:
    return {
        "key_text": ref["text"][start:end],
        "key_type": key_type,
        "source_ref": {
            "document_id": document_id,
            "physical_page": ref["physical_page"],
            "start": ref["start"] + start,
            "end": ref["start"] + end,
        },
        "derivation": derivation,
    }


def plan(unit: dict, lead: dict, permanently_secondary: set[str]) -> dict:
    document_id = unit["document_id"]
    parent = unit["parent_heading_source_ref"]
    tier1 = keys_from_refs(document_id, unit["source_refs"], parent)
    tier2 = []
    tier3 = []
    tier4 = []
    if lead["panel"] == "A":
        # The complete printed heading is an exact-string fallback, not an ID.
        tier2.append(span_key(parent, 0, len(parent["text"]), "HEADING", "PRINTED_ALLOWED_PARENT", document_id))
    for ref in unit["source_refs"]:
        for match in QUOTED.finditer(ref["text"]):
            words = match.group(1).split()
            if len(words) >= 2:
                tier3.append(span_key(ref, match.start(1), match.end(1), "QUOTED_NAME_CANDIDATE", "PRINTED_IN_UNIT", document_id))
            if 2 <= len(words) <= 5:
                tier4.append(span_key(ref, match.start(1), match.end(1), "LITERAL_PHRASE_CANDIDATE", "PRINTED_IN_UNIT", document_id))
        if lead["panel"] == "C":
            for match in EXPLICIT_DISCLOSURE.finditer(ref["text"]):
                tier2.append(span_key(ref, match.start(), match.end(), "COMMENT_DISCLOSURE_ID", "PRINTED_IN_UNIT", document_id))
    significant = [w for w in re.findall(r"[A-Za-z]+", parent["text"]) if w.casefold() not in {"of", "the", "and", "in", "for", "to", "on"}]
    title_cased = len(significant) >= 2 and all(w[0].isupper() for w in significant)
    if title_cased and NAMED_HEADING.fullmatch(parent["text"].strip()) and not re.match(r"(?:Appendix\s+\w+\s*[–—-]\s*)?(?:Form|Standard)?\s*[A-Z]{1,2}[-‐‑‒–—―−﹣－]\d+", parent["text"].strip(), re.I):
        heading = parent["text"]
        tier3.append(span_key(parent, 0, len(heading), "PRINTED_TECHNICAL_HEADING", "PRINTED_ALLOWED_PARENT", document_id))
    # Every candidate remains a candidate until source-only judgment confirms
    # that the phrase is a technical name rather than an example or generic text.
    def dedupe(items: list[dict]) -> list[dict]:
        return list({(x["key_type"], *x["source_ref"].values()): x for x in items}.values())

    tiers = {"tier1": tier1, "tier2": dedupe(tier2), "tier3": dedupe(tier3), "tier4": dedupe(tier4)}
    identity = json.dumps({"unit_id": unit["unit_id"], "tiers": tiers}, sort_keys=True, ensure_ascii=False)
    return {
        "lead_id": unit["lead_id"],
        "unit_id": unit["unit_id"],
        "panel": lead["panel"],
        "cycle": lead["standards_cycle"],
        "document_id": document_id,
        "source_unit_status": unit["boundary_verification"],
        "tiers": tiers,
        "tier3_review_status": "SOURCE_ONLY_CANDIDATES_REQUIRE_NAME_REVIEW" if tiers["tier3"] else "NO_EXPLICIT_NAME_FOUND",
        "tier4_review_status": "SOURCE_ONLY_CANDIDATES_REQUIRE_GENERIC_PHRASE_FILTER" if tiers["tier4"] else "NOT_MATERIALIZABLE_WITHOUT_SOURCE_ONLY_JUDGMENT",
        "counterpart_search_executed": False,
        "permanently_secondary": unit["lead_id"] in permanently_secondary,
        "primary_eligible": False,
        "source_only_plan_sha256": hashlib.sha256(identity.encode()).hexdigest(),
    }


def main() -> None:
    units = read(OUT / "canonical_source_units.jsonl")
    leads = {x["lead_id"]: x for x in read(BASE / "checkpoint2/lead_source_dossiers.jsonl")}
    old = read(BASE / "checkpoint2/pair_search_inputs.jsonl")
    secondary = {x["lead_id"] for x in old if not x["primary_protocol_clean"]}
    extra = json.loads((OUT / "repair_deviations.json").read_text())
    secondary.update(x["lead_id"] for x in extra["newly_deviated_leads"])
    if len(secondary) != 19:
        raise ValueError(f"expected 19 permanent secondary plans; found {len(secondary)}")
    result = [plan(unit, leads[unit["lead_id"]], secondary) for unit in units]
    path = OUT / "source_only_typed_key_plans.jsonl"
    path.write_text("".join(json.dumps(x, sort_keys=True, ensure_ascii=False) + "\n" for x in result))
    print(f"frozen source-only key plans: {len(result)}; permanent secondary: {len(secondary)}")


if __name__ == "__main__":
    main()
