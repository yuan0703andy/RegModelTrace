# FG-3 Checkpoint 2 source audit — not yet passed

This is a source-only progress record against the frozen FG-3 v1.3 protocols. It is **not** a natural-case truth freeze, an inference result, or permission to run Qwen. The frozen 1,708 discovery hits and 85 selected page leads have not been changed.

## Verified source custody

All six source PDFs used by the selected leads matched their frozen SHA-256 identities. All 85 leads were re-located at the frozen first-match anchor in layout-extracted physical-page text and confirmed in a second `pdftotext -raw` extraction. Source unit drafts exist for 37 leads; each exact extracted span has been checked against a fresh original-PDF extraction, and each draft contains its selected anchor. Standards physical page 227 and 2023 reviewer-report physical page 7 were also visually inspected. This verifies textual/source location for those checks; it is not a claim that every page was visually reviewed or that every natural-unit boundary is final.

The source screen records 45 `EXCLUDED_AT_FIXED_ANCHOR`, three `NOT_ADJUDICABLE_FOR_PANEL_B`, and 37 requiring full source-unit and pairing review (Panel A: 7; B: 1; C: 29). These are provisional case-formation decisions, not semantic labels. Three reviewer blocks contained multiple independent actions without numbered subitems; the selected anchor was not reduced to a convenient sentence.

The 36 Panel A/C search plans produced 30 first-tier literal match sets, three over the frozen 20-paragraph limit, and three with no usable source key. These are **literal hit sets**, not verified substantive counterparts. The extractor preserves all matched paragraphs and exact physical-page spans. Panel A's full matching vendor sections and Panel C's complete counterpart units still require source review; a table-of-contents hit or copied standard heading cannot be treated as a substantive pair. A no-pair or overflow result is only a bounded-protocol outcome, never absence from the fixed corpus.

The frozen 347-file known-exposure ledger was checksum-verified and searched for exact 12-token overlaps. One draft source unit and seven pairing-audit hit sets have at least one exact overlap candidate. Those matches require source-role and substantial-equivalence review. No exact match elsewhere is **not** exposure clearance. Accordingly, no case has been marked `NO_KNOWN_EXPOSURE_UNDER_FROZEN_LEDGER` or primary eligible.

## Corrections and procedural issue

The first source-unit builder used the first literal occurrence of an anchor phrase on a page. An independent normalized-offset check found two wrong boundaries. On standards physical page 227, the selected `all` is in Form A-5 subsection C, not B; the fixed unit and pairing key now use subsection C and A-5 only. On the 2023 reviewer report's physical page 7, the selected `no changes` belongs to numbered Audit 3's vulnerability-vintage discussion, not Audit 5's separate general model-change discussion. Both corrections preserve the originally selected page and anchor. The builder now maps the frozen normalized offset to the raw PDF page and fails if any draft unit misses that anchor.

Before writing the formal counterpart key file, a diagnostic counted selected standard identifiers in counterpart PDFs. Eighteen plans intersected those earlier counts. The later keys were derived from printed source identifiers, and no favorable passage was chosen, but the required **keys-before-search** chronology was not met for those plans. They are explicitly marked `primary_protocol_clean=false` in `pair_search_inputs.jsonl`; this deviation cannot be erased by rewriting the file. It requires a separate owner decision about use, and it is not a reason to relax or rerun frozen discovery.

## Checkpoint gate

`CHECKPOINT_2 = IN_PROGRESS / NOT_PASS`. The remaining source-only work is to verify final natural-unit boundaries and hierarchy, expand and review every first-tier counterpart set under the frozen rule, resolve exact/substantial exposure against the ledger for the complete paired units, and form dependency clusters. The 45 provisional screen exclusions also need a final rule-by-rule check where a normative administrative clause may have been rejected only because it is outside a technical-method topic. Until this work is recorded, there are zero primary eligible natural cases and no basis for a model-facing packet, human gold, or Qwen run.

The integrity check in `audit_integrity_verification.json` confirms counts, hashes, exact spans, and anchor inclusion. Its `AUDIT_INTEGRITY_VERIFIED_NOT_CHECKPOINT_PASS` status is intentional.
