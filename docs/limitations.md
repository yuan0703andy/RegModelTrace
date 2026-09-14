# Limitations and claim boundaries

1. **Partial alignment remains the central model failure.** All five saved truth-`PARTIALLY_ALIGNED` primary cases were classified `ALIGNED`. The system should not be used as an unattended conformance decision maker.

2. **Conflict detection is unvalidated.** No natural truth-`CONFLICT` case occurred in the final saved fixtures. Zero observed conflict errors does not establish conflict sensitivity.

3. **The probability vectors are interface outputs.** They are candidate-renormalized next-token scores under fixed prompts and verbalizers. They are not calibrated epistemic probabilities or Bayesian posteriors.

4. **Documentary alignment is bounded by the evidence.** Vendor submissions and reviewer reports do not expose hidden production implementation. Reviewer verification cannot fill a missing vendor-demonstration facet.

5. **Citation resolution is weaker than entailment.** The host guarantees that a citation maps to an exact source assertion. Human review still found unsupported claims in the same-corpus unseen audit.

6. **A retrieval miss is not corpus absence.** `UNRESOLVED_FROM_RETRIEVED_EVIDENCE` describes the bundle supplied to the generator. It does not prove the fixed corpus lacks evidence or that an event did not occur.

7. **Review and change do not imply causation.** A requirement, reviewer scrutiny, and a documented update are separate facts unless an explicit post-review response or causal link connects them.

8. **Parser portability is layout-specific.** Narrative evidence remained reconstructable in KCC, while four numeric table panels failed identity recovery. The project does not claim universal PDF/table parsing.

9. **Ray improved throughput without exact generative determinism.** One of 4,096 outputs changed across environments near a decision boundary. The historical parity failure is preserved.

10. **The public repository is compact.** Raw PDFs, retrieval databases, embeddings, model weights, and cluster journals are omitted. The package supports code review, offline contract tests, and a static evidence demo; it cannot independently replay the historical GPU runs.

11. **Test E is spent.** KCC results may motivate future work but cannot serve as an untouched test for a method designed after observing them.

12. **Fine-tuning was not justified for the closed release.** A future adapter study needs prospective label rules, counterexamples, leakage-aware splits, and a new evaluation arrangement.

