"""Source-only lexical candidate listing for a human known-exposure review.

BM25 is only an audit aid. It never assigns exposure clearance or gold.
"""

from __future__ import annotations
import json
import re
import sqlite3
import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT / "experiments/fg3_natural_boundary"
STOP = {
    "about",
    "above",
    "after",
    "again",
    "against",
    "because",
    "before",
    "between",
    "could",
    "described",
    "describe",
    "document",
    "during",
    "following",
    "from",
    "given",
    "hurricane",
    "model",
    "modeling",
    "organization",
    "other",
    "their",
    "there",
    "these",
    "those",
    "through",
    "under",
    "which",
    "within",
    "would",
    "shall",
    "should",
    "reviewed",
    "review",
    "version",
    "standard",
    "submission",
    "with",
    "will",
    "were",
    "have",
    "been",
    "that",
    "this",
    "they",
    "then",
    "also",
    "where",
    "when",
    "same",
    "into",
    "used",
    "using",
    "only",
    "each",
    "results",
    "current",
    "accepted",
    "source",
    "data",
    "change",
    "changes",
    "modified",
    "modification",
    "provide",
    "discussed",
}


def terms(s):
    return [w for w in re.findall(r"[a-z][a-z0-9]{3,}", s.casefold()) if w not in STOP]


def main():
    m = json.loads((BASE / "protocol/known_exposure_file_manifest_v1.json").read_text())
    c = sqlite3.connect(":memory:")
    c.execute("CREATE VIRTUAL TABLE chunks USING fts5(path UNINDEXED, body)")
    count = 0
    for f in m["files"]:
        p = ROOT / f["path"]
        raw = p.read_bytes()
        if hashlib.sha256(raw).hexdigest() != f["sha256"]:
            raise ValueError("ledger drift " + f["path"])
        try:
            t = raw.decode("utf-8")
        except UnicodeDecodeError:
            continue
        # Fixed text-only windows; never inspect case truth when indexing.
        for i in range(0, len(t), 1400):
            body = t[i : i + 1800]
            if body.strip():
                c.execute("INSERT INTO chunks(path,body) VALUES(?,?)", (f["path"], body))
                count += 1
    c.commit()
    units = [
        json.loads(x)
        for x in (BASE / "checkpoint2/source_unit_drafts.jsonl").read_text().splitlines()
    ]
    rows = []
    for u in units:
        qterms = list(dict.fromkeys(terms(u["unit_text"])))[:12]
        if not qterms:
            matches = []
        else:
            query = " OR ".join(qterms)
            try:
                matches = c.execute(
                    "SELECT path, body, bm25(chunks) AS score FROM chunks WHERE chunks MATCH ? ORDER BY score LIMIT 8",
                    (query,),
                ).fetchall()
            except sqlite3.OperationalError:
                matches = []
        rows.append(
            {
                "lead_id": u["lead_id"],
                "source_unit_id": u["source_unit_id"],
                "query_terms": qterms,
                "lexical_candidate_files": [
                    {"path": p, "score": s, "excerpt": re.sub(r"\s+", " ", b)[:500]}
                    for p, b, s in matches
                ],
                "method": "SQLite FTS5 BM25 over 1400-character ledger windows, 12 first distinct non-stopword unit terms with OR; review aid only, not exposure clearance",
            }
        )
    out = BASE / "checkpoint2/exposure_similarity_candidates.jsonl"
    out.write_text("".join(json.dumps(x, ensure_ascii=False, sort_keys=True) + "\n" for x in rows))
    print("ledger chunks", count, "units", len(rows))


if __name__ == "__main__":
    main()
