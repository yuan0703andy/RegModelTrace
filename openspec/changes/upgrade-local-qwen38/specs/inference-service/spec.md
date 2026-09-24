## MODIFIED Requirements

### Requirement: Pinned local generation runtime

The active inference service SHALL identify its local model by repository and
exact revision, SHALL reject an incompatible checkpoint path, and SHALL apply
the same explicit chat-template thinking setting to token counting and
generation.

#### Scenario: New local model is ready

- **WHEN** the pinned Qwen3.8 checkpoint passes the typed-GPU runtime smoke
- **THEN** active service configuration points to that revision and preserves
  host-owned source and citation identity.

#### Scenario: Runtime compatibility fails

- **WHEN** the checkpoint cannot load or the structured response is invalid
- **THEN** active service configuration remains on its prior checkpoint, and
  the failure is recorded without changing historical evaluation artifacts.
