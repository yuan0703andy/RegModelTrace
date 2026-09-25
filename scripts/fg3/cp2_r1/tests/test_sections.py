from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from cp2_r1.sections import section_candidates  # noqa: E402


def test_form_section_does_not_absorb_standard_with_same_number():
    pages = [
        "Standard A-5: This is not a Form heading.\nA-5 Hurricane Policy Conditions\n",
        "Form A‐5: Percentage Change in Hurricane Output Ranges\n\nC. Provide this form.\n",
        "Form A-6: Another Form\n",
    ]
    found = section_candidates(pages, "FORM:A-5")
    assert len(found) == 1
    assert found[0]["heading"]["physical_page"] == 2
    assert found[0]["end_boundary"]["physical_page"] == 3


def test_table_of_contents_page_number_does_not_become_heading():
    pages = [
        "Form A-5: Percentage Change 455\n",
        "Form A-5: Percentage Change\n\nC. Provide this form.\n",
        "Form A-6: Next form\n",
    ]
    found = section_candidates(pages, "FORM:A-5")
    assert len(found) == 1
    assert found[0]["heading"]["physical_page"] == 2


def test_appendix_form_section_replaces_see_appendix_pointer():
    pages = [
        "Form A-5: Percentage Change\nSee Appendix F.\n",
        "Appendix F – Form A-5: Percentage Change\nA. Automated scripts were used.\n",
        "Appendix G – Form A-6: Logical Relationship\n",
    ]
    found = section_candidates(pages, "FORM:A-5")
    assert len(found) == 1
    assert found[0]["heading"]["physical_page"] == 2
    assert found[0]["end_boundary"]["physical_page"] == 3
