"""Rebuild source-only units without changing frozen FG-3 leads or anchors.

Every exceptional boundary is a printed source marker, never a semantic target.
Unresolved units remain in the ledger and cannot enter primary pairing.
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


def rows(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text().splitlines()]


def pages(path: Path) -> list[str]:
    result = subprocess.run(
        ["pdftotext", "-layout", "-enc", "UTF-8", str(path), "-"],
        capture_output=True,
        text=True,
        check=True,
    )
    values = result.stdout.split("\f")
    if values and not values[-1].strip():
        values.pop()
    return values


def unique_span(page: str, start: str, end: str) -> tuple[int, int]:
    if page.count(start) != 1:
        raise ValueError(f"start marker is not unique: {start}")
    a = page.index(start)
    if page.count(end, a + len(start)) != 1:
        raise ValueError(f"end marker is not unique after start: {end}")
    return a, page.index(end, a + len(start))


def source_ref(page_text: str, page_number: int, start: int, end: int) -> dict:
    if not 0 <= start < end <= len(page_text):
        raise ValueError("invalid source span")
    return {
        "physical_page": page_number,
        "start": start,
        "end": end,
        "text": page_text[start:end],
    }


def printed_heading(page_text: str, page_number: int, text: str, kind: str | None = None) -> dict:
    if page_text.count(text) != 1:
        raise ValueError(f"heading not unique: {text}")
    a = page_text.index(text)
    ref = source_ref(page_text, page_number, a, a + len(text))
    if kind:
        ref["heading_family"] = kind
    return ref


def repaired_refs(lead_id: str, doc_pages: list[str], draft: dict) -> tuple[list[dict], dict | None, str, str | None]:
    """Return refs, parent-heading override, end witness, or source-only exit."""
    if lead_id == "FG3L_464684973341bd4c":
        return draft["source_refs"], None, "FIGURE_CAPTION_ONLY", "FIXED_ANCHOR_CAPTION_WITHOUT_SUBSTANTIVE_VENDOR_CLAIM"
    if lead_id in {"FG3L_790bc4c0e7c53a42", "FG3L_890ac5146ded6275"}:
        return draft["source_refs"], None, "PARENT_HEADING_NOT_ESTABLISHED", "SOURCE_UNIT_HIERARCHY_UNRESOLVED"
    if lead_id == "FG3L_2b40fc1569aee3c3":
        return draft["source_refs"], None, "NEXT_NUMBERED_ITEM", "PANEL_B_COMPOUND_STATUS_UNRESOLVED"

    def on(page_number: int, start: str, end: str) -> dict:
        page = doc_pages[page_number - 1]
        a, b = unique_span(page, start, end)
        return source_ref(page, page_number, a, b)

    if lead_id == "FG3L_6f53a0cfedaf6849":
        ref = on(
            59,
            "20. A-3.B, page 319:",
            "                                               59",
        )
        return [ref], None, "NUMBERED_ITEM_20_TO_PHYSICAL_PAGE_FOOTER", None
    numbered_reviewer_items = {
        "FG3L_3be8237cdfa15ed2": (20, "1. The statistical goodness-of-fit", "2. The method and supporting material"),
        "FG3L_e2057e9306160d6c": (23, "5. The previous and current hurricane parameters", "6. For windfields not previously reviewed"),
        "FG3L_5ad54c3b24878917": (28, "4. Justification for the variation", "5. Methods (including any software)"),
        "FG3L_a53b716eb384ff7c": (41, "15. Form V-1, pages 591-594:", "Audit\n\n1. Supporting material"),
    }
    if lead_id in numbered_reviewer_items:
        page_number, start, end = numbered_reviewer_items[lead_id]
        return [on(page_number, start, end)], None, "NEXT_SAME_LEVEL_REVIEW_ITEM_OR_AUDIT_SECTION", None
    verified_review_comments = {
        "FG3L_6c1ee859ddc2b2fa",
        "FG3L_886b02414646aaef",
        "FG3L_cd52022a16054dc1",
        "FG3L_036eb6d3e6f0d413",
    }
    if lead_id in verified_review_comments:
        page_number = draft["source_refs"][0]["physical_page"]
        page = doc_pages[page_number - 1]
        match = re.search(r"(?m)^Verified:\s+YES\s*$", page)
        if not match:
            raise ValueError(f"verified disposition not found: {lead_id}")
        disposition = source_ref(page, page_number, match.start(), match.end())
        return [disposition, *draft["source_refs"]], None, "VERIFIED_DISPOSITION_AND_ATTACHED_UNNUMBERED_COMMENT", None
    if lead_id == "FG3L_8c88e4e755a7923c":
        heading = printed_heading(
            doc_pages[117],
            118,
            "G-2 Qualifications of Modeling Organization Personnel and\n"
            "    Consultants Engaged in Development and Implementation\n"
            "    of the Hurricane Model*",
            "STANDARD",
        )
        return draft["source_refs"], heading, "NEXT_LETTERED_SUBSECTION", None
    if lead_id == "FG3L_18d2fb07596f74f1":
        return [on(274, "1. Describe any modifications", "2. Provide a flowchart")], None, "NEXT_NUMBERED_DISCLOSURE", None
    if lead_id == "FG3L_3ae09c36fb37f2e7":
        first = on(268, "      Treatment of water infiltration", "FPHLM V8.3 May 30th")
        second = on(269, "                                                                                        ( V1-10 )", "Rain admittance factor, RAF")
        heading = printed_heading(doc_pages[267], 268, "Treatment of water infiltration in the commercial residential mid/high-rise model")
        return [first, second], heading, "NEXT_SUBHEADING_ON_PAGE_269", None
    if lead_id == "FG3L_6cdb30a54d7fbce5":
        ref = on(372, "Standard A-2:", "Standard A-3:")
        heading = printed_heading(doc_pages[371], 372, "Standard A-2:", "STANDARD")
        return [ref], heading, "NEXT_PRINTED_STANDARD_IN_LETTER", None
    if lead_id == "FG3L_a1c2811f877b0acd":
        ref = on(509, "Notional Set 1 – Deductible Sensitivity", "Notional Set 2 – Policy Form Sensitivity")
        heading = printed_heading(doc_pages[508], 509, "Notional Set 1 – Deductible Sensitivity")
        return [ref], heading, "NEXT_NOTIONAL_SET_HEADING", None
    if lead_id == "FG3L_1284d77ca859d9fd":
        first = on(600, "B. Confirm that the structures", "FPHLM V8.3 May 30th")
        second = on(601, "value at $100,000 will produce", "C. Provide separate plots")
        heading = printed_heading(doc_pages[597], 598, "Appendix R – Form V-1: One Hypothetical Event", "FORM")
        return [first, second], heading, "NEXT_LETTERED_FORM_SUBSECTION", None
    if lead_id == "FG3L_de59a1b8a204553a":
        ref = on(622, "C. Provide a summary description", "D. Provide this form")
        heading = printed_heading(
            doc_pages[620],
            621,
            "Appendix U – Form V-4: Differences in Hurricane Mitigation Measures and\n"
            " Secondary Characteristics",
            "FORM",
        )
        return [ref], heading, "NEXT_LETTERED_FORM_SUBSECTION", None
    return draft["source_refs"], None, draft["boundary_rule"], None


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    drafts = rows(BASE / "checkpoint2/source_unit_drafts.jsonl")
    leads = {row["lead_id"]: row for row in rows(BASE / "checkpoint2/lead_source_dossiers.jsonl")}
    audit = {row["lead_id"]: row for row in rows(OUT / "source_unit_boundary_audit.jsonl")}
    docs = {}
    result = []
    for draft in drafts:
        lead_id = draft["lead_id"]
        lead = leads[lead_id]
        document_id = draft["document_id"]
        if document_id not in docs:
            pdf = ROOT / lead["source_path"]
            if hashlib.sha256(pdf.read_bytes()).hexdigest() != lead["source_sha256"]:
                raise ValueError("source PDF drift")
            docs[document_id] = pages(pdf)
        doc_pages = docs[document_id]
        refs, override_heading, witness, exit_reason = repaired_refs(lead_id, doc_pages, draft)
        parent = override_heading or audit[lead_id]["parent_heading_candidate"]
        for ref in refs:
            page = doc_pages[ref["physical_page"] - 1]
            if page[ref["start"] : ref["end"]] != ref["text"]:
                raise ValueError(f"source span drift: {lead_id}")
        if parent:
            page = doc_pages[parent["physical_page"] - 1]
            if page[parent["start"] : parent["end"]] != parent["text"]:
                raise ValueError(f"parent heading drift: {lead_id}")
        # The anchor was already mapped from its frozen normalized offset; it must
        # occur in the repaired source refs on the same physical page.
        normalized_anchor = lead["anchor_text"].casefold()
        if not any(
            normalized_anchor in re.sub(r"\s+", " ", ref["text"]).casefold()
            and ref["physical_page"] == lead["physical_page"]
            for ref in refs
        ):
            raise ValueError(f"repaired unit lost anchor: {lead_id}")
        status = "SOURCE_UNIT_UNRESOLVED" if exit_reason else "BOUNDARY_CANDIDATE_REQUIRES_FINAL_VERIFICATION"
        text = "\n".join(ref["text"].strip() for ref in refs)
        result.append(
            {
                "lead_id": lead_id,
                "legacy_source_unit_id": draft["source_unit_id"],
                "document_id": document_id,
                "source_sha256": draft["source_sha256"],
                "source_refs": refs,
                "unit_text": text,
                "physical_page_start": refs[0]["physical_page"],
                "physical_page_end": refs[-1]["physical_page"],
                "raw_start": refs[0]["start"],
                "raw_end": refs[-1]["end"],
                "parent_heading_source_ref": parent,
                "boundary_rule": draft["boundary_rule"],
                "boundary_end_witness": witness,
                "boundary_verification": status,
                "exit_reason": exit_reason,
                "primary_eligible": False,
            }
        )
    (OUT / "repaired_source_unit_candidates.jsonl").write_text(
        "".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in result)
    )
    print(f"Rebuilt {len(result)} source-unit candidates; final boundary verification remains separate")


if __name__ == "__main__":
    main()
