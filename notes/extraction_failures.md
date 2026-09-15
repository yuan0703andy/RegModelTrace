
2026-09-15

Record/unit: FT-1 historical candidate pack (19 cases)

Observed problem: Candidate evidence memberships and facet definitions were imported from post-adjudication fixtures. Removing labels did not make the resulting packs source-only independent inputs.

Why this matters: A blinded-looking pack can still inherit outcome-dependent selection and obscure missing or contradictory facets.

Disposition: Retired all 19 current bundles for independent adjudication. Retained raw-source seeds separately; rebuild a new regulator-selected development pack without historical memberships or predictions.

2026-09-15

Record/unit: FT-1 matched A/B/C experiment

Observed problem: Historical A predictions bind historical bundles, while the clean rebuild produces new bundles. Comparing them directly would mix evidence changes with representation changes.

Why this matters: An improvement could not be attributed to explicit facet representation alone.

Disposition: Historical A remains reference-only. Record matched prospective A protocol as pending before any controlled A/B/C claim or compute.

2026-09-15

Record/unit: DCC source preparation preflight

Observed problem: Default compute-node Python has no pypdf and pdftotext was not found on PATH.

Why this matters: Re-extraction with an ad hoc environment would introduce unnecessary source representation drift.

Disposition: Use the retained outcome-free M2 parser products, verify against original-PDF hashes and canonical page spans, and use the existing project runtime on CPU compute for preparation. Do not change the frozen parser.

2026-09-15

Record/unit: FT-1 source-only pack / B-C model payload adapter

Observed problem: Source document roles (STANDARDS, VENDOR_SUBMISSION, PROFESSIONAL_TEAM_REPORT) differ from the old payload grouping names (REGULATOR, VENDOR, REVIEWER). The old adapter silently ignored unknown roles.

Why this matters: A valid source pack could produce empty model evidence without an explicit failure.

Disposition: Add a generic document-role alias map and reject unknown roles. Preserve rich source provenance in the freeze sidecar while adapting only the known model-facing fields. No inference occurred.

2026-09-15

Record/unit: FT-1 clean source-only rebuild

Observed problem: The retained parser products preserve text, but report 452 Impact and 142 Verisk alignment failures, plus 5 and 21 unsupported table-header diagnostics respectively. The mechanical 24-case scope contains 7,846 block references including page context; it is broad navigation material, not 7,846 Gold facts.

Why this matters: Text recoverability does not establish reliable geometry/table structure, and context blocks may belong to adjacent standards or forms.

Disposition: Preserve warnings, full source pools, and all five original PDFs. Require independent scope verification and visual checking of material table/geometry evidence; do not silently use a parser warning as an evidence-sufficiency judgment. Mechanical subsection proposals require actual human atomic splitting and OR/condition review.

2026-09-15

Record/unit: FT-1 human freeze gate

Observed problem: The original research adapter accepted signed empty returns, silently collapsed duplicate identities, and did not bind source-scope verification to pilot bytes. Those are preparation interface defects, not Qwen errors.

Why this matters: Incomplete or stale human metadata could appear to satisfy a gate.

Disposition: Require nonempty unique cases, applicability/coverage/rationales, distinct adjudicator identities, source-scope signature and pilot hash, and vendor support for demonstrated vendor facets. Preserve the rich source pilot as a freeze sidecar. No truth or model output was edited.

2026-09-15

Record/unit: Public-release size verification during FT-1 preparation

Observed problem: The release verifier scans ignored working files too, and detected the 66 MB Verisk PDF in the temporary input workspace. The PDF was not staged in Git.

Why this matters: Public source-tree checks and external research inputs have different storage boundaries.

Disposition: Preserved the original PDF copies by moving the entire temporary raw folder to Downloads/RegModelTrace-FT1-SourceOnly-raw-backup-20260915. The self-contained review package also holds all originals. No PDF or historical data was deleted; no release gate was weakened.

2026-09-15

Record/unit: FT-1 navigation-context CPU tokenization diagnostic

Observed problem: 0/24 broad navigation prototype contexts exceed the frozen model context limit when reserving output tokens. These are not final B/C requests.

Why this matters: The mechanical audit scope is too broad to assume it can be directly submitted as a model context.

Disposition: Preserve all source evidence; require independently verified bounded scope before human outcomes and exact final-template token counting before compute. No truncation, weight loading, classification, or model inference occurred.

2026-09-15

Record/unit: FT-1 CPU budget diagnostic v1 (INVALID)

Observed problem: All contexts reported two tokens. The tokenizer returned a mapping, so len() counted two mapping fields rather than input token IDs. The preliminary 0/24 over-budget note above is invalid.

Why this matters: This return-shape mismatch could bypass the research runner's no-truncation check too. It is a tokenizer interface bug, not a model reasoning result.

Disposition: Preserve the invalid v1 receipt separately; use explicit return_dict=False and count input_ids defensively in both the CPU diagnostic and research runner. Rerun only CPU tokenization, not inference; no weights or model decisions are involved.

2026-09-15

Record/unit: FT-1 research decision adapter

Observed problem: The scorer could consider weight adaptation even when saved A has no matching new case/bundle reference; it also presented a research finding as lora_authorized despite Condition D remaining unauthorized.

Why this matters: A preparation or incomplete diagnostic must not become a controlled representation claim or implicit permission to train.

Disposition: Unmatched A forces EVIDENCE_INCONCLUSIVE. Scorer reports LoRA authorization false; a separately approved matched-reference protocol and later training proposal remain required. No historical score, truth, or weights were changed.

2026-09-15

Record/unit: Corrected CPU token-ID budget diagnostic

Observed result: 19/24 broad navigation prototypes exceed the frozen input-plus-output context budget. The invalid v1 count is superseded, not erased.

Disposition: Independently finalize bounded source scopes before outcomes, preserve material reversal evidence, and count the exact final B/C template before compute. Do not truncate or treat navigation prototypes as final requests. No model inference occurred.
