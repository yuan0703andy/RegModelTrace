# Design

## Inputs

Inputs are an explicit manifest of saved v2.2 freezes, run manifests, scored rows, closure receipts, RAG evaluation artifacts, SQLite databases, Parquet/JSON/JSONL stores, raw PDFs, and systems receipts. Each certified metric is joined by persisted case identity and bound to input hashes.

## Reporting pipeline

1. Discover and hash selected immutable inputs.
2. Read SQLite through URI `mode=ro` and inspect schema/index/count metadata without writes.
3. Convert saved scored rows into one canonical reporting row per corpus and case.
4. Derive sufficiency, conditional relation, and joint metrics with explicit invalid and undefined accounting.
5. Reconcile derived values with frozen scorer counts and proper scores.
6. Generate deterministic machine-readable outputs and human-readable reports.
7. Re-hash historical inputs and fail closure if any changed.

## Metric rules

Primary comparisons and adverse controls remain separate. Relation eligibility is determined by human truth sufficiency and prescribed applicability. Undefined metrics are represented as `{value: null, reason: ...}`. No threshold is fitted and no new semantic label is produced.

## Storage rules

Logical corpus membership, unique content hashes, physical copies, SQL rows, FTS shadow tables, Parquet rows, JSONL requests, and model caches are separate quantities. KCC table-identity failures remain excluded from validated numeric evidence.

## Future-design boundary

The vendor-integration, LoRA, and sequential-audit deliverables are architecture/research memos only. They do not authorize implementation or external action.

