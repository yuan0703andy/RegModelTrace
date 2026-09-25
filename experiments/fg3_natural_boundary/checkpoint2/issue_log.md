# FG-3 Checkpoint 2 issues

## CP2-01 — Wrong first-occurrence source boundary (corrected)

The initial builder searched for the first raw occurrence of an anchor string instead of mapping the frozen first-match normalized offset. It selected Form A-5 subsection B for `FG3L_38d49e13a06daf85`, whose fixed anchor is in subsection C, and a general model-change comment for `FG3L_199e296b691cc21d`, whose fixed anchor is in Audit 3's vulnerability-vintage comment. Both source units were corrected without changing the frozen lead. All 39 rebuilt units now contain their fixed anchors; the verification script enforces this invariant.

## CP2-02 — Pairing-key chronology deviation (open)

Counterpart PDF counts for selected standard IDs were viewed before the full key plan was saved. Eighteen affected plans are listed in `pair_search_inputs.jsonl` with `primary_protocol_clean=false` and the previously counted IDs. Source-derived keys and all literal matches remain preserved, but those plans cannot be represented as cleanly prospective. No model inference or gold labels were viewed.

## CP2-03 — Literal hit is not a complete counterpart (open)

The 36 pairing audits currently retain exact matching paragraphs and provenance. They do not yet expand every Panel A matching vendor section or verify every Panel C review/vendor source unit and same substantive object. The 30 non-overflow, non-ambiguous literal hit sets therefore remain `AWAIT_SOURCE_UNIT_REVIEW`. Three hit sets exceed the frozen paragraph limit and three lack a usable recorded key. Do not construct model packets from these draft matches.

## CP2-04 — Exposure equivalence is unresolved (open)

One source-unit exact-overlap candidate and seven counterpart-hit-set exact-overlap candidates were found against the checksum-verified known-exposure ledger. Exact overlap can arise from a copied standard or audit prompt, while no exact match cannot rule out substantial equivalence. The 347-file ledger must be reviewed at the final clause and complete paired-passage level, recording matched file IDs and the reason for any exposure conclusion. All present draft cases remain `MATCH_UNRESOLVED`, except the already documented developer-exposed page, which remains `KNOWN_EXPOSED`.

## CP2-05 — Provisional exclusion rule needs review (open)

Forty-five first anchors were provisionally screened out for nontechnical, expository, prospective-audit, glossary, copied-heading, or unrelated-causation reasons. The frozen protocol explicitly excludes some of those classes, but a normative administrative requirement is not automatically excluded merely because it is not a model-method clause. Revisit these cases against the exact panel eligibility rule before calling their exclusions final; never substitute a later page occurrence.

## CP2-05A — Panel B compound blocks (excluded under frozen rule)

The complete numbered S-5.1 item 12 and CI-4 Audit 6 each include multiple independent reviewer actions without numbered subitems. Along with the previously identified unnumbered multi-action group, these are recorded as `NOT_ADJUDICABLE_FOR_PANEL_B`. Their full text is retained in the original lead dossiers; no favorable sentence was isolated.

## CP2-06 — No scientific conclusion yet (standing boundary)

This checkpoint has not established natural-case gold, independent case counts, source-recovery performance, or Qwen semantic accuracy. No source-only failure or no-pair outcome should be described as fixed-corpus absence.
