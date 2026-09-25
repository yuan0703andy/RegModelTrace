"""Reproduce FG-3 lead anchors and exact-match exposure precheck without gold.

This does not adjudicate substantial equivalence or verify PDF rendering.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT / "experiments/fg3_natural_boundary"


def norm(s: str) -> str:
    return re.sub(r"\s+", " ", s).strip().casefold()


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=BASE / "checkpoint2")
    args = ap.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    leads = [
        json.loads(s) for s in (BASE / "candidates/source_leads.jsonl").read_text().splitlines()
    ]
    discovery = json.loads((BASE / "protocol/discovery_protocol.json").read_text())
    ledger = json.loads((BASE / "protocol/known_exposure_file_manifest_v1.json").read_text())
    exposed = []
    for item in ledger["files"]:
        p = ROOT / item["path"]
        raw = p.read_bytes()
        if digest(raw) != item["sha256"]:
            raise RuntimeError("exposure file drift: " + item["path"])
        try:
            t = raw.decode("utf-8")
        except UnicodeDecodeError:
            continue
        exposed.append((item["path"], norm(t)))
    pages = {}
    for lead in leads:
        doc = lead["document_id"]
        if doc in pages:
            continue
        pdf = ROOT / lead["source_path"]
        if digest(pdf.read_bytes()) != lead["source_sha256"]:
            raise RuntimeError("PDF hash mismatch: " + doc)
        r = subprocess.run(
            ["pdftotext", "-layout", "-enc", "UTF-8", str(pdf), "-"],
            capture_output=True,
            text=True,
            check=True,
        )
        t = r.stdout.split("\f")
        if t and not t[-1].strip():
            t.pop()
        pages[doc] = t
    out = []
    manual_touch = {
        (x["document_id"], p)
        for x in json.loads((BASE / "protocol/known_exposure_ledger_v1.json").read_text())[
            "known_manual_touchpoints"
        ]
        for p in x["physical_pages"]
    }
    for lead in leads:
        page = pages[lead["document_id"]][lead["physical_page"] - 1]
        normalized = norm(page)
        regexes = []
        for qid in lead["discovery_query_ids"]:
            expression = discovery["query_sets"][lead["panel"]]["queries"][qid]
            m = re.compile(expression, re.IGNORECASE).search(normalized)
            if m:
                regexes.append((m.start(), qid, m.end(), m.group()))
        if not regexes:
            raise RuntimeError("frozen anchor absent: " + lead["lead_id"])
        start, qid, end, phrase = min(regexes, key=lambda x: (x[0], x[1]))
        before = normalized[max(0, start - 200) : start]
        after = normalized[end : end + 250]
        # An exact-match candidate is generated from the longest bounded run
        # around the first anchor; it is only a precheck, never clearance.
        excerpt = normalized[max(0, start - 70) : min(len(normalized), end + 100)]
        tokens = excerpt.split()
        windows = []
        for k in (14, 10):
            if len(tokens) < k:
                continue
            for j in range(0, len(tokens) - k + 1):
                windows.append(" ".join(tokens[j : j + k]))
            if windows:
                break
        matches = []
        for path, content in exposed:
            found = next((w for w in windows if w in content), None)
            if found:
                matches.append({"file_path": path, "matched_window": found})
        out.append(
            {
                "lead_id": lead["lead_id"],
                "panel": lead["panel"],
                "document_id": lead["document_id"],
                "document_role": lead["document_role"],
                "standards_cycle": lead["standards_cycle"],
                "physical_page": lead["physical_page"],
                "source_path": lead["source_path"],
                "source_sha256": lead["source_sha256"],
                "page_text_sha256": digest(page.encode()),
                "anchor_query_id": qid,
                "anchor_text": phrase,
                "anchor_start_in_normalized_page": start,
                "anchor_end_in_normalized_page": end,
                "anchor_context_before": before,
                "anchor_context_after": after,
                "page_text": page,
                "prior_manual_page_touch": (lead["document_id"], lead["physical_page"])
                in manual_touch,
                "exact_window_exposure_candidates": matches,
                "exact_precheck_method": "14-token window from normalized 170-character anchor excerpt searched in 347 frozen textual files; candidate match requires source-role/equivalence review; no match is not exposure clearance",
            }
        )
    p = args.out / "lead_source_dossiers.jsonl"
    p.write_text("".join(json.dumps(r, ensure_ascii=False, sort_keys=True) + "\n" for r in out))
    print(
        json.dumps(
            {
                "leads": len(out),
                "exact_candidate_leads": sum(
                    bool(x["exact_window_exposure_candidates"]) for x in out
                ),
                "prior_manual_pages": sum(x["prior_manual_page_touch"] for x in out),
                "output": str(p),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
