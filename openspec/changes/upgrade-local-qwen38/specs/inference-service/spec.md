## MODIFIED Requirements

### Requirement: Pinned local generation runtime

The active inference service SHALL identify its local model by repository and
exact revision, SHALL reject an incompatible checkpoint path, and SHALL apply
the same explicit chat-template thinking setting to token counting and
generation.

#### Scenario: New local model is selected

- **WHEN** the owner selects the pinned Qwen3.8 checkpoint
- **THEN** active service configuration points to that revision and preserves
  host-owned source and citation identity, while readiness remains pending
  until the typed-GPU smoke passes.

#### Scenario: Runtime compatibility fails

- **WHEN** the checkpoint cannot load or the structured response is invalid
- **THEN** the failure is recorded, the active service does not silently load a
  different checkpoint, and the prior frozen configuration remains available
  for explicit rollback without changing historical evaluation artifacts.
