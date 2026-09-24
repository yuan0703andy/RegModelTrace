I would freeze the next phase as a narrow continuation of FG-2, using the inventory you just completed.

# RegModelTrace FG-3
## Natural Evidence-Boundary Validation

**Version:** 1.1 (five contract amendments)
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

Before candidate adjudication, every candidate natural case must receive an exposure status.

Allowed values are:

```text
CLEAR_FOR_PROSPECTIVE_EVALUATION
SOURCE_SEEN_BUT_OUTCOME_NOT_USED
DEVELOPER_EXPOSED
GOLD_OR_ADJUDICATION_EXPOSED
SUBSTANTIALLY_EQUIVALENT_TO_EXPOSED_CASE
EXPOSURE_UNKNOWN
```

Only:

```text
CLEAR_FOR_PROSPECTIVE_EVALUATION
```

may enter the primary prospective evaluation.

`SOURCE_SEEN_BUT_OUTCOME_NOT_USED` may be retained as a secondary sensitivity set if exposure truly consisted only of mechanical processing or uninspected inference.

The remaining categories are excluded from confirmatory evaluation.

`EXPOSURE_UNKNOWN` remains excluded until resolved.

Exposure checks must cover:

- exact regulatory clause;
- substantially equivalent clause;
- vendor passage;
- reviewer passage;
- prior question wording;
- prior adjudication;
- prior demo use;
- prior model-output inspection;
- synthetic case derived from the same source fact.

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

# 10. Panel C — Review-to-modification causal link

## 10.1 Question

Does the documentary evidence explicitly establish that reviewer action caused a vendor model-method or implementation modification?

The target is deliberately narrow.

---

## 10.2 Labels

### EXPLICIT_REVIEW_CAUSED_MODIFICATION

Use only when the available documentary evidence explicitly links:

```text
reviewer request / instruction / objection
```

to:

```text
vendor modification
```

and both concern the same substantive object.

The evidence must establish more than chronology.

---

### NOT_ESTABLISHED

Use when:

- review and modification both occurred but no causal link is stated;
- the modification predated the review;
- a revision occurred after review but the reason is unstated;
- reviewer scrutiny occurred without a requested change;
- a document was revised, but only the disclosure or written response changed;
- reviewer and vendor passages concern different substantive objects.

---

### NOT_ADJUDICABLE_FOR_PANEL_C

Use when chronology, object identity, or the meaning of "modification" cannot be established from the permitted source record.

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

For each discovered candidate:

```text
DISCOVERED
    ↓
SOURCE_CONTEXT_VERIFIED
    ↓
EXPOSURE_CHECKED
    ↓
ADJUDICABLE / NOT_ADJUDICABLE
    ↓
MODEL-FACING EVIDENCE PACKET FROZEN
    ↓
INDEPENDENT HUMAN JUDGMENT ON EXACTLY THAT PACKET
    ↓
HUMAN_CONTEXT_SUFFICIENT / HUMAN_CONTEXT_INSUFFICIENT / HUMAN_CONTEXT_DISAGREEMENT
    ↓
TRUTH_FROZEN (sufficient cases only)
    ↓
MODEL_INFERENCE
```

No model inference may occur before `TRUTH_FROZEN`.

A case that fails any earlier gate remains in the audit ledger but does not enter the evaluation set.

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

Both independent adjudicators must decide whether the **exact model-facing evidence packet** suffices to derive their label. The human adjudication packet and model packet must have the same source text, surrounding context, and permitted source roles; source-verification staff may inspect the original PDF before packet freeze but may not silently give adjudicators extra evidence. Only `HUMAN_CONTEXT_SUFFICIENT` with resolved agreement enters the primary semantic-capability analysis. `HUMAN_CONTEXT_INSUFFICIENT` and `HUMAN_CONTEXT_DISAGREEMENT` remain in the audit ledger. Record each adjudicator's sufficiency decision and the frozen packet hash in scorer-only truth. Do not compare a human judgment made from a whole PDF with a model judgment made from excerpts.

---

# 14. Hypotheses

FG-3 uses four preregistered hypotheses.

These are natural-replication hypotheses, not population-wide accuracy claims.

---

## H1 — Requirement representation interaction

The effect of whole-versus-facet representation depends on the semantic family.

Formally, for natural multi-proposition cases:

$$
\Delta_g
=
J_{\text{facet},g}
-
J_{\text{whole},g},
$$

where $g$ indexes semantic family.

The hypothesis is not:

$$
J_{\text{facet}}>J_{\text{whole}}
$$

universally.

The hypothesis is:

$$
\Delta_g
$$

varies by semantic condition.

Particular attention goes to whether natural cases reproduce the FG-2 pattern:

```text
cross-clause scope:
facet may help

illustrative modality:
facet may hurt

undefined equivalence:
facet may fail to help
```

---

## H2 — Reviewer-action boundary instability

Natural reviewer language near the boundary between examination and challenge produces systematic model errors.

Primary directional errors are:

```text
SCRUTINY_ONLY → CHALLENGE_ESTABLISHED
```

and:

```text
CHALLENGE_ESTABLISHED → SCRUTINY_ONLY
```

Both must be reported separately.

A single "challenge accuracy" number is insufficient.

---

## H3 — Explicit causal-link sensitivity

