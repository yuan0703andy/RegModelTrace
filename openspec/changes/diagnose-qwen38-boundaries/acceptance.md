# Acceptance

- Exactly 18 frozen cases and 18 expected labels, with matching unique IDs.
- The model-facing file contains no expected labels; the runner never imports
  or reads the oracle.
- Every generated response, including invalid JSON or a wrong label, is
  persisted before scoring; failures are not retried to improve the result.
- The report includes source text, expected label, model label, structural
  validity, case-level errors, runtime identity, and the original case repeat.
- The report explicitly does not claim natural-domain accuracy, calibrated
  probabilities, or readiness to change the active product default.
