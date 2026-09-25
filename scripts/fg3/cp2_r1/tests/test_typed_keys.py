from __future__ import annotations

import importlib.util
from pathlib import Path


MODULE = Path(__file__).resolve().parents[1] / "typed_keys.py"
spec = importlib.util.spec_from_file_location("cp2_r1_keys", MODULE)
assert spec and spec.loader
keys = importlib.util.module_from_spec(spec)
spec.loader.exec_module(keys)


def test_form_and_standard_are_distinct_with_unicode_hyphen():
    ref = {
        "physical_page": 1,
        "start": 0,
        "end": 50,
        "text": "Form A‐5 and Standard A-5 are separate sources.",
    }
    found = keys.keys_from_refs("doc", [ref], None)
    assert {key["normalized_key"] for key in found} == {"FORM:A-5", "STANDARD:A-5"}
    assert all(key["source_span"][1] > key["source_span"][0] for key in found)


def test_bare_identifier_in_body_is_not_a_key():
    ref = {"physical_page": 1, "start": 0, "end": 30, "text": "V-1 figures were updated."}
    assert keys.keys_from_refs("doc", [ref], None) == []


def test_bare_parent_heading_requires_explicit_heading_family():
    parent = {"physical_page": 1, "start": 0, "end": 28, "text": "V-1 Development of Functions"}
    assert keys.keys_from_refs("doc", [], parent) == []
    parent["heading_family"] = "STANDARD"
    found = keys.keys_from_refs("doc", [], parent)
    assert found[0]["normalized_key"] == "STANDARD:V-1"
