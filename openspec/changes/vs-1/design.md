# VS-1 Design

## 1. Identity model

Separate immutable corpus identity from rebuildable retrieval identity.

### CorpusSnapshot

Identifies authoritative source/canonical content:

```text
source manifest
parser identity
canonical passage inventory
```

It excludes retrieval-artifact build hashes.

### IndexBuildManifest

Identifies one retrieval representation built over a corpus:

```text
embedding model / revision
embedding artifacts
FTS artifacts
retrieval config
```

Every `RetrievalRun` binds both.

## 2. Provenance resolver

One authoritative resolver maps:

```text
assertion / passage / source span
→ document hash
→ physical page
→ canonical quote
→ source geometry when available
```

Terminal failures invalidate authoritative binding.

Geometry absence is a warning, not failure:

```json
{
  "status": "RESOLVED",
  "location_precision": "PAGE_TEXT",
  "warnings": ["SOURCE_GEOMETRY_UNAVAILABLE"]
}
```

## 3. Stage semantics

Stages use:

```text
NOT_REACHED
YES
NO
```

This prevents retrieval-only mode from being mislabeled as model failure.

A model-related `NO` is valid only if the model stage actually executed.

## 4. Reviewer workflow

```text
Case
→ RetrievalRun
→ CandidateEvidence[]
→ resolver
→ original PDF
→ ReviewDisposition[]
→ evidence packet
```

Qwen is not required for this path.

## 5. Persistence

Human dispositions are append-only events.

Broader search creates a new `RetrievalRun` with a parent pointer.

## 6. PDF navigation

Priority:

```text
exact geometry
→ page-text navigation
→ page-only navigation
```

Display the actual precision.

## 7. Retrieval fixtures

Ordinary product questions may validly have no relevant evidence in one or more roles.

Therefore the three-role acceptance test uses a predeclared frozen fixture known to contain relevant passages in all three roles.

## 8. Boundaries

No new retriever/model optimization is part of VS-1.
