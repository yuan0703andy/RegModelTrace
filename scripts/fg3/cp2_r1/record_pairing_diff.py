"""Record the old/nonconforming versus repaired candidate-set delta.

Counts use different search units and are descriptive, not comparable recall.
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
BASE = ROOT / "experiments/fg3_natural_boundary"
OUT = BASE / "checkpoint2_r1"


def read(path: Path) -> list[dict]:
    return [json.loads(x) for x in path.read_text().splitlines()]


def main() -> None:
    old = {x["lead_id"]: x for x in read(BASE / "checkpoint2/pairing_literal_audit.jsonl")}
    plans = {x["lead_id"]: x for x in read(OUT / "source_only_typed_key_plans.jsonl")}
    new = read(OUT / "panel_a_typed_section_candidates.jsonl") + read(OUT / "panel_c_typed_counterpart_candidates.jsonl")
    rows = []
    for value in new:
        old_value = old.get(value["lead_id"])
        rows.append(
            {
                "lead_id": value["lead_id"],
                "panel": plans[value["lead_id"]]["panel"],
                "old_status": old_value["pairing_audit_status"] if old_value else None,
                "old_literal_candidate_count": old_value["literal_candidate_count"] if old_value else None,
                "new_preliminary_status": value["pairing_status"],
                "new_candidate_count": value.get("candidate_paragraph_count", value.get("literal_candidate_count")),
                "new_typed_keys": value.get("typed_keys", []),
                "permanently_secondary": plans[value["lead_id"]]["permanently_secondary"],
                "counts_comparable_as_recall": False,
                "explanation": "The old whole-document literal paragraphs and new typed section/member candidates have different units and boundaries. Both are retained for provenance; neither is a final case pair.",
            }
        )
    (OUT / "old_new_pairing_diff.jsonl").write_text(
        "".join(json.dumps(x, sort_keys=True, ensure_ascii=False) + "\n" for x in rows)
    )
    print(f"Recorded {len(rows)} old/new pairing diagnostics")


if __name__ == "__main__":
    main()
