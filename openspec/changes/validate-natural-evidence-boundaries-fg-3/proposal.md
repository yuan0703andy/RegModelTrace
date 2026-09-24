# Validate FG-2 boundaries in natural Florida documents

FG-2 and the Qwen3.8 boundary diagnostic used constructed evidence. Their errors may be artifacts of wording rather than recurring behavior in regulatory documents. FG-3 tests the narrow question of whether those semantic success and failure boundaries appear when **the same sufficient, verified natural evidence** is supplied to two pinned local checkpoints. It does not test retrieval or general regulatory compliance.

The source pool is restricted to the Florida Public Hurricane Loss Model 2021 and 2023 standards cycles identified in the 2026-09-24 corpus inventory. Only case-level exposure-cleared material can enter the primary prospective set. Previously evaluated vendors, exposed FG-1 issues, and KCC Test E remain outside the fresh set. If exposure or human-context sufficiency leaves too few cases, FG-3 closes as insufficient evidence rather than manufacturing cases.

The main assumption is that original PDF text, chronology, and source roles can be reconstructed accurately enough for two independent humans to adjudicate from the **exact packet shown to the model**. That assumption is tested before inference. Natural cases are dependent within one lineage and two standards cycles, so FG-3 supports bounded replication claims, not population accuracy estimates.

The full prospective contract is [the FG-3 protocol](../../../experiments/fg3_natural_boundary/protocol/spec.md). The first checkpoint is source-only exposure audit and candidate discovery. No natural inference is authorized by completion of that checkpoint alone.
