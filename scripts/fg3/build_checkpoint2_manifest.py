"""Hash the provisional FG-3 Checkpoint 2 audit without upgrading its status."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT / "experiments/fg3_natural_boundary"
OUT = BASE / "checkpoint2"


def entry(path: Path) -> dict:
    raw = path.read_bytes()
    return {
        "path": str(path.relative_to(ROOT)),
        "sha256": hashlib.sha256(raw).hexdigest(),
        "bytes": len(raw),
    }


def main() -> None:
    frozen = [
        BASE / "candidates/source_leads.jsonl",
        BASE / "candidates/discovery_manifest.json",
        BASE / "protocol/case_formation_protocol.json",
        BASE / "protocol/known_exposure_file_manifest_v1.json",
        BASE / "protocol/known_exposure_ledger_v1.json",
    ]
    outputs = sorted(
        p for p in OUT.iterdir() if p.is_file() and p.name != "checkpoint2_manifest.json"
    )
    scripts = sorted((ROOT / "scripts/fg3").glob("*.py"))
    manifest = {
        "status": "IN_PROGRESS_NOT_CHECKPOINT_PASS",
        "frozen_inputs": [entry(p) for p in frozen],
        "audit_outputs": [entry(p) for p in outputs],
        "scripts": [entry(p) for p in scripts],
        "scientific_eligibility_claimed": False,
        "human_gold_records": 0,
        "model_runs": 0,
    }
    (OUT / "checkpoint2_manifest.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n"
    )
    print(f"Manifested {len(outputs)} audit files and {len(scripts)} scripts")


if __name__ == "__main__":
    main()
