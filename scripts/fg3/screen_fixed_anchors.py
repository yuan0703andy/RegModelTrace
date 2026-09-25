import json
from collections import Counter
from pathlib import Path

base = Path("experiments/fg3_natural_boundary/checkpoint2")
rows = [json.loads(x) for x in (base / "lead_source_dossiers.jsonl").read_text().splitlines()]
# Decisions concern only the fixed first anchor, never another occurrence on its page.
ex = {
    # A: historical/expository/procedure/glossary or future audit text, not a bounded model-evidence comparison.
    "FG3L_4a5a33cd74efdefb": 'Historical standards-process narrative; anchor is "required" in a statutory-history description.',
    "FG3L_4997199034f402f3": "Sunshine Law public-meeting rule rather than a vendor model requirement.",
    "FG3L_f1a1f3aa3e410c17": "Expository definition of stochastic forecasting, not a prescriptive vendor-facing clause at the anchor.",
    "FG3L_9b81ac232333a6cb": "Commission presentation procedure; the selected anchor begins in a page-continuation of meeting-medium instructions.",
    "FG3L_ac6bb57d3b40ccbe": "On-site-review material presentation procedure, not a model-method requirement.",
    "FG3L_9e2b88445f49ed0b": "The fixed anchor is in a Purpose explanation, not the adjacent normative clauses.",
    "FG3L_7ba06bd16989103d": 'The anchor is in prospective Audit language ("will be reviewed"), not an implementation requirement.',
    "FG3L_84227cde3c689718": "The anchor is in prospective Audit language, not an implementation requirement.",
    "FG3L_a764920236f75faa": "Glossary definition of insurance to value; no bounded vendor implementation proposition at the anchor.",
    "FG3L_ef3c9a4844c54911": "Glossary definition of modular-home permitting; no bounded vendor model requirement at the anchor.",
    "FG3L_79ee87ff07b17fe6": "Glossary definition of standard flood insurance; no bounded vendor implementation proposition at the anchor.",
    "FG3L_f3c86c02277d64f7": "Commission committee procedure rather than a vendor-facing model requirement.",
    "FG3L_8aadd919b3b0d268": "Expository definition of Commission role, not a vendor implementation clause.",
    "FG3L_c62f1a244637491a": "Commission action-plan procedure rather than model-method requirement.",
    "FG3L_42d833daa5f78bbf": "Prewritten interim-update certification template statement, not a documented vendor implementation at the anchor.",
    "FG3L_af199d540a0a9e98": "Pre-review conference-call procedure, not a vendor model requirement.",
    "FG3L_4ec3103613af52bb": "Pre-visit materials checklist rather than bounded technical model requirement.",
    "FG3L_9700d81c1027238b": "Computer-terminology glossary definition, not a prescriptive vendor-facing clause.",
    "FG3L_97c78a1fb48c4283": "Flood glossary definition of an enclosure condition, not a bounded hurricane-model requirement.",
    "FG3L_36fb1e7983de58fe": "Flood insurance glossary definition, not a bounded hurricane-model requirement.",
    "FG3L_2dd4438dc43cbcc9": "Statutory appendix text about appointments, not a model requirement.",
    "FG3L_4de175e3e5fe7db9": "Statutory appendix text about roof deductible claims payments, not a model requirement.",
    # B: fixed anchor in procedure, copied requirement/header, or prospective audit rather than observed action.
    "FG3L_e2b3177c15765dc7": "Conditional pre-review logistics (conference if requested by FIU), not a completed reviewer challenge.",
    "FG3L_0e8330a5f34879f7": 'The first anchor is the copied standard header "Significant Revision", not a reviewer action.',
    "FG3L_201b63c0942da0fc": 'The first anchor is the copied standard header "Significant Revision", not a reviewer action.',
    "FG3L_26b1342fe7ed6b63": 'The first anchor is prospective Audit text ("will be reviewed"), not the later actual Team comment.',
    "FG3L_0dcba6735531cbdc": "The first anchor is prospective Audit text, not actual completed scrutiny.",
    "FG3L_a18cdadc1128d143": "The first anchor is prospective Audit text, not actual completed scrutiny.",
    "FG3L_cad3b26dd932ab3c": 'The first anchor is copied S-3 standard header "Significant Revision".',
    "FG3L_16445ad3af7bd178": 'The first anchor is copied V-1 standard header "Significant Revision".',
    "FG3L_4e7944dd9390ada0": 'The first anchor is prospective Audit text ("will be reviewed"), not the subsequent discussion.',
    "FG3L_d916e532fceaf0e6": 'The first anchor is copied CI-1 standard header "Significant Revision".',
    "FG3L_a437b47c3629a7a3": 'The first anchor is copied CI-5 standard header "Significant Revision".',
    # C: fixed anchor is a header/template/citation or a physical/business causal phrase unrelated to reviewer intervention.
    "FG3L_5eeb04549c55d02f": "General pre-visit process for responses to deficiencies; no specific model object to pair.",
    "FG3L_4b503411f4b6a7fd": "Future audit of submission-document modification history, not a review-linked model modification.",
    "FG3L_e9eef62e8cc7b72f": 'Copied M-4 standard header "Significant Revision".',
    "FG3L_a40b96fe3f50ebe1": '"As a result of" links storm damage to water ingress, not review to model modification.',
    "FG3L_5b1dd7be3567bdde": 'Bibliographic title "Modification of mean flow" (1969), not a vendor revision claim.',
    "FG3L_ed33cfe02acec50f": '"As a result of" links debris impact to opening failure, not review to model modification.',
    "FG3L_b294840cc1a6e50a": 'Form A-7 title "Percentage Change" rather than a substantive revision statement.',
    "FG3L_58568ba031dfc64f": 'Copied M-4 standard header "Significant Revision".',
    "FG3L_51ace481aec8204b": 'Copied CI-5 standard header "Significant Revision".',
    "FG3L_13801f0cf6153905": "Historical building-code map boundary change, not a current vendor model modification.",
    "FG3L_05b3aef005e5f07c": "Copied disclosure prompt about climate change followed by Not Applicable, not a vendor revision claim.",
    "FG3L_c6d87bf0d6b18c79": "Historical building-code enforcement explanation, not review-linked model change.",
}
# B page 9: copied "Verified" disposition controls a long unnumbered group of independent acts.
amb = {
    "FG3L_159d18d1a52a191a": "The first anchor is Verified YES preceding multiple independent unnumbered Team comments on different objects; the frozen rule does not permit selecting one favorable action.",
    "FG3L_a67170a73a9dc42c": "Numbered S-5.1 item 12 contains several independent Team actions (Table 14 correction, claims-data exclusion, loss comparisons, scatter plots) without numbered subitems; the frozen Panel B compound-block rule forbids selecting one.",
    "FG3L_e167ff03e7759c00": "Numbered CI-4 Audit 6 contains separate code-count reviews for storm-track generator and vulnerability matrix without numbered subitems; the frozen Panel B compound-block rule forbids selecting one.",
}
assert set(ex).isdisjoint(amb)
assert set(ex | amb).issubset({r["lead_id"] for r in rows})
out = []
for x in rows:
    lid = x["lead_id"]
    if lid in ex:
        status = "EXCLUDED_AT_FIXED_ANCHOR"
        reason = ex[lid]
    elif lid in amb:
        status = "NOT_ADJUDICABLE_FOR_PANEL_B"
        reason = amb[lid]
    else:
        status = "SOURCE_UNIT_AND_PAIRING_REVIEW_REQUIRED"
        reason = "First anchor is a potentially substantive source unit; complete source-unit boundary and frozen counterpart rule still require review."
    exposure = "KNOWN_EXPOSED" if x["prior_manual_page_touch"] else "MATCH_UNRESOLVED"
    out.append(
        {
            "lead_id": lid,
            "panel": x["panel"],
            "document_id": x["document_id"],
            "physical_page": x["physical_page"],
            "anchor_query_id": x["anchor_query_id"],
            "anchor_text": x["anchor_text"],
            "source_pdf_sha256_verified": True,
            "raw_mode_anchor_check": "RAW_MODE_ANCHOR_FOUND",
            "source_context_screening_status": status,
            "source_context_rationale": reason,
            "exposure_precheck_status": exposure,
            "exposure_exact_window_candidate_files": [
                m["file_path"] for m in x["exact_window_exposure_candidates"]
            ],
            "exposure_precheck_limitation": "Unmatched exact-window search is not known-exposure clearance; full clause and counterpart equivalence checks pending.",
            "case_id": None,
            "pairing_status": "NOT_REACHED"
            if status != "SOURCE_UNIT_AND_PAIRING_REVIEW_REQUIRED"
            else "PENDING",
            "human_gold": None,
        }
    )
(base / "lead_screening.jsonl").write_text(
    "".join(json.dumps(r, ensure_ascii=False, sort_keys=True) + "\n" for r in out)
)
print(
    Counter(r["source_context_screening_status"] for r in out),
    Counter(
        r["panel"]
        for r in out
        if r["source_context_screening_status"] == "SOURCE_UNIT_AND_PAIRING_REVIEW_REQUIRED"
    ),
)
