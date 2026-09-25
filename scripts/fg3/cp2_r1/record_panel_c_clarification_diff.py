"""Audit old broad-section counts against exact ID-bearing search anchors."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "experiments/fg3_natural_boundary/checkpoint2_r1"


def read(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text().splitlines()]


def main() -> None:
    broad = {row["lead_id"]: row for row in read(OUT / "panel_c_typed_counterpart_candidates.jsonl")}
    narrow = read(OUT / "panel_c_tier1_explicit_unit_candidates.jsonl")
    if len(broad) != 27 or len(narrow) != 27:
        raise ValueError("Panel C plan count changed")
    records = []
    for row in narrow:
        old = broad[row["lead_id"]]
        records.append(
            {
                "lead_id": row["lead_id"],
                "old_broad_section_paragraph_candidates": old["literal_candidate_count"],
                "old_preliminary_limit_exceeded": old["preliminary_limit_exceeded"],
                "new_printed_id_occurrences": row["identifier_occurrence_count"],
                "new_distinct_id_bearing_paragraphs": row["distinct_candidate_paragraph_count"],
                "new_rejected_toc_or_heading_occurrences": len(row["rejected_search_matches"]),
                "natural_unit_count": None,
                "final_overflow": None,
                "counts_comparable_as_recall": False,
                "new_status": row["pairing_status"],
                "permanently_secondary": row["permanently_secondary"],
            }
        )
    (OUT / "panel_c_broad_vs_explicit_diff.jsonl").write_text(
        "".join(json.dumps(item, ensure_ascii=False, sort_keys=True) + "\n" for item in records)
    )
    print(f"Recorded {len(records)} Panel C candidate-definition changes")


if __name__ == "__main__":
    main()
