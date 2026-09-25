from scripts.fg3.cp2_r1.freeze_source_keys import plan
from scripts.fg3.cp2_r1.typed_keys import keys_from_refs


def test_numbered_comment_target_keeps_hierarchical_subsection():
    ref = {"physical_page": 1, "start": 20, "text": "20. A-3.B, page 319: Provide a sample."}
    keys = keys_from_refs("review", [ref], None)
    assert keys[0]["normalized_key"] == "STANDARD:A-3.B"
    assert keys[0]["source_span"] == [24, 29]


def test_source_only_plan_does_not_use_counterpart_or_invent_tier_four():
    unit = {
        "lead_id": "L1",
        "unit_id": "U1",
        "document_id": "vendor",
        "boundary_verification": "CANONICAL_SOURCE_UNIT",
        "source_refs": [{"physical_page": 2, "start": 10, "text": "No changes were made."}],
        "parent_heading_source_ref": {
            "physical_page": 2,
            "start": 0,
            "text": "Notional Set 1 – Deductible Sensitivity",
        },
    }
    result = plan(unit, {"panel": "C", "standards_cycle": 2023}, set())
    assert result["tiers"]["tier1"] == []
    assert result["tiers"]["tier3"][0]["key_text"] == "Notional Set 1 – Deductible Sensitivity"
    assert result["tiers"]["tier4"] == []
    assert result["counterpart_search_executed"] is False
