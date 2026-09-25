from scripts.fg3.cp2_r1.pair_panel_c_explicit_units import candidate_records, typed_id_occurrences


def test_heading_does_not_expand_to_every_child_paragraph():
    pages = [
        "G-1 Scope of the Hurricane Model\n\n"
        "The model has a stochastic storm generator.\n\n"
        "The process described in Standard G-1 was updated.\n\n"
        "This unrelated paragraph remains in the same section.\n",
    ]
    matches, rejected = candidate_records(pages, "florida_public_2023_fphlm_submission", "sha", {"STANDARD:G-1"})
    assert len(matches) == 1
    assert rejected == []
    assert matches[0]["text"] == "The process described in Standard G-1 was updated."
    assert matches[0]["identifier_source_ref"]["text"] == "Standard G-1"


def test_form_and_standard_remain_separate_with_unicode_dash():
    pages = ["Form A‐5 describes a result.\n\nStandard A-5 requires a different thing.\n"]
    matches, _ = candidate_records(pages, "florida_public_2023_fphlm_submission", "sha", {"FORM:A-5"})
    assert len(matches) == 1
    assert matches[0]["text"] == "Form A‐5 describes a result."


def test_bare_numbered_target_is_typed_only_in_review_comment():
    text = "20. A-3.B, page 319: Explain the calculation."
    reviewer = typed_id_occurrences(text, True)
    vendor = typed_id_occurrences(text, False)
    assert [x["normalized_key"] for x in reviewer] == ["STANDARD:A-3.B"]
    assert vendor == []


def test_toc_match_is_retained_as_rejected_not_a_tier_one_unit():
    pages = [
        "Table of Contents\nForm M-1 ........ 3\nForm M-2 ........ 5\nForm M-3 ........ 7\n",
        "A substantive discussion cites Form M-1.\n",
    ]
    matches, rejected = candidate_records(pages, "florida_public_2023_fphlm_submission", "sha", {"FORM:M-1"})
    assert len(matches) == 1
    assert len(rejected) == 1
    assert rejected[0]["rejection_reason"] == "TABLE_OF_CONTENTS_PAGE"
