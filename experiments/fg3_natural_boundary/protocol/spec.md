I would freeze the next phase as a narrow continuation of FG-2, using the inventory you just completed.

# RegModelTrace FG-3
## Natural Evidence-Boundary Validation

**Version:** 1.3 (measurement and eligibility amendment before source screening)
**Date:** 2026-09-24
**Status:** FROZEN PROSPECTIVE PROTOCOL — NATURAL CASES NOT YET ADJUDICATED

---

## 0. Purpose

FG-3 tests whether the semantic boundary behaviors observed in the completed synthetic diagnostics also occur in natural Florida regulatory documents.

FG-3 is a direct continuation of:

1. **FG-2 synthetic semantic contrasts**, which examined requirement decomposition and evidence alignment; and
2. **Qwen3.8 synthetic evidence-boundary diagnostic**, which examined reviewer-action semantics and explicit review-to-modification causality.

FG-3 does **not** introduce a new RAG architecture.

FG-3 does **not** evaluate temporal RAG.

FG-3 does **not** evaluate product-output compliance, accounting standards, SEC filings, calibration, fine-tuning, or reinforcement learning.

The scientific question is:

> **Do the semantic success and failure boundaries observed in controlled synthetic diagnostics reproduce in natural regulatory documents when the correct source evidence is supplied to the model?**

The immediate objective is to distinguish:

$$
\text{semantic/judgment failure}
$$

from later:

$$
\text{retrieval failure}.
$$

Retrieval remains fixed and oracle-controlled in FG-3.

---

# 1. Frozen prior state

## 1.1 FG-2

FG-2 is closed as a synthetic diagnostic.

Its relevant observations are:

- whole-requirement accuracy: 10/12;
- individual-facet accuracy: 22/24;
- case-level facet aggregation: 10/12;
- facet decomposition was not uniformly beneficial.

Observed candidate semantic boundaries included:

1. cross-clause aggregation;
2. illustrative versus mandatory language;
3. unsupported equivalence between undefined terminology.

Successful controls included:

- quantifier distinctions;
- source-role distinctions;
- simple paraphrase invariance.

FG-2 remains synthetic evidence only.

No FG-2 result or gold label may be changed during FG-3.

---

## 1.2 Qwen3.8 synthetic boundary diagnostic

The completed Qwen3.8 diagnostic used:

```text
Model:
Qwen/Qwen3.8-27B-FP8

Revision:
017b9c7af6b5689d5dd426a76e0bc077eb5ca20a

Runtime:
vLLM 0.29.0

Thinking:
disabled

Temperature:
0

Seed:
1847
```

Observed descriptive results were:

```text
Reviewer panel: 8/12 correct
Causal panel:   5/6 correct
Total:          13/18
```

These counts describe the constructed fixture only.

Observed candidate boundaries were:

### Reviewer-action semantics

Some neutral review language was classified as challenge:

```text
reviewed the methodology
examined the calculations
```

while one explicit rejection statement was classified as scrutiny.

Therefore the synthetic evidence does not support a simple monotone "overclaiming" explanation.

The candidate phenomenon is:

$$
\text{instability in the SCRUTINY / CHALLENGE semantic boundary}.
$$

### Review-to-modification causality

All four no-link controls remained:

```text
NOT_ESTABLISHED
```

but the concise explicit causal statement:

```text
In response to the Professional Team's request ...
RMS revised ...
```

was missed.

A more explicit two-sentence causal statement was correctly classified.

The candidate phenomenon is:

$$
\text{causal recognition may depend on linguistic realization}.
$$

These are hypotheses to test in natural documents, not established natural-domain findings.

---

## 1.3 Active model status

The active RegModelTrace production/default configuration remains:

```text
system_v1.json
Qwen2.5
```

Qwen3.8 remains an opt-in candidate.

FG-3 must not modify the active default.

For reproducibility, the exact Qwen2.5 model name, revision, tokenizer, prompt contract, and runtime configuration must be loaded from the persisted project configuration rather than reconstructed from chat history.

---

# 2. Verified natural-document inventory

The 2026-09-24 inventory establishes local custody of:

```text
45 Florida PDF paths
33 distinct PDF contents
```

after deduplication by SHA-256.

Normalized path counts are:

```text
REGULATOR: 7 paths / 3 unique contents
VENDOR:    19 paths / 15 unique contents
REVIEWER:  19 paths / 15 unique contents
```

All 45 inventoried paths matched their previously recorded SHA-256 and file size.

Six source manifests also matched their recorded hashes.

These checks establish file identity only.

They do not establish:

- parser correctness;
- source-span correctness;
- case eligibility;
- independent human truth;
- model accuracy.

---

# 3. Eligible natural source pool

The primary prospective source pool is restricted to the two Florida Public Hurricane Loss Model standards cycles.

## 3.1 2021 cycle

```text
Regulator:
shared_standards_2021_standards.pdf

Vendor:
florida_public_2021_fphlm_submission.pdf

Reviewer:
florida_public_2021_fphlm_review.pdf
```

## 3.2 2023 cycle

```text
Regulator:
shared_standards_2023_standards.pdf

Vendor:
florida_public_2023_fphlm_submission.pdf

Reviewer:
florida_public_2023_fphlm_review.pdf
```

