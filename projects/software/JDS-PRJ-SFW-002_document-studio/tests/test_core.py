"""Unit + integration tests for the Studio core (no third-party deps).

Run from the project folder:  python3 tests/test_core.py
These cover the JDS-critical logic — numbering, registry append, template
instantiation, and end-to-end document creation against a temporary sandbox
repo — without touching the real repository.
"""

import os
import sys
import tempfile
from pathlib import Path

# Make the `studio` package importable when run directly.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from studio import numbering, registry, templates, creator, config  # noqa: E402


# --- numbering --------------------------------------------------------------

def test_build_prefix():
    assert numbering.build_prefix("PRO") == "JDS-PRO"
    assert numbering.build_prefix("RPT", domain="MEC") == "JDS-RPT-MEC"
    assert numbering.build_prefix("TMP", template_type="RPT") == "JDS-TMP-RPT"


def test_used_numbers_is_prefix_anchored():
    text = "JDS-RPT-001 and JDS-RPT-MEC-005 and JDS-RPT-MEC-011"
    # Bare RPT prefix must NOT swallow the RPT-MEC numbers.
    assert numbering.used_numbers("JDS-RPT", text, []) == {1}
    assert numbering.used_numbers("JDS-RPT-MEC", text, []) == {5, 11}


def test_next_number_and_format():
    text = "JDS-PRO-001 JDS-PRO-010"
    assert numbering.next_number("JDS-PRO", text, []) == 11
    assert numbering.next_number("JDS-DWG-MAR", "", []) == 1  # none used yet
    assert numbering.format_number("JDS-RPT-MEC", 5) == "JDS-RPT-MEC-005"


def test_next_number_counts_filenames_not_in_registry():
    # A file on disk that was never registered must still block its number.
    assert numbering.next_number("JDS-LOG-MEC", "", ["JDS-LOG-MEC-007_x.md"]) == 8


# --- registry ---------------------------------------------------------------

SAMPLE_REGISTRY = """# JDS Document Register

## Procedures (PRO)

| Doc No. | Title | Rev | Date | Status | Author |
|---------|-------|-----|------|--------|--------|
| [JDS-PRO-001](../procedures/JDS-PRO-001_a.md) | Doc A | A | 2026-01-01 | APPROVED | N. J. |
| [JDS-PRO-010](../procedures/JDS-PRO-010_b.md) | Doc B | B | 2026-01-02 | APPROVED | N. J. |

## Reports (RPT)

| Doc No. | Title | Rev | Date | Status | Author |
|---------|-------|-----|------|--------|--------|
| [JDS-RPT-001](../examples/JDS-RPT-001_c.md) | Doc C | A | 2026-01-03 | EXAMPLE | N. J. |
"""


def test_parse_entries():
    entries = registry.parse_entries(SAMPLE_REGISTRY)
    assert [e["doc_no"] for e in entries] == ["JDS-PRO-001", "JDS-PRO-010", "JDS-RPT-001"]
    assert entries[1]["rev"] == "B"
    assert entries[2]["status"] == "EXAMPLE"


def test_append_entry_inserts_under_correct_section():
    out = registry.append_entry(
        SAMPLE_REGISTRY, "PRO", "JDS-PRO-011", "../procedures/JDS-PRO-011_new.md",
        "New Proc", "A", "2026-06-26", "DRAFT", "N. J.",
    )
    lines = out.splitlines()
    pro_idx = lines.index("## Procedures (PRO)")
    rpt_idx = lines.index("## Reports (RPT)")
    new_line = next(i for i, l in enumerate(lines) if "JDS-PRO-011" in l)
    # The new row must sit inside the PRO section, after PRO-010, before RPT.
    assert pro_idx < new_line < rpt_idx
    assert "JDS-PRO-010" in lines[new_line - 1]


# --- templates --------------------------------------------------------------

SAMPLE_TEMPLATE = """# [Report Title]

| | |
|---|---|
| **Document No.** | JDS-RPT-[NNN] |
| **Revision** | DRAFT |
| **Date** | YYYY-MM-DD |
| **Status** | DRAFT |
| **Author** | [Author Name] |

## 1. Summary

[body stays untouched]
"""


def test_instantiate_fills_title_and_metadata():
    out = templates.instantiate(
        SAMPLE_TEMPLATE, title="Pump Test", doc_no="JDS-RPT-MEC-005",
        rev="A", date="2026-06-26", status="DRAFT", author="N. Johansson",
    )
    assert out.startswith("# Pump Test\n")
    assert "| **Document No.** | JDS-RPT-MEC-005 |" in out
    assert "| **Author** | N. Johansson |" in out
    assert "[body stays untouched]" in out          # body preserved
    assert "[Report Title]" not in out               # placeholder replaced


