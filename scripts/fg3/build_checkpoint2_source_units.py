"""Build reviewable source-unit drafts for frozen FG-3 leads; no gold or model use."""

from __future__ import annotations
import hashlib
import json
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT / "experiments/fg3_natural_boundary"


def pages(pdf: Path) -> list[str]:
    r = subprocess.run(
        ["pdftotext", "-layout", "-enc", "UTF-8", str(pdf), "-"],
        capture_output=True,
        text=True,
        check=True,
    )
    p = r.stdout.split("\f")
    if p and not p[-1].strip():
        p.pop()
    return p


def span(page: str, start_phrase: str, end_phrase: str | None = None) -> tuple[int, int]:
    a = page.find(start_phrase)
    if a < 0:
        raise ValueError("start phrase absent " + repr(start_phrase))
    b = page.find(end_phrase, a + len(start_phrase)) if end_phrase else len(page)
    if b < 0:
        raise ValueError("end phrase absent " + repr(end_phrase))
    return a, b


def paragraph(page: str, at: int) -> tuple[int, int]:
    # Blank lines are frozen PDF-layout paragraph boundaries, not semantic selection.
    bounds = [(m.start(), m.end()) for m in re.finditer(r"[^\n]+(?:\n(?!\s*\n)[^\n]+)*", page)]
    for a, b in bounds:
        if a <= at < b:
            return a, b
    raise ValueError("paragraph absent")


def normalized_anchor_to_raw(page: str, normalized_offset: int) -> int:
    """Map the frozen whitespace-normalized offset back to exact PDF text."""
    raw_offsets = []
    previous_space = False
    for raw_offset, char in enumerate(page):
        if char.isspace():
            if raw_offsets and not previous_space:
                raw_offsets.append(raw_offset)
            previous_space = True
        else:
            raw_offsets.extend([raw_offset] * len(char.casefold()))
            previous_space = False
    if not 0 <= normalized_offset < len(raw_offsets):
        raise ValueError("anchor offset outside normalized page")
    return raw_offsets[normalized_offset]


