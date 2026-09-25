"""Recompute an explicit v2 raw-mode PDF receipt for all frozen leads."""

from __future__ import annotations

import hashlib
import json
import platform
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
BASE = ROOT / "experiments/fg3_natural_boundary"
OUT = BASE / "checkpoint2_r1"
LAYOUT_COMMAND = ["pdftotext", "-layout", "-enc", "UTF-8", "PDF", "-"]
RAW_COMMAND = ["pdftotext", "-raw", "-enc", "UTF-8", "PDF", "-"]
NORMALIZATION = "Python re.sub(r'\\s+', ' ', page).strip().casefold()"


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    leads = [
        json.loads(line)
        for line in (BASE / "checkpoint2/lead_source_dossiers.jsonl").read_text().splitlines()
    ]
    prior = {
        row["lead_id"]: row
        for row in map(json.loads, (BASE / "checkpoint2/pdf_text_verification.jsonl").open())
    }
    version = subprocess.run(
        ["pdftotext", "-v"], capture_output=True, text=True, check=True
    ).stderr.strip()
    documents = {}
    for lead in leads:
        doc = lead["document_id"]
        if doc in documents:
            continue
        pdf = ROOT / lead["source_path"]
        if hashlib.sha256(pdf.read_bytes()).hexdigest() != lead["source_sha256"]:
            raise ValueError(f"PDF hash drift: {pdf}")
        command = ["pdftotext", "-raw", "-enc", "UTF-8", str(pdf), "-"]
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        pages = result.stdout.split("\f")
        if pages and not pages[-1].strip():
            pages.pop()
        documents[doc] = pages
    rows = []
    for lead in leads:
        page = documents[lead["document_id"]][lead["physical_page"] - 1]
        normalized = re.sub(r"\s+", " ", page).strip().casefold()
        query = lead["anchor_text"].casefold()
        count = len(list(re.finditer(re.escape(query), normalized)))
        if count == 0:
            raise ValueError(f"Anchor absent in raw-mode page: {lead['lead_id']}")
        old_hash = prior[lead["lead_id"]]["raw_mode_page_sha256"]
        new_hash = hashlib.sha256(page.encode("utf-8")).hexdigest()
        rows.append(
            {
                "lead_id": lead["lead_id"],
                "document_id": lead["document_id"],
                "physical_page": lead["physical_page"],
                "source_pdf_sha256": lead["source_sha256"],
                "raw_mode_anchor_match_count": count,
                "raw_mode_page_sha256_v2": new_hash,
                "legacy_raw_mode_hash": old_hash,
                "legacy_hash_reproduced_under_current_environment": old_hash == new_hash,
                "command_template": RAW_COMMAND,
                "normalization": NORMALIZATION,
            }
        )
    (OUT / "raw_mode_verification_v2.jsonl").write_text(
        "".join(json.dumps(row, sort_keys=True) + "\n" for row in rows)
    )
    receipt = {
        "pdftotext_version": version,
        "python": sys.version,
        "platform": platform.platform(),
        "layout_command_template": LAYOUT_COMMAND,
        "raw_command_template": RAW_COMMAND,
        "encoding": "UTF-8",
        "normalization": NORMALIZATION,
        "raw_mode_sha256_v2_algorithm": "SHA-256 of UTF-8 encoding of each Python-decoded form-feed-delimited pdftotext -raw page, before normalization",
        "legacy_raw_hash_reproduced_count": sum(
            row["legacy_hash_reproduced_under_current_environment"] for row in rows
        ),
        "legacy_raw_hash_total": len(rows),
        "legacy_algorithm_status": "UNCONFIRMED_IF_HASHES_DIFFER",
    }
    (OUT / "environment_receipt.json").write_text(
        json.dumps(receipt, indent=2, sort_keys=True) + "\n"
    )
    print(
        f"raw-mode anchors verified: {len(rows)}; legacy hashes reproduced: {receipt['legacy_raw_hash_reproduced_count']}"
    )


if __name__ == "__main__":
    main()
