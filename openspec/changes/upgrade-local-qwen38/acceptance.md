# Acceptance

- The cached checkpoint resolves to the pinned public revision and required
  weight files are complete.
- A DCC compute node with compatible GPUs loads the checkpoint and persists
  both raw responses before schema validation.
- Both synthetic responses are valid under their fixed JSON schemas, with thinking
  disabled explicitly; no semantic retries or truth-dependent corrections.
- Active configuration and model snapshot agree on exact model and revision;
  prompt accounting uses the same chat-template options as generation.
- Frozen FG-2 and historical evaluation outputs remain unchanged.
- A successful smoke is reported only as runtime compatibility, never as a
  RegModelTrace accuracy result.
