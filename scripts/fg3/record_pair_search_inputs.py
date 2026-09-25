import json
from pathlib import Path

base = Path("experiments/fg3_natural_boundary/checkpoint2")
unit = {x["lead_id"]: x for x in map(json.loads, (base / "source_unit_drafts.jsonl").open())}
# Literal identifiers are from the fixed anchor unit or its printed parent heading.
# No key is chosen on the basis of a desired Panel A/C label.
keys = {
    "FG3L_790bc4c0e7c53a42": [],
    "FG3L_d92901032170e6ad": ["G-1"],
    "FG3L_8d73174a11ec3837": ["G-5"],
    "FG3L_38d49e13a06daf85": ["A-5"],
    "FG3L_890ac5146ded6275": [],
    "FG3L_8c88e4e755a7923c": ["G-2"],
    "FG3L_6b4af3d3e7ae2478": ["A-6"],
    "FG3L_4ed6206247fe6d31": ["G-1.2"],
    "FG3L_6c1ee859ddc2b2fa": ["G-3"],
    "FG3L_886b02414646aaef": ["A-1.5", "A-1"],
    "FG3L_cd52022a16054dc1": ["CI-5"],
    "FG3L_036eb6d3e6f0d413": ["CI-7"],
    "FG3L_464684973341bd4c": ["G-1"],
    "FG3L_be8884cc2a6294ac": ["M-2"],
    "FG3L_e79a0b1ba83930cf": ["M-6"],
    "FG3L_0c164dcb3d119057": ["M-6", "G-1.2"],
    "FG3L_3ba2fe6c757519f4": ["S-2", "S-6"],
    "FG3L_44b259effabc1f58": ["S-3"],
    "FG3L_18d2fb07596f74f1": ["V-2"],
    "FG3L_3b5f0d649c860649": ["A-1"],
    "FG3L_936344c65a94bee4": ["CI-5"],
    "FG3L_199e296b691cc21d": ["G-1"],
    "FG3L_3be8237cdfa15ed2": ["M-3", "M-1"],
    "FG3L_e2057e9306160d6c": ["M-4"],
    "FG3L_5ad54c3b24878917": ["M-6"],
    "FG3L_a53b716eb384ff7c": ["V-1"],
    "FG3L_6f53a0cfedaf6849": ["A-3"],
    "FG3L_086fc7cf20367b5b": ["A-5"],
    "FG3L_6b2c31c560c4164d": ["M-2"],
    "FG3L_e851f5e0cc9cb428": ["M-3"],
    "FG3L_9abdab4658738f64": ["S-2"],
    "FG3L_3ae09c36fb37f2e7": ["V-1"],
    "FG3L_6cdb30a54d7fbce5": ["A-1", "A-2"],
    "FG3L_a1c2811f877b0acd": [],
    "FG3L_1284d77ca859d9fd": ["V-1"],
    "FG3L_de59a1b8a204553a": ["V-4", "V-2"],
}
assert set(keys) == {k for k, v in unit.items() if v["panel"] in ("A", "C")}
queried_before_record = {
    (2021, "REVIEWER"): set("G-1.2 G-1.7 S-6 CI-5 CI-7 A-1.5 V-2 M-4".split()),
    (2023, "REVIEWER"): set("M-3 M-4 V-1 A-3 A-5 CI-5 G-1.2".split()),
    (2021, "VENDOR"): set("G-1.2 G-1.7 S-6 V-2 CI-5 A-7".split()),
    (2023, "VENDOR"): set("M-2 S-1.2 V-1 V-4 A-2 A-6 S-6".split()),
}
rows = []
for lid in sorted(keys):
    u = unit[lid]
    other = (
        "VENDOR"
        if u["document_role"] == "REGULATOR" or u["document_role"] == "REVIEWER"
        else "REVIEWER"
    )
    impacted = sorted(
        set(keys[lid])
        & queried_before_record.get((u["standards_cycle"], u["document_role"]), set())
    )
    rows.append(
        {
            "lead_id": lid,
            "source_unit_id": u["source_unit_id"],
            "panel": u["panel"],
            "cycle": u["standards_cycle"],
            "anchor_document_id": u["document_id"],
            "counterpart_role": other,
            "tier1_literal_identifiers": keys[lid],
            "tier1_key_basis": "Printed identifier in fixed unit or parent standard/form heading; no semantic synonym",
            "tier2_exact_heading": None,
            "tier3_explicit_name": None,
            "tier4_literal_phrases": [],
            "input_status": "RECORDED_AFTER_EARLIER_DIAGNOSTIC_ID_COUNTS"
            if impacted
            else "RECORDED_BEFORE_THIS_COUNTERPART_SEARCH",
            "presearch_count_exposure_ids": impacted,
            "primary_protocol_clean": not bool(impacted),
        }
    )
(base / "pair_search_inputs.jsonl").write_text(
    "".join(json.dumps(r, sort_keys=True) + "\n" for r in rows)
)
print("plans", len(rows), "with IDs", sum(bool(r["tier1_literal_identifiers"]) for r in rows))
