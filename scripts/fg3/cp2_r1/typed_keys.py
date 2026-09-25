"""Source-ref-bearing typed identifiers for FG-3 CP2-R1 pairing."""

from __future__ import annotations

import re

DASHES = str.maketrans({dash: "-" for dash in "‐‑‒–—―−﹣－"})
ID = r"[A-Z]{1,2}[-‐‑‒–—―−﹣－]\d+(?:\.[A-Z0-9]+)?"
EXPLICIT = re.compile(rf"\b(Form|Forms|Standard|Standards)\s+({ID})\b", re.I)
BARE_HEADING = re.compile(rf"^\s*({ID})\s+[^\n]+", re.I)
NUMBERED_COMMENT_TARGET = re.compile(rf"^\s*\d+\.\s+({ID})(?:\.[A-Z])?\b", re.I)


def normalized_id(identifier: str) -> str:
    return identifier.translate(DASHES).upper()


def _key(
    document_id: str, ref: dict, local_start: int, local_end: int, kind: str, derivation: str
) -> dict:
    printed = ref["text"][local_start:local_end]
    identifier = re.search(ID, printed, re.I)
    if not identifier:
        raise ValueError("typed key does not contain a printed identifier")
    return {
        "key_text": printed,
        "key_type": kind,
        "normalized_key": f"{kind}:{normalized_id(identifier.group())}",
        "source_document_id": document_id,
        "source_page": ref["physical_page"],
        "source_span": [ref["start"] + local_start, ref["start"] + local_end],
        "source_ref": {
            "document_id": document_id,
            "physical_page": ref["physical_page"],
            "start": ref["start"] + local_start,
            "end": ref["start"] + local_end,
        },
        "derivation": derivation,
    }


def keys_from_refs(
    document_id: str, source_refs: list[dict], parent_heading_ref: dict | None
) -> list[dict]:
    results = []
    for ref in source_refs:
        for match in EXPLICIT.finditer(ref["text"]):
            kind = "FORM" if match.group(1).casefold().startswith("form") else "STANDARD"
            results.append(
                _key(document_id, ref, match.start(), match.end(), kind, "PRINTED_IN_UNIT")
            )
        # A numbered review comment may print its target as ``4. G-1.2, ...``.
        # A bare identifier elsewhere in prose does not establish its type.
        match = NUMBERED_COMMENT_TARGET.match(ref["text"])
        if match:
            results.append(
                _key(
                    document_id,
                    ref,
                    match.start(1),
                    match.end(1),
                    "STANDARD",
                    "PRINTED_NUMBERED_COMMENT_TARGET",
                )
            )
    if parent_heading_ref:
        text = parent_heading_ref["text"]
        match = EXPLICIT.search(text)
        if match:
            kind = "FORM" if match.group(1).casefold().startswith("form") else "STANDARD"
            results.append(
                _key(
                    document_id,
                    parent_heading_ref,
                    match.start(),
                    match.end(),
                    kind,
                    "PRINTED_IN_ALLOWED_PARENT_HEADING",
                )
            )
        else:
            match = BARE_HEADING.match(text)
            if match and parent_heading_ref.get("heading_family") == "STANDARD":
                results.append(
                    _key(
                        document_id,
                        parent_heading_ref,
                        match.start(1),
                        match.end(1),
                        "STANDARD",
                        "PRINTED_IN_ALLOWED_PARENT_HEADING",
                    )
                )
    distinct = {}
    for key in results:
        identity = (key["normalized_key"], key["source_page"], *key["source_span"])
        distinct[identity] = key
    return list(distinct.values())
