# VS-1 Proposal — Auditable Evidence Review Vertical Slice

## Why

RegModelTrace already contains deterministic parsing, provenance-bearing evidence units, role-aware retrieval, and bounded model citation contracts. The missing product proof is an end-to-end reviewer workflow that turns retrieved evidence into a persistent, source-verifiable audit record.

The immediate product risk is not lack of model capability. It is incomplete product integration across:

```text
frozen corpus
→ retrieval trace
→ authoritative source resolution
→ original-PDF inspection
→ human review
→ audit export
```

## What changes

VS-1 introduces or formalizes:

1. implementation inventory before code changes;
2. immutable `CorpusSnapshot`;
3. separate `IndexBuildManifest`;
4. authoritative source resolver;
5. retrieval candidate serialization;
6. tri-state stage tracing;
7. retrieval-only evidence workbench;
8. original-PDF navigation;
9. append-only human dispositions;
10. reproducible evidence/audit export;
11. bounded Qwen reconnection only after the evidence workflow is reliable.

## What does not change

VS-1 does not authorize:

- statistical hurricane research;
- longitudinal research program;
- GraphRAG or agents;
- new model evaluation/fine-tuning;
- Ray optimization;
- embedding replacement;
- broad retrieval tuning;
- reopening closed semantic evaluations;
- broad UI redesign.

## Product principle

> Machine retrieves and proposes; human verifies against the original PDF.

## Current authorization

Task 0 was completed and accepted by the project owner. Gate A passed.

Task 1 is authorized only for source authority and real-corpus binding:

```text
CorpusSnapshot
+ SourceDocument identities and verified hashes
+ separate IndexBuildManifest
+ recovered retrieval-asset binding
+ real-corpus provenance round trip
```

Tasks 2+ remain pending except for the minimum resolver behavior required to
prove the Task 1 real-corpus round trip. No inference or retrieval/model tuning
is authorized.
