"""Deterministic, source-only FG-3 page-lead discovery.

The output is deliberately not a case registry or a truth file. PDF context,
exposure, and evidence sufficiency require later independent checks.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PROTOCOL = ROOT / "experiments/fg3_natural_boundary/protocol/discovery_protocol.json"
INVENTORY = ROOT / "artifacts/corpus-inventory-20260923/inventory.json"
OUT = ROOT / "experiments/fg3_natural_boundary/candidates"


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def write_jsonl(path: Path, rows: list[dict]) -> None:
    path.write_text("".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in rows))


def extract_pages(path: Path) -> list[str]:
    run = subprocess.run(
        ["pdftotext", "-layout", "-enc", "UTF-8", str(path), "-"],
        check=True,
        capture_output=True,
        text=True,
    )
    pages = run.stdout.split("\f")
    if pages and not pages[-1].strip():
        pages.pop()
    return pages


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, default=OUT)
    args = parser.parse_args()
    protocol_bytes = PROTOCOL.read_bytes()
    protocol = json.loads(protocol_bytes)
    inventory = json.loads(INVENTORY.read_text())
    docs = {d["document_id"]: d for d in inventory["documents"]}
    preseen = {
        (item["document_id"], page)
        for item in protocol["preexisting_exploratory_pages"]
        for page in item["physical_pages"]
    }
    groups = {
        (2021, "REGULATOR"): "shared_standards_2021_standards",
        (2023, "REGULATOR"): "shared_standards_2023_standards",
        (2021, "VENDOR"): "florida_public_2021_fphlm_submission",
        (2023, "VENDOR"): "florida_public_2023_fphlm_submission",
        (2021, "REVIEWER"): "florida_public_2021_fphlm_review",
        (2023, "REVIEWER"): "florida_public_2023_fphlm_review",
    }
    needed = {groups[(cycle, role)] for panel in protocol["query_sets"].values() for cycle in protocol["cycles"] for role in panel["document_roles"]}
    pages_by_doc = {}
    for doc_id in sorted(needed):
        item = docs[doc_id]
        pdf = ROOT / item["local_path"]
        if sha256(pdf.read_bytes()) != item["sha256"]:
            raise ValueError(f"source hash mismatch: {doc_id}")
        pages_by_doc[doc_id] = extract_pages(pdf)

    hit_rows = []
    selected: dict[tuple[str, int, str, int], dict] = {}
    query_counts = []
    for panel_id, panel in protocol["query_sets"].items():
        for cycle in protocol["cycles"]:
            for role in panel["document_roles"]:
                doc_id = groups[(cycle, role)]
                item = docs[doc_id]
                for query_id, expression in panel["queries"].items():
                    regex = re.compile(expression, re.IGNORECASE)
                    hits = []
                    for page_number, page_text in enumerate(pages_by_doc[doc_id], 1):
                        normalized = re.sub(r"\s+", " ", page_text).strip()
                        match = regex.search(normalized)
                        if not match:
                            continue
                        rank_key = "|".join(
                            [protocol["discovery_protocol_id"], panel_id, str(cycle), doc_id, query_id, str(page_number)]
                        )
                        hits.append((sha256(rank_key.encode()), page_number, match.group(0), normalized, match.start(), match.end()))
                    hits.sort(key=lambda row: (row[0], row[1]))
                    cap = panel["max_selected_pages_per_document_and_query"]
                    query_counts.append({"panel": panel_id, "cycle": cycle, "document_id": doc_id, "query_id": query_id, "hit_pages": len(hits), "selected_pages": min(len(hits), cap)})
                    for rank, (rank_hash, page_number, match_text, normalized, start, end) in enumerate(hits, 1):
                        is_selected = rank <= cap
                        hit_rows.append({"panel": panel_id, "standards_cycle": cycle, "document_id": doc_id, "document_role": role, "physical_page": page_number, "discovery_query_id": query_id, "discovery_rank": rank, "selection_status": "SELECTED_PAGE_LEAD" if is_selected else "BEYOND_PREDECLARED_CAP", "ranking_sha256": rank_hash, "matched_text": match_text})
                        if not is_selected:
                            continue
                        key = (panel_id, cycle, doc_id, page_number)
                        row = selected.setdefault(key, {"lead_id": "FG3L_" + sha256("|".join(map(str, key)).encode())[:16], "discovery_protocol_id": protocol["discovery_protocol_id"], "panel": panel_id, "standards_cycle": cycle, "document_id": doc_id, "document_role": role, "source_path": item["local_path"], "source_sha256": item["sha256"], "physical_page": page_number, "discovery_query_ids": [], "discovery_ranks": {}, "dedup_cluster": f"{doc_id}:physical-page-{page_number}", "selection_reason": "Predeclared hash rank within document/query cap", "selection_status": "SOURCE_LEAD_ONLY", "source_context_verified": False, "exposure_status": "DEVELOPER_EXPOSED" if (doc_id, page_number) in preseen else "EXPOSURE_UNKNOWN", "adjudicability_status": "NOT_ASSESSED", "model_evidence_packet_id": None, "model_evidence_packet_hash": None, "gold_label": None, "matched_excerpts": []})
                        row["discovery_query_ids"].append(query_id)
                        row["discovery_ranks"][query_id] = rank
                        row["matched_excerpts"].append({"query_id": query_id, "match": match_text, "pdftotext_context_unverified": normalized[max(0, start - 180):min(len(normalized), end + 180)]})

    args.out.mkdir(parents=True, exist_ok=True)
    hit_rows.sort(key=lambda r: (r["panel"], r["standards_cycle"], r["document_id"], r["discovery_query_id"], r["discovery_rank"]))
    leads = sorted(selected.values(), key=lambda r: (r["panel"], r["standards_cycle"], r["document_id"], r["physical_page"]))
    write_jsonl(args.out / "all_query_hits.jsonl", hit_rows)
    write_jsonl(args.out / "source_leads.jsonl", leads)
    manifest = {"status": "SOURCE_LEADS_ONLY_EXPOSURE_AND_PDF_VERIFICATION_PENDING", "discovery_protocol_id": protocol["discovery_protocol_id"], "discovery_protocol_sha256": sha256(protocol_bytes), "source_inventory_sha256": sha256(INVENTORY.read_bytes()), "documents_searched": sorted(needed), "physical_pages_by_document": {k: len(v) for k, v in sorted(pages_by_doc.items())}, "query_counts": query_counts, "all_query_hit_count": len(hit_rows), "selected_page_lead_count": len(leads), "selected_by_panel": {panel: sum(row["panel"] == panel for row in leads) for panel in protocol["query_sets"]}, "developer_exposed_page_leads": sum(row["exposure_status"] == "DEVELOPER_EXPOSED" for row in leads), "model_inference_runs": 0, "human_truth_records": 0, "output_sha256": {p: sha256((args.out / p).read_bytes()) for p in ("all_query_hits.jsonl", "source_leads.jsonl")}}
    (args.out / "discovery_manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"selected_page_lead_count": len(leads), "selected_by_panel": manifest["selected_by_panel"], "developer_exposed_page_leads": manifest["developer_exposed_page_leads"], "all_query_hit_count": len(hit_rows)}, sort_keys=True))


if __name__ == "__main__":
    main()
