"""Run repaired exact-overlap scanner over source units only.

An unmatched unit remains UNKNOWN_EXPOSURE pending substantial-equivalence
review. This script never marks exposure clear or primary eligible.
"""

from __future__ import annotations

import json
from pathlib import Path

from .exposure import ALGORITHM_VERSION, scan_unit

ROOT = Path(__file__).resolve().parents[3]
BASE = ROOT / "experiments/fg3_natural_boundary"
OUT = BASE / "checkpoint2_r1"


def main() -> None:
    manifest = json.loads((BASE / "protocol/known_exposure_file_manifest_v1.json").read_text())
    units = [json.loads(line) for line in (OUT / "canonical_source_units.jsonl").read_text().splitlines()]
    records = []
    for unit in units:
        matches, failures = scan_unit(unit["unit_text"], manifest, ROOT)
        records.append(
            {
                "lead_id": unit["lead_id"],
                "unit_id": unit["unit_id"],
                "algorithm_version": ALGORITHM_VERSION,
                "files_verified": len(manifest["files"]),
                "exact_overlap_candidates": matches,
                "parse_failures": failures,
                "exposure_status": "CANDIDATE_REQUIRES_ROLE_AND_EQUIVALENCE_REVIEW" if matches else "UNKNOWN_EXPOSURE_NOT_CLEARED_BY_EXACT_SEARCH",
                "primary_eligible": False,
            }
        )
    (OUT / "source_exact_exposure_candidates.jsonl").write_text(
        "".join(json.dumps(x, ensure_ascii=False, sort_keys=True) + "\n" for x in records)
    )
    print(f"Scanned {len(records)} source units; {sum(bool(x['exact_overlap_candidates']) for x in records)} have exact candidates; {sum(bool(x['parse_failures']) for x in records)} have parse failures")


if __name__ == "__main__":
    main()
