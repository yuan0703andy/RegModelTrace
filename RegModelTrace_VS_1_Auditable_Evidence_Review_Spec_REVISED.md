# RegModelTrace VS-1 — Auditable Evidence Review Vertical Slice

**Change ID:** `VS-1`
**Status:** `APPROVE_WITH_4_CONTRACT_FIXES` → revised for OpenSpec packaging
**Date:** 2026-09-16
**Authoritative parent direction:** `RMT-PRODUCT-1`
**Implementation authorization:** **NO**
**Next action:** **IMPLEMENTATION_INVENTORY_ONLY**

---

## 0. Formal project state

```text
CURRENT_PROJECT_CORE = INFRASTRUCTURE_AND_PRODUCT_RELIABILITY
RMT_PRODUCT_1 = AUTHORITATIVE_DIRECTION
ER_1 = RETAINED_AND_INTEGRATED
STATISTICAL_RESEARCH = DEFERRED
LONGITUDINAL_RESEARCH = DEFERRED
NEXT_DELIVERY = END_TO_END_EVIDENCE_WORKBENCH_VERTICAL_SLICE

VS_1 = APPROVED_FOR_OPENSPEC_PACKAGING
IMPLEMENTATION_AUTHORIZED_BY_THIS_SPEC = NO
NEXT_ACTION = IMPLEMENTATION_INVENTORY_ONLY
```

This specification does not authorize code modification, inference, retrieval tuning, model changes, Ray changes, embedding changes, or UI-architecture changes.

---

# 1. Purpose

VS-1 proves one bounded reviewer workflow:

```text
Select a frozen Florida corpus
→ ask one regulatory question
→ retrieve regulator/vendor/reviewer evidence
→ inspect the complete retrieval trace
→ open each result in the original PDF
→ confirm, reject, or request broader search
→ export the evidence packet and audit record
```

The product principle is:

> **Machine retrieves and proposes; human verifies against the original PDF.**

---

# 2. Non-goals

```text
NO statistical hurricane experiments
NO Florida inductive-bias experiments
NO longitudinal research program
NO temporal-RAG benchmark
NO GraphRAG
NO automatic agents
NO new foundation-model comparison
NO fine-tuning
NO adapter training
NO Ray optimization
NO broad retrieval tuning
NO new reranker study
NO embedding-model replacement
NO reopening closed semantic evaluations
NO new held-out semantic test
NO broad UI redesign
NO compliance pass/fail automation
NO publication-novelty work
```

---

# 3. Retained RegModelTrace invariants

1. Regulator, vendor, and reviewer evidence remain distinct.
2. Source identity and citations are host-owned.
3. Retrieval miss does not imply corpus absence.
4. Review/change chronology does not establish causation.
5. Original PDFs are authoritative.
6. Parsed/indexed/generated artifacts are derivative.
7. Human disposition is the terminal product state.
8. Evidence must remain traceable through every product stage.

---

# 4. Required implementation inventory before any code change

Every VS-1 capability must be assigned exactly one status:

```text
IMPLEMENTED
IMPLEMENTED_BUT_NOT_PRODUCTIZED
SYNTHETICALLY_VALIDATED_ONLY
PARTIALLY_IMPLEMENTED
NOT_IMPLEMENTED
OUT_OF_SCOPE_FOR_VS1
```

Inventory must reconcile:

```text
active repository
recovered artifacts
ER-1 outputs
corpus-recovery manifests / receipts
parser outputs
retrieval assets
static/demo workbench
freeze/release receipts
```

Required first outputs:

```text
artifacts/vs-1/implementation_inventory.json
artifacts/vs-1/implementation_inventory.md
```

No implementation starts before inventory approval.

---

# 5. Contract fix 1 — Separate corpus identity from retrieval-build identity

## 5.1 CorpusSnapshot

`CorpusSnapshot` identifies the immutable source/canonical corpus only.

It MUST NOT contain hashes that change when indexes or embeddings are rebuilt.

```json
{
  "corpus_snapshot_id": "CS_...",
  "created_at": "...",
  "document_ids": ["D_..."],
  "source_manifest_sha256": "...",
  "parser_version": "...",
  "parser_config_sha256": "...",
  "passage_inventory_sha256": "...",
  "status": "VALID | INVALID",
  "notes": "..."
}
```

### Snapshot identity changes when

- a source PDF is added, removed, or replaced;
- a source hash changes;
- parser output changes in a way that changes canonical passage/source identities;
- the canonical passage inventory changes.

### Snapshot identity does not change merely because

- embeddings are recomputed;
- BM25/FTS index is rebuilt;
- vector-index format changes;
- retrieval configuration changes;
- reranking or ranking code changes.