def main():
    src = {
        x["lead_id"]: x
        for x in map(json.loads, (BASE / "checkpoint2/lead_source_dossiers.jsonl").open())
    }
    decisions = [
        json.loads(x) for x in (BASE / "checkpoint2/lead_screening.jsonl").read_text().splitlines()
    ]
    docs = {}
    for x in src.values():
        d = x["document_id"]
        if d not in docs:
            docs[d] = pages(ROOT / x["source_path"])
    out = []
    for d in decisions:
        if d["source_context_screening_status"] != "SOURCE_UNIT_AND_PAIRING_REVIEW_REQUIRED":
            continue
        x = src[d["lead_id"]]
        doc = x["document_id"]
        n = x["physical_page"]
        page = docs[doc][n - 1]
        anchor_raw = normalized_anchor_to_raw(page, x["anchor_start_in_normalized_page"])
        normalized_page = re.sub(r"\s+", " ", page).strip().casefold()
        at = x["anchor_start_in_normalized_page"]
        if normalized_page[at : at + len(x["anchor_text"])] != x["anchor_text"].casefold():
            raise RuntimeError("frozen anchor mapping failed " + d["lead_id"])
        a, b = paragraph(page, anchor_raw)
        refs = [{"physical_page": n, "start": a, "end": b, "text": page[a:b]}]
        boundary = "CONTAINING_LAYOUT_PARAGRAPH"
        lid = d["lead_id"]
        if lid == "FG3L_d92901032170e6ad":
            a, b = span(page, "   B. Percentage difference", "   C. Color-coded maps")
            refs = [{"physical_page": n, "start": a, "end": b, "text": page[a:b]}]
            boundary = "COMPLETE_B_SUBSECTION_WITH_BOTH_ENUMERATED_ITEMS"
        elif lid == "FG3L_38d49e13a06daf85":
            a, b = span(page, "C. Provide this form", "D. Provide color-coded maps")
            refs = [{"physical_page": n, "start": a, "end": b, "text": page[a:b]}]
            boundary = "COMPLETE_C_SUBSECTION_AT_FIXED_ANCHOR"
        elif lid == "FG3L_a67170a73a9dc42c":
            a, b = span(page, "12. S-5.1, Table 14", None)
            # exclude physical-page footer only
            b = (
                page.rfind("                                                   31")
                if "                                                   31" in page
                else b
            )
            refs = [{"physical_page": n, "start": a, "end": b, "text": page[a:b]}]
            boundary = "NUMBERED_PREVISIT_ITEM_12_WITH_ATTACHED_DISPOSITION_AND_COMMENTS"
        elif lid == "FG3L_2b40fc1569aee3c3":
            prev = docs[doc][n - 2]
            a0, b0 = span(
                prev,
                "2. The method and supporting material",
                "                                                20",
            )
            a1, b1 = span(
                page,
                "   Reviewed the storm track generator",
                "3. The method and supporting material",
            )
            refs = [
                {"physical_page": n - 1, "start": a0, "end": b0, "text": prev[a0:b0]},
                {"physical_page": n, "start": a1, "end": b1, "text": page[a1:b1]},
            ]
            boundary = "AUDIT_2_WITH_PAGE_CONTINUATION_AND_COMMENTS"
        elif lid == "FG3L_e167ff03e7759c00":
            prev = docs[doc][n - 2]
            a0, b0 = span(
                prev,
                "6. The table of all software components",
                "                                               76",
            )
            a1, b1 = span(page, "   Reviewed the code count table", "7. Hurricane model components")
            refs = [
                {"physical_page": n - 1, "start": a0, "end": b0, "text": prev[a0:b0]},
                {"physical_page": n, "start": a1, "end": b1, "text": page[a1:b1]},
            ]
            boundary = "AUDIT_6_WITH_PAGE_CONTINUATION_AND_COMMENTS"
        elif lid in {"FG3L_44b259effabc1f58", "FG3L_9abdab4658738f64", "FG3L_18d2fb07596f74f1"}:
            # Include the attached answer when the fixed anchor is a copied disclosure prompt.
            pars = [
                (q.start(), q.end()) for q in re.finditer(r"[^\n]+(?:\n(?!\s*\n)[^\n]+)*", page)
            ]
            i = next(i for i, (aa, bb) in enumerate(pars) if aa <= anchor_raw < bb)
            if i + 1 < len(pars):
                b = pars[i + 1][1]
            refs = [{"physical_page": n, "start": a, "end": b, "text": page[a:b]}]
            boundary = "DISCLOSURE_PROMPT_AND_ATTACHED_RESPONSE"
        elif lid == "FG3L_086fc7cf20367b5b":
            a, b = span(page, "25. Form A-5", "Audit")
            refs = [{"physical_page": n, "start": a, "end": b, "text": page[a:b]}]
            boundary = "NUMBERED_PREVISIT_ITEM_25_WITH_ATTACHED_DISCUSSION"
        elif lid == "FG3L_4ed6206247fe6d31":
            # Numbered pre-visit comment ends at the next same-level item.
            a, b = span(page, "4. G-1.2, Vulnerability Matrices", "5. G-1.2")
            refs = [{"physical_page": n, "start": a, "end": b, "text": page[a:b]}]
            boundary = "NUMBERED_PREVISIT_ITEM_4"
        elif lid == "FG3L_199e296b691cc21d":
            a, b = span(page, "3. Justification for the vintage", "4. Supporting material")
            refs = [{"physical_page": n, "start": a, "end": b, "text": page[a:b]}]
            boundary = "NUMBERED_AUDIT_ITEM_3_AT_FIXED_ANCHOR"
        elif lid == "FG3L_936344c65a94bee4":
            next_page = docs[doc][n]
            a1, b1 = span(
                next_page, "The model produces the same loss costs", "2. Provide an overview"
            )
            refs = [
                {"physical_page": n, "start": a, "end": b, "text": page[a:b]},
                {"physical_page": n + 1, "start": a1, "end": b1, "text": next_page[a1:b1]},
            ]
            boundary = "DISCLOSURE_PROMPT_WITH_EXPLICIT_PAGE_CONTINUATION_RESPONSE"
        for ref in refs:
            original = docs[doc][ref["physical_page"] - 1]
            assert original[ref["start"] : ref["end"]] == ref["text"]
        if not any(
            ref["physical_page"] == n and ref["start"] <= anchor_raw < ref["end"] for ref in refs
        ):
            raise RuntimeError("source unit misses fixed anchor " + lid)
        payload = f"{doc}|" + "|".join(
            f"{r['physical_page']}:{r['start']}:{r['end']}" for r in refs
        )
        unit_id = "FG3U_" + hashlib.sha256(payload.encode()).hexdigest()[:20]
        text = "\n".join(r["text"].strip() for r in refs)
        out.append(
            {
                "source_unit_id": unit_id,
                "lead_id": lid,
                "panel": x["panel"],
                "document_id": doc,
                "document_role": x["document_role"],
                "standards_cycle": x["standards_cycle"],
                "source_sha256": x["source_sha256"],
                "anchor_query_id": x["anchor_query_id"],
                "anchor_text": x["anchor_text"],
                "source_refs": refs,
                "unit_text": text,
                "boundary_rule": boundary,
                "source_text_status": "EXACT_PDF_TEXT_EXTRACT_AND_RAW_MODE_ANCHOR_CONFIRMED",
                "context_status": "BOUNDARY_DRAFT_FOR_SOURCE_REVIEW",
            }
        )
    p = BASE / "checkpoint2/source_unit_drafts.jsonl"
    p.write_text("".join(json.dumps(r, ensure_ascii=False, sort_keys=True) + "\n" for r in out))
    print("source units", len(out), "output", p)


if __name__ == "__main__":
    main()
