"""Exact-overlap candidates under the frozen FG-3 exposure file manifest.

Matches never confer exposure clearance or semantic equivalence.
"""

from __future__ import annotations

import hashlib
import json
import re
import unicodedata
from pathlib import Path
from typing import Iterator

ALGORITHM_VERSION = "FG3-CP2-R1-EXACT-12-STRIDE1-JSON-VALUES-v1"


def tokens(text: str) -> list[str]:
    logical = unicodedata.normalize("NFKC", text)
    return re.findall(r"\S+", logical.casefold())


def windows(text: str) -> set[tuple[str, ...]]:
    words = tokens(text)
    return {tuple(words[i : i + 12]) for i in range(max(0, len(words) - 11))}


def json_strings(value: object, pointer: str = "") -> Iterator[tuple[str, str]]:
    if isinstance(value, str):
        yield pointer or "/", value
    elif isinstance(value, list):
        for index, child in enumerate(value):
            yield from json_strings(child, f"{pointer}/{index}")
    elif isinstance(value, dict):
        for key, child in value.items():
            escaped = str(key).replace("~", "~0").replace("/", "~1")
            yield from json_strings(child, f"{pointer}/{escaped}")


def text_segments(path: Path, raw: bytes) -> Iterator[tuple[str, str]]:
    content = raw.decode("utf-8")
    if path.suffix.lower() == ".json":
        yield from json_strings(json.loads(content))
    elif path.suffix.lower() == ".jsonl":
        for line_number, line in enumerate(content.splitlines(), 1):
            if line.strip():
                yield from json_strings(json.loads(line), f"/line/{line_number}")
    else:
        yield "/text", content


def scan_unit(unit_text: str, manifest: dict, root: Path) -> tuple[list[dict], list[dict]]:
    query_windows = windows(unit_text)
    matches: list[dict] = []
    failures: list[dict] = []
    for item in manifest["files"]:
        path = root / item["path"]
        raw = path.read_bytes()
        if hashlib.sha256(raw).hexdigest() != item["sha256"]:
            raise ValueError(f"Frozen exposure file hash mismatch: {item['path']}")
        try:
            segments = text_segments(path, raw)
            for pointer, text in segments:
                words = tokens(text)
                found = set()
                for i in range(max(0, len(words) - 11)):
                    candidate = tuple(words[i : i + 12])
                    if candidate in query_windows:
                        found.add(" ".join(candidate))
                for phrase in sorted(found):
                    matches.append(
                        {
                            "file_path": item["path"],
                            "json_pointer_or_text": pointer,
                            "exact_12_token_phrase": phrase,
                        }
                    )
        except (UnicodeDecodeError, json.JSONDecodeError) as error:
            failures.append(
                {
                    "file_path": item["path"],
                    "failure": type(error).__name__,
                    "message": str(error),
                }
            )
    return matches, failures
