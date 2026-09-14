# Project narrative

RegModelTrace addresses a recurring failure mode in technical-document assistants: fluent answers collapse requirement text, vendor claims, reviewer activity, and inferred model behavior into one story. In a regulatory setting, that collapse can turn an incomplete record into an unsupported compliance or causal claim.

The system makes evidence identity a host responsibility. A deterministic parser preserves physical pages and exact source spans; complete assertions become citation units; larger passages become retrieval units. A question fans out across regulator, vendor, and reviewer document roles. Qwen receives role-partitioned evidence, returns a constrained answer, and selects only request-scoped handles. The host validates those handles and renders the source metadata.

The same evidence discipline supports a second task: comparing an applicable regulatory requirement with documented vendor implementation. A forced-choice interface separates evidence sufficiency from the substantive relation. This exposed the main model weakness: the base Qwen model recognized clear alignment but repeatedly upgraded incomplete multi-facet documentation to full alignment. The project preserved that negative result and declined to fine-tune from a small, selected dataset.

The systems contribution is a Ray backend that schedules persistent vLLM replicas while preserving request and provenance accounting. Two GPUs achieved 2.004× the one-GPU Ray throughput on 4,096 frozen requests. One environment-sensitive label prevented an exact-determinism claim, so the release records both the scaling success and the parity limitation.

The resulting contribution is a defensible local LLM workflow for regulated technical evidence: source-traceable answers, explicit uncertainty, actor separation, prospective evaluation, and multi-GPU execution. The project demonstrates how system contracts and evidence boundaries can matter more than adding a larger model or agent framework.

