"""Literal first-tier counterpart audit for FG-3; never infers semantic relevance."""

from __future__ import annotations
import hashlib
import json
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT / "experiments/fg3_natural_boundary"


def norm(s):
    return re.sub(r"\s+", " ", s).strip().casefold()


def paragraphs(text):
    return [
        (m.start(), m.end(), m.group()) for m in re.finditer(r"[^\n]+(?:\n(?!\s*\n)[^\n]+)*", text)
    ]


def main():
    plans = [
        json.loads(s)
        for s in (BASE / "checkpoint2/pair_search_inputs.jsonl").read_text().splitlines()
    ]
    docs = {}
    for p in plans:
        role = p["counterpart_role"]
        cycle = p["cycle"]
        doc = f"florida_public_{cycle}_fphlm_" + ("submission" if role == "VENDOR" else "review")
        if doc not in docs:
            path = ROOT / "regmodeltrace/data/corpus/scale-1/raw" / f"{doc}.pdf"
            rr = subprocess.run(
                ["pdftotext", "-layout", "-enc", "UTF-8", str(path), "-"],
                capture_output=True,
                text=True,
                check=True,
            )
            pages = rr.stdout.split("\f")
            if pages and not pages[-1].strip():
                pages.pop()
            docs[doc] = (path, hashlib.sha256(path.read_bytes()).hexdigest(), pages)
    out = []
    for p in plans:
        doc = f"florida_public_{p['cycle']}_fphlm_" + (
            "submission" if p["counterpart_role"] == "VENDOR" else "review"
        )
        path, sha, pages = docs[doc]
        chosen_tier = None
        keys = []
        matches = []
        for tier, terms in [
            ("IDENTIFIER", p["tier1_literal_identifiers"]),
            ("EXACT_HEADING", [p["tier2_exact_heading"]] if p["tier2_exact_heading"] else []),
            ("EXPLICIT_NAME", [p["tier3_explicit_name"]] if p["tier3_explicit_name"] else []),
            ("BOUNDED_LITERAL_TERMINOLOGY", p["tier4_literal_phrases"]),
        ]:
            if not terms:
                continue
            found = []
            for pgnum, t in enumerate(pages, 1):
                for a, b, para in paragraphs(t):
                    hit = []
                    for term in terms:
                        if tier == "IDENTIFIER":
                            yes = bool(
                                re.search(
                                    r"(?<![A-Za-z0-9])" + re.escape(term) + r"(?![\d.])", para, re.I
                                )
                            )
                        else:
                            yes = norm(term) in norm(para)
                        if yes:
                            hit.append(term)
                    if hit:
                        found.append(
                            {
                                "document_id": doc,
                                "source_sha256": sha,
                                "physical_page": pgnum,
                                "start": a,
                                "end": b,
                                "matched_keys": hit,
                                "text": para,
                            }
                        )
            if found:
                chosen_tier = tier
                keys = terms
                matches = found
                break
        words = sum(len(x["text"].split()) for x in matches)
        status = (
            "NO_PAIR_UNDER_FROZEN_RULE"
            if not matches
            and any(
                (
                    p["tier1_literal_identifiers"],
                    p["tier2_exact_heading"],
                    p["tier3_explicit_name"],
                    p["tier4_literal_phrases"],
                )
            )
            else "PAIRING_AMBIGUOUS_NO_SOURCE_KEY"
            if not matches
            else "PAIRING_OVERFLOW"
            if len(matches) > 20 or words > 3000
            else "FIRST_NONEMPTY_TIER_LITERAL_MATCHES_AWAIT_SOURCE_UNIT_REVIEW"
        )
        out.append(
            {
                "lead_id": p["lead_id"],
                "panel": p["panel"],
                "anchor_document_id": p["anchor_document_id"],
                "counterpart_document_id": doc,
                "counterpart_source_sha256": sha,
                "first_nonempty_tier": chosen_tier,
                "keys_searched": keys,
                "literal_candidate_count": len(matches),
                "literal_candidate_words": words,
                "pairing_audit_status": status,
                "presearch_count_exposure_ids": p["presearch_count_exposure_ids"],
                "literal_candidates": matches,
                "limitation": "Literal counterpart matches are not yet verified as complete substantive source units or same-object pairs. For Panel A, a matched section may require expansion before final pairing.",
            }
        )
    target = BASE / "checkpoint2/pairing_literal_audit.jsonl"
    target.write_text(
        "".join(json.dumps(x, ensure_ascii=False, sort_keys=True) + "\n" for x in out)
    )
    from collections import Counter

    print(Counter(x["pairing_audit_status"] for x in out))
    for x in out:
        print(
            x["lead_id"],
            x["panel"],
            x["pairing_audit_status"],
            x["first_nonempty_tier"],
            x["literal_candidate_count"],
            x["literal_candidate_words"],
        )


if __name__ == "__main__":
    main()
