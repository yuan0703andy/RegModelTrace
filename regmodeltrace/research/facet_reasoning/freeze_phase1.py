"""Freeze double-adjudicated facet truth and B/C requests before inference."""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .adjudication import agreement, validate_return
from .aggregate import AGGREGATION_RULE_VERSION, aggregate_relation
from .baselines import build_request
from .schema import EvidenceSufficiency, FacetCase, FacetDefinition, FacetState


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write(path: Path, value: Any) -> None:
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8")


def adjudicated_cases(pilot_path: Path, resolution: dict[str, Any]) -> list[FacetCase]:
    pilot = {case["case_id"]: case for case in load(pilot_path)}
    resolved = {case["case_id"]: case for case in resolution["cases"]}
    if set(pilot) != set(resolved):
        raise ValueError("Resolution and pilot case identities differ")
    cases = []
    for case_id in sorted(pilot):
        base = dict(pilot[case_id])
        outcome = resolved[case_id]
        allowed_ids = {item["proposition_id"] for item in base["evidence"]}
        facets = []
        for item in outcome["facets"]:
            support = set(item["supporting_proposition_ids"])
            limits = set(item["limiting_proposition_ids"])
            if not support | limits <= allowed_ids:
                raise ValueError(f"Unknown proposition membership in {case_id}/{item['facet_id']}")
            facets.append(
                FacetDefinition(
                    facet_id=item["facet_id"],
                    text=item["text_confirmed_or_revised"],
                    state=FacetState(item["state"]),
                    supporting_proposition_ids=sorted(support),
                    limiting_proposition_ids=sorted(limits),
                    annotation_status="RESOLVED_DOUBLE_HUMAN_FACET_TRUTH",
                ).model_dump(mode="json")
            )
        base["facets"] = facets
        base["constraint_status"] = outcome["constraint_status"]
        base["evidence_sufficiency"] = outcome["evidence_sufficiency"]
        base["relation"] = outcome["overall_relation"]
        base["truth_status"] = "FROZEN_HUMAN_FACET_TRUTH"
        case = FacetCase.model_validate(base)
        expected = aggregate_relation(
            constraint_status=case.constraint_status,
            evidence_sufficiency=case.evidence_sufficiency or EvidenceSufficiency.INSUFFICIENT,
            facet_states=[facet.state for facet in case.facets if facet.state is not None],
        )
        if expected != case.relation:
            raise ValueError(
                f"Human relation conflicts with frozen aggregation for {case_id}: {case.relation} != {expected}"
            )
        cases.append(case)
    return cases


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--pilot", type=Path, required=True)
    parser.add_argument("--adjudicator-a", type=Path, required=True)
    parser.add_argument("--adjudicator-b", type=Path, required=True)
    parser.add_argument("--resolution", type=Path, required=True)
    parser.add_argument("--annotation-guide", type=Path, required=True)
    parser.add_argument("--aggregation-rule", type=Path, required=True)
    parser.add_argument("--model-config", type=Path, required=True)
    parser.add_argument("--decision-rule", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    if args.output.exists():
        raise RuntimeError("Refusing to overwrite an FT-1 freeze")
    a, b, resolution = load(args.adjudicator_a), load(args.adjudicator_b), load(args.resolution)
    report = agreement(a, b)
    validate_return(resolution)
    if not resolution.get("resolution_panel"):
        raise ValueError("Resolution must identify the human resolution panel")
    cases = adjudicated_cases(args.pilot, resolution)

    args.output.mkdir(parents=True)
    write(args.output / "agreement_report.json", report)
    write(args.output / "truth.json", [case.model_dump(mode="json") for case in cases])
    requests = []
    for case in cases:
        requests.extend([build_request(case, "B"), build_request(case, "C")])
    with (args.output / "model_requests.jsonl").open("w", encoding="utf-8") as handle:
        for request in requests:
            handle.write(json.dumps(request, ensure_ascii=False, sort_keys=True) + "\n")
    for source, name in [
        (args.adjudicator_a, "adjudicator_a_return.json"),
        (args.adjudicator_b, "adjudicator_b_return.json"),
        (args.resolution, "resolution_return.json"),
        (args.annotation_guide, "annotation_guide.md"),
        (args.aggregation_rule, "aggregation_rule.json"),
        (args.model_config, "model_config.json"),
        (args.decision_rule, "decision_rule.json"),
    ]:
        shutil.copy2(source, args.output / name)
    files = sorted(path for path in args.output.iterdir() if path.name != "freeze.json")
    lock = {
        "version": "ft1-phase1-1.0",
        "status": "FROZEN_BEFORE_INFERENCE",
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "aggregation_rule_version": AGGREGATION_RULE_VERSION,
        "conditions": ["B", "C"],
        "condition_a": "SAVED_HISTORICAL_RESULTS_ONLY",
        "condition_d": "NOT_AUTHORIZED",
        "files": {path.name: sha(path) for path in files},
    }
    write(args.output / "freeze.json", lock)


if __name__ == "__main__":
    main()