## 5.2 IndexBuildManifest

Retrieval/index build identity is separate:

```json
{
  "index_build_id": "IB_...",
  "corpus_snapshot_id": "CS_...",
  "created_at": "...",
  "retrieval_artifact_manifest_sha256": "...",
  "embedding_model_id": "...|null",
  "embedding_model_revision": "...|null",
  "passage_matrix_sha256": "...|null",
  "fts_index_sha256": "...|null",
  "retrieval_config_sha256": "...",
  "status": "VALID | INVALID"
}
```

A `RetrievalRun` MUST record both:

```text
corpus_snapshot_id
index_build_id
```

This allows one immutable corpus to support multiple rebuildable retrieval representations.

---

# 6. SourceDocument contract

```json
{
  "document_id": "D_...",
  "document_sha256": "...",
  "title": "...",
  "document_role": "STANDARDS | VENDOR_SUBMISSION | PROFESSIONAL_TEAM_REPORT | OTHER",
  "organization": "...",
  "source_url": "...|null",
  "local_original_path": "...",
  "mime_type": "application/pdf",
  "standard_cycle": "...|null",
  "model_version": "...|null",
  "document_version_label": "...|null"
}
```

Full longitudinal lineage remains out of scope for VS-1.

---

# 7. SourceSpan contract

```json
{
  "source_span_id": "SS_...",
  "document_id": "D_...",
  "physical_page_index": 67,
  "printed_page_label": "61|null",
  "page_text_sha256": "...",
  "char_start": 144,
  "char_end": 391,
  "bbox": [72.1, 233.8, 516.2, 318.4],
  "line_geometry": [],
  "location_precision": "EXACT_GEOMETRY | PAGE_TEXT | PAGE_ONLY",
  "alignment_status": "ALIGNED | ALIGNMENT_FAILED"
}
```

Rules:

- physical and printed pages remain distinct;
- offsets are relative to declared canonical page text;
- absent geometry remains absent;
- location precision is explicit;
- geometry is never synthesized to satisfy UI expectations.

---

# 8. Contract fix 2 — Geometry unavailability is a resolver warning, not a terminal failure

## 8.1 Authoritative resolver

```text
resolve_source(
    corpus_snapshot_id,
    assertion_id | passage_id | source_span_id
)
```

## 8.2 Successful exact resolution

```json
{
  "status": "RESOLVED",
  "location_precision": "EXACT_GEOMETRY",
  "warnings": [],
  "document_id": "D_...",
  "document_sha256": "...",
  "physical_page_index": 67,
  "quote": "...",
  "source_spans": ["SS_..."]
}
```

## 8.3 Successful degraded resolution

If authoritative page/text provenance succeeds but geometry is absent:

```json
{
  "status": "RESOLVED",
  "location_precision": "PAGE_TEXT",
  "warnings": ["SOURCE_GEOMETRY_UNAVAILABLE"],
  "document_id": "D_...",
  "document_sha256": "...",
  "physical_page_index": 67,
  "quote": "...",
  "source_spans": ["SS_..."]
}
```

If only page-level provenance is reliable:

```json
{
  "status": "RESOLVED",
  "location_precision": "PAGE_ONLY",
  "warnings": ["SOURCE_GEOMETRY_UNAVAILABLE", "SOURCE_TEXT_LOCATION_UNAVAILABLE"]
}
```

## 8.4 Terminal resolver failures

Only failures that invalidate authoritative source binding are terminal:

```text
UNKNOWN_CORPUS_SNAPSHOT
ID_NOT_IN_SNAPSHOT
UNKNOWN_DOCUMENT
SOURCE_FILE_MISSING
SOURCE_HASH_MISMATCH
UNKNOWN_PAGE
PAGE_TEXT_HASH_MISMATCH
INVALID_SOURCE_SPAN
SOURCE_SPAN_TEXT_MISMATCH
```

`SOURCE_GEOMETRY_UNAVAILABLE` is NOT in the terminal-failure list.

## 8.5 Forbidden fallback

Failure to resolve an authoritative ID must not trigger fuzzy replacement by a similar passage elsewhere.

---

# 9. Contract fix 3 — Stage state is tri-state

Boolean fields are insufficient because retrieval-only mode has stages that have not yet executed.

Each stage uses:

```text
NOT_REACHED
YES
NO
```

Recommended stage record:

```json
{
  "stage": "MODEL_SELECTED",
  "status": "NOT_REACHED",
  "timestamp": null,
  "reason": "LLM_NOT_EXECUTED"
}
```

Minimum stage ledger:

```text
SEARCHABLE
RETRIEVED
RETAINED_AFTER_RANKING
INCLUDED_IN_MODEL_CONTEXT
MODEL_SELECTED
HOST_RESOLVED
DELIVERED_TO_HUMAN
HUMAN_VERIFIED
```

## 9.1 Example — retrieval-only mode

```json
{
  "RETRIEVED": "YES",
  "RETAINED_AFTER_RANKING": "YES",
  "INCLUDED_IN_MODEL_CONTEXT": "NOT_REACHED",
  "MODEL_SELECTED": "NOT_REACHED",
  "HOST_RESOLVED": "YES",
  "DELIVERED_TO_HUMAN": "YES",
  "HUMAN_VERIFIED": "NO"
}
```

This MUST NOT be classified as `MODEL_NON_SELECTION`.

## 9.2 Failure classification rule

`MODEL_NON_SELECTION` may only be emitted when:

```text
MODEL stage was actually reached
AND candidate was present in model context
AND model did not select it when the evaluation contract says selection was required
```

Append-only stage events are also acceptable if they preserve equivalent semantics.

---

# 10. RetrievalRun and CandidateEvidence

## 10.1 RetrievalRun

```json
{
  "retrieval_run_id": "RR_...",
  "case_id": "CASE_...",
  "corpus_snapshot_id": "CS_...",
  "index_build_id": "IB_...",
  "question": "...",
  "allowed_document_ids": ["D_..."],
  "retrieval_config_sha256": "...",
  "started_at": "...",
  "completed_at": "..."
}
```

## 10.2 CandidateEvidence

```json
{
  "candidate_id": "CE_...",
  "retrieval_run_id": "RR_...",
  "passage_id": "P_...",
  "document_id": "D_...",
  "document_role": "...",
  "bm25_rank": 5,
  "dense_rank": 2,
  "combined_rank": 1,
  "combined_score": 0.0314,
  "stages": {
    "RETRIEVED": "YES",
    "RETAINED_AFTER_RANKING": "YES",
    "INCLUDED_IN_MODEL_CONTEXT": "NOT_REACHED",
    "MODEL_SELECTED": "NOT_REACHED",
    "HOST_RESOLVED": "YES",
    "DELIVERED_TO_HUMAN": "YES",
    "HUMAN_VERIFIED": "NO"
  }
}
```

If a rank/score is not meaningful under the active retriever, store `null`.

---

# 11. Retrieval-only evidence workbench

The first working product mode must not require Qwen.

```text
question
→ existing role-aware retrieval
→ candidate packet
→ retrieval trace
→ provenance resolution
→ original PDF
→ human disposition
→ export
```

Minimum surfaces:

1. case header;
2. candidate list;
3. trace inspector;
4. original-PDF viewer;
5. human review controls.

Human controls:

```text
CONFIRM
REJECT
INSUFFICIENT_EVIDENCE
MISSING_QUALIFICATION
NEED_BROADER_SEARCH
WRONG_SOURCE
WRONG_VERSION
```

---

# 12. Original-PDF navigation

Navigation precision:

```text
EXACT_GEOMETRY
PAGE_TEXT
PAGE_ONLY
```

Preferred:

```text
document hash
→ physical page
→ bbox / line geometry
```

Fallback:

```text
document hash
→ physical page
→ canonical text matching
```

Last fallback:

```text
document hash
→ physical page
```

Kotaemon may be referenced for page-opening/viewer behavior, but fuzzy text matching is navigation assistance only, not provenance authority.

---

# 13. Human disposition persistence

Review actions are append-only events.

```json
{
  "disposition_id": "HD_...",
  "review_session_id": "HR_...",
  "candidate_id": "CE_...",
  "action": "CONFIRM | REJECT | INSUFFICIENT_EVIDENCE | MISSING_QUALIFICATION | NEED_BROADER_SEARCH | WRONG_SOURCE | WRONG_VERSION",
  "note": "...|null",
  "created_at": "..."
}
```

Changing a judgment creates a new event.

---

# 14. Broader search

`NEED_BROADER_SEARCH` creates a new retrieval run.

```text
new retrieval_run_id
parent_retrieval_run_id
reason
query
scope
index_build_id
retrieval_config_sha256
```

The prior trace remains immutable.

No autonomous agent or retrieval-tuning program is authorized.

---

# 15. Evidence packet export

Required:

```text
evidence_packet.json
evidence_packet.md
audit_record.jsonl
```

Packet contains:

```text
case metadata
corpus_snapshot_id
index_build_id
source manifest identity
question
retrieval runs
candidate evidence
tri-state stage ledger
source-resolution output and warnings
human dispositions
optional bounded LLM output if later enabled
```

---

# 16. Qwen reconnection gate

Qwen remains disconnected until the retrieval-only workflow passes Gate C.