The four vendor/reviewer PDFs are currently marked `SCALE_UNLABELLED`.

This means they have no frozen semantic labels in that Scale-1 split.

It does **not** mean every passage is unseen.

The standards documents are already in `HISTORICAL_CLOSED`.

Therefore eligibility must be determined at the **case/span level**, not merely from document partition labels.

---

# 4. Protected and excluded sources

The following material must not be promoted into fresh independent FG-3 test cases:

- Gold Case 001;
- FG-1 source issues;
- ARA M-3.B;
- CoreLogic CI-5;
- RMS M-3.B;
- CoreLogic M-2;
- historical Impact evaluation cases;
- historical CoreLogic evaluation cases;
- historical Verisk evaluation cases;
- KCC Test E;
- any FG-2 synthetic cases;
- any Qwen3.8 synthetic-boundary cases;
- demonstration questions whose outputs influenced prior development;
- any passage whose previous model outcome was inspected and used to alter the semantic interface.

Protected historical materials may still be used to clarify annotation definitions.

They do not count as independent FG-3 evidence.

KCC Test E remains sealed.

FG-3 does not authorize opening it.

---

# 5. Exposure audit

FG-3 uses `KNOWN_EXPOSURE_LEDGER_V1`, frozen before substantive screening. Its exact searchable files and known development/demonstration touchpoints are recorded in [`known_exposure_ledger_v1.json`](known_exposure_ledger_v1.json) and its file manifest. The scope covers Gold Case 001, FG-1 and FG-2, the Qwen3.8 synthetic fixture, historical Impact/CoreLogic/Verisk evaluation metadata and outcomes, saved demo questions and model-facing requests, adjudication assets, and notes containing case outcomes. KCC Test E is a protected closed partition: its sealed content is not opened for FG-3. The ledger records that exclusion. Mechanical parser/index processing alone is recorded separately from observed outcomes or developer use.

Every selected lead and every formed case receives one of:

```text
NO_KNOWN_EXPOSURE_UNDER_FROZEN_LEDGER
KNOWN_EXPOSED
SUBSTANTIALLY_EQUIVALENT_TO_KNOWN_EXPOSURE
MATCH_UNRESOLVED
```

Only `NO_KNOWN_EXPOSURE_UNDER_FROZEN_LEDGER` may enter the primary prospective set. This means the frozen ledger search found no known exposure after exact and substantially equivalent clause, counterpart passage, question, prior adjudication, demo, model-output, and synthetic-derivation checks. It does **not** prove the material was never seen. Undocumented historical exposure outside the ledger cannot be excluded. `MATCH_UNRESOLVED` remains outside the primary set until resolved. A known developer-inspected page remains `KNOWN_EXPOSED` even if no model result was viewed.

The first-checkpoint `EXPOSURE_UNKNOWN` and `DEVELOPER_EXPOSED` fields remain unchanged as historical discovery state. Checkpoint 2 writes a separate ledger-v1 assessment with matched file IDs, span or question, exact/equivalence rationale, assessor, and resolution. The assessment is repeated after cross-document pairing, because a regulator lead can be unexposed while its paired vendor or reviewer passage is exposed. Absence of a text match in a shortlist is never evidence of corpus absence.

---

# 6. Unit of analysis

The base unit is a **natural source-grounded case**.

Each case must have:

```text
case_id
panel
standards_cycle
dependency_cluster
regulator_document_id
vendor_document_id
reviewer_document_id
source_sha256s
physical_pdf_page
source_span
surrounding_context
target_question
exposure_status
adjudicability_status
```

Different prompts, whole/facet variants, models, or repeated inference runs derived from the same source case are **not independent cases**.

Repeated or near-duplicate source spans must share the same `dependency_cluster`.

The study must never report model requests as though they were independent natural examples.

---

# 7. Candidate discovery

Candidate discovery is source-only.

No FG-3 model inference is allowed during discovery.

Candidate discovery may use:

- deterministic text search;
- the existing parser;
- keyword search;
- section headings;
- source-role metadata;
- manual PDF reading.

Candidate discovery must not use model correctness to decide whether a case is retained.

Searches should be broad enough to locate both easy and difficult examples.

Cases must not be selected only because they are expected to produce errors.

No class balance or panel quota may be artificially manufactured.

## 7.1 Predeclared stopping rule

Before source screening, freeze a separate discovery procedure for each panel. Each procedure records the exact documents and sections searched, deterministic query set, inclusion and deduplication rules, candidate cap if any, and stopping condition. Discovery terminates under that rule regardless of whether the resulting candidates look interesting or likely to challenge either model. If eligible candidates exceed the cap, select by a deterministic hash rank within dependency clusters; never select on expected difficulty or similarity to synthetic errors. Each screened lead records `discovery_protocol_id`, `discovery_query_id`, `discovery_rank`, `dedup_cluster`, and `selection_reason`. Keyword hits are leads, not cases or gold labels.

## 7.2 Predeclared case formation and pairing protocol