# --- creator (integration against a temp sandbox repo) ----------------------

def test_create_document_end_to_end():
    sandbox = Path(tempfile.mkdtemp(prefix="jds-studio-"))
    (sandbox / "jds" / "registry").mkdir(parents=True)
    (sandbox / "jds" / "procedures").mkdir(parents=True)
    (sandbox / "jds" / "templates" / "reports").mkdir(parents=True)
    (sandbox / "projects").mkdir(parents=True)
    (sandbox / "jds" / "registry" / "document-register.md").write_text(SAMPLE_REGISTRY)
    (sandbox / "jds" / "templates" / "reports" / "tmpl.md").write_text(SAMPLE_TEMPLATE)

    saved = (config.REPO_ROOT, config.REGISTRY_PATH, config.TEMPLATES_DIR)
    config.REPO_ROOT = sandbox
    config.REGISTRY_PATH = sandbox / "jds" / "registry" / "document-register.md"
    config.TEMPLATES_DIR = sandbox / "jds" / "templates"
    try:
        result = creator.create_document(
            template_rel_path="jds/templates/reports/tmpl.md",
            target_dir="jds/procedures",
            title="Inspection Routine",
            category="PRO",
            author="N. Johansson",
            date="2026-06-26",
        )
        assert result["doc_no"] == "JDS-PRO-011"          # next after 010
        new_file = sandbox / result["path"]
        assert new_file.exists()
        assert new_file.name == "JDS-PRO-011_inspection-routine.md"
        body = new_file.read_text()
        assert "# Inspection Routine" in body
        assert "| **Document No.** | JDS-PRO-011 |" in body
        # Registry updated with a row pointing at the new file.
        reg = config.REGISTRY_PATH.read_text()
        # Exactly one registry ROW for the new doc (the number appears twice per
        # row — in the link label and the file path — so count the link label).
        assert reg.count("[JDS-PRO-011]") == 1
        assert "JDS-PRO-011" in [e["doc_no"] for e in registry.parse_entries(reg)]
    finally:
        config.REPO_ROOT, config.REGISTRY_PATH, config.TEMPLATES_DIR = saved


def _sandbox():
    """Create a temp repo and point config at it. Returns (sandbox, saved)."""
    sandbox = Path(tempfile.mkdtemp(prefix="jds-studio-"))
    (sandbox / "jds" / "registry").mkdir(parents=True)
    (sandbox / "jds" / "templates" / "reports").mkdir(parents=True)
    (sandbox / "projects").mkdir(parents=True)
    (sandbox / "jds" / "registry" / "document-register.md").write_text(SAMPLE_REGISTRY)
    (sandbox / "jds" / "templates" / "reports" / "tmpl.md").write_text(SAMPLE_TEMPLATE)
    saved = (config.REPO_ROOT, config.REGISTRY_PATH, config.TEMPLATES_DIR)
    config.REPO_ROOT = sandbox
    config.REGISTRY_PATH = sandbox / "jds" / "registry" / "document-register.md"
    config.TEMPLATES_DIR = sandbox / "jds" / "templates"
    return sandbox, saved


def _raises(func):
    try:
        func()
    except ValueError:
        return True
    return False


def test_create_document_rejects_invalid_input():
    sandbox, saved = _sandbox()
    try:
        def call(**over):
            args = dict(template_rel_path="jds/templates/reports/tmpl.md",
                        target_dir="jds/procedures", title="Valid Title",
                        category="PRO", author="N. J.", date="2026-06-26")
            args.update(over)
            return lambda: creator.create_document(**args)

        assert _raises(call(title="   "))                  # empty title
        assert _raises(call(rev="I"))                      # I is not a JDS rev letter
        assert _raises(call(category="ZZZ"))               # unknown category
        assert _raises(call(domain="ZZZ"))                 # unknown domain
        assert _raises(call(status="BOGUS"))               # invalid status
        assert _raises(call(target_dir="../../etc"))       # path traversal blocked
    finally:
        config.REPO_ROOT, config.REGISTRY_PATH, config.TEMPLATES_DIR = saved


# --- runner -----------------------------------------------------------------

def _main():
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    failed = 0
    for test in tests:
        try:
            test()
            print(f"  PASS  {test.__name__}")
        except AssertionError as exc:
            failed += 1
            print(f"  FAIL  {test.__name__}: {exc}")
        except Exception as exc:  # noqa: BLE001
            failed += 1
            print(f"  ERROR {test.__name__}: {type(exc).__name__}: {exc}")
    print(f"\n{len(tests) - failed}/{len(tests)} passed")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(_main())
