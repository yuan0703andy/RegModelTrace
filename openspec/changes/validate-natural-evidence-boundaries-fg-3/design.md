# Design

The execution order is: freeze deterministic discovery procedure; search the six identified PDFs; record all page-level leads and exclusions; verify exact source context; audit prior exposure at the clause and passage level; freeze model-facing evidence packets; obtain two independent human judgments on precisely those packets; freeze scorer-only truth; qualify runtime repeatability on exposed synthetic controls; run one predeclared schedule for both checkpoints; persist raw results before scoring; report label and evidence-grounded joint correctness. Model identities are blinded for post-hoc error coding.

Panel A concerns requirement/evidence semantics and uses the existing `SUPPORTED`, `CONTRADICTED`, `CONFLICTING`, `UNRESOLVED` contract. Panel B distinguishes `SCRUTINY_ONLY` from `CHALLENGE_ESTABLISHED` with an explicit not-adjudicable exit. Panel C requires an explicit review-to-**model method/implementation** modification link, the same substantive object, and chronology; disclosure-response changes alone do not satisfy it.

The candidate registry holds discovery provenance and source references, never gold. The evidence packet is immutable and hash-bound to both human adjudication and model inference. Scorer-only truth is inaccessible to the runner. Discovery and exposure ledgers preserve rejected and ambiguous candidates so a missing case cannot be mistaken for corpus absence. Host citation resolution checks identity; independent source review checks whether a cited span supports the verdict.

No new retrieval architecture, oracle ladder, temporal filtering, fine-tuning, calibration, or active-default switch is part of this change. Those are possible later questions only if FG-3 findings warrant them.
