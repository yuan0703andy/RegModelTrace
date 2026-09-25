"""Typed heading and bounded-section candidates for Panel A source review.

The scanner returns *candidates*. Ambiguous headings or boundaries must be
reviewed from the original PDF before a section is certified for pairing.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

from .typed_keys import normalized_id

IDENTIFIER = r"[A-Z]{1,2}[-‐‑‒–—―−﹣－]\d+(?:\.\d+)?"
FORM_HEADING = re.compile(rf"(?m)^[ \t]{{0,8}}Form\s+({IDENTIFIER})\s*:\s*([^\n]+)", re.I)
APPENDIX_FORM_HEADING = re.compile(
    rf"(?m)^[ \t]{{0,8}}Appendix\s+[A-Z0-9]+\s*[–—-]\s*Form\s+({IDENTIFIER})\s*:\s*([^\n]+)",
    re.I,
)
STANDARD_HEADING = re.compile(rf"(?m)^[ \t]{{0,8}}({IDENTIFIER})\s+([A-Z][^\n]+)", re.I)
APPENDIX_HEADING = re.compile(r"(?m)^[ \t]{0,8}APPENDIX\s+[A-Z0-9]+\s*[–—-]", re.I)


@dataclass(frozen=True)
class Heading:
    key_type: str
    normalized_key: str
    physical_page: int
    start: int
    end: int
    text: str


def headings(pages: list[str]) -> list[Heading]:
    result = []
    for page_number, page in enumerate(pages, 1):
        for kind, pattern in (
            ("FORM", APPENDIX_FORM_HEADING),
            ("FORM", FORM_HEADING),
            ("STANDARD", STANDARD_HEADING),
        ):
            for match in pattern.finditer(page):
                printed = match.group().strip()
                if "...." in printed or re.search(r"\s\d{1,3}$", printed):
                    continue  # TOC candidate, never a section boundary.
                if re.search(r"\s{10,}Appendix\s+[A-Z0-9]+\s*$", printed, re.I):
                    continue  # Running appendix header, not a new section.
                if kind == "FORM" and not printed.casefold().startswith("appendix "):
                    continuation = page[match.end() : match.end() + 100]
                    if re.match(r"\s*See Appendix\b", continuation, re.I):
                        continue  # A pointer to the Form, not the Form section.
                result.append(
                    Heading(
                        key_type=kind,
                        normalized_key=f"{kind}:{normalized_id(match.group(1))}",
                        physical_page=page_number,
                        start=match.start(),
                        end=match.end(),
                        text=page[match.start() : match.end()],
                    )
                )
    distinct = {(h.physical_page, h.start, h.end, h.normalized_key): h for h in result}
    return sorted(distinct.values(), key=lambda h: (h.physical_page, h.start, h.key_type))


def section_candidates(pages: list[str], normalized_key: str) -> list[dict]:
    """Return every typed matching section with a following-boundary witness."""
    all_headings = headings(pages)
    result = []
    for index, heading in enumerate(all_headings):
        if heading.normalized_key != normalized_key:
            continue
        next_headings = [
            later for later in all_headings[index + 1 :] if later.key_type == heading.key_type
        ]
        next_heading = next_headings[0] if next_headings else None
        following_appendices = []
        for page_number in range(heading.physical_page, len(pages) + 1):
            page = pages[page_number - 1]
            for match in APPENDIX_HEADING.finditer(page):
                if (page_number, match.start()) > (heading.physical_page, heading.start):
                    following_appendices.append((page_number, match.start(), match.group()))
        boundaries = []
        if next_heading:
            boundaries.append((next_heading.physical_page, next_heading.start, "NEXT_SAME_TYPE_HEADING", next_heading.text))
        boundaries += [
            (page_number, offset, "NEXT_APPENDIX_HEADING", printed)
            for page_number, offset, printed in following_appendices
        ]
        boundary = min(boundaries, key=lambda x: (x[0], x[1])) if boundaries else None
        result.append(
            {
                "heading": heading.__dict__,
                "end_boundary": (
                    {
                        "physical_page": boundary[0],
                        "start": boundary[1],
                        "kind": boundary[2],
                        "text": boundary[3],
                    }
                    if boundary
                    else None
                ),
                "status": "SECTION_BOUNDARY_CANDIDATE_NEEDS_SOURCE_REVIEW" if boundary else "SECTION_END_UNRESOLVED",
            }
        )
    return result
