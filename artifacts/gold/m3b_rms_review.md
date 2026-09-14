# Gold Case 001 — M-3.B, RMS 21.0

**Frozen development reference: gold-case-001-v0.3.0. Causal attribution: UNRESOLVED. User-reported critical-page spot-check and conclusion endorsement are recorded; full passage-level independent adjudication is not claimed.**

**Gold Core: 12 records. Audit Context: 57 records.** Start with the [short Gold Core review](m3b_rms_gold_core.md). Only Gold Core enters the primary recall denominator.

The corpus establishes a requirement, completed scrutiny, vendor methodology/justification, and updates relative to a prior model. It does not establish an explicit post-review M-3.B response or a review-induced M-3.B modification. No-change methodology comments further constrain the claim; causation remains unresolved.

The strongest objection to treating scrutiny as causal evidence is the documented baseline: RMS describes updates from its previously accepted model to this year’s initial submission, and the Team lists the HURDAT2 update in its opening briefing. Conversely, the procedures allow corrections during review, so verification cannot prove that no change occurred. Both directions are preserved below.

This case uses five explicit chain questions. They are five questions within one case, not five independent evaluation cases. The evaluation text supplied no separately enumerated five-question list.

## Slot decisions

| Question | Slot | Status | Minimal interpretation |
|---|---|---|---|
| Q1 | requirement | **FOUND** | The requirement and connected provisions are located. |
| Q2 | reviewer scrutiny | **FOUND** | Completed scrutiny is recorded. |
| Q2 | specific m3b challenge | **SEARCHED_AND_NOT_FOUND_IN_FIXED_CORPUS** | No explicit coastal-landfall-frequency M-3.B objection was found; bypass, footprint, and wind-radius questions have different targets. |
| Q3 | vendor methodology and justification | **FOUND** | The revised submission contains methodology and consistency assertions. |
| Q3 | explicit post review vendor response | **SEARCHED_AND_NOT_FOUND_IN_FIXED_CORPUS** | No passage explicitly identifies an RMS response after completion of this review to an M-3.B challenge. An April 22 snapshot or compliance response is insufficient chronology. |
| Q4 | documented model updates | **FOUND** | Landfall/bypass rates and the storm set changed relative to a prior model; this is not a newly identified review-induced change. |
| Q4 | review induced model modification | **SEARCHED_AND_NOT_FOUND_IN_FIXED_CORPUS** | No explicit documentary link from April reviewer scrutiny to an M-3.B model alteration was found in the three PDFs. |
| Q4 | causal attribution | **UNRESOLVED** | Requirements, review, justification, and prior-version updates do not identify review causation. Original/within-cycle revisions and actual dated version history remain unmatched. |
| Q5 | qualifications and counterevidence | **FOUND** | Conditional adjustments, nonidentical frequencies, no-methodology-change comments, chronology, and adjacent-topic questions constrain the interpretation. |
| Q5 | cross reference completeness | **UNRESOLVED** | Key internal form/figure links are resolved, with source numbering discrepancies retained; underlying history, original revisions, spreadsheet, and procedural amendment remain outside the snapshots. |

No slot is labeled DOCUMENT_UNAVAILABLE: none of the three PDFs failed access, and public availability of the missing dependencies has not been established. A document absent from these snapshots is not thereby unavailable.

## How to verify the exact source spans

Each passage below reports its document, section, physical PDF page, **complete source-span interval**, and minimal interpretation. Intervals are zero-based Unicode character positions `[start,end)` in whitespace-normalized `pdftotext -layout -enc UTF-8` page text; the end is excluded. The JSON also records each complete slice’s SHA-256, the page-text SHA-256, and the original PDF checksum. These are lossless source locations, not short identifying quotations.

Long passages are not republished here. Follow the PDF page links to read them in context. The local reader prints the complete literal source slices, verifying them against the original PDF, for a passage, a question, or the whole case:

```sh
.venv/bin/python regmodeltrace/scripts/inspect_gold_passage.py --evidence V_SMOOTHING
.venv/bin/python regmodeltrace/scripts/inspect_gold_passage.py --question Q4
.venv/bin/python regmodeltrace/scripts/inspect_gold_passage.py --all
```

Run from the repository root. For figures, tables, signatures, and blank form fields, text offsets alone do not represent visual content: read the specified figure/table/field on the linked original page. All cited pages were visually inspected. Printed page numbers match physical pages at the cited numbered pages; the cover is unnumbered.

## Source documents