The frozen page-lead selection remains unchanged. Before interpreting the 85 selected leads, freeze the separate [case formation contract](case_formation_protocol.json). It fixes how a page lead becomes a bounded source unit, how counterpart passages are searched, when a pair is ambiguous or unavailable, and how dependent observations are grouped. A lead anchors at most one case: take the earliest first match among its selected query IDs, using query ID to break a tie. If that anchor is boilerplate or unusable, record the exclusion; do not move to a more interesting occurrence on the page. Preserve every candidate pair returned by the first applicable pairing tier and every exclusion reason.

For **Panel A**, identify the complete requirement clause containing the anchor, its hierarchy, and immediately attached qualifications. Search only the same-cycle vendor submission. Use the exact hierarchical standard/disclosure identifier first, the exact subsection heading second, and literal quoted or title-cased technical terms appearing in the clause third. Record all source candidates returned by the first nonempty tier before judging support. A broad section, overflow, or no bounded match is documented as such; do not choose the passage that makes the answer easiest. An unresolved bounded packet cannot establish absence from the full corpus.

For **Panel B**, the natural unit is the complete numbered reviewer comment and its attached disposition, or the containing unnumbered paragraph with an immediately attached disposition line. The parent heading travels with the unit. A compound block that cannot be separated by the document's own numbering is marked not adjudicable for the binary target. Do not vary the context window according to the likely label.

For **Panel C**, a selected reviewer or vendor lead is paired only with the same-cycle counterpart document. Try exact requirement/standard ID, then explicit comment/response ID, then an exact named substantive object, then bounded literal terminology recorded from the anchor **before** counterpart search. Stop at the first nonempty tier and preserve every candidate at that tier. Every pair records `review_object`, `vendor_object`, `pairing_basis`, `same_object_status`, modification type, and chronology. `same_object_status` is `CONFIRMED`, `NOT_SAME_OBJECT`, or `UNRESOLVED`. Only `CONFIRMED` same-object pairs can support `EXPLICIT_REVIEW_LINK_STATED`; a revised disclosure or written response alone is not a model-method change. Shared broad topic or temporal order does not form a causal pair.

The page-level `dedup_cluster` is a discovery artifact. Formed cases get a separate `dependency_cluster`. Exact or substantially equivalent clauses across 2021/2023, repeated reviewer comments or vendor responses, shared source units, and whole/facet variants are linked into one cluster before any independence claim or case count. When substantial equivalence remains uncertain, group conservatively and record the uncertainty. Two cycle-specific observations in one cluster are not independent replications.

---

## 7.3 Cue-defined sampling frame and negative-frame audit

The 1,708 query/page hits cover only pages captured by the frozen cue-based searches. They are not a census of all natural regulatory phenomena. The 85 selected page leads are a capped hash-ranked sample within that cue-defined frame; they are not a prevalence sample of Florida regulatory reasoning.

Before reading substantive natural outcomes, freeze a target 24-page negative-frame audit: four hash-ranked pages per each of the six source PDFs from pages with **no hit under any query applicable to that document**. If fewer than four no-hit pages exist, use all and report the shortfall. The [selection rule](negative_frame_protocol.json) yields 21 pages because the 2021 reviewer report has only two no-hit pages and the 2023 reviewer report only three; the [selected page IDs](../candidates/negative_frame_pages.jsonl) were frozen without viewing their content. Human reviewers inspect only whether a Panel A/B/C target phenomenon exists despite the missing cue, recording `YES`, `NO`, or `AMBIGUOUS`. These pages never enter primary model evaluation, do not replace failed leads, and do not reopen discovery. Report the denominator and observed misses as a limited frame diagnostic, not an estimate of corpus-wide recall.

---

# 8. Panel A — Requirement semantics

## 8.1 Question

Does the requirement–evidence judgment behavior observed in FG-2 reproduce in natural regulatory text?

Panel A uses:

```text
regulatory requirement
+
vendor evidence
```

and optionally reviewer evidence only when the target explicitly concerns reviewer evidence.

---

## 8.2 Candidate semantic families

Search for natural examples involving:

### A1. Illustrative versus mandatory language

Examples of cues:

```text
such as
including
for example
may include
shall include
must
shall
required
```

### A2. Cross-clause scope

Cases where multiple requirements or propositions occur near one another and evidence supports different propositions differently.

### A3. Quantifiers

Examples:

```text
all
each
every
some
at least one
```

### A4. Defined versus undefined equivalence

Cases in which two terms are:

- explicitly defined as equivalent;
- clearly different;
- or not linked by available source evidence.

### A5. Actor/source distinction

Examples in which:

```text
vendor statement
reviewer observation
regulator requirement
```

must not be substituted for one another.

---

## 8.3 Panel A labels

Use the existing documentary relation contract:

```text
SUPPORTED
CONTRADICTED
CONFLICTING
UNRESOLVED
```

Do not create a new compliance ontology in FG-3.

---

## 8.4 Whole versus facet design

For a case containing multiple genuine propositions, create:

```text
WHOLE
```

and human-defined:

```text
FACET_1
FACET_2
...
```

before any FG-3 model output is observed.

Facets must preserve necessary parent context.

Do not create facets merely to increase the number of test requests.

Single-proposition requirements are not eligible for the whole-versus-facet comparison.

---

# 9. Panel B — Reviewer scrutiny versus challenge

