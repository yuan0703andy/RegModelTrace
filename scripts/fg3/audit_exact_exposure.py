"""List exact textual overlap with the frozen known-exposure ledger.

This is candidate generation for source-only review, never exposure clearance.
"""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT / "experiments/fg3_natural_boundary"
OUT = BASE / "checkpoint2"


def rows(path: Path):
    return [json.loads(line) for line in path.read_text().splitlines()]


def normalize(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip().casefold()


def windows(value: str, width: int = 12):
    tokens = normalize(value).split()
    return sorted(
        set(
            " ".join(tokens[start : start + width])
            for start in range(0, max(0, len(tokens) - width + 1), 3)
            if len(" ".join(tokens[start : start + width])) >= 70
        )
    )


def main() -> None:
    manifest = json.loads((BASE / "protocol/known_exposure_file_manifest_v1.json").read_text())
    ledger = []
    for item in manifest["files"]:
        raw = (ROOT / item["path"]).read_bytes()
        if hashlib.sha256(raw).hexdigest() != item["sha256"]:
            raise ValueError(f"Frozen exposure ledger drift: {item['path']}")
        try:
            content = raw.decode("utf-8")
        except UnicodeDecodeError:
            continue
        ledger.append((item["path"], normalize(content)))

    unit_rows = []
    for unit in rows(OUT / "source_unit_drafts.jsonl"):
        phrases = windows(unit["unit_text"])
        files = sorted(
            path for path, content in ledger if any(phrase in content for phrase in phrases)
        )
        unit_rows.append(
            {
                "lead_id": unit["lead_id"],
                "source_unit_id": unit["source_unit_id"],
                "exact_12_token_match_files": files,
                "method": "12-token normalized source-unit windows at stride 3, minimum 70 characters, searched against 347 checksum-verified textual ledger files; exact candidates only",
            }
        )
    (OUT / "unit_exact_exposure_matches.jsonl").write_text(
        "".join(json.dumps(row, sort_keys=True) + "\n" for row in unit_rows)
    )

    pair_rows = []
    for audit in rows(OUT / "pairing_literal_audit.jsonl"):
        matches = []
        for candidate in audit["literal_candidates"]:
            phrases = windows(candidate["text"])
            files = sorted(
                path for path, content in ledger if any(phrase in content for phrase in phrases)
            )
            if files:
                matches.append(
                    {
                        "physical_page": candidate["physical_page"],
                        "start": candidate["start"],
                        "end": candidate["end"],
                        "files": files,
                    }
                )
        pair_rows.append({"lead_id": audit["lead_id"], "counterpart_exact_matches": matches})
    (OUT / "counterpart_exact_exposure_matches.jsonl").write_text(
        "".join(json.dumps(row, sort_keys=True) + "\n" for row in pair_rows)
    )
    print(
        f"Checked {len(unit_rows)} source units and {len(pair_rows)} pairing audits against {len(manifest['files'])} ledger files"
    )


if __name__ == "__main__":
    main()