| Code | Document, author, date | Local PDF |
|---|---|---|
| S | [Hurricane Standards Report of Activities as of November 1, 2019](https://fchlpm.sbafla.com/media/o10dfucl/2019_hurricaneroa.pdf). Florida Commission on Hurricane Loss Projection Methodology. 2019-11-01. | [Open local PDF](</Users/andyhou/Documents/ChatGPT/CIRCAD-LLM/regmodeltrace/data/raw/standards/fchlpm_2019_hurricane_standards.pdf>) |
| V | [RMS North Atlantic Hurricane Models 21.0 (Build 2050): 2019 Standards submission](https://fchlpm.sbafla.com/media/c5apncqi/rms19standardsdisclosures_04222021.pdf). Risk Management Solutions, Inc.. 2021-04-22. | [Open local PDF](</Users/andyhou/Documents/ChatGPT/CIRCAD-LLM/regmodeltrace/data/raw/submissions/rms_21_0_2019_submission_20210422.pdf>) |
| T | [RMS Professional Team Report, April 19-22, 2021](https://fchlpm.sbafla.com/media/uzkplkto/20210422_rms_2019stds_ptrpt.pdf). FCHLPM Professional Team. review April 19–22, 2021; posting date unknown. | [Open local PDF](</Users/andyhou/Documents/ChatGPT/CIRCAD-LLM/regmodeltrace/data/raw/reviews/rms_21_0_2019_professional_team_20210422.pdf>) |

The vendor document is a revised April 22 snapshot, not the original November 2020 submission. Its model-identification page separately says June 2021; these fields cannot supply the date of a particular M-3.B reply.

## Q1. What exactly does M-3.B require, and which connected disclosure/audit provisions govern the comparison?

M-3.B imposes historical coastal consistency. Connected M-1/Form M-1/S-1 provisions preserve justified adjustments and statistical interpretation; exact equality is not stipulated.

**Gold Core for this question:** [S_M3B](#s-m3b), [S_M3_CONTEXT](#s-m3-context).

**Audit Context, excluded from primary recall:** [S_M2_DISCLOSURE](#s-m2-disclosure), [S_M2_AUDIT](#s-m2-audit), [S_M3_AUDIT](#s-m3-audit), [S_M1_QUAL](#s-m1-qual), [S_M1_DISC_AUDIT](#s-m1-disc-audit), [S_M2_PURPOSE](#s-m2-purpose), [S_FORM_M1](#s-form-m1), [S_FORM_M1_NOTES](#s-form-m1-notes), [S_S1_FIT](#s-s1-fit), [S_S1_DIFFERENCES](#s-s1-differences), [T_M3_STANDARD](#t-m3-standard), [T_M1_AUDIT](#t-m1-audit), [S_GLOSSARY](#s-glossary).

## Q2. What reviewer scrutiny of landfall frequencies is actually recorded, and is there a specific M-3.B challenge?

The Team reviewed coastal gates, category-specific landfall updates, smoothing, and related forms, and verified M-3. An explicit M-3.B frequency challenge was not located.

**Gold Core for this question:** [T_M3_REVIEW](#t-m3-review), [T_LANDFALL_REVIEW](#t-landfall-review).

**Audit Context, excluded from primary recall:** [S_M2_AUDIT](#s-m2-audit), [S_M3_AUDIT](#s-m3-audit), [S_M1_DISC_AUDIT](#s-m1-disc-audit), [S_REVIEW_SCOPE](#s-review-scope), [S_PREVISIT](#s-previsit), [T_M3_STANDARD](#t-m3-standard), [T_M1_REVIEW](#t-m1-review), [T_BYPASS_QUESTION](#t-bypass-question), [T_M2_QUESTIONS](#t-m2-questions), [T_AMENDMENT](#t-amendment), [T_INDEPENDENCE](#t-independence), [T_FORM_M3](#t-form-m3), [T_S1_REVIEW](#t-s1-review), [T_M1_AUDIT](#t-m1-audit).

## Q3. What does RMS say its methodology/justification is, and is there an explicit vendor response after the review?

RMS describes smoothed calibration targets and regional consistency justification. A matched, explicit post-review vendor response was not located.

**Gold Core for this question:** [V_M3B](#v-m3b), [V_SMOOTHING](#v-smoothing), [V_POISSON](#v-poisson), [V_M1_TABLE](#v-m1-table).

**Audit Context, excluded from primary recall:** [S_M2_DISCLOSURE](#s-m2-disclosure), [S_RESPONSE_FORMAT](#s-response-format), [S_REVISION_PROCESS](#s-revision-process), [S_PREVISIT](#s-previsit), [S_REGION_MAP](#s-region-map), [V_GATES](#v-gates), [V_GATE_PLOTS](#v-gate-plots), [V_M3_DISC](#v-m3-disc), [V_FIT_RESULTS](#v-fit-results), [V_FORM_S3](#v-form-s3), [V_BASE_TRACKS](#v-base-tracks), [V_BYPASS](#v-bypass), [V_LIMITED_RECORD](#v-limited-record), [V_M1_REFERENCES](#v-m1-references), [V_ADDED_STORMS](#v-added-storms), [V_M1_NOTES](#v-m1-notes), [V_REGION_PLOTS](#v-region-plots), [V_STORM_PLOTS](#v-storm-plots), [V_S1_TABLE](#v-s1-table), [V_MET_CERT](#v-met-cert), [V_EDITOR_CERT](#v-editor-cert), [V_COVER](#v-cover), [V_MODEL_ID](#v-model-id), [V_TRACK_SMOOTHING](#v-track-smoothing), [V_XLSX_REFERENCE](#v-xlsx-reference), [T_BYPASS_QUESTION](#t-bypass-question), [T_ORIGINAL_REQUEST](#t-original-request), [T_EDITORIAL](#t-editorial), [V_M3A](#v-m3a), [V_S1_ASSURANCE](#v-s1-assurance).

## Q4. Is a model modification documented, and can it be attributed to the April 2021 review?

Prior-version rate and storm-set updates are documented. Their attribution to this April review remains unresolved; no explicit review-induced M-3.B alteration was located.

**Gold Core for this question:** [V_SMOOTHING](#v-smoothing), [V_PRIOR_UPDATE](#v-prior-update), [V_BASELINE_VERSION](#v-baseline-version), [T_M3_REVIEW](#t-m3-review), [T_LANDFALL_REVIEW](#t-landfall-review), [T_OPENING_UPDATES](#t-opening-updates), [T_HISTORY](#t-history).

**Audit Context, excluded from primary recall:** [S_CORRECTION_PROCESS](#s-correction-process), [S_REVISION_PROCESS](#s-revision-process), [S_REVIEW_SCOPE](#s-review-scope), [V_GATE_PLOTS](#v-gate-plots), [V_ADDED_STORMS](#v-added-storms), [V_STORM_PLOTS](#v-storm-plots), [V_MEDIUM_TERM](#v-medium-term), [V_HISTORY_POLICY](#v-history-policy), [V_MET_CERT](#v-met-cert), [V_EDITOR_CERT](#v-editor-cert), [V_COVER](#v-cover), [V_MODEL_ID](#v-model-id), [T_M1_REVIEW](#t-m1-review), [T_ORIGINAL_REQUEST](#t-original-request), [T_EDITORIAL](#t-editorial), [T_REVISION_AUDIT](#t-revision-audit), [T_NO_REFITTING](#t-no-refitting), [T_NO_METHOD_S2](#t-no-method-s2), [T_NO_METHOD_S3](#t-no-method-s3), [T_FORM_M3](#t-form-m3), [V_WIND_NO_CHANGE](#v-wind-no-change).

## Q5. Which qualifications, exceptions, contrary passages, and unresolved references could change or limit the interpretation?

Conditional base changes, actual bypass-count adjustments, unequal rates, no-methodology-change comments, and baseline/chronology limits materially qualify the case. Missing references could still change the causal assessment.

**Gold Core for this question:** [S_M3_CONTEXT](#s-m3-context), [V_SMOOTHING](#v-smoothing), [V_M1_TABLE](#v-m1-table), [V_PRIOR_UPDATE](#v-prior-update), [V_BASELINE_VERSION](#v-baseline-version), [T_LANDFALL_REVIEW](#t-landfall-review), [T_OPENING_UPDATES](#t-opening-updates), [T_HISTORY](#t-history).

**Audit Context, excluded from primary recall:** [S_M1_QUAL](#s-m1-qual), [S_M1_DISC_AUDIT](#s-m1-disc-audit), [S_M2_PURPOSE](#s-m2-purpose), [S_FORM_M1](#s-form-m1), [S_FORM_M1_NOTES](#s-form-m1-notes), [S_S1_FIT](#s-s1-fit), [S_S1_DIFFERENCES](#s-s1-differences), [S_RESPONSE_FORMAT](#s-response-format), [S_CORRECTION_PROCESS](#s-correction-process), [S_REVISION_PROCESS](#s-revision-process), [S_REVIEW_SCOPE](#s-review-scope), [S_PREVISIT](#s-previsit), [S_REGION_MAP](#s-region-map), [V_GATES](#v-gates), [V_GATE_PLOTS](#v-gate-plots), [V_M3_DISC](#v-m3-disc), [V_FIT_RESULTS](#v-fit-results), [V_BASE_TRACKS](#v-base-tracks), [V_BYPASS](#v-bypass), [V_LIMITED_RECORD](#v-limited-record), [V_M1_REFERENCES](#v-m1-references), [V_ADDED_STORMS](#v-added-storms), [V_M1_NOTES](#v-m1-notes), [V_REGION_PLOTS](#v-region-plots), [V_S1_TABLE](#v-s1-table), [V_MEDIUM_TERM](#v-medium-term), [V_HISTORY_POLICY](#v-history-policy), [V_MET_CERT](#v-met-cert), [V_EDITOR_CERT](#v-editor-cert), [V_MODEL_ID](#v-model-id), [V_TRACK_SMOOTHING](#v-track-smoothing), [V_XLSX_REFERENCE](#v-xlsx-reference), [T_M1_REVIEW](#t-m1-review), [T_BYPASS_QUESTION](#t-bypass-question), [T_M2_QUESTIONS](#t-m2-questions), [T_ORIGINAL_REQUEST](#t-original-request), [T_AMENDMENT](#t-amendment), [T_EDITORIAL](#t-editorial), [T_REVISION_AUDIT](#t-revision-audit), [T_NO_REFITTING](#t-no-refitting), [T_NO_METHOD_S2](#t-no-method-s2), [T_NO_METHOD_S3](#t-no-method-s3), [T_INDEPENDENCE](#t-independence), [T_FORM_M3](#t-form-m3), [T_S1_REVIEW](#t-s1-review), [T_M1_AUDIT](#t-m1-audit), [S_GLOSSARY](#s-glossary), [V_WIND_NO_CHANGE](#v-wind-no-change), [V_S1_ASSURANCE](#v-s1-assurance).

## Passage register

Every record in this register is **FOUND as a source passage**. Only the twelve records explicitly labeled gold_core are primary recall targets. The remaining 57 records preserve supporting, rejected, adjacent, and reversal-search context. A found passage does not imply that the proposition under investigation is supported.

<a id="s-m3b"></a>

### S_M3B — M-3.B

**Document:** S · **Layer:** gold_core · **Passage state:** FOUND · **Questions:** Q1 · **Role:** support

| PDF page | Exact complete source span |
|---|---|
| [120](https://fchlpm.sbafla.com/media/o10dfucl/2019_hurricaneroa.pdf#page=120) | `[191,463)` |

**Minimal interpretation:** Historical coastal-frequency consistency is required for categories 1–5 in Florida and the three named neighboring states.

<a id="s-m3-context"></a>

### S_M3_CONTEXT — M-3.A/C and Purpose

**Document:** S · **Layer:** gold_core · **Passage state:** FOUND · **Questions:** Q1, Q5 · **Role:** qualification

| PDF page | Exact complete source span |
|---|---|
| [120](https://fchlpm.sbafla.com/media/o10dfucl/2019_hurricaneroa.pdf#page=120) | `[0,190)` |
| [120](https://fchlpm.sbafla.com/media/o10dfucl/2019_hurricaneroa.pdf#page=120) | `[464,1714)` |

**Minimal interpretation:** Intensity has a common wind definition; geographic continuity and reasonable historical agreement frame consistency, without a numeric gatewise tolerance here.

**Visual source:** narrative and table; inspect the named object on the original page, including its caption, labels, and notes.

<a id="s-m2-disclosure"></a>

### S_M2_DISCLOSURE — M-2 disclosures 8–9

**Document:** S · **Layer:** audit_context · **Passage state:** FOUND · **Questions:** Q1, Q3 · **Role:** support

| PDF page | Exact complete source span |
|---|---|
| [119](https://fchlpm.sbafla.com/media/o10dfucl/2019_hurricaneroa.pdf#page=119) | `[220,1010)` |

**Minimal interpretation:** Disclose data changes and coastal segmentation; compare historical, current-model, and previously accepted rates by category groups.

<a id="s-m2-audit"></a>

### S_M2_AUDIT — M-2 Audit 2

**Document:** S · **Layer:** audit_context · **Passage state:** FOUND · **Questions:** Q1, Q2 · **Role:** support

| PDF page | Exact complete source span |
|---|---|
| [119](https://fchlpm.sbafla.com/media/o10dfucl/2019_hurricaneroa.pdf#page=119) | `[1214,1644)` |

**Minimal interpretation:** The prescribed audit includes fitted-data sources, methods, and smoothing. This prescribes scrutiny; it does not record completed review.

<a id="s-m3-audit"></a>

### S_M3_AUDIT — M-3 disclosures 1–2 and Audit 1–5

**Document:** S · **Layer:** audit_context · **Passage state:** FOUND · **Questions:** Q1, Q2 · **Role:** support

| PDF page | Exact complete source span |
|---|---|
| [121](https://fchlpm.sbafla.com/media/o10dfucl/2019_hurricaneroa.pdf#page=121) | `[128,1124)` |

**Minimal interpretation:** Requires assumptions, rationale, border fit, track/strike methods, and Form S-3 review.

<a id="s-m1-qual"></a>

### S_M1_QUAL — M-1.A/B and Purpose

**Document:** S · **Layer:** audit_context · **Passage state:** FOUND · **Questions:** Q1, Q5 · **Role:** qualification

| PDF page | Exact complete source span |
|---|---|
| [116](https://fchlpm.sbafla.com/media/o10dfucl/2019_hurricaneroa.pdf#page=116) | `[79,1820)` |

**Minimal interpretation:** July 2019-or-later HURDAT2 through 2018 is the baseline. Complete extra seasons and literature-justified changes are permitted; weights/partitions require justification and full-set validation.

<a id="s-m1-disc-audit"></a>

### S_M1_DISC_AUDIT — M-1 disclosures 1–4 and Audit 1–7

**Document:** S · **Layer:** audit_context · **Passage state:** FOUND · **Questions:** Q1, Q2, Q5 · **Role:** support

| PDF page | Exact complete source span |
|---|---|
| [117](https://fchlpm.sbafla.com/media/o10dfucl/2019_hurricaneroa.pdf#page=117) | `[12,2275)` |

**Minimal interpretation:** Requires landfall-data change explanations, historical comparisons, full-set checks, and consistency between Forms M-1 and S-1.

<a id="s-m2-purpose"></a>

### S_M2_PURPOSE — M-2 requirement, Purpose, disclosure 4

**Document:** S · **Layer:** audit_context · **Passage state:** FOUND · **Questions:** Q1, Q5 · **Role:** qualification

| PDF page | Exact complete source span |
|---|---|
| [118](https://fchlpm.sbafla.com/media/o10dfucl/2019_hurricaneroa.pdf#page=118) | `[0,765)` |
| [118](https://fchlpm.sbafla.com/media/o10dfucl/2019_hurricaneroa.pdf#page=118) | `[1468,1606)` |

**Minimal interpretation:** Methods require scientific support; different treatment of historical and stochastic parameters must be justified.

<a id="s-form-m1"></a>

### S_FORM_M1 — Form M-1 Purpose and B–F

**Document:** S · **Layer:** audit_context · **Passage state:** FOUND · **Questions:** Q1, Q5 · **Role:** qualification

| PDF page | Exact complete source span |
|---|---|
| [127](https://fchlpm.sbafla.com/media/o10dfucl/2019_hurricaneroa.pdf#page=127) | `[34,388)` |
| [127](https://fchlpm.sbafla.com/media/o10dfucl/2019_hurricaneroa.pdf#page=127) | `[519,2559)` |

**Minimal interpretation:** Distinguishes landfall from damaging bypass events; permits specified base differences and nearest-border coastal statistics; requires variations and storm additions/removals to be disclosed.

<a id="s-form-m1-notes"></a>

### S_FORM_M1_NOTES — Form M-1 notes 1–3

**Document:** S · **Layer:** audit_context · **Passage state:** FOUND · **Questions:** Q1, Q5 · **Role:** qualification

| PDF page | Exact complete source span |
|---|---|
| [128](https://fchlpm.sbafla.com/media/o10dfucl/2019_hurricaneroa.pdf#page=128) | `[44,1917)` |

**Minimal interpretation:** Regional and statewide counts use different counting rules. Zero-modeled-damage exclusions, complete extra seasons, and literature-based changes are permitted with reconciled forms.

<a id="s-s1-fit"></a>

### S_S1_FIT — S-1.A/B, Purpose, disclosure 1

**Document:** S · **Layer:** audit_context · **Passage state:** FOUND · **Questions:** Q1, Q5 · **Role:** qualification

| PDF page | Exact complete source span |
|---|---|
| [133](https://fchlpm.sbafla.com/media/o10dfucl/2019_hurricaneroa.pdf#page=133) | `[87,865)` |
| [133](https://fchlpm.sbafla.com/media/o10dfucl/2019_hurricaneroa.pdf#page=133) | `[1324,1813)` |

**Minimal interpretation:** Statistical agreement requires appropriate methods; chi-square alone may be insufficient. Distribution choices, tests, and p-values must be disclosed.

<a id="s-s1-differences"></a>

### S_S1_DIFFERENCES — S-1 disclosures 5–6 and Audit 1

**Document:** S · **Layer:** audit_context · **Passage state:** FOUND · **Questions:** Q1, Q5 · **Role:** qualification

| PDF page | Exact complete source span |
|---|---|
| [134](https://fchlpm.sbafla.com/media/o10dfucl/2019_hurricaneroa.pdf#page=134) | `[216,546)` |
| [134](https://fchlpm.sbafla.com/media/o10dfucl/2019_hurricaneroa.pdf#page=134) | `[874,1322)` |

**Minimal interpretation:** Historical/model differences require statistical justification and graphical/test comparisons, subject to review.

<a id="s-response-format"></a>

### S_RESPONSE_FORMAT — Submission format 4.d

**Document:** S · **Layer:** audit_context · **Passage state:** FOUND · **Questions:** Q3, Q5 · **Role:** qualification

| PDF page | Exact complete source span |
|---|---|
| [53](https://fchlpm.sbafla.com/media/o10dfucl/2019_hurricaneroa.pdf#page=53) | `[841,2029)` |

**Minimal interpretation:** Standard text and vendor answers have different formatting. A submission answer is a compliance statement, not inherently a later reply to reviewers.

<a id="s-correction-process"></a>

### S_CORRECTION_PROCESS — On-site compliance outcomes 1–2.c

**Document:** S · **Layer:** audit_context · **Passage state:** FOUND · **Questions:** Q4, Q5 · **Role:** qualification

| PDF page | Exact complete source span |
|---|---|
| [57](https://fchlpm.sbafla.com/media/o10dfucl/2019_hurricaneroa.pdf#page=57) | `[0,2559)` |

**Minimal interpretation:** Corrections can occur during or after review. The Team may react to vendor proposals but does not prescribe how to correct problems; verification alone cannot date or exclude changes.

<a id="s-revision-process"></a>

### S_REVISION_PROCESS — Compliance disagreement and Submission Revisions

**Document:** S · **Layer:** audit_context · **Passage state:** FOUND · **Questions:** Q3, Q4, Q5 · **Role:** qualification

| PDF page | Exact complete source span |
|---|---|
| [58](https://fchlpm.sbafla.com/media/o10dfucl/2019_hurricaneroa.pdf#page=58) | `[1647,2894)` |
| [59](https://fchlpm.sbafla.com/media/o10dfucl/2019_hurricaneroa.pdf#page=59) | `[0,1826)` |

**Minimal interpretation:** Provides contest/withdrawal options and requires revision letters, dates, marked copies, and final documentation. The process does not prove a particular RMS change occurred.

<a id="s-review-scope"></a>

### S_REVIEW_SCOPE — On-site review: General Purpose

**Document:** S · **Layer:** audit_context · **Passage state:** FOUND · **Questions:** Q2, Q4, Q5 · **Role:** qualification

| PDF page | Exact complete source span |
|---|---|
| [78](https://fchlpm.sbafla.com/media/o10dfucl/2019_hurricaneroa.pdf#page=78) | `[52,2211)` |

**Minimal interpretation:** Review covers compliance, changed and unchanged components, and controlled tests; its anti-recalibration safeguard is a procedure, not evidence of actual tuning.

<a id="s-previsit"></a>

### S_PREVISIT — Review preparation and presentation materials

**Document:** S · **Layer:** audit_context · **Passage state:** FOUND · **Questions:** Q2, Q3, Q5 · **Role:** qualification

| PDF page | Exact complete source span |
|---|---|
| [79](https://fchlpm.sbafla.com/media/o10dfucl/2019_hurricaneroa.pdf#page=79) | `[0,1015)` |
| [79](https://fchlpm.sbafla.com/media/o10dfucl/2019_hurricaneroa.pdf#page=79) | `[2699,3299)` |

**Minimal interpretation:** Review questions may be supplemented; presentations precede commencement. Presented methodology is not thereby a post-review response.

<a id="s-region-map"></a>

### S_REGION_MAP — Figure 3

**Document:** S · **Layer:** audit_context · **Passage state:** FOUND · **Questions:** Q3, Q5 · **Role:** cross reference

| PDF page | Exact complete source span |
|---|---|
| [130](https://fchlpm.sbafla.com/media/o10dfucl/2019_hurricaneroa.pdf#page=130) | `[0,99)` |

**Minimal interpretation:** Regional map resolves the RMS Figure 52 reference by figure identity: this snapshot has it on page 130, despite RMS citing page 131.

**Visual source:** figure; inspect the named object on the original page, including its caption, labels, and notes.

<a id="v-m3b"></a>

### V_M3B — M-3.B requirement and non-italic response

**Document:** V · **Layer:** gold_core · **Passage state:** FOUND · **Questions:** Q3 · **Role:** support

| PDF page | Exact complete source span |
|---|---|
| [67](https://fchlpm.sbafla.com/media/c5apncqi/rms19standardsdisclosures_04222021.pdf#page=67) | `[250,856)` |

**Minimal interpretation:** RMS asserts regional total/intensity consistency and cites Form M-1; this is submission justification without a matched reviewer-response chronology.

<a id="v-smoothing"></a>

### V_SMOOTHING — G-1.2 calibration paragraph

**Document:** V · **Layer:** gold_core · **Passage state:** FOUND · **Questions:** Q3, Q4, Q5 · **Role:** support

| PDF page | Exact complete source span |
|---|---|
| [16](https://fchlpm.sbafla.com/media/c5apncqi/rms19standardsdisclosures_04222021.pdf#page=16) | `[259,841)` |

**Minimal interpretation:** RMS describes smoothed historical targets on 69 coastal segments and adjusting simulated events toward them to reduce sampling artifacts; this is an existing method description.

<a id="v-gates"></a>

### V_GATES — M-2.8–9 responses and Figure 11

**Document:** V · **Layer:** audit_context · **Passage state:** FOUND · **Questions:** Q3, Q5 · **Role:** support

| PDF page | Exact complete source span |
|---|---|
| [64](https://fchlpm.sbafla.com/media/c5apncqi/rms19standardsdisclosures_04222021.pdf#page=64) | `[866,2180)` |

**Minimal interpretation:** RMS describes 50-mile validation gates and historical/current/prior category-group comparisons; its no-data-modification statement is not a no-calibration statement.

**Visual source:** narrative and figure; inspect the named object on the original page, including its caption, labels, and notes.

<a id="v-gate-plots"></a>

### V_GATE_PLOTS — Figures 12–13

**Document:** V · **Layer:** audit_context · **Passage state:** FOUND · **Questions:** Q3, Q4, Q5 · **Role:** support

| PDF page | Exact complete source span |
|---|---|
| [65](https://fchlpm.sbafla.com/media/c5apncqi/rms19standardsdisclosures_04222021.pdf#page=65) | `[0,1353)` |

**Minimal interpretation:** Plots compare historical rates, version 21.0, and version 18.1; differences are visible, but within-review timing and causation are not supplied.

**Visual source:** figure; inspect the named object on the original page, including its caption, labels, and notes.

<a id="v-m3-disc"></a>

### V_M3_DISC — M-3.C and disclosures 1–2 responses

**Document:** V · **Layer:** audit_context · **Passage state:** FOUND · **Questions:** Q3, Q5 · **Role:** support

| PDF page | Exact complete source span |
|---|---|
| [68](https://fchlpm.sbafla.com/media/c5apncqi/rms19standardsdisclosures_04222021.pdf#page=68) | `[745,1493)` |

**Minimal interpretation:** RMS uses the common intensity definition and points to Form S-3 for distributions/data; it asserts no additional database assumptions.

<a id="v-poisson"></a>

### V_POISSON — S-1.1 Storm Frequency, continued

**Document:** V · **Layer:** gold_core · **Passage state:** FOUND · **Questions:** Q3 · **Role:** support

| PDF page | Exact complete source span |
|---|---|
| [88](https://fchlpm.sbafla.com/media/c5apncqi/rms19standardsdisclosures_04222021.pdf#page=88) | `[3550,3753)` |
| [89](https://fchlpm.sbafla.com/media/c5apncqi/rms19standardsdisclosures_04222021.pdf#page=89) | `[62,446)` |

**Minimal interpretation:** RMS describes storm-specific Poisson means calibrated toward smoothed coastal counts and reports goodness-of-fit checks.

<a id="v-fit-results"></a>

### V_FIT_RESULTS — S-1 Storm Frequency

**Document:** V · **Layer:** audit_context · **Passage state:** FOUND · **Questions:** Q3, Q5 · **Role:** qualification

| PDF page | Exact complete source span |
|---|---|
| [99](https://fchlpm.sbafla.com/media/c5apncqi/rms19standardsdisclosures_04222021.pdf#page=99) | `[1313,1805)` |

**Minimal interpretation:** RMS reports conditional chi-square and Neyman–Scott p-values of 17%, and a regional/category comparison p-value of 98%; these vendor-reported results do not independently certify each gate.

<a id="v-form-s3"></a>

### V_FORM_S3 — Form S-3, Table 24, Storm Frequency row

**Document:** V · **Layer:** audit_context · **Passage state:** FOUND · **Questions:** Q3 · **Role:** support

| PDF page | Exact complete source span |
|---|---|
| [193](https://fchlpm.sbafla.com/media/c5apncqi/rms19standardsdisclosures_04222021.pdf#page=193) | `[472,766)` |

**Minimal interpretation:** The row identifies Poisson frequency, HURDAT2, and 1900–2018; read the table headings with the row.

**Visual source:** table; inspect the named object on the original page, including its caption, labels, and notes.

<a id="v-base-tracks"></a>

### V_BASE_TRACKS — M-1.A/B and disclosures 1–4

**Document:** V · **Layer:** audit_context · **Passage state:** FOUND · **Questions:** Q3, Q5 · **Role:** qualification

| PDF page | Exact complete source span |
|---|---|
| [60](https://fchlpm.sbafla.com/media/c5apncqi/rms19standardsdisclosures_04222021.pdf#page=60) | `[108,2674)` |

**Minimal interpretation:** RMS repeatedly states official HURDAT2 tracks were unmodified and no trend/weight/partition was used. That does not deny smoothed targets or adjusted bypass membership.

<a id="v-bypass"></a>

### V_BYPASS — Form M-1.B and response

**Document:** V · **Layer:** audit_context · **Passage state:** FOUND · **Questions:** Q3, Q5 · **Role:** qualification

| PDF page | Exact complete source span |
|---|---|
| [176](https://fchlpm.sbafla.com/media/c5apncqi/rms19standardsdisclosures_04222021.pdf#page=176) | `[691,1818)` |

**Minimal interpretation:** RMS explicitly reports updating historical bypass counts to events producing RMS loss; this qualifies any blanket claim that historical inputs were untouched.

<a id="v-limited-record"></a>

### V_LIMITED_RECORD — Form M-1.C and response

**Document:** V · **Layer:** audit_context · **Passage state:** FOUND · **Questions:** Q3, Q5 · **Role:** qualification

| PDF page | Exact complete source span |
|---|---|
| [176](https://fchlpm.sbafla.com/media/c5apncqi/rms19standardsdisclosures_04222021.pdf#page=176) | `[1819,2032)` |

**Minimal interpretation:** RMS justifies agreement by reference to limited historical observations; the standard is not presented as exact numerical equality.

<a id="v-m1-references"></a>

### V_M1_REFERENCES — Form M-1.D/E and responses

**Document:** V · **Layer:** audit_context · **Passage state:** FOUND · **Questions:** Q3, Q5 · **Role:** qualification

| PDF page | Exact complete source span |
|---|---|
| [176](https://fchlpm.sbafla.com/media/c5apncqi/rms19standardsdisclosures_04222021.pdf#page=176) | `[2033,2875)` |

**Minimal interpretation:** RMS points to regional histograms and says data were not partitioned or modified. Read this with the explicit bypass-count adjustment on the same page.

<a id="v-added-storms"></a>

### V_ADDED_STORMS — Form M-1.F and storm-change table

**Document:** V · **Layer:** audit_context · **Passage state:** FOUND · **Questions:** Q3, Q4, Q5 · **Role:** support

| PDF page | Exact complete source span |
|---|---|
| [176](https://fchlpm.sbafla.com/media/c5apncqi/rms19standardsdisclosures_04222021.pdf#page=176) | `[2876,3126)` |
| [177](https://fchlpm.sbafla.com/media/c5apncqi/rms19standardsdisclosures_04222021.pdf#page=177) | `[60,304)` |

**Minimal interpretation:** Irma 2017, Nate 2017, and Michael 2018 were added relative to the previously accepted storm set; the passage does not attribute these additions to the April review.

**Visual source:** narrative and table; inspect the named object on the original page, including its caption, labels, and notes.

<a id="v-m1-notes"></a>

### V_M1_NOTES — Form M-1 notes 1–3

**Document:** V · **Layer:** audit_context · **Passage state:** FOUND · **Questions:** Q3, Q5 · **Role:** qualification

| PDF page | Exact complete source span |
|---|---|
| [177](https://fchlpm.sbafla.com/media/c5apncqi/rms19standardsdisclosures_04222021.pdf#page=177) | `[655,2571)` |

**Minimal interpretation:** The submission reproduces the conditional historical-set adjustments and counting/reconciliation rules; these instructions are not evidence RMS used every exception.

<a id="v-m1-table"></a>

### V_M1_TABLE — Form M-1, Table 18

**Document:** V · **Layer:** gold_core · **Passage state:** FOUND · **Questions:** Q3, Q5 · **Role:** qualification

| PDF page | Exact complete source span |
|---|---|
| [178](https://fchlpm.sbafla.com/media/c5apncqi/rms19standardsdisclosures_04222021.pdf#page=178) | `[0,1468)` |

**Minimal interpretation:** Historical and modeled rates differ: statewide category 1 is 0.218 versus 0.182; northwest Florida category 4 is 0 versus 0.012. These differences alone establish neither noncompliance nor review-induced change.

**Visual source:** table; inspect the named object on the original page, including its caption, labels, and notes.

<a id="v-region-plots"></a>

### V_REGION_PLOTS — Figure 52

**Document:** V · **Layer:** audit_context · **Passage state:** FOUND · **Questions:** Q3, Q5 · **Role:** qualification

| PDF page | Exact complete source span |
|---|---|
| [179](https://fchlpm.sbafla.com/media/c5apncqi/rms19standardsdisclosures_04222021.pdf#page=179) | `[0,293)` |

**Minimal interpretation:** Regional/category and bypass comparisons corroborate nonidentical historical/model frequencies; the map reference has a page-number mismatch.

**Visual source:** figure; inspect the named object on the original page, including its caption, labels, and notes.

<a id="v-storm-plots"></a>

### V_STORM_PLOTS — Figure 53

**Document:** V · **Layer:** audit_context · **Passage state:** FOUND · **Questions:** Q3, Q4 · **Role:** cross reference

| PDF page | Exact complete source span |
|---|---|
| [180](https://fchlpm.sbafla.com/media/c5apncqi/rms19standardsdisclosures_04222021.pdf#page=180) | `[0,278)` |

**Minimal interpretation:** Plots identify the three added storm tracks. The page 177 reference to Figure 56 does not match this figure number; identification is by caption/storm names.

**Visual source:** figure; inspect the named object on the original page, including its caption, labels, and notes.

<a id="v-s1-table"></a>

### V_S1_TABLE — Form S-1, Table 21 and instructions

**Document:** V · **Layer:** audit_context · **Passage state:** FOUND · **Questions:** Q3, Q5 · **Role:** qualification

| PDF page | Exact complete source span |
|---|---|
| [191](https://fchlpm.sbafla.com/media/c5apncqi/rms19standardsdisclosures_04222021.pdf#page=191) | `[0,2127)` |

**Minimal interpretation:** The annual count distribution also differs: one-hurricane probability is 0.252 historical versus 0.310 modeled; this is not a coastal-gate comparison.

**Visual source:** table; inspect the named object on the original page, including its caption, labels, and notes.

<a id="v-prior-update"></a>

### V_PRIOR_UPDATE — G-1.7.A, Stochastic Module

**Document:** V · **Layer:** gold_core · **Passage state:** FOUND · **Questions:** Q4, Q5 · **Role:** support

| PDF page | Exact complete source span |
|---|---|
| [35](https://fchlpm.sbafla.com/media/c5apncqi/rms19standardsdisclosures_04222021.pdf#page=35) | `[651,1180)` |
| [35](https://fchlpm.sbafla.com/media/c5apncqi/rms19standardsdisclosures_04222021.pdf#page=35) | `[1639,1918)` |

**Minimal interpretation:** Landfall and bypass rates were revised using July 2019 HURDAT2; the question sets the comparison from previously accepted model to this year’s initial submission.

<a id="v-baseline-version"></a>

### V_BASELINE_VERSION — G-1.7.B

**Document:** V · **Layer:** gold_core · **Passage state:** FOUND · **Questions:** Q4, Q5 · **Role:** qualification

| PDF page | Exact complete source span |
|---|---|
| [36](https://fchlpm.sbafla.com/media/c5apncqi/rms19standardsdisclosures_04222021.pdf#page=36) | `[1690,2237)` |

**Minimal interpretation:** The identified comparison is version 21.0 build 2050 versus version 18.1 build 1945; it is not a before/after-April-review comparison.

<a id="v-medium-term"></a>

### V_MEDIUM_TERM — G-1 other changes, medium-term rates

**Document:** V · **Layer:** audit_context · **Passage state:** FOUND · **Questions:** Q4, Q5 · **Role:** excluded candidate

| PDF page | Exact complete source span |
|---|---|
| [36](https://fchlpm.sbafla.com/media/c5apncqi/rms19standardsdisclosures_04222021.pdf#page=36) | `[261,582)` |

**Minimal interpretation:** RMS says medium-term event-rate updates are not used in the certified analysis profiles; they must not be substituted for this case’s frequency change.

<a id="v-history-policy"></a>

### V_HISTORY_POLICY — CI-6.C/D and responses

**Document:** V · **Layer:** audit_context · **Passage state:** FOUND · **Questions:** Q4, Q5 · **Role:** unresolved dependency

| PDF page | Exact complete source span |
|---|---|
| [163](https://fchlpm.sbafla.com/media/c5apncqi/rms19standardsdisclosures_04222021.pdf#page=163) | `[691,1639)` |

**Minimal interpretation:** RMS describes change tracking and promises a within-cycle version list. This page does not contain the actual dated change history.

<a id="v-met-cert"></a>

### V_MET_CERT — Form G-2 certification and signature/date fields

**Document:** V · **Layer:** audit_context · **Passage state:** FOUND · **Questions:** Q3, Q4, Q5 · **Role:** qualification

| PDF page | Exact complete source span |
|---|---|
| [170](https://fchlpm.sbafla.com/media/c5apncqi/rms19standardsdisclosures_04222021.pdf#page=170) | `[82,872)` |
| [170](https://fchlpm.sbafla.com/media/c5apncqi/rms19standardsdisclosures_04222021.pdf#page=170) | `[963,1530)` |

**Minimal interpretation:** Original certification is dated October 29, 2020; revision/final signatures April 22, 2021. Both document and model revisions trigger signatures. The blank deficiency line cannot prove absence of a reply.

**Visual source:** form; inspect the named object on the original page, including its caption, labels, and notes.

<a id="v-editor-cert"></a>

### V_EDITOR_CERT — Form G-7 editorial certification and dates

**Document:** V · **Layer:** audit_context · **Passage state:** FOUND · **Questions:** Q3, Q4, Q5 · **Role:** qualification

| PDF page | Exact complete source span |
|---|---|
| [175](https://fchlpm.sbafla.com/media/c5apncqi/rms19standardsdisclosures_04222021.pdf#page=175) | `[74,1419)` |
| [175](https://fchlpm.sbafla.com/media/c5apncqi/rms19standardsdisclosures_04222021.pdf#page=175) | `[1515,2082)` |

**Minimal interpretation:** Editorial review covers submission changes and has April 22 revision/final signatures; it does not identify an M-3.B model alteration.

**Visual source:** form; inspect the named object on the original page, including its caption, labels, and notes.

<a id="v-cover"></a>

### V_COVER — Cover

**Document:** V · **Layer:** audit_context · **Passage state:** FOUND · **Questions:** Q3, Q4 · **Role:** chronology

| PDF page | Exact complete source span |
|---|---|
| [1](https://fchlpm.sbafla.com/media/c5apncqi/rms19standardsdisclosures_04222021.pdf#page=1) | `[0,341)` |

**Minimal interpretation:** April 22, 2021 identifies the revised snapshot and coincides with the review’s last day; it does not establish a response after review ended.

**Visual source:** cover; inspect the named object on the original page, including its caption, labels, and notes.

<a id="v-model-id"></a>

### V_MODEL_ID — Hurricane Model Identification

**Document:** V · **Layer:** audit_context · **Passage state:** FOUND · **Questions:** Q3, Q4, Q5 · **Role:** qualification

| PDF page | Exact complete source span |
|---|---|
| [4](https://fchlpm.sbafla.com/media/c5apncqi/rms19standardsdisclosures_04222021.pdf#page=4) | `[0,873)` |

**Minimal interpretation:** The model-identification field says June 2021 while the footer says April 22, 2021; neither dates an M-3.B instruction-response exchange.

**Visual source:** form; inspect the named object on the original page, including its caption, labels, and notes.

<a id="v-track-smoothing"></a>

### V_TRACK_SMOOTHING — S-1.1 Track Translational Speed and Heading

**Document:** V · **Layer:** audit_context · **Passage state:** FOUND · **Questions:** Q3, Q5 · **Role:** excluded candidate

| PDF page | Exact complete source span |
|---|---|
| [88](https://fchlpm.sbafla.com/media/c5apncqi/rms19standardsdisclosures_04222021.pdf#page=88) | `[1160,2008)` |

**Minimal interpretation:** Leave-one-out selection is described for track-step smoothing scales; this does not establish how coastal-frequency smoothing bandwidth was selected.

<a id="v-xlsx-reference"></a>

### V_XLSX_REFERENCE — Form M-1.G

**Document:** V · **Layer:** audit_context · **Passage state:** FOUND · **Questions:** Q3, Q5 · **Role:** unresolved dependency

| PDF page | Exact complete source span |
|---|---|
| [177](https://fchlpm.sbafla.com/media/c5apncqi/rms19standardsdisclosures_04222021.pdf#page=177) | `[305,654)` |

**Minimal interpretation:** The underlying RMS19FormM1.xlsx is referenced but not contained in the PDFs; its reported table is present on page 178.

<a id="t-m3-standard"></a>

### T_M3_STANDARD — M-3.B and Audit 1–5

**Document:** T · **Layer:** audit_context · **Passage state:** FOUND · **Questions:** Q1, Q2 · **Role:** support

| PDF page | Exact complete source span |
|---|---|
| [19](https://fchlpm.sbafla.com/media/uzkplkto/20210422_rms_2019stds_ptrpt.pdf#page=19) | `[47,510)` |
| [19](https://fchlpm.sbafla.com/media/uzkplkto/20210422_rms_2019stds_ptrpt.pdf#page=19) | `[1192,1873)` |
| [20](https://fchlpm.sbafla.com/media/uzkplkto/20210422_rms_2019stds_ptrpt.pdf#page=20) | `[47,127)` |

**Minimal interpretation:** The report reproduces the requirement and planned audits; these are separate from its completed-review comments.

<a id="t-m3-review"></a>

### T_M3_REVIEW — M-3 verification and Team comments

**Document:** T · **Layer:** gold_core · **Passage state:** FOUND · **Questions:** Q2, Q4 · **Role:** support

| PDF page | Exact complete source span |
|---|---|
| [20](https://fchlpm.sbafla.com/media/uzkplkto/20210422_rms_2019stds_ptrpt.pdf#page=20) | `[128,313)` |

**Minimal interpretation:** The Team marks M-3 verified and records gate-map and Form S-3 distribution/source review. No change instruction is stated in these comments.

<a id="t-landfall-review"></a>

### T_LANDFALL_REVIEW — M-2 verification and Team comments

**Document:** T · **Layer:** gold_core · **Passage state:** FOUND · **Questions:** Q2, Q4, Q5 · **Role:** support

| PDF page | Exact complete source span |
|---|---|
| [17](https://fchlpm.sbafla.com/media/uzkplkto/20210422_rms_2019stds_ptrpt.pdf#page=17) | `[1921,2024)` |
| [18](https://fchlpm.sbafla.com/media/uzkplkto/20210422_rms_2019stds_ptrpt.pdf#page=18) | `[47,162)` |

**Minimal interpretation:** The Team reviewed annual-rate updates, gate/category methodology, and historical-frequency smoothing; examination is not evidence that reviewers caused the updates.

<a id="t-m1-review"></a>

### T_M1_REVIEW — M-1 verification and Team comments

**Document:** T · **Layer:** audit_context · **Passage state:** FOUND · **Questions:** Q2, Q4, Q5 · **Role:** support

| PDF page | Exact complete source span |
|---|---|
| [16](https://fchlpm.sbafla.com/media/uzkplkto/20210422_rms_2019stds_ptrpt.pdf#page=16) | `[653,1360)` |

**Minimal interpretation:** Review covered the historical set, prior/current rates, bypass methodology/calibration, Forms M-1/S-1, and implementation of HURDAT2-based landfall updates.

<a id="t-bypass-question"></a>

### T_BYPASS_QUESTION — M-1 pre-visit Question 15

**Document:** T · **Layer:** audit_context · **Passage state:** FOUND · **Questions:** Q2, Q3, Q5 · **Role:** qualification

| PDF page | Exact complete source span |
|---|---|
| [16](https://fchlpm.sbafla.com/media/uzkplkto/20210422_rms_2019stds_ptrpt.pdf#page=16) | `[479,652)` |

**Minimal interpretation:** The Team asks why simulated bypass counts exceed historical counts, 43 versus 26. This is adjacent bypass scrutiny, not a direct coastal-landfall-frequency challenge or a quoted vendor reply.

<a id="t-m2-questions"></a>

### T_M2_QUESTIONS — M-2 Audit 2 and pre-visit Questions 8–9

**Document:** T · **Layer:** audit_context · **Passage state:** FOUND · **Questions:** Q2, Q5 · **Role:** qualification

| PDF page | Exact complete source span |
|---|---|
| [17](https://fchlpm.sbafla.com/media/uzkplkto/20210422_rms_2019stds_ptrpt.pdf#page=17) | `[560,990)` |
| [17](https://fchlpm.sbafla.com/media/uzkplkto/20210422_rms_2019stds_ptrpt.pdf#page=17) | `[1761,1920)` |

**Minimal interpretation:** Smoothing is in the audit remit; the listed questions concern Rmax, Amax, and EOFs, not a specific M-3.B frequency objection.

<a id="t-opening-updates"></a>

### T_OPENING_UPDATES — Opening briefing

**Document:** T · **Layer:** gold_core · **Passage state:** FOUND · **Questions:** Q4, Q5 · **Role:** qualification

| PDF page | Exact complete source span |
|---|---|
| [3](https://fchlpm.sbafla.com/media/uzkplkto/20210422_rms_2019stds_ptrpt.pdf#page=3) | `[393,1390)` |

**Minimal interpretation:** The opening briefing already lists the July 2019 HURDAT2 event-set update. This weighs against attributing that listed update to later scrutiny in the same review.

<a id="t-original-request"></a>

### T_ORIGINAL_REQUEST — Pre-visit preamble: changes since original submission

**Document:** T · **Layer:** audit_context · **Passage state:** FOUND · **Questions:** Q3, Q4, Q5 · **Role:** unresolved dependency

| PDF page | Exact complete source span |
|---|---|
| [4](https://fchlpm.sbafla.com/media/uzkplkto/20210422_rms_2019stds_ptrpt.pdf#page=4) | `[1009,1490)` |

**Minimal interpretation:** Conditionally requests descriptions/reasons and difference forms for changes since November 1, 2020; it does not state that such changes occurred.

<a id="t-amendment"></a>

### T_AMENDMENT — Remote-review procedural references

**Document:** T · **Layer:** audit_context · **Passage state:** FOUND · **Questions:** Q2, Q5 · **Role:** unresolved dependency

| PDF page | Exact complete source span |
|---|---|
| [3](https://fchlpm.sbafla.com/media/uzkplkto/20210422_rms_2019stds_ptrpt.pdf#page=3) | `[47,392)` |
| [4](https://fchlpm.sbafla.com/media/uzkplkto/20210422_rms_2019stds_ptrpt.pdf#page=4) | `[1491,1889)` |

**Minimal interpretation:** The Team cites a December 10, 2020 procedural amendment; it is not present in this standards snapshot and cannot be assumed to modify M-3.B.

<a id="t-editorial"></a>

### T_EDITORIAL — Editorial Items 1–12

**Document:** T · **Layer:** audit_context · **Passage state:** FOUND · **Questions:** Q3, Q4, Q5 · **Role:** qualification

| PDF page | Exact complete source span |
|---|---|
| [4](https://fchlpm.sbafla.com/media/uzkplkto/20210422_rms_2019stds_ptrpt.pdf#page=4) | `[1959,2867)` |
| [5](https://fchlpm.sbafla.com/media/uzkplkto/20210422_rms_2019stds_ptrpt.pdf#page=5) | `[47,526)` |

**Minimal interpretation:** The report records corrected/clarified submission items, including G-1 and M-4; no M-3 item appears in this list. This documents editorial revisions, not an M-3.B model alteration.

<a id="t-revision-audit"></a>

### T_REVISION_AUDIT — G-1 Audit 6, continued

**Document:** T · **Layer:** audit_context · **Passage state:** FOUND · **Questions:** Q4, Q5 · **Role:** qualification

| PDF page | Exact complete source span |
|---|---|
| [6](https://fchlpm.sbafla.com/media/uzkplkto/20210422_rms_2019stds_ptrpt.pdf#page=6) | `[1781,2224)` |
| [7](https://fchlpm.sbafla.com/media/uzkplkto/20210422_rms_2019stds_ptrpt.pdf#page=7) | `[47,1295)` |

**Minimal interpretation:** Audit instructions distinguish prior accepted, initial, intermediate, and revised baselines; those prescribed comparisons are not actual before/after findings.

<a id="t-history"></a>

### T_HISTORY — CI-6.D, Question 46, and Team comments

**Document:** T · **Layer:** gold_core · **Passage state:** FOUND · **Questions:** Q4, Q5 · **Role:** unresolved dependency

| PDF page | Exact complete source span |
|---|---|
| [62](https://fchlpm.sbafla.com/media/uzkplkto/20210422_rms_2019stds_ptrpt.pdf#page=62) | `[675,930)` |
| [62](https://fchlpm.sbafla.com/media/uzkplkto/20210422_rms_2019stds_ptrpt.pdf#page=62) | `[1625,1970)` |

**Minimal interpretation:** The Team requested and reviewed model-version history. The underlying entries are absent from these pages, so dates/reasons cannot be reconstructed here.

<a id="t-no-refitting"></a>

### T_NO_REFITTING — M-2 remaining Team comments

**Document:** T · **Layer:** audit_context · **Passage state:** FOUND · **Questions:** Q4, Q5 · **Role:** qualification

| PDF page | Exact complete source span |
|---|---|
| [18](https://fchlpm.sbafla.com/media/uzkplkto/20210422_rms_2019stds_ptrpt.pdf#page=18) | `[163,640)` |

**Minimal interpretation:** A no-refitting statement occurs among windfield/HWind discussions; its parameter scope is not explicit enough to prove landfall calibration was unchanged.

<a id="t-no-method-s2"></a>

### T_NO_METHOD_S2 — S-2 verification and Team comments

**Document:** T · **Layer:** audit_context · **Passage state:** FOUND · **Questions:** Q4, Q5 · **Role:** qualification

| PDF page | Exact complete source span |
|---|---|
| [27](https://fchlpm.sbafla.com/media/uzkplkto/20210422_rms_2019stds_ptrpt.pdf#page=27) | `[794,981)` |

**Minimal interpretation:** The Team reports no methodology changes from the previously accepted model and no new sensitivity analysis. This counters a new-method claim, without excluding data/rate updates.

<a id="t-no-method-s3"></a>

### T_NO_METHOD_S3 — S-3 verification and Team comments

**Document:** T · **Layer:** audit_context · **Passage state:** FOUND · **Questions:** Q4, Q5 · **Role:** qualification

| PDF page | Exact complete source span |
|---|---|
| [28](https://fchlpm.sbafla.com/media/uzkplkto/20210422_rms_2019stds_ptrpt.pdf#page=28) | `[938,1125)` |

**Minimal interpretation:** The corresponding uncertainty comment repeats no methodology changes and no new uncertainty analysis; it is not a dated M-3.B change history.

<a id="t-independence"></a>

### T_INDEPENDENCE — M-4 pre-visit Question 11

**Document:** T · **Layer:** audit_context · **Passage state:** FOUND · **Questions:** Q2, Q5 · **Role:** excluded candidate

| PDF page | Exact complete source span |
|---|---|
| [22](https://fchlpm.sbafla.com/media/uzkplkto/20210422_rms_2019stds_ptrpt.pdf#page=22) | `[459,799)` |

**Minimal interpretation:** An explicit independence challenge concerns spatially adjusted Irma wind footprints. It must not be assigned to coastal-frequency smoothing under M-3.B.

<a id="t-form-m3"></a>

### T_FORM_M3 — M-6, Form M-3, Question 16 and comments

**Document:** T · **Layer:** audit_context · **Passage state:** FOUND · **Questions:** Q2, Q4, Q5 · **Role:** excluded candidate

| PDF page | Exact complete source span |
|---|---|
| [24](https://fchlpm.sbafla.com/media/uzkplkto/20210422_rms_2019stds_ptrpt.pdf#page=24) | `[463,607)` |
| [24](https://fchlpm.sbafla.com/media/uzkplkto/20210422_rms_2019stds_ptrpt.pdf#page=24) | `[1612,1805)` |

**Minimal interpretation:** Form M-3 concerns wind radii; its discrepancy question and no-Rmax-change comment are not evidence about Standard M-3.B.

<a id="t-s1-review"></a>

### T_S1_REVIEW — S-1 Questions 17–18 and Team comments

**Document:** T · **Layer:** audit_context · **Passage state:** FOUND · **Questions:** Q2, Q5 · **Role:** qualification

| PDF page | Exact complete source span |
|---|---|
| [26](https://fchlpm.sbafla.com/media/uzkplkto/20210422_rms_2019stds_ptrpt.pdf#page=26) | `[1213,1736)` |

**Minimal interpretation:** The Team reviews forms, tests, and historical/model distributions. Questions about data ending in 2008 concern central pressure and Rmax, not storm frequency.

<a id="t-m1-audit"></a>

### T_M1_AUDIT — M-1 requirement and Audit 1–7

**Document:** T · **Layer:** audit_context · **Passage state:** FOUND · **Questions:** Q1, Q2, Q5 · **Role:** qualification

| PDF page | Exact complete source span |
|---|---|
| [15](https://fchlpm.sbafla.com/media/uzkplkto/20210422_rms_2019stds_ptrpt.pdf#page=15) | `[0,2060)` |
| [16](https://fchlpm.sbafla.com/media/uzkplkto/20210422_rms_2019stds_ptrpt.pdf#page=16) | `[47,462)` |

**Minimal interpretation:** The report reproduces permitted base-set adjustments and the review program; this is regulatory context, not completed-change evidence.

<a id="s-glossary"></a>

### S_GLOSSARY — Glossary: Landfall and Landfall Frequency Distribution

**Document:** S · **Layer:** audit_context · **Passage state:** FOUND · **Questions:** Q1, Q5 · **Role:** qualification

| PDF page | Exact complete source span |
|---|---|
| [249](https://fchlpm.sbafla.com/media/o10dfucl/2019_hurricaneroa.pdf#page=249) | `[0,468)` |

**Minimal interpretation:** Landfall is a sea-to-land center crossing; the frequency definition uses one initial crossing for a multiply crossing path. Preserve this alongside the specific Form M-1 regional/statewide counting instructions.

<a id="v-m3a"></a>

### V_M3A — M-3.A response and frequency cross-reference

**Document:** V · **Layer:** audit_context · **Passage state:** FOUND · **Questions:** Q3 · **Role:** support

| PDF page | Exact complete source span |
|---|---|
| [66](https://fchlpm.sbafla.com/media/c5apncqi/rms19standardsdisclosures_04222021.pdf#page=66) | `[256,1201)` |

**Minimal interpretation:** RMS locates intensity-by-region landfall comparisons in Form M-1 and relates other parameter comparisons to S-1.6. These are submission assertions and cross-references.

<a id="v-wind-no-change"></a>

### V_WIND_NO_CHANGE — M-4.1 continuation

**Document:** V · **Layer:** audit_context · **Passage state:** FOUND · **Questions:** Q4, Q5 · **Role:** qualification

| PDF page | Exact complete source span |
|---|---|
| [72](https://fchlpm.sbafla.com/media/c5apncqi/rms19standardsdisclosures_04222021.pdf#page=72) | `[59,202)` |

**Minimal interpretation:** RMS states its wind profile and wind field are unchanged since the previous submission; this statement does not concern the coastal-frequency calibration targets.

<a id="v-s1-assurance"></a>

### V_S1_ASSURANCE — S-1.A/B responses

**Document:** V · **Layer:** audit_context · **Passage state:** FOUND · **Questions:** Q3, Q5 · **Role:** support

| PDF page | Exact complete source span |
|---|---|
| [87](https://fchlpm.sbafla.com/media/c5apncqi/rms19standardsdisclosures_04222021.pdf#page=87) | `[285,1524)` |

**Minimal interpretation:** RMS asserts empirical matching and development-stage checks, including landfall-frequency goodness of fit. These are vendor assurances, not independently established performance.

## Reversal search and candidate dispositions

Nine lexical pattern groups were applied to all 710 pages. Connected M-1/M-2/M-3/S-1 provisions, linked forms, review comments, revision procedures, certifications, and plausible counterexamples were read in context. The audit stores patterns, hit offsets, and page hashes. Lexical coverage does not establish exhaustive semantic recall.

| Candidate | Evidence | Disposition |
|---|---|---|
| C01: prior version update | [V_PRIOR_UPDATE](#v-prior-update), [V_BASELINE_VERSION](#v-baseline-version), [V_ADDED_STORMS](#v-added-storms), [T_OPENING_UPDATES](#t-opening-updates) | Supports an update, but baseline and opening-briefing chronology do not establish April review causation. |
| C02: completed scrutiny | [T_LANDFALL_REVIEW](#t-landfall-review), [T_M3_REVIEW](#t-m3-review), [T_M1_REVIEW](#t-m1-review) | Supports examination/verification, not a modification instruction or causal link. |
| C03: vendor methodology | [V_M3B](#v-m3b), [V_SMOOTHING](#v-smoothing), [V_POISSON](#v-poisson) | Describes implementation and justification; no explicit post-review reply. |
| C04: revision without specific model change | [T_EDITORIAL](#t-editorial), [V_MET_CERT](#v-met-cert), [V_EDITOR_CERT](#v-editor-cert), [V_COVER](#v-cover), [V_MODEL_ID](#v-model-id) | Revised documentation and dates do not identify an M-3.B alteration or a response after review completion. |
| C05: counterevidence to method change | [T_NO_METHOD_S2](#t-no-method-s2), [T_NO_METHOD_S3](#t-no-method-s3) | Retain literal scope: comments state no model methodology changes from the previously accepted model. This opposes a newly introduced method but does not negate data/rate updates. |
| C06: adjacent parameter no change | [T_NO_REFITTING](#t-no-refitting), [T_FORM_M3](#t-form-m3) | Cannot globalize windfield/Rmax language to all landfall-frequency parameters. |
| C07: bypass question and method | [T_BYPASS_QUESTION](#t-bypass-question), [V_BYPASS](#v-bypass), [V_M1_TABLE](#v-m1-table) | An actual question plus a related methodology statement, but no explicit timing/matched answer; bypass and coastal landfall remain distinct. |
| C08: different smoothing quantity | [T_INDEPENDENCE](#t-independence), [V_TRACK_SMOOTHING](#v-track-smoothing) | Footprint independence and track-step cross-validation do not establish criticism or selection of coastal-frequency smoothing. |
| C09: qualification to exact match | [S_M1_QUAL](#s-m1-qual), [S_FORM_M1_NOTES](#s-form-m1-notes), [S_S1_FIT](#s-s1-fit), [S_S1_DIFFERENCES](#s-s1-differences), [V_LIMITED_RECORD](#v-limited-record), [V_FIT_RESULTS](#v-fit-results) | Consistency is qualified by scientific justification, count conventions, and statistical fit; none is an unrestricted exemption. |
| C10: scope of unchanged data | [V_BASE_TRACKS](#v-base-tracks), [V_M1_REFERENCES](#v-m1-references), [V_BYPASS](#v-bypass) | Unmodified track data, smoothed calibration targets, and adjusted bypass membership are different objects. Preserve the apparent tension without assuming a contradiction is resolved. |
| C11: plausible missing causal record | [S_CORRECTION_PROCESS](#s-correction-process), [S_REVISION_PROCESS](#s-revision-process), [T_ORIGINAL_REQUEST](#t-original-request), [T_HISTORY](#t-history) | Procedures allow corrections and point to missing before/after history. These are the strongest avenues for reversing the unresolved conclusion, but no actual causal record is present. |
| C12: outside certified profile | [V_MEDIUM_TERM](#v-medium-term) | The source excludes these event-rate updates from certified profiles; not a substitute target. |
| C13: different parameter vintage | [T_S1_REVIEW](#t-s1-review) | Central-pressure and Rmax vintage questions do not establish outdated storm-frequency data. |

Additional lexical candidates were screened by their surrounding text. Standards pages 23/35 concern Commission requests; pages 66/71/73–75 concern interim or platform procedures; page 231 concerns deterministic reruns. Vendor pages 53/69 concern earlier peer review or land cover, pages 97/113 concern storm heading or a roof-engineering workshop, pages 161/297/309 concern reruns or staff responsibilities. Review pages 40/42/63 concern time-element losses, vulnerability modifiers, or security. None supplies a dated M-3.B reviewer-request/vendor-change link. These excluded topic hits do not enter the positive evidence set.

## Cross-references and missing dependencies

| Link | Source → target | Resolution |
|---|---|---|
| M3_VENDOR | [S_M3B](#s-m3b) → [V_M3B](#v-m3b) | Explicit same-standard compliance response; not temporal response. |
| M3_REVIEW | [S_M3B](#s-m3b) → [T_M3_STANDARD](#t-m3-standard), [T_M3_REVIEW](#t-m3-review) | Same standard reproduced and reviewed. |
| COASTAL_DISCLOSURE | [S_M2_DISCLOSURE](#s-m2-disclosure) → [V_GATES](#v-gates), [V_GATE_PLOTS](#v-gate-plots) | Disclosure 9 response and comparison figures. |
| VENDOR_M1 | [V_M3B](#v-m3b) → [V_BYPASS](#v-bypass), [V_LIMITED_RECORD](#v-limited-record), [V_M1_REFERENCES](#v-m1-references), [V_M1_TABLE](#v-m1-table), [V_REGION_PLOTS](#v-region-plots) | Explicit Form M-1 link resolved to pages 176–179. |
| VENDOR_S3 | [V_M3_DISC](#v-m3-disc) → [V_FORM_S3](#v-form-s3) | Explicit Form S-3 reference resolved to page 193. |
| TEAM_S3 | [T_M3_REVIEW](#t-m3-review) → [V_FORM_S3](#v-form-s3) | Same named form; not evidence of chronology. |
| S1_FORM | [V_FIT_RESULTS](#v-fit-results) → [V_S1_TABLE](#v-s1-table) | Storm-frequency discussion followed by Form S-1 disclosure; table on page 191. |
| REGION_MAP | [V_REGION_PLOTS](#v-region-plots) → [S_REGION_MAP](#s-region-map) | Source says Figure 3 page 131; matching Figure 3 is page 130. Preserve discrepancy. |
| ADDED_TRACKS | [V_ADDED_STORMS](#v-added-storms) → [V_STORM_PLOTS](#v-storm-plots) | Source page 177 says Figure 56; matching three-storm Figure 53 is page 180. Resolved by caption and storm identities, with mismatch retained. |
| SMOOTHING_TOPIC | [V_SMOOTHING](#v-smoothing) → [T_LANDFALL_REVIEW](#t-landfall-review) | Analyst topic alignment only; no explicit instruction-response linkage. |

| Dependency | State | Origin | Limit |
|---|---|---|---|
| Original November 1, 2020 submission, marked revisions, notification letters, and within-cycle difference forms | UNRESOLVED | [T_ORIGINAL_REQUEST](#t-original-request), [S_REVISION_PROCESS](#s-revision-process) | Not identified in the three PDFs or prior bounded official-domain locator searches. Actual accessibility is unknown; do not label DOCUMENT_UNAVAILABLE. |
| Actual dated model-version entries and change reasons | UNRESOLVED | [T_HISTORY](#t-history), [V_HISTORY_POLICY](#v-history-policy) | The report says history was reviewed; the submission supplies maintenance policy, not the entries. |
| December 10, 2020 remote-review amendment | UNRESOLVED | [T_AMENDMENT](#t-amendment) | Referenced amendment not contained in the fixed standards PDF; prior locator searches did not identify it. No M-3.B exception is inferred. |
| RMS19FormM1.xlsx | UNRESOLVED | [V_XLSX_REFERENCE](#v-xlsx-reference) | The referenced spreadsheet is not in the three-PDF corpus. Table 18 and its notes are available and inspected; spreadsheet formulas are unverified. |

A dated M-3.B review request, explicit vendor reply, and attributable before/after change record could reverse the present causal assessment. A baseline comparison alone could establish what changed but would still need timing and an explicit link to the review. No missing document has been assigned a hypothetical substantive content.

## Validation and evidence limits

The manual record contains 69 passage records, 91 complete text spans, five questions, and ten separately labeled slots. The authoritative annotation is [m3b_rms_chain.json](m3b_rms_chain.json).

The old validator prescribed the model-change label, the overall UNRESOLVED outcome, and rejection of all change candidates. Those substantive conditions were removed. The replacement checks document identity, exact spans, references, search provenance, and state structure. Its tests explicitly permit an alternative substantive judgment in memory; that test is not evidence that the alternative judgment is true.

These checks do not measure evidence assignment precision, conclusion-critical recall, qualification recall, or agreement with an independent human. The old broad criticality flags have been removed. Only twelve unique core records define the primary recall denominator; content and structural recovery remain to be measured. Milestone 2 design has begun; no parser-run or extraction/retrieval result is claimed.

Earlier fixtures and validation results are preserved under [archive/manual-chain-0.1](archive/manual-chain-0.1/) and [archive/manual-chain-0.2](archive/manual-chain-0.2/).
