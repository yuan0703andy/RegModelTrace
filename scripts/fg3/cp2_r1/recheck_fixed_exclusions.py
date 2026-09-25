"""Recheck the 45 provisional fixed-anchor exits under the frozen panel targets.

The five vendor-facing procedural/conditional clauses are reopened for source
unit work; their original anchors are not changed and no counterpart is read.
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
BASE = ROOT / "experiments/fg3_natural_boundary"
OUT = BASE / "checkpoint2_r1"

REOPEN = {
    "FG3L_9b81ac232333a6cb": "A readable-medium instruction is explicitly directed to the modeling organization; procedural scope alone cannot exclude a mandatory-language contrast.",
    "FG3L_ac6bb57d3b40ccbe": "The modeling organization is required to present material, including trade-secret material; the illustrative/mandatory scope must be checked at the fixed anchor.",
    "FG3L_c62f1a244637491a": "The plan-of-action clause uses mandatory inclusion language for model revisions; conditional/procedural status does not itself exclude the semantic contrast.",
    "FG3L_42d833daa5f78bbf": "The certification template may impose a required representation of functional equivalence; source-unit hierarchy and applicability need verification.",
    "FG3L_4ec3103613af52bb": "The pre-visit materials list may be a vendor-facing mandatory disclosure; its including-clause cannot be excluded simply as administrative.",
}


def main() -> None:
    leads = {x["lead_id"]: x for x in map(json.loads, (BASE / "checkpoint2/lead_source_dossiers.jsonl").read_text().splitlines())}
    screen = [json.loads(x) for x in (BASE / "checkpoint2/lead_screening.jsonl").read_text().splitlines()]
    excluded = [x for x in screen if x["source_context_screening_status"] == "EXCLUDED_AT_FIXED_ANCHOR"]
    if len(excluded) != 45 or not REOPEN.keys() <= {x["lead_id"] for x in excluded}:
        raise ValueError("frozen exclusion membership drift")
    output = []
    for old in excluded:
        lead = leads[old["lead_id"]]
        reopened = old["lead_id"] in REOPEN
        output.append(
            {
                "lead_id": old["lead_id"],
                "panel": old["panel"],
                "document_id": old["document_id"],
                "physical_page": old["physical_page"],
                "source_sha256": lead["source_sha256"],
                "frozen_anchor_query_id": lead["anchor_query_id"],
                "frozen_anchor_start_in_normalized_page": lead["anchor_start_in_normalized_page"],
                "frozen_anchor_text": lead["anchor_text"],
                "old_status": old["source_context_screening_status"],
                "old_rationale": old["source_context_rationale"],
                "r1_status": "REOPEN_CANONICAL_SOURCE_UNIT_PENDING" if reopened else "ORIGINAL_EXCLUSION_RETAINED_PENDING_PDF_REVIEW",
                "r1_reason": REOPEN.get(old["lead_id"], "The original first-anchor rationale identifies a non-target source role, prospective-only action, glossary/copy, or unrelated causal/change object; no later occurrence was substituted."),
                "counterpart_search_executed": False,
                "human_gold": None,
                "primary_eligible": False,
            }
        )
    (OUT / "fixed_anchor_exclusion_recheck.jsonl").write_text(
        "".join(json.dumps(x, ensure_ascii=False, sort_keys=True) + "\n" for x in output)
    )
    print(f"Rechecked {len(output)} fixed-anchor exits; reopened {sum(x['r1_status'].startswith('REOPEN') for x in output)} for source-unit verification")


if __name__ == "__main__":
    main()
