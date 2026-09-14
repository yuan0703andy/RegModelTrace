# REVIEW-1 — database inventory and identified-vendor integration design

## What exists now

RegModelTrace does use SQL, but the current SQL layer is three historical SQLite/FTS5 stores for the original three-document RMS retrieval work. It is not a unified cross-vendor application database.

| Store | Size | Main logical content |
|---|---:|---|
| `m4-foundation-v1.sqlite` | 45.55 MiB | 9,946 searchable records: 9,750 narrative candidates and 196 table-cell records; 8,390 blocks; 1,443 units; 3 documents; 16 classifications; 17 membership links |
| `m4a-v1/narrative.sqlite` | 44.63 MiB | 9,750 narrative candidates, 8,390 blocks, 1,443 units, and 3 documents; classification and membership projections are empty |
| `m4c-v1/passages.sqlite` | 16.38 MiB | 6,009 deterministic retrieval passages |

All three databases were opened with SQLite URI `mode=ro&immutable=1`. No WAL or SHM companion was present. Each contains an FTS5 `search_text` index; its shadow tables are storage internals and are not additional evidence records. The schema has primary keys but no declared foreign-key constraints. Payloads are stored as JSON text, so many logical relationships are enforced by application code rather than SQL constraints.

Most later project data is outside SQL:

- parser blocks, pages, words, semantic units, and some extraction outputs are Parquet;
- frozen truth, fixtures, scores, manifests, provenance, tables, and reports are JSON;
- requests and durable journals are JSONL;
- dense vectors are NumPy arrays;
- source documents are immutable PDFs.

The current `regmodeltrace/data` snapshot, excluding REVIEW-1's own outputs, occupies 1,749,354,564 bytes (1,668.31 MiB). SQLite contributes 111,738,880 bytes (106.56 MiB), Parquet 164,523,796 bytes (156.90 MiB), JSON 812,364,454 bytes (774.73 MiB), JSONL 140,586,910 bytes (134.07 MiB), NumPy vectors 42,793,984 bytes (40.81 MiB), and PDFs 435,870,289 bytes (415.68 MiB).

There are 45 physical PDF copies but only 33 unique content hashes. Unique PDF content occupies 321,047,536 bytes (306.17 MiB). Physical copies reflect frozen corpus snapshots and do not create additional logical documents. SCALE-1 itself declares 28 logical documents: 20 in the bulk-eligible partition and 8 protected Validation D/Test E documents.

## Scale and adjudication boundaries

The saved SCALE-1 bulk partition contains 5,129 pages, 57,030 source blocks, 9,010 deterministic semantic units, 47,458 eligible source assertions, and 1,112 numeric cells. The 4,096-request systems workload is a stratified sample of eligible assertions. Each large direct/Ray run recorded 4,078 valid and 18 invalid outputs; synthetic or repeated systems runs do not increase the semantic denominator.

Only 30 primary v2.2 comparisons across five fixtures are owner-adjudicated alignment cases. The 22 adverse controls are constructed boundary tests. The 47,458 source assertions are machine-processable candidates, not Gold comparisons, and the historical RMS retrieval database contains only 16 stored classifications.

KCC's four affected table panels on vendor PDF pages 184–185 retain `FAIL_TABLE_IDENTITY` because 140 row/column identities are duplicated. Those panels are excluded from verified numeric evidence.

## Model and runtime storage

The DCC runtime snapshot was measured on a CPU compute node. The Hugging Face cache occupies 41,099,264,788 bytes (38.28 GiB), including several Qwen variants. The final Qwen2.5-32B-Instruct-AWQ cache occupies 19,340,650,363 bytes (18.01 GiB). Other cached models occupy 21,764,929,071 bytes (20.27 GiB). The Python GPU environment occupies 8,231,243,434 bytes (7.67 GiB); the vLLM cache was 970 bytes. These runtime assets are separate from corpus and result storage.

## Minimal identified-vendor envelope

A future upload should preserve the real organization identity and create a new immutable artifact version. It should not overwrite a prior submission or score.

```json
{
  "organization_id": "registered legal or program identity",
  "uploader_permission_ref": "authorization record",
  "submission_id": "stable versioned submission identity",
  "standards_edition": "applicable regulatory edition",
  "model": {
    "name": "declared model name",
    "version": "declared version",
    "build": "declared build",
    "effective_date": "declared date"
  },
  "artifact_kind": "submission | review | validation_report | test_result",
  "document_role": "REGULATOR | VENDOR | REVIEWER | INDEPENDENT_TESTER",
  "source_origin": "PUBLIC_REGULATORY_DOCUMENT | VENDOR_UPLOADED_DOCUMENT | VENDOR_REPORTED_TEST_RESULT | INDEPENDENTLY_OBSERVED_TEST_RESULT",
  "content_sha256": "...",
  "received_at": "timestamp",
  "source_uri": "origin reference",
  "access_designation": "permission class",
  "sharing_authorization_ref": "approval record or null",
  "supersedes_submission_id": "prior identity or null",
  "related_submission_ids": [],
  "provenance_completeness": "COMPLETE | PARTIAL",
  "parse_status": "PENDING | PASS | FAIL_WITH_DIAGNOSTICS"
}
```

A vendor-provided test report remains vendor-reported evidence. A declared build identifier does not prove equivalence to a deployed production build.

## Logical mapping to the current design

The proposed relationships can initially remain application-level records alongside the existing files:

```text
organization -> model_version -> submission/artifact
artifact -> source_block -> assertion/proposition
regulatory_requirement -> requirement_facet
comparison_case -> evidence_membership -> proposition
comparison_case -> machine_forecast
comparison_case -> owner_adjudication
future_audit_action -> response_artifact or test_run -> new evidence_membership
```

Machine forecasts, reviewer findings, vendor assertions, independently observed tests, and owner decisions require separate actor and origin fields. A future database migration should add explicit foreign keys and version constraints, but REVIEW-1 does not select PostgreSQL, create an upload endpoint, alter access policy, or implement a portal.

## Gaps before implementation

The current stores lack a cross-corpus organization/model/submission registry, formal source-version foreign keys, access-designation enforcement, and one canonical distinction between vendor-reported and independently observed behavior. They also do not provide transactional ingestion or immutable supersession rules. Those are requirements for a future approved release, not defects to repair in the closed release.

