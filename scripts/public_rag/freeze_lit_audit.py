"""Freeze a source-only LIT-RAGBench judge-audit subset before answers exist."""

from __future__ import annotations

import hashlib
import json
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
ARCHIVE = ROOT / "experiments/public_rag/datasets/official/LIT-RAGBench-5c3f30d924bc1615c08eb85f560f3aceb2fac7d4.zip"
OUTPUT = ROOT / "experiments/public_rag/lit_scorer/audit_subset.json"
SALT = "RegModelTrace-LIT-A0.4c-human-audit-v1"
EXPECTED_SHA = "471cbae289bdb0bdf44f4b3d4bbd44a668eae2b18902db695c2e0dd7ed1abef0"
LETTERS = "IRLTA"


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def main() -> None:
    assert digest(ARCHIVE.read_bytes()) == EXPECTED_SHA
    with zipfile.ZipFile(ARCHIVE) as zf:
        name = next(name for name in zf.namelist() if name.endswith("/datasets/en.jsonl"))
        source = zf.read(name)
    rows = [json.loads(line) for line in source.splitlines() if line.strip()]
    assert len(rows) == 114

    selected: list[int] = []
    by_type: dict[str, list[int]] = {}
    # Multi-label rows may qualify for several strata, but each is selected once.
    # The fixed type order and hash priority make the assignment reproducible.
    for letter in LETTERS:
        candidates = [
            i for i, row in enumerate(rows)
            if i not in selected and any(str(t).startswith(letter + "_") for t in row["qa_type"])
        ]
        candidates.sort(key=lambda i: digest(f"{SALT}|{letter}|{i}".encode()))
        assert len(candidates) >= 6, letter
        by_type[letter] = candidates[:6]
        selected.extend(candidates[:6])

    assert len(selected) == len(set(selected)) == 30
    output = {
        "status": "FROZEN_BEFORE_GENERATOR_OR_JUDGE_OUTPUT",
        "source_archive_sha256": EXPECTED_SHA,
        "english_dataset_sha256": digest(source),
        "language": "en",
        "row_identity": "zero_based_line_index_in_official_en_jsonl",
        "salt": SALT,
        "selection_rule": "Six previously unselected cases per I, R, L, T, A stratum, ordered by SHA-256(salt|stratum|row_index); multi-label rows selected once in fixed IRLTA order.",
        "strata": by_type,
        "row_indices": sorted(selected),
        "audit_rule": "Two humans score answer correctness independently and mark ambiguous cases; compare fixed local judge with adjudicated human labels, preserving disagreements rather than dropping cases.",
        "qualification_status": "PENDING_GENERATOR_OUTPUT_AND_HUMAN_AUDIT",
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(output, indent=2, ensure_ascii=False) + "\n")
    print(json.dumps({"audit_rows": len(selected), "strata": by_type, "sha256": digest(OUTPUT.read_bytes())}))


if __name__ == "__main__":
    main()
