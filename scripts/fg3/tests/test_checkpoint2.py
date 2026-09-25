"""Regression checks for fixed-anchor source custody."""

from __future__ import annotations

import importlib.util
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "build_checkpoint2_source_units.py"
spec = importlib.util.spec_from_file_location("fg3_units", SCRIPT)
assert spec and spec.loader
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def test_normalized_anchor_maps_across_line_break():
    page = "Header\n\n3. No\n   changes have been made.\n\n5. No changes to the model."
    normalized = " ".join(page.split()).casefold()
    offset = normalized.index("no changes")
    raw_offset = module.normalized_anchor_to_raw(page, offset)
    assert page[raw_offset : raw_offset + 2] == "No"
    first_unit_start = page.index("3. No")
    first_unit_end = page.index("5. No")
    assert first_unit_start <= raw_offset < first_unit_end


def test_later_occurrence_is_not_replaced_by_first_literal():
    page = "A. All changes combined.\n\nC. Also include all tables in Form A-5."
    normalized = " ".join(page.split()).casefold()
    offset = normalized.index("all tables")
    raw_offset = module.normalized_anchor_to_raw(page, offset)
    assert raw_offset == page.rindex("all")
    assert raw_offset > page.index("C. Also")
