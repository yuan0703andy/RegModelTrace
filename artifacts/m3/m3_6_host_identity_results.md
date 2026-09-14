# M3.6 — Host-owned identity: PASS / FREEZE

M3 is frozen under the user-approved primary assertion-classification contract. The model produces only `evidence_type`; the host attaches its known assertion ID after verifying response binding.

| Gate | First: job 55144926 | Repeat: job 55145000 |
|---|---|---|
| Valid structured outputs | 16/16 | 16/16 |
| Correct primary evidence types | 16/16 | 16/16 |
| Source and request-binding errors | 0 | 0 |
| Critical field stability | Reference | PASS: 16/16 identical |

Both jobs ran independently on Duke DCC using the same Qwen2.5-32B-Instruct-AWQ revision `5c7cb76a268fc6cfbb9c4777eb24ba6e27f9ee6c`, vLLM 0.29.0, temperature 0 and seed 0. The repeat was submitted only after the first persisted run independently passed. First and repeat job elapsed times were 72 and 57 seconds, including startup. No API calls or full-corpus inference were made.

The sixteen original assertions, source context, primary labels and ten-type ontology are unchanged from M3.5. Only identifier ownership changed. The 53 pre-inference software controls passed; maximum complete input was 869 tokens. The scorer independently regenerated expected request tokens, verified raw-output inventory and source identity, and scored labels only after persistence and hashing.

## Results by source assertion

| Core record / claim | Primary type | First | Repeat |
|---|---|---|---|
| S_M3B / 1 | REGULATORY_REQUIREMENT | PASS | PASS |
| S_M3_CONTEXT / 1 | REGULATORY_REQUIREMENT | PASS | PASS |
| V_M3B / 1 | VENDOR_COMPLIANCE_ASSERTION | PASS | PASS |
| V_SMOOTHING / 1 | VENDOR_METHODOLOGY | PASS | PASS |
| V_POISSON / 1 | VENDOR_METHODOLOGY | PASS | PASS |
| V_POISSON / 2 | VENDOR_METHODOLOGY | PASS | PASS |
| T_LANDFALL_REVIEW / 1 | REVIEWER_SCRUTINY | PASS | PASS |
| T_M3_REVIEW / 1 | REVIEWER_SCRUTINY | PASS | PASS |
| T_M3_REVIEW / 2 | REVIEWER_SCRUTINY | PASS | PASS |
| V_PRIOR_UPDATE / 1 | MODEL_UPDATE | PASS | PASS |
| V_BASELINE_VERSION / 1 | VERSION_BASELINE | PASS | PASS |
| V_BASELINE_VERSION / 2 | VERSION_BASELINE | PASS | PASS |
| T_OPENING_UPDATES / 1 | CHRONOLOGY_EVIDENCE | PASS | PASS |
| T_OPENING_UPDATES / 2 | MODEL_UPDATE | PASS | PASS |
| T_HISTORY / 1 | REGULATORY_REQUIREMENT | PASS | PASS |
| T_HISTORY / 2 | REVIEWER_SCRUTINY | PASS | PASS |

## Audit artifacts

- [First independent score](m3_6_benchmark/first.json).
- [Repeat independent score and stability](m3_6_benchmark/repeat.json).
- [Frozen pre-inference contract](frozen/m3.6-host-identity-evaluator-1.0/freeze.json).
- [Final M3 freeze receipt](m3_classification_freeze.json).
- [First raw outputs](../extraction/m3-6-local-55144926/results.json).
- [Repeat raw outputs](../extraction/m3-6-local-55145000/results.json).

First results SHA-256: `d566b2fc7298111f790a33d83d6f655d9c6cb883755053ee104ae9c88bada09f`.

Repeat results SHA-256: `607540a72ec5e64679707bb0f2363eb1bde219ad27419f7bc73ca8cc2ebdebda`.

The result files have different hashes because execution metadata differs. Stability concerns the identical host-bound assertion IDs and primary types, not timestamps.

## Interpretation and transition

This establishes local-model feasibility on the fixed sixteen-assertion development fixture. It does not establish held-out generalization, complete-corpus classification, assertion selection or retrieval accuracy. The 160 numeric cells remain on the unchanged deterministic M2 route. Qualification, reference and causal relations remain for M5; causal attribution in Gold Case 001 remains UNRESOLVED.

The historical M3.5 score remains 15/16: its incorrect generated identifier is neither repaired nor retroactively accepted. Earlier tag, span and candidate-selection failures also remain unchanged. The new M3 acceptance scope prospectively supersedes those interfaces.

M3 extraction tuning stops here. M4 may now build the evidence store and retrieval layer. The sixteen oracle-selected assertions must not be the sole search pool or be used to claim full retrieval coverage.
