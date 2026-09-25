"""Freeze a TimelyQABench split without crossing exact document-text overlap."""

from __future__ import annotations

import hashlib
import io
import json
from collections import Counter, defaultdict
from pathlib import Path
from zipfile import ZipFile


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "experiments" / "public_rag" / "timely_split"
ARCHIVE_DIR = ROOT / "experiments" / "public_rag" / "datasets" / "official"
SALT = "RegModelTrace-TimelyQABench-A0.4b-2026-09-25-v1"
TARGET_CONFIRMATION_FRACTION = 0.20
MAX_CONFIRMATION_COMPONENT_ROWS = 10


def digest(text: bytes) -> str:
    return hashlib.sha256(text).hexdigest()


def find(parents: dict[str, str], key: str) -> str:
    while parents[key] != key:
        parents[key] = parents[parents[key]]
        key = parents[key]
    return key


def union(parents: dict[str, str], left: str, right: str) -> None:
    a, b = find(parents, left), find(parents, right)
    if a != b:
        parents[max(a, b)] = min(a, b)


def main() -> None:
    archive = next(ARCHIVE_DIR.glob("TimelyQABench-*.zip"))
    inventory = json.loads((ROOT / "experiments/public_rag/public_benchmark_inventory.json").read_text())
    pin = next(x for x in inventory["benchmarks"] if x["id"] == "TimelyQABench")
    if digest(archive.read_bytes()) != pin["archive_sha256"]:
        raise ValueError("Timely source archive differs from frozen pin")

    rows: dict[str, dict] = {}
    owners: dict[str, str] = {}
    text_owners: dict[str, set[str]] = defaultdict(set)
    parents: dict[str, str] = {}
    duplicate_text_hashes: set[str] = set()
    duplicate_id_cross_rows = 0
    domain_ids: dict[str, set[int]] = defaultdict(set)
    with ZipFile(archive) as outer:
        dataset_bytes = next(outer.read(n) for n in outer.namelist() if n.endswith("datasets.zip"))
    if digest(dataset_bytes) != pin["inner_dataset_sha256"]:
        raise ValueError("Timely inner dataset differs from frozen pin")
    with ZipFile(io.BytesIO(dataset_bytes)) as inner:
        for filename in sorted(inner.namelist()):
            if not filename.endswith(".jsonl") or filename.startswith("__MACOSX"):
                continue
            domain = filename.removeprefix("timelyrag_").removesuffix("_dataset_v2.jsonl")
            for line in inner.read(filename).splitlines():
                item = json.loads(line)
                key = f"{domain}:{item['index']:04d}"
                if key in rows:
                    raise ValueError(f"Duplicate row key: {key}")
                rows[key] = {"domain": domain, "index": item["index"], "category": item["category"]}
                parents[key] = key
                for doc in item["docs_ko"]:
                    gid = doc["global_doc_id"]
                    if gid in domain_ids[domain]:
                        duplicate_id_cross_rows += 1
                    domain_ids[domain].add(gid)
                    text_hash = digest(doc["text"].encode("utf-8"))
                    text_owners[text_hash].add(key)
                    if text_hash in owners:
                        if owners[text_hash] != key:
                            duplicate_text_hashes.add(text_hash)
                        union(parents, key, owners[text_hash])
                    else:
                        owners[text_hash] = key

    components: dict[str, list[str]] = defaultdict(list)
    for key in sorted(rows):
        components[find(parents, key)].append(key)
    canonical_components = {min(members): members for members in components.values()}
    row_to_component = {row: component for component, members in canonical_components.items() for row in members}

    strata: dict[tuple[str, str], list[str]] = defaultdict(list)
    forced_development: set[str] = set()
    for component, members in canonical_components.items():
        if len(members) > MAX_CONFIRMATION_COMPONENT_ROWS:
            forced_development.add(component)
            continue
        counts = Counter((rows[m]["domain"], rows[m]["category"]) for m in members)
        dominant_stratum = min(counts, key=lambda k: (-counts[k], k))
        strata[dominant_stratum].append(component)

    confirmation: set[str] = set()
    for stratum, group in sorted(strata.items()):
        group.sort(key=lambda component: digest(f"{SALT}|{component}".encode()))
        target = round(TARGET_CONFIRMATION_FRACTION * sum(len(canonical_components[g]) for g in group))
        selected = 0
        for component in group:
            if selected >= target:
                break
            confirmation.add(component)
            selected += len(canonical_components[component])

    assignments = []
    actual_strata: dict[str, Counter] = defaultdict(Counter)
    for key in sorted(rows):
        item = rows[key]
        component = row_to_component[key]
        split = "CONFIRMATION" if component in confirmation else "DEVELOPMENT"
        actual_strata[f"{item['domain']}|{item['category']}"][split] += 1
        assignments.append({"row_id": key, **item, "exact_overlap_component": component, "split": split})

    # Every exact text hash must remain in one connected component and one split.
    split_by_row = {item["row_id"]: item["split"] for item in assignments}
    for text_hash, members in text_owners.items():
        if len({row_to_component[row] for row in members}) != 1:
            raise ValueError(f"Unmerged exact document text: {text_hash}")
        if len({split_by_row[row] for row in members}) != 1:
            raise ValueError(f"Exact document text crosses split: {text_hash}")

    OUT.mkdir(parents=True, exist_ok=True)
    lines = "".join(json.dumps(item, ensure_ascii=False, sort_keys=True) + "\n" for item in assignments)
    (OUT / "split_assignments.jsonl").write_text(lines)
    split_counts = Counter(item["split"] for item in assignments)
    manifest = {
        "status": "FROZEN_BEFORE_MODEL_OUTPUT",
        "source_archive_sha256": pin["archive_sha256"],
        "inner_dataset_sha256": pin["inner_dataset_sha256"],
        "algorithm": "Union rows sharing an exact UTF-8 document-text SHA-256 across all domains; force components larger than 10 rows into development; group remaining components by dominant domain/category; order by salted SHA-256 and assign whole components until approximately 20% of each stratum is confirmation.",
        "salt": SALT,
        "target_confirmation_fraction": TARGET_CONFIRMATION_FRACTION,
        "maximum_confirmation_component_rows": MAX_CONFIRMATION_COMPONENT_ROWS,
        "row_count": len(rows),
        "component_count": len(canonical_components),
        "largest_component_rows": max(map(len, canonical_components.values())),
        "forced_development_component_count": len(forced_development),
        "forced_development_row_count": sum(len(canonical_components[c]) for c in forced_development),
        "exact_text_hashes_shared_across_rows": len(duplicate_text_hashes),
        "exact_document_text_cross_split_count": 0,
        "duplicate_global_doc_ids_within_domain": duplicate_id_cross_rows,
        "split_counts": dict(split_counts),
        "actual_domain_category_counts": {k: dict(v) for k, v in sorted(actual_strata.items())},
        "split_assignments_sha256": digest(lines.encode("utf-8")),
        "limitation": "Exact-text overlap is isolated, but near-duplicate/template overlap has not yet been measured. This is a project-defined split, not an official benchmark split.",
    }
    (OUT / "split_manifest.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n")
    print(json.dumps({k: manifest[k] for k in ("row_count", "component_count", "largest_component_rows", "exact_text_hashes_shared_across_rows", "split_counts", "split_assignments_sha256")}))


if __name__ == "__main__":
    main()