## 9.1 Question

Can the model distinguish ordinary reviewer examination from an explicit reviewer challenge?

The target distinction is:

$$
\text{SCRUTINY ONLY}
\quad\text{versus}\quad
\text{CHALLENGE ESTABLISHED}.
$$

---

## 9.2 SCRUTINY_ONLY

Use this label when the source establishes examination, review, inspection, assessment, verification, or consideration but does not establish explicit negative evaluation or required corrective action.

Possible natural language includes:

```text
reviewed
examined
inspected
assessed
verified
confirmed
considered
```

These verbs are discovery cues only.

They do not determine gold labels.

---

## 9.3 CHALLENGE_ESTABLISHED

Use this label only when the context establishes an explicit challenge beyond mere scrutiny, such as:

- identified deficiency;
- stated noncompliance with a requirement;
- rejected an approach;
- issued an objection;
- requested correction;
- required revision;
- directed the vendor to change or correct something.

Again, lexical presence alone does not determine the label.

Full surrounding context must be read.

---

## 9.4 Compound or ambiguous cases

If a passage combines scrutiny and challenge in a way that cannot be cleanly reduced to the binary target, mark:

```text
NOT_ADJUDICABLE_FOR_PANEL_B
```

Do not force ambiguous natural text into a binary gold label.

These cases remain documented and may motivate a later ontology revision.

---

# 10. Panel C — Stated review-to-modification link

## 10.1 Question

Do the permitted documents **explicitly state** that a reviewer action or request prompted a vendor change to the same substantive model method, parameterization, implementation, or output? The task detects a source-attributed statement. It does not independently establish real-world causation.

---

## 10.2 Labels

### EXPLICIT_REVIEW_LINK_STATED

Use only when vendor, reviewer, or both explicitly state a link from reviewer request, instruction, objection, or intervention to a substantive vendor model modification concerning the **same object**. Record the exact linking language and `link_statement_source_role = VENDOR | REVIEWER | BOTH`. Chronology alone is insufficient. A statement that only a disclosure or written response was revised does not satisfy this model-modification target.

---

### REVIEW_LINK_NOT_ESTABLISHED

Use when the bounded source packet contains review and later change without an explicit link, a predating change, scrutiny without requested modification, documentation-only revision, or passages about different objects. This label means the link is not established **from the frozen packet**; it does not assert full-corpus absence.

---

### NOT_ADJUDICABLE_FOR_PANEL_C

Use when source chronology, object identity, modification type, or the meaning of the linking statement cannot be determined from the permitted source record. No minimum positive count is required. A high rate of not-adjudicable cases is a valid result, including when earlier versions or initial submission material are unavailable.

---

## 10.3 Modification type

Every candidate causal case must separately record:

```text
MODEL_METHOD
MODEL_PARAMETERIZATION
MODEL_IMPLEMENTATION
MODEL_OUTPUT
DOCUMENTATION_ONLY
DISCLOSURE_RESPONSE_ONLY
UNKNOWN
```

A revised written response is not automatically a model modification.

This distinction is mandatory.

---

## 10.4 Chronology

Every Panel C candidate must record, where available:

```text
submission_snapshot_date
review_date
request_date
response_date
revision_date
final_submission_date
```

Unknown dates remain null.

Do not infer a causal sequence from file names or nominal standards years.

Chronology supports interpretation but does not by itself establish causality.

---

# 11. Candidate screening workflow

For each discovered lead:

```text
DISCOVERED
    ↓
KNOWN-EXPOSURE PRECHECK
    ↓
SOURCE_CONTEXT_VERIFIED
    ↓
CASE_FORMED / EXCLUDED under frozen pairing rule
    ↓
CASE-LEVEL EXPOSURE CHECKED
    ↓
MODEL-FACING EVIDENCE PACKET CONSTRUCTED AND HASHED
    ↓
INDEPENDENT HUMAN JUDGMENT ON EXACTLY THAT PACKET
    ↓
HUMAN_CONTEXT_SUFFICIENT / PACKET_INSUFFICIENT /
SOURCE_INDETERMINATE / HUMAN_DISAGREEMENT
    ↓
TRUTH_FROZEN (eligible sufficient cases only)
    ↓
MODEL_INFERENCE
```

No model inference may occur before `TRUTH_FROZEN`. A lead or case failing an earlier gate remains in the audit ledger. Exposure screening can exclude a lead before costly case formation; final exposure status is still rechecked after pairing.

## 11.1 Evidence packet construction

The independent packet assembler uses the target question, verified source-unit boundaries, permitted source roles, and frozen case-pairing output. It cannot use a gold label, adjudicator answer, model prediction, or anticipated model correctness. The [packet construction contract](packet_construction_protocol.json) fixes ordered content, all-match retention, length/overflow handling, canonical serialization, and SHA-256 identity **before** human adjudication. It does not select the most supportive or contradictory span. Panel A includes the complete regulator unit and all first-tier vendor counterpart units; Panel B includes the complete reviewer comment/disposition unit; Panel C includes the complete reviewer unit and all first-tier vendor counterpart units. If the bounded packet is too large, it exits as overflow without selective truncation.