The models should distinguish:

$$
\text{review + later change}
$$

from:

$$
\text{explicitly documented review-caused change}.
$$

Two failure directions are primary:

### False causal attribution

```text
gold = NOT_ESTABLISHED
model = EXPLICIT_REVIEW_CAUSED_MODIFICATION
```

### Missed explicit causality

```text
gold = EXPLICIT_REVIEW_CAUSED_MODIFICATION
model = NOT_ESTABLISHED
```

The synthetic Qwen3.8 result suggests both directions matter.

FG-3 tests whether either occurs in natural sources.

---

## H4 — Checkpoint dependence

The same frozen natural cases are evaluated using:

```text
active Qwen2.5 default
```

and:

```text
Qwen3.8 candidate
```

under the same semantic task contract.

The question is:

> Are observed boundary failures shared across checkpoints or checkpoint-specific?

Possible outcomes include:

```text
SHARED_FAILURE
QWEN25_SPECIFIC
QWEN38_SPECIFIC
NO_NATURAL_REPLICATION
MIXED
```

No active-default change follows automatically from H4.

---

# 14.1 Pre-natural-run repeatability qualification

Before any natural truth is unsealed or natural inference begins, run a fixed, predeclared number of repeats (default three) on already exposed synthetic fixtures under identical settings for each checkpoint. Persist request bytes, runtime configuration hash, raw response hashes, parsed labels, run indices, and label flips. This qualification is not a new synthetic accuracy estimate. If no semantic flips occur, use one canonical natural response per request. If flips occur, freeze a three-repetition natural rule with modal label and separately report within-case instability **before** seeing natural results. Transport retries are distinct from semantic replicates. Never repeat only an incorrect natural answer.

---

# 15. Model execution

## 15.1 General rule

All natural cases must be frozen before inference.

Inference uses the human-selected evidence packet.

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
NOT_ESTABLISHED recall
EXPLICIT_REVIEW_CAUSED_MODIFICATION recall
false causal attribution count
missed explicit causality count
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

FG-3 primary conclusions are:

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
mere review + unrelated update correctly left NOT_ESTABLISHED
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
  "adjudicability_status": "",

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
  "human_context_sufficiency": "PASS | FAIL | DISAGREEMENT",
  "human_context_sufficiency_a": "",
  "human_context_sufficiency_b": "",

  "gold_label": "",
  "acceptable_evidence_sets": [],

  "semantic_family": "",
  "modification_type": null,

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

# 26. Decision after FG-3

FG-3 determines what should happen next.

## Branch A — semantic failure persists with gold evidence

If natural cases reproduce meaningful semantic failures even when correct evidence is supplied:

$$
\boxed{
\text{next work}
=
\text{semantic representation / judgment intervention}
}
$$

Only then should we test targeted improvements such as parent-context preservation or proposition-aware evidence alignment.

---

## Branch B — gold-evidence judgment is strong

If both models are largely correct when supplied with verified evidence:

$$
\boxed{
\text{next bottleneck}
=
\text{retrieval / evidence construction}
}
$$

Then run the same frozen natural cases through:

```text
current RAG
BM25
dense
hybrid
```

and later temporal/version-aware retrieval if the cases require it.

This is the correct point to introduce TimelyRAG or VersionRAG.

---

## Branch C — natural documents do not reproduce the synthetic boundaries

If the synthetic failures do not reproduce naturally:

do not build a new method to solve them.

The result is:

> the constructed diagnostics exposed possible boundaries, but they were not demonstrated as important in the bounded natural source pool.

The study then moves to whatever natural failure actually appears.

---

## Branch D — insufficient fresh cases

If exposure or source ambiguity leaves too few natural cases:

close FG-3 with:

```text
INSUFFICIENT_ELIGIBLE_NATURAL_EVIDENCE
```

Do not compensate by relabelling previously exposed material.

A later study may prospectively acquire a new organization or standards cycle under a separately frozen protocol.

---

# 27. Scientific claim boundary

FG-3 may support a claim of the form:

> Controlled semantic boundary behaviors were or were not reproduced in a bounded set of independently adjudicated natural regulatory passages from the Florida Public Hurricane Loss Model 2021 and 2023 standards cycles.

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

The next actions are therefore:

```text
1. Freeze this FG-3 protocol.
2. Audit exposure for the Florida Public 2021/2023 source pool.
3. Run deterministic candidate discovery for Panels A/B/C.
4. Verify every candidate against original PDF context.
5. Mark ambiguous and ineligible cases.
6. Independently adjudicate the remaining natural cases.
7. Freeze and hash truth.
8. Construct identical evidence packets for Qwen2.5 and Qwen3.8.
9. Execute one frozen run per checkpoint.
10. Persist raw outputs.
11. Score only after persistence.
12. Produce the natural success/failure boundary map.
13. Close FG-3.
14. Decide whether the next scientific problem is semantic judgment or retrieval.
```

The first FG-3 checkpoint is therefore:

$$
\boxed{
\textbf{Exposure audit + natural candidate registry}
}
$$

—not another model run.

This version deliberately keeps the scope narrow: the existing Florida corpus first, natural replication of FG-2/Qwen3.8 boundaries second, retrieval only after we know whether judgment with correct evidence is actually the bottleneck.