Reuse the existing host-evidence-ref contract.

Qwen never owns:

```text
document identity
page
hash
source span
citation URL
human disposition
```

No new model evaluation is authorized by VS-1.

---

# 17. Contract fix 4 — T10 uses a deliberately constructed/frozen three-role fixture

The old generic test:

> search returns candidates from all three roles

is invalid because an arbitrary question need not have relevant evidence in all roles.

Replace it with:

### T10 — known three-role fixture preserves all relevant roles

**Given**

A frozen fixture whose gold setup establishes that relevant passages exist in all three roles:

```text
STANDARDS
VENDOR_SUBMISSION
PROFESSIONAL_TEAM_REPORT
```

**When**

the existing role-aware retrieval path is executed under the fixture's predefined query and scope,

**Then**

the serialized candidate set preserves at least one expected relevant candidate from each role, subject to the fixture's frozen retrieval budget.

This fixture must be declared before execution and may not be created after seeing a failure merely to make the test pass.

For ordinary production questions, a valid zero-hit role is not a system failure.

---

# 18. Acceptance tests

## Inventory

- T01 inventory complete.
- T02 every `IMPLEMENTED*` status cites actual repo/artifact paths and verification method.

## Corpus / index identity

- T03 one Florida corpus has a valid `CorpusSnapshot`.
- T04 every selected source has verified SHA-256.
- T05 rebuilding retrieval artifacts does not change `corpus_snapshot_id`.
- T06 a changed retrieval build produces a new `index_build_id`.

## Provenance

- T07 passage/assertion → document → page → span → original PDF round trip.
- T08 altered source hash fails closed.
- T09 no geometry yields `RESOLVED` + warning + downgraded precision.
- T10 invalid evidence ID does not trigger fuzzy substitution.

## Retrieval trace

- T11 frozen known-three-role fixture preserves expected relevant candidates from all three roles.
- T12 BM25/dense/rank metadata serializes correctly when available.
- T13 retrieval miss remains bounded to retrieved evidence.
- T14 intentionally lost candidate is classified at the correct stage.
- T15 unexecuted model stages remain `NOT_REACHED`.

## PDF navigation

- T16 authoritative original PDF opens.
- T17 correct physical page opens.
- T18 exact region highlights when geometry exists.
- T19 page/text fallback works and displays downgraded precision.

## Human review

- T20 `CONFIRM` persists.
- T21 `REJECT` persists.
- T22 `NEED_BROADER_SEARCH` persists against original run.
- T23 disposition journal is append-only.

## Export

- T24 machine-readable packet complete.
- T25 human-readable packet complete.
- T26 export records both corpus and index-build identity.

## Qwen reconnection — only after Gate C

- T27 only host-valid evidence refs accepted.
- T28 citation fields remain host-owned.
- T29 reviewer can reject a correctly cited but unsupported generated claim.

---

# 19. Stop/go gates

## Gate A — Implementation inventory

GO only when:

```text
repository state reconciled
recovered artifacts reconciled
ER-1 state reconciled
all capabilities formally classified
```

Until then:

```text
NO CODE CHANGES
NO INFERENCE
NO RETRIEVAL TUNING
NO UI-ARCHITECTURE CHANGES
```

## Gate B — Source authority

GO only when:

```text
frozen CorpusSnapshot valid
source hashes verified
provenance round trip verified
geometry warnings behave non-fatally
```

## Gate C — Retrieval-only reviewer workflow

GO only when:

```text
candidate serialization works
tri-state trace works
PDF navigation works
human dispositions persist
export works
```

## Gate D — Qwen reconnection

GO only after Gate C.

---

# 20. Required OpenSpec artifacts

This change is represented by:

```text
openspec/changes/vs-1/
├── proposal.md
├── design.md
├── tasks.md
└── acceptance.md
```

No implementation is authorized by creation of these artifacts.

---

# 21. First authorized work product

Only the following work product is next:

```text
artifacts/vs-1/implementation_inventory.json
artifacts/vs-1/implementation_inventory.md
```

The inventory must rely on actual repository paths, artifact paths, manifests, and verification results.

Specifications, conversations, or prior claims are not implementation evidence.

---

# 22. Definition of done

VS-1 is eventually done when:

> For one frozen Florida regulatory corpus and one real review question, RegModelTrace can retrieve role-separated evidence, preserve the complete candidate/search trace with correct stage semantics, deterministically resolve selected evidence to the authoritative original PDF, let a reviewer inspect and disposition the evidence, persist the review state, and export a reproducible audit packet — without relying on a new model, retrieval tuning, Ray optimization, or statistical research.

Anything beyond that belongs to a later bounded change.