The same frozen packet bytes, source text, role labels, source references, and surrounding context are supplied to both human adjudicators and to both model configurations. Scorer-only truth is stored separately. A packet can be judged insufficient without modifying it after a human sees the case.

The frozen v1.2 case-formation JSON retains its historical checksum. For Panel C, its legacy positive label `EXPLICIT_REVIEW_CAUSED_MODIFICATION` is superseded **only for v1.3 adjudication and inference** by `EXPLICIT_REVIEW_LINK_STATED`; its legacy negative wording is superseded by `REVIEW_LINK_NOT_ESTABLISHED`. The v1.2 pairing tiers, anchors, match limits, and dependency rules remain unchanged.

---

# 12. Source verification

Every candidate source span must be checked against the original PDF.

For each cited passage record:

```text
document_id
content_sha256
physical_pdf_page
printed_page_if_available
section
exact_text
character_span_if_available
parser_record_id
```

If parser text differs materially from the PDF, the PDF controls.

Parser/source reconstruction problems must be recorded separately from semantic-model errors.

---

# 13. Independent human adjudication

Natural gold must not be generated from model output.

Use two independent human adjudications when feasible.

Each adjudicator receives:

- the target definition;
- the source packet;
- relevant surrounding context;
- no model prediction;
- no other adjudicator's label.

Record:

```text
adjudicator_A
adjudicator_B
agreement
disagreement_reason
final_resolution
```

A disagreement may resolve to:

```text
NOT_ADJUDICABLE
```

rather than forcing consensus.

The frozen truth file must be hashed before any model request is run.

Both independent adjudicators first judge the **exact model-facing packet** without access to full PDFs, model output, or each other's labels. Each records a tentative verdict and whether the packet alone supports it. If both can derive an agreed, source-supported verdict, mark `HUMAN_CONTEXT_SUFFICIENT`; only these cases can enter the primary semantic analysis.

If the packet does not support a verdict, an independent source-scope resolver, blind to model outputs and the proposed gold label, inspects the full **allowed** source record. If the answer is available there but absent from the frozen packet, mark `PACKET_INSUFFICIENT` (evidence construction failure). If the allowed source record itself cannot establish the judgment, mark `SOURCE_INDETERMINATE` (documentary limitation). If humans disagree about the boundary or sufficiency after the permitted resolution process, mark `HUMAN_DISAGREEMENT`; do not force a binary label. Preserve the resolver's source references, scope, and rationale. Never repair a packet after seeing human or model correctness within this frozen evaluation.

Record both independent judgments, raw agreement, resolution, packet SHA-256, and final context category. A correct human verdict based on extra PDF context cannot be used as gold for a model given only excerpts. The frozen truth file must be hashed before any model request is run.

---

# 14. Hypotheses

FG-3 uses four preregistered hypotheses.

These are natural-replication hypotheses, not population-wide accuracy claims.

---

## H1 — Directional natural replication of representation transitions

FG-3 does not estimate a family-specific numerical effect from a handful of dependent cases. It asks whether natural cases repeat the three preidentified FG-2 whole-to-facet transitions:

```text
cross-clause scope: whole wrong → facet correct
illustrative modality: whole correct → facet wrong
undefined equivalence: whole wrong → facet does not rescue
```

Evaluate each semantic family at the **dependency-cluster** level. `REPEATED_DIRECTIONAL_REPLICATION` requires at least two distinct clusters showing the same preidentified direction and no opposite-direction cluster. `SINGLE_CLUSTER_SIGNAL` means exactly one supporting cluster and no opposite direction. `MIXED_DIRECTION` means both supporting and opposite-direction clusters occur. `NO_REPLICATION` means there was an adjudicable opportunity but no supporting direction. `INSUFFICIENT_OPPORTUNITY` means no suitable adjudicable opportunity. These are descriptive transition states, not significance tests or population effects. Preserve all case-level outcomes, including successes and unchanged errors.

---

## H2 — Reviewer-action boundary instability

On **human-agreed** natural Panel B cases, test whether either configuration confuses `SCRUTINY_ONLY` with `CHALLENGE_ESTABLISHED`. Report both error directions. Separately report independent human A-versus-B disagreement before resolution and each model-versus-frozen-gold disagreement. Human-disagreed cases do not enter H2's primary model-error denominator. Concentrated errors near human disagreement indicate construct ambiguity and must not be described solely as model-side semantic failure.

---

## H3 — Sensitivity to a stated review link

Distinguish a documentary statement explicitly linking reviewer intervention to a same-object model-method, parameterization, implementation, or output modification from review plus a later change without that stated link. The positive label `EXPLICIT_REVIEW_LINK_STATED` detects **what the vendor or reviewer document says**; it does not independently prove causation. The negative label is `REVIEW_LINK_NOT_ESTABLISHED` from the frozen packet, not a fixed-corpus absence finding. Report both false positive and missed stated-link directions, plus `link_statement_source_role` and modification type. Do not require a positive quota.

---

## H4 — Two-configuration comparison

Only the exact pinned Qwen2.5 and Qwen3.8 RegModelTrace configurations are compared. Outcome vocabulary is:

```text
SHARED_ACROSS_THE_TWO_TESTED_CONFIGURATIONS
QWEN25_CONFIGURATION_ONLY
QWEN38_CONFIGURATION_ONLY
NO_NATURAL_REPLICATION
MIXED
```

The comparison jointly varies checkpoint generation, quantization/runtime configuration, and reasoning mode. It does not identify which component caused a difference and does not establish a Qwen-family or general-LLM effect. No active-default switch follows automatically.

---

# 14.1 Pre-natural-run repeatability qualification

Before any natural truth is unsealed or natural inference begins, run a fixed, predeclared number of repeats (default three) on already exposed synthetic fixtures under identical settings for each checkpoint. Persist request bytes, runtime configuration hash, raw response hashes, parsed labels, run indices, and label flips. This qualification is not a new synthetic accuracy estimate. If no semantic flips occur, use one canonical natural response per request. If flips occur, freeze a three-repetition natural rule with modal label and separately report within-case instability **before** seeing natural results. Transport retries are distinct from semantic replicates. Never repeat only an incorrect natural answer.

---

# 15. Model execution

## 15.1 General rule

All natural cases must be frozen before inference.

Inference uses the gold-blind, mechanically assembled, hash-frozen evidence packet defined in Section 11.1. Human adjudication cannot revise it after seeing a judgment.

No RAG retrieval is run in FG-3.

The scientific quantity is therefore approximately:

$$
P(
\text{correct semantic judgment}
\mid
\text{correct evidence supplied}
).
$$

---

## 15.2 Qwen2.5

Use the exact active default model configuration recorded in `system_v1.json`.

Do not reconstruct configuration from memory.

Record:

```text
model_id
revision
tokenizer_revision
runtime
quantization
chat_template
temperature
seed
max_tokens
schema
prompt_hash
```

---

## 15.3 Qwen3.8

Use the frozen candidate identity:

```text
Qwen/Qwen3.8-27B-FP8

revision:
017b9c7af6b5689d5dd426a76e0bc077eb5ca20a
```

Unless a prospective protocol explicitly changes them before inference, preserve:

```text
thinking disabled
temperature 0
seed 1847
vLLM 0.29.0
```

---

## 15.4 Interface equality

The semantic instructions, target definitions, evidence packet, and output schema must be equivalent across checkpoints.

Mechanical model-specific requirements such as tokenizer or chat-template syntax may differ and must be recorded.

Do not silently optimize the prompt separately for one model.

---

## 15.5 No semantic retries

For every planned request:

```text
1 planned request
→ 1 canonical semantic response
```

Transport retries are allowed only for infrastructure failure and must not expose oracle information.

Invalid JSON or invalid semantic output remains a model failure.

Raw responses must be persisted before the scorer accesses gold labels.

---

# 16. Evaluation

Primary correctness is **joint auditable correctness**: the predicted verdict equals the frozen gold **and** the model-selected source role, source reference, and exact cited span validly support that verdict. For Panel C, the reviewer action and vendor modification must refer to the same substantive object. A correct label citing only a neutral review statement for an explicit challenge fails this joint metric. Report `label_accuracy`, `evidence_localization_accuracy`, and `joint_auditable_correctness` separately; do not allow citation validity to be inferred from label agreement. Host citation binding validates identity, while independent source review validates support.

## 16.1 Panel A

Report:

- whole-case accuracy;
- facet accuracy;
- facet-aggregated case accuracy;
- rescue count;
- regression count;
- performance by semantic family;
- evidence-reference validity.

Do not compare `22/24`-style facet denominators directly against whole-case denominators as evidence of overall improvement.

---

## 16.2 Panel B

Report:

```text
SCRUTINY_ONLY recall
CHALLENGE_ESTABLISHED recall
false-challenge count
missed-challenge count
overall accuracy
```

Also report lexical/context strata if enough cases naturally exist.

Do not manufacture those strata.

---

## 16.3 Panel C

Report:

```text
REVIEW_LINK_NOT_ESTABLISHED recall
EXPLICIT_REVIEW_LINK_STATED recall
false stated-link attribution count
missed explicit-link statement count
NOT_ADJUDICABLE_FOR_PANEL_C count
link_statement_source_role distribution
```

Results must also be stratified by:

```text
MODEL_* modification
vs
DOCUMENTATION_ONLY / DISCLOSURE_RESPONSE_ONLY
```

when sample size permits.

---

## 16.4 Model comparison

Use paired case tables:

| Case | Gold | Qwen2.5 | Qwen3.8 | Q25 correct? | Q38 correct? |
|---|---|---|---|---:|---:|

Report:

```text
both correct
both wrong
Qwen2.5 only correct
Qwen3.8 only correct
```

Do not infer superiority from unpaired aggregate percentages.

---

# 17. Statistical interpretation

The eligible natural source pool contains only two Florida Public standards cycles from one model lineage.

Therefore FG-3 does **not** estimate general Florida-domain error rates.

Cases within the same documents and standards cycle are dependent.

The discovery frame is cue-defined; neither the 1,708 hits nor the 85 leads estimate prevalence of the target phenomena. Report the frozen 24-page no-hit audit and its `YES / NO / AMBIGUOUS` findings separately. FG-3 primary conclusions are:

- natural replication of a synthetic boundary;
- failure-direction counts;
- paired checkpoint disagreements;
- success/failure conditions.

Classical population-level p-values are not required for closure.

If enough independent natural units unexpectedly emerge, any formal inferential analysis must be separately frozen before results are inspected.

No post-hoc claim of statistical independence is allowed.

---

# 18. Success modes must be recorded

FG-3 is not a failure-hunting exercise.

For every panel, record conditions under which the model succeeds.

Examples may include:

```text
explicit objection language
clear mandatory requirement
explicit definition
direct vendor response
mere review + unrelated update correctly left REVIEW_LINK_NOT_ESTABLISHED
```

The desired output is a **boundary map**, such as:

```text
condition
→ robust success
→ unstable
→ reproducible failure
→ insufficient natural evidence
```

A model error is scientifically useful only when compared with appropriate success controls.

---

# 18.1 Blinded post-hoc failure-mode coding

For any mechanism-level claim, hide checkpoint identities as `SYSTEM_A` and `SYSTEM_B` from at least two independent failure coders. Freeze the coding taxonomy before they inspect natural model results: `SCOPE_ALIGNMENT`, `ILLUSTRATIVE_MODALITY`, `UNSUPPORTED_EQUIVALENCE`, `SCRUTINY_TO_CHALLENGE`, `CHALLENGE_TO_SCRUTINY`, `FALSE_CAUSAL_LINK`, `MISSED_EXPLICIT_CAUSAL_LINK`, `EVIDENCE_LOCALIZATION`, `OTHER`, and `UNCLASSIFIABLE`. Report raw agreement, a suitable agreement statistic when defined, disagreements, and resolved coding. Model rationale may describe an output but cannot establish its internal error mechanism.

---

# 19. Required machine-readable artifacts

Recommended structure:

```text
experiments/fg3_natural_boundary/
    protocol/
        spec.md
        hypotheses.json
        prompt_manifest.json
        model_manifest.json

    inventory/
        eligible_documents.json
        exposure_audit.jsonl
        excluded_sources.jsonl

    candidates/
        candidate_registry.jsonl
        source_verification.jsonl

    adjudication/
        adjudicator_a.jsonl
        adjudicator_b.jsonl
        resolution.jsonl
        truth_frozen.jsonl
        truth_freeze_receipt.json

    requests/
        qwen25_requests.jsonl
        qwen38_requests.jsonl

    runs/
        qwen25/
            manifest.json
            raw_responses.jsonl
            runtime.log
        qwen38/
            manifest.json
            raw_responses.jsonl
            runtime.log

    scoring/
        qwen25_results.json
        qwen38_results.json
        paired_results.json
        panel_summary.json

    report/
        failure_success_map.csv
        fg3_report.md
        closure_receipt.json
```

Actual repository naming may follow existing project conventions.

Do not duplicate existing framework code unnecessarily.

---

# 20. Minimum candidate registry schema

Each candidate must contain at least:

```json
{
  "case_id": "",
  "discovery_protocol_id": "",
  "discovery_query_id": "",
  "discovery_rank": null,
  "dedup_cluster": "",
  "selection_reason": "",
  "selection_status": "",
  "model_evidence_packet_id": "",
  "model_evidence_packet_hash": "",
  "panel": "",
  "semantic_family": "",
  "standards_cycle": "",
  "dependency_cluster": "",

  "regulator_document_id": null,
  "vendor_document_id": null,
  "reviewer_document_id": null,

  "source_sha256s": [],
  "physical_pages": [],
  "source_refs": [],

  "target_question": "",
  "whole_requirement": null,
  "facets": [],

  "modification_type": null,
  "chronology": {},

  "exposure_status": "",
  "exposure_ledger_version": "KNOWN_EXPOSURE_LEDGER_V1",
  "exposure_match_ids": [],
  "adjudicability_status": "",
  "packet_context_status": "",
  "link_statement_source_role": null,

  "discovery_notes": ""
}
```

No gold label appears in the model-facing candidate registry.

---

# 21. Truth schema

The scorer-only truth record should include:

```json
{
  "case_id": "",
  "model_evidence_packet_hash": "",
  "packet_context_status": "HUMAN_CONTEXT_SUFFICIENT | PACKET_INSUFFICIENT | SOURCE_INDETERMINATE | HUMAN_DISAGREEMENT",
  "human_context_sufficiency_a": "",
  "human_context_sufficiency_b": "",

  "gold_label": "",
  "acceptable_evidence_sets": [],

  "semantic_family": "",
  "modification_type": null,
  "link_statement_source_role": null,

  "adjudicator_a": "",
  "adjudicator_b": "",
  "agreement": true,

  "resolution_notes": "",
  "adjudication_status": "FROZEN"
}
```

Truth files must remain inaccessible to the inference runner.

---

# 22. Mandatory records for every model request

Record:

```text
request_id
case_id
panel
variant
model
revision
prompt_hash
evidence_packet_hash
source_refs
input_token_count
output_token_count
temperature
seed
thinking_setting
finish_reason
raw_response
schema_valid
parsed_label
runtime_timestamp
```

Never overwrite raw model output with the parsed form.

---

# 23. Prohibited actions

