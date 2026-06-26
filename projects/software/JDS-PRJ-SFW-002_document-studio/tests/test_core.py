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

from studio import (numbering, registry, templates, creator, placement,  # noqa: E402
                    revision, editor, doctor, config)


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


# --- placement --------------------------------------------------------------

def test_suggest_target_dir():
    assert placement.suggest_target_dir("PRO") == "jds/procedures"
    assert placement.suggest_target_dir("QMS") == "jds/quality-manual"
    assert placement.suggest_target_dir("TMP", template_type="RPT") == "jds/templates/reports"
    assert placement.suggest_target_dir("TMP", template_type="LOG") == "jds/templates/logs"
    assert placement.suggest_target_dir("TMP") == "jds/templates"   # type unknown
    assert placement.suggest_target_dir("RPT") == ""                # not confident


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


# --- revision & editor ------------------------------------------------------

DOC_SAMPLE = """# Sample Procedure

| | |
|---|---|
| **Document No.** | JDS-PRO-001 |
| **Revision** | A |
| **Date** | 2026-01-01 |
| **Status** | APPROVED |
| **Author** | N. J. |

---

Body text.

## Revision History

| Rev | Date | Author | Description |
|-----|------|--------|-------------|
| A | 2026-01-01 | N. J. | Initial |
"""


def test_next_revision_skips_ambiguous_letters():
    assert revision.next_revision("DRAFT") == "A"
    assert revision.next_revision("") == "A"
    assert revision.next_revision("A") == "B"
    assert revision.next_revision("H") == "J"      # skips I
    assert revision.next_revision("N") == "P"      # skips O
    assert _raises(lambda: revision.next_revision("Y"))   # sequence exhausted
    assert _raises(lambda: revision.next_revision("I"))   # not a valid letter


def test_registry_update_entry():
    out = registry.update_entry(SAMPLE_REGISTRY, "JDS-PRO-010", rev="C",
                                date="2026-06-26", status="CURRENT")
    row = next(l for l in out.splitlines() if "JDS-PRO-010" in l)
    assert "| C |" in row and "2026-06-26" in row and "CURRENT" in row
    assert "Doc B" in row              # title preserved
    assert _raises(lambda: registry.update_entry(SAMPLE_REGISTRY, "JDS-PRO-999"))


def test_revise_document_end_to_end():
    sandbox, saved = _sandbox()
    (sandbox / "jds" / "procedures").mkdir(parents=True)
    doc = sandbox / "jds" / "procedures" / "JDS-PRO-001_a.md"
    doc.write_text(DOC_SAMPLE)
    try:
        result = editor.revise_document(
            "jds/procedures/JDS-PRO-001_a.md",
            author="N. Johansson", description="Clarified scope", date="2026-06-26")
        assert result["new_rev"] == "B"
        text = doc.read_text()
        assert "| **Revision** | B |" in text
        assert "| **Date** | 2026-06-26 |" in text
        assert text.count("| B | 2026-06-26 | N. Johansson | Clarified scope |") == 1
        # Register row for JDS-PRO-001 now reads Rev B.
        reg = config.REGISTRY_PATH.read_text()
        pro1 = next(l for l in reg.splitlines() if "[JDS-PRO-001]" in l)
        assert "| B |" in pro1 and "2026-06-26" in pro1
        # A revision requires a description.
        assert _raises(lambda: editor.revise_document(
            "jds/procedures/JDS-PRO-001_a.md", author="x", description=" "))
    finally:
        config.REPO_ROOT, config.REGISTRY_PATH, config.TEMPLATES_DIR = saved


def test_revise_blocks_path_escape():
    sandbox, saved = _sandbox()
    try:
        assert _raises(lambda: editor.read_document("../../etc/passwd"))
    finally:
        config.REPO_ROOT, config.REGISTRY_PATH, config.TEMPLATES_DIR = saved


def test_doctor_check_reports_known_dependencies():
    report = doctor.check()
    assert "weasyprint" in report and "fastapi" in report
    for info in report.values():
        assert set(info) == {"present", "purpose", "package"}


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
