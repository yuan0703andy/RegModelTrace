"""Build the FT-1 historical inventory and blinded human pilot.

This module never manufactures facet truth.  It imports explicit historical
human facet decisions where available and otherwise leaves states blank.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

from .schema import EvidenceProposition, FacetCase, FacetDefinition, FacetState
from .metrics import classification_metrics


CORPUS_METADATA = {
    "alignment-v2-2-pilot-1.0": {
        "corpus_id": "rms-ara-2019-development",
        "model_version_group": "fchlpm-2019",
        "review_ancestry": "fchlpm-2019-review-lineage",
    },
    "alignment-impact-2023-v2-2-1.0": {
        "corpus_id": "impact-forecasting-2023",
        "model_version_group": "fchlpm-2023-impact",
        "review_ancestry": "fchlpm-2023-impact-review",
    },
    "alignment-corelogic-2023-v2-2-1.0": {
        "corpus_id": "corelogic-cotality-2023",
        "model_version_group": "fchlpm-2023-corelogic",
        "review_ancestry": "fchlpm-2023-corelogic-review",
    },
    "alignment-verisk-2023-v2-2-1.0": {
        "corpus_id": "verisk-2023-validation-d",
        "model_version_group": "fchlpm-2023-verisk",
        "review_ancestry": "fchlpm-2023-verisk-review",
    },
    "alignment-kcc-2023-test-e-v2-2-1.0": {
        "corpus_id": "kcc-2023-exposed-test-e",
        "model_version_group": "fchlpm-2023-kcc",
        "review_ancestry": "fchlpm-2023-kcc-review",
    },
}


def canonical_json_bytes(value: Any) -> bytes:
    return (json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(",", ":")) + "\n").encode()


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def text_hash(text: str) -> str:
    return hashlib.sha256(" ".join(text.split()).encode()).hexdigest()


def load_json(path: Path) -> Any:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def requirement_family(requirement_id: str) -> str:
    match = re.search(r"(?:^|[-:])((?:CI)|[GMSVA])-?\d+", requirement_id.upper())
    return match.group(1) if match else "OTHER"


def explicit_facet_decisions(record: dict[str, Any]) -> list[dict[str, Any]]:
    return list(record.get("vendor_dimension", {}).get("facet_decisions") or [])


def requirement_facets(record: dict[str, Any]) -> list[str]:
    req = record["requirement_dimension"]
    candidates = req.get("required_facets") or []
    if candidates:
        return [str(item) for item in candidates]
    value = req.get("required_value") or req.get("label")
    return [str(value)]


def build_facets(record: dict[str, Any]) -> tuple[list[FacetDefinition], str]:
    decisions = explicit_facet_decisions(record)
    required = requirement_facets(record)
    facets: list[FacetDefinition] = []
    has_noncanonical = False

    if decisions:
        for index, decision in enumerate(decisions, 1):
            raw = decision.get("demonstration_status")
            state = raw if raw in set(FacetState) else None
            if state is None:
                has_noncanonical = True
            facets.append(
                FacetDefinition(
                    facet_id=str(decision.get("facet_id") or f"F{index}"),
                    text=str(decision.get("requirement") or required[min(index - 1, len(required) - 1)]),
                    state=state,
                    supporting_proposition_ids=list(decision.get("vendor_proposition_ids") or []),
                    limiting_proposition_ids=list(decision.get("limiting_proposition_ids") or []),
                    annotation_status=(
                        "HISTORICAL_HUMAN_FACET_DECISION"
                        if state is not None
                        else f"REQUIRES_ATOMIC_REANNOTATION:{raw}"
                    ),
                )
            )
        status = "REQUIRES_HUMAN_REANNOTATION" if has_noncanonical else "FROZEN_HUMAN_FACET_TRUTH"
        return facets, status

    dimension_id = str(record["requirement_dimension"].get("dimension_id", "REQ"))
    for index, text in enumerate(required, 1):
        facets.append(
            FacetDefinition(
                facet_id=f"{dimension_id}.F{index}",
                text=text,
                annotation_status="CANDIDATE_BOUNDARY_REQUIRES_HUMAN_REVIEW",
            )
        )
    return facets, "UNADJUDICATED"


def make_case(
    fixture_name: str,
    record: dict[str, Any],
    model_case: dict[str, Any],
    truth: dict[str, Any],
    assertions: dict[str, dict[str, Any]],
) -> FacetCase:
    metadata = CORPUS_METADATA[fixture_name]
    req = record["requirement_dimension"]
    facets, truth_status = build_facets(record)
    evidence = []
    source_group_ids = []
    for member in model_case.get("evidence", []):
        assertion_id = member["assertion_id"]
        assertion = assertions[assertion_id]
        evidence.append(
            EvidenceProposition(
                proposition_id=assertion_id,
                actor_role=assertion["actor_role"],
                evidence_role=assertion.get("evidence_role"),
                text=assertion["text"],
                document_id=assertion["document_id"],
                pages=list(assertion.get("pages") or []),
            )
        )
        source_group_ids.extend(
            span.get("block_text_sha256") or span.get("page_text_sha256") or assertion_id
            for span in assertion.get("source_spans", [])
        )

    organization = record.get("vendor_dimension", {}).get("organization_id", "unknown")
    requirement_id = str(req.get("dimension_id") or req.get("label"))
    requirement_text = "\n".join(requirement_facets(record))
    frozen_truth = truth_status == "FROZEN_HUMAN_FACET_TRUTH"
    suff = truth.get("evidence_sufficiency") if frozen_truth else None
    relation = truth.get("relation") if frozen_truth else None
    return FacetCase(
        case_id=model_case["case_id"],
        comparison_id=record["comparison_id"],
        corpus_id=metadata["corpus_id"],
        requirement_id=requirement_id,
        requirement_text=requirement_text,
        constraint_status=truth.get("constraint_status") or truth.get("constraint_status", req.get("constraint_status", "PRESCRIBED")),
        facets=facets,
        evidence=evidence,
        evidence_sufficiency=suff,
        relation=relation,
        vendor_group=organization,
        model_version_group=metadata["model_version_group"],
        requirement_family=requirement_family(requirement_id),
        regulator_text_group=text_hash(requirement_text),
        source_group_ids=sorted(set(source_group_ids)),
        revision_ancestry=metadata["model_version_group"],
        review_ancestry=metadata["review_ancestry"],
        truth_status=truth_status,
    )


class DisjointSet:
    def __init__(self, items: list[str]):
        self.parent = {item: item for item in items}

    def find(self, item: str) -> str:
        parent = self.parent[item]
        if parent != item:
            self.parent[item] = self.find(parent)
        return self.parent[item]

    def union(self, left: str, right: str) -> None:
        left_root, right_root = self.find(left), self.find(right)
        if left_root != right_root:
            self.parent[right_root] = left_root


def assign_leakage_groups(cases: list[FacetCase]) -> None:
    dsu = DisjointSet([case.case_id for case in cases])
    indexes: dict[tuple[str, str], list[str]] = defaultdict(list)
    for case in cases:
        keys = [
            ("vendor", case.vendor_group),
            ("version", case.model_version_group),
            ("regulator_text", case.regulator_text_group),
            ("revision", case.revision_ancestry),
            ("review", case.review_ancestry),
        ]
        keys.extend(("source", value) for value in case.source_group_ids)
        for key in keys:
            indexes[key].append(case.case_id)
    for members in indexes.values():
        for member in members[1:]:
            dsu.union(members[0], member)
    roots = {case.case_id: dsu.find(case.case_id) for case in cases}
    root_to_group = {
        root: f"LG-{text_hash(root)[:12]}" for root in sorted(set(roots.values()))
    }
    for case in cases:
        case.leakage_group = root_to_group[roots[case.case_id]]


def load_cases(input_root: Path) -> tuple[list[FacetCase], list[dict[str, Any]]]:
    cases: list[FacetCase] = []
    manifest: list[dict[str, Any]] = []
    for fixture_name, metadata in CORPUS_METADATA.items():
        fixture = input_root / fixture_name
        if not fixture.is_dir():
            raise FileNotFoundError(f"Missing frozen fixture: {fixture}")
        files = sorted(path for path in fixture.iterdir() if path.is_file())
        manifest.extend(
            {
                "fixture": fixture_name,
                "path": f"{fixture_name}/{path.name}",
                "source_archive": "/hpc/home/yh421/CIRCAD-LLM/regmodeltrace/data/evaluation/frozen",
                "size": path.stat().st_size,
                "sha256": file_sha256(path),
            }
            for path in files
        )
        records = {item["comparison_id"]: item for item in load_json(fixture / "comparison_records.json")}
        truths = {item["comparison_id"]: item for item in load_json(fixture / "comparison_truth.json")}
        assertions = {item["assertion_id"]: item for item in load_json(fixture / "source_assertions.json")}
        for model_case in load_json(fixture / "model_cases.json"):
            if not model_case["case_id"].startswith("FC-"):
                continue
            comparison_id = model_case["comparison_id"]
            cases.append(
                make_case(
                    fixture_name,
                    records[comparison_id],
                    model_case,
                    truths[comparison_id],
                    assertions,
                )
            )
    assign_leakage_groups(cases)
    return cases, manifest


def select_pilot(cases: list[FacetCase], size: int = 24) -> list[FacetCase]:
    """Outcome-independent stable selection with corpus and family coverage.

    Selection uses case identity, corpus, and family only. Historical truth is not
    consulted, which prevents hand-picking errors or relation classes.
    """
    ranked = sorted(cases, key=lambda case: (text_hash(case.case_id), case.case_id))
    selected: list[FacetCase] = []
    by_corpus: dict[str, list[FacetCase]] = defaultdict(list)
    for case in ranked:
        by_corpus[case.corpus_id].append(case)
    while len(selected) < min(size, len(cases)):
        progressed = False
        for corpus in sorted(by_corpus):
            if by_corpus[corpus] and len(selected) < size:
                selected.append(by_corpus[corpus].pop(0))
                progressed = True
        if not progressed:
            break
    return selected


def blinded_case(case: FacetCase) -> dict[str, Any]:
    data = case.model_dump(mode="json")
    for key in ["evidence_sufficiency", "relation", "truth_status"]:
        data.pop(key, None)
    for facet in data["facets"]:
        facet["state"] = None
        facet["supporting_proposition_ids"] = []
        facet["limiting_proposition_ids"] = []
        facet["annotation_status"] = "TO_BE_ADJUDICATED"
    return data


def return_template(pilot: list[FacetCase], adjudicator_slot: str) -> dict[str, Any]:
    return {
        "contract": "ft1-independent-adjudication-1.0",
        "adjudicator_slot": adjudicator_slot,
        "adjudicator_name": None,
        "adjudication_date": None,
        "attestation": None,
        "cases": [
            {
                "case_id": case.case_id,
                "constraint_status": None,
                "evidence_sufficiency": None,
                "facets": [
                    {
                        "facet_id": facet.facet_id,
                        "text_confirmed_or_revised": None,
                        "state": None,
                        "supporting_proposition_ids": [],
                        "limiting_proposition_ids": [],
                        "rationale": None,
                    }
                    for facet in case.facets
                ],
                "overall_relation": None,
                "review_coverage": None,
                "case_rationale": None,
            }
            for case in pilot
        ],
    }


def historical_counts(input_root: Path, cases: list[FacetCase]) -> dict[str, Any]:
    relation = Counter()
    sufficiency = Counter()
    constraint = Counter()
    facet_states = Counter()
    legacy_states = Counter()
    for fixture_name in CORPUS_METADATA:
        for truth in load_json(input_root / fixture_name / "comparison_truth.json"):
            relation[str(truth.get("relation"))] += 1
            sufficiency[str(truth.get("evidence_sufficiency"))] += 1
            constraint[str(truth.get("constraint_status"))] += 1
    for case in cases:
        for facet in case.facets:
            if facet.state is not None:
                facet_states[facet.state.value] += 1
            elif facet.annotation_status.startswith("REQUIRES_ATOMIC_REANNOTATION:"):
                legacy_states[facet.annotation_status.split(":", 1)[1]] += 1
    return {
        "historical_comparison_truth_records": sum(constraint.values()),
        "model_evaluable_primary_cases": len(cases),
        "constraint_status": dict(sorted(constraint.items())),
        "evidence_sufficiency": dict(sorted(sufficiency.items())),
        "relation": dict(sorted(relation.items())),
        "explicit_canonical_facet_states": dict(sorted(facet_states.items())),
        "legacy_noncanonical_facet_states_requiring_readjudication": dict(sorted(legacy_states.items())),
        "frozen_human_facet_cases": sum(case.truth_status == "FROZEN_HUMAN_FACET_TRUTH" for case in cases),
        "cases_requiring_facet_adjudication": sum(case.truth_status != "FROZEN_HUMAN_FACET_TRUTH" for case in cases),
    }


def render_pilot_markdown(pilot: list[FacetCase]) -> str:
    lines = [
        "# FT-1 Blinded Human Adjudication Pilot",
        "",
        "Historical labels and model outputs are intentionally omitted. Use the annotation guide and one blank return file.",
        "",
    ]
    for index, case in enumerate(pilot, 1):
        lines.extend(
            [
                f"## {index}. {case.case_id}",
                "",
                f"- Corpus: `{case.corpus_id}`",
                f"- Requirement: `{case.requirement_id}`",
                f"- Vendor group: `{case.vendor_group}`",
                "",
                "### Candidate regulatory facets",
                "",
            ]
        )
        for facet in case.facets:
            lines.append(f"- `{facet.facet_id}`: {facet.text}")
        lines.extend(["", "### Bounded source propositions", ""])
        for evidence in case.evidence:
            pages = ", ".join(map(str, evidence.pages)) or "unknown"
            lines.extend(
                [
                    f"**{evidence.proposition_id} — {evidence.actor_role} — {evidence.document_id}, p. {pages}**",
                    "",
                    f"> {evidence.text}",
                    "",
                ]
            )
    return "\n".join(lines)


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(canonical_json_bytes(value))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-root", type=Path, required=True)
    parser.add_argument("--output-root", type=Path, required=True)
    parser.add_argument("--baseline-csv", type=Path)
    args = parser.parse_args()

    cases, manifest = load_cases(args.input_root)
    pilot = select_pilot(cases)
    output = args.output_root
    write_json(output / "historical_input_manifest.json", {"files": manifest})
    write_json(output / "facet_case_inventory.json", [case.model_dump(mode="json") for case in cases])
    write_json(output / "historical_counts.json", historical_counts(args.input_root, cases))
    write_json(output / "pilot_pack.json", [blinded_case(case) for case in pilot])
    (output / "pilot_pack.md").write_text(render_pilot_markdown(pilot), encoding="utf-8")
    write_json(output / "adjudicator_a_return.json", return_template(pilot, "A"))
    write_json(output / "adjudicator_b_return.json", return_template(pilot, "B"))
    resolution = return_template(pilot, "RESOLUTION")
    resolution["resolution_panel"] = []
    resolution["disagreement_report_sha256"] = None
    write_json(output / "resolution_return.json", resolution)

    if args.baseline_csv:
        rows = list(csv.DictReader(args.baseline_csv.open(encoding="utf-8")))
        primary = [row for row in rows if row["case_kind"] == "PRIMARY"]
        write_json(output / "condition_a_saved_predictions.json", primary)
        relation_rows = [
            {"truth": row["truth_relation"], "prediction": row["relation_prediction"]}
            for row in primary
            if row["truth_relation"] and row["relation_prediction"]
        ]
        baseline_summary = classification_metrics(relation_rows)
        baseline_summary["evidence_sufficiency"] = {
            "correct": sum(row["binary_prediction_correct"] == "True" for row in primary),
            "total": len(primary),
        }
        baseline_summary["joint_two_stage_correct"] = {
            "correct": sum(
                row["binary_prediction_correct"] == "True"
                and (not row["truth_relation"] or row["relation_prediction_correct"] == "True")
                for row in primary
            ),
            "total": len(primary),
        }
        write_json(output / "condition_a_summary.json", baseline_summary)

    status = {
        "historical_release": {
            "PROJECT_TECHNICAL_DEVELOPMENT": "CLOSED",
            "FINAL_MODEL": "Base Qwen",
            "FINE_TUNING": "NOT_JUSTIFIED",
            "TEST_E": "CLOSED",
            "RERUN": "NOT_AUTHORIZED",
        },
        "research_track": {
            "NEXT_RELEASE_RESEARCH": "OPEN",
            "FINE_TUNING_EXPERIMENT": "CONDITIONALLY_JUSTIFIED",
            "TRAINING_DATA_READY": "NO",
            "PRODUCTION_DEPLOYMENT": "NOT_AUTHORIZED",
        },
        "pilot_size": len(pilot),
        "independent_human_returns_complete": 0,
        "conditions": {"A": "IMPORTED_SAVED_RESULTS", "B": "BLOCKED_HUMAN_GATE", "C": "BLOCKED_HUMAN_GATE", "D": "NOT_AUTHORIZED"},
        "decision": "EVIDENCE_INCONCLUSIVE",
        "decision_reason": "Independent double-adjudication and prospective facet-truth freeze are incomplete; B/C inference is prohibited.",
    }
    write_json(output / "phase1_status.json", status)


if __name__ == "__main__":
    main()