Before FG-3 closure, do not:

- tune the prompt against natural FG-3 errors;
- add examples after seeing natural model outputs;
- convert ambiguous cases into convenient gold;
- reopen KCC Test E;
- relabel historical cases as fresh independent data;
- add SEC or IFRS data;
- implement TimelyRAG or VersionRAG;
- fine-tune Qwen;
- calibrate confidence probabilities;
- change the active RegModelTrace default;
- infer model-method modification from documentation revision alone;
- infer causality from temporal ordering alone.

---

# 24. Closure states

Each panel receives one of:

```text
NATURAL_REPLICATION_OBSERVED
NO_NATURAL_REPLICATION_OBSERVED
INSUFFICIENT_ELIGIBLE_CASES
INSUFFICIENT_ADJUDICABLE_CASES
BLOCKED_BY_EXPOSURE
BLOCKED_BY_SOURCE_QUALITY
```

Each hypothesis receives:

```text
SUPPORTED_WITHIN_FG3_SCOPE
NOT_SUPPORTED_WITHIN_FG3_SCOPE
MIXED
INSUFFICIENT_EVIDENCE
```

These statuses describe the bounded FG-3 source pool only.

---

# 25. FG-3 completion requirements

FG-3 is complete when:

1. exposure audit is complete for every screened candidate;
2. candidate discovery is closed under the predeclared search procedure;
3. source spans are verified against original PDFs;
4. ambiguous cases remain explicitly ambiguous;
5. independent adjudication is complete for all eligible cases;
6. truth files are frozen and hashed before model inference;
7. Qwen2.5 and Qwen3.8 each receive exactly the frozen eligible requests;
8. all raw responses are persisted before scoring;
9. no semantic retry or post-outcome prompt change occurs;
10. paired results are reported;
11. success and failure modes are both reported;
12. limitations from one lineage and two standards cycles are explicit;
13. a closure receipt records hashes, counts, exclusions, and unresolved cases;
14. exact-context human sufficiency passed for every primary case;
15. repeatability qualification completed before natural inference;
16. blinded post-hoc coding completed for every case used in mechanism-level claims.

Perfect model accuracy is not required for closure.

A failed hypothesis is a valid FG-3 result.

---

# 26. Decision after FG-3: orthogonal semantic and retrieval axes

FG-3 measures semantic judgment $S$ when a frozen, source-verified packet is supplied. A future FG-4 may measure retrieval and evidence construction $R$ against the same source-grounded cases. Good or poor $S$ does not establish good or poor $R$; both bottlenecks can coexist.

FG-4 is scientifically admissible once a frozen, source-verified natural evaluation set exists **and** a separate prospective FG-4 protocol establishes that the available cases are sufficient for its intended retrieval analysis. FG-3 semantic performance informs priority and interpretation, not FG-4 eligibility. No accuracy threshold for FG-3 is an FG-4 gate. FG-4 sample-size and retrieval metrics must be frozen in its own protocol before execution. Do not run FG-4 within FG-3.

If natural semantic boundaries do not replicate, report that result without inventing an intervention. If fresh, adjudicable cases are insufficient, close FG-3 as `INSUFFICIENT_ELIGIBLE_NATURAL_EVIDENCE`; do not relabel exposed cases. Either result remains separate from FG-4 eligibility.

---

# 27. Scientific claim boundary

FG-3 may support a claim of the form:

> Controlled semantic boundary behaviors were or were not reproduced in a bounded set of independently adjudicated natural regulatory passages from the cue-defined, bounded Florida Public Hurricane Loss Model 2021 and 2023 standards-cycle frame.

FG-3 may not support a claim about the prevalence of the target phenomena outside the cue-defined frame. The small no-hit-page audit is diagnostic, not a corpus-wide recall estimate. Undocumented prior exposure outside `KNOWN_EXPOSURE_LEDGER_V1` cannot be excluded.

FG-3 may not support:

> Qwen has X% accuracy on Florida regulatory documents.

FG-3 may not support:

> one checkpoint is generally superior.

FG-3 may not support:

> temporal RAG is necessary.

FG-3 may not support:

> the system can determine real-world model compliance.

Those require later experiments.

---

# 28. Immediate execution order

```text
1. Freeze the v1.3 amendment, known-exposure ledger scope, packet rule, and 24-page negative-frame selection rule; preserve v1.2 receipts.
2. Checkpoint 2: assess all 85 frozen leads under the ledger and verify original-PDF context without changing discovery.
3. Form cases using the v1.2 pairing tiers, retaining all first-tier matches and dependency clusters.
4. Assemble and hash gold-blind packets before human adjudication.
5. Independently adjudicate the exact packets; resolve packet insufficiency versus source indeterminacy separately and preserve human disagreement.
6. Freeze scorer-only truth; qualify repeatability on exposed synthetic controls.
7. Run the two pinned configurations on identical packet content; persist raw outputs before scoring.
8. Report natural transition directions, human/model disagreement, source-grounded correctness, frame audit, exposure limits, and closure receipt.
9. Consider FG-4 only under its own prospective protocol.
```

No discovery rerun, natural-case screening, human gold, or model inference is part of the v1.3 amendment itself.
