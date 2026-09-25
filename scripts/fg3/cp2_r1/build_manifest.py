"""Hash-reference frozen FG-3 inputs and the CP2-R1 repair artifacts."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
BASE = ROOT / "experiments/fg3_natural_boundary"
OUT = BASE / "checkpoint2_r1"

FROZEN = [
    "experiments/fg3_natural_boundary/protocol/spec.md",
    "experiments/fg3_natural_boundary/protocol/v1_3_amendment_receipt.json",
    "experiments/fg3_natural_boundary/protocol/discovery_protocol.json",
    "experiments/fg3_natural_boundary/protocol/case_formation_protocol.json",
    "experiments/fg3_natural_boundary/protocol/known_exposure_ledger_v1.json",
    "experiments/fg3_natural_boundary/protocol/known_exposure_file_manifest_v1.json",
    "experiments/fg3_natural_boundary/candidates/discovery_manifest.json",
    "experiments/fg3_natural_boundary/checkpoint2/lead_source_dossiers.jsonl",
]


def record(path: Path) -> dict:
    data = path.read_bytes()
    return {
        "path": str(path.relative_to(ROOT)),
        "bytes": len(data),
        "sha256": hashlib.sha256(data).hexdigest(),
    }


def main() -> None:
    paths = [ROOT / x for x in FROZEN]
    paths += sorted(x for x in OUT.iterdir() if x.is_file() and x.name != "cp2_r1_manifest.json")
    paths += sorted(x for x in (ROOT / "scripts/fg3/cp2_r1").rglob("*.py") if "__pycache__" not in x.parts)
    paths += sorted((ROOT / "openspec/changes/fg3-cp2-r1").rglob("*.md"))
    entries = [record(x) for x in paths]
    manifest = {
        "status": "CP2_R1_ARTIFACT_CUSTODY_ONLY_NOT_CHECKPOINT_PASS",
        "frozen_protocol_commit": "92eb571dc19c7a424a766f758f9bcbbd7a2c3632",
        "initial_source_only_key_plan_commit": "e6a04df8",
        "subsequent_source_only_change": "Panel B source-unit inclusion was adjudicated after the initial plan commit; A/C source keys were unchanged.",
        "entries": entries,
    }
    (OUT / "cp2_r1_manifest.json").write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")
    print(f"Hashed {len(entries)} frozen inputs and repair files")


if __name__ == "__main__":
    main()
