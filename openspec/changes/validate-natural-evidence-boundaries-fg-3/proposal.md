# Validate FG-2 boundaries in natural Florida documents

FG-2 and the Qwen3.8 boundary diagnostic used constructed evidence. Their errors may be artifacts of wording rather than recurring behavior in regulatory documents. FG-3 tests the narrow question of whether those semantic success and failure boundaries appear when **the same gold-blind, hash-frozen natural evidence packet** is supplied to two pinned local checkpoints. It does not test retrieval or general regulatory compliance.

The source pool is restricted to the Florida Public Hurricane Loss Model 2021 and 2023 standards cycles identified in the 2026-09-24 corpus inventory. Only cases with no known exposure under the frozen ledger can enter the primary prospective set. Previously evaluated vendors, exposed FG-1 issues, and KCC Test E remain outside the fresh set. If exposure or human-context sufficiency leaves too few cases, FG-3 closes as insufficient evidence rather than manufacturing cases.

The main assumption is that original PDF text, chronology, and source roles can be reconstructed accurately enough for two independent humans to adjudicate from the **exact packet shown to the model**. That assumption is tested before inference. Natural cases are dependent within one lineage and two standards cycles, so FG-3 supports bounded replication claims, not population accuracy estimates.

The full prospective contract is [the FG-3 protocol](../../../experiments/fg3_natural_boundary/protocol/spec.md). The first checkpoint froze 1,708 cue hits and 85 selected page leads. The v1.3 amendment fixes packet construction, known-exposure scope, adjudicability states, and interpretation before Checkpoint 2 source screening. No natural inference is authorized by this amendment.
