#!/usr/bin/env python3
"""Final assembly entrypoint for the protected Venture natural revision.

Extends `assemble_venture_natural.py` with prose replacements that were completed after the
first deterministic assembler was committed. Keeping this wrapper small makes the editorial
selection explicit without duplicating the base assembly logic.
"""
from __future__ import annotations

import importlib.util
from pathlib import Path

HERE = Path(__file__).resolve().parent
BASE_PATH = HERE / "assemble_venture_natural.py"

spec = importlib.util.spec_from_file_location("venture_base_assembler", BASE_PATH)
if spec is None or spec.loader is None:
    raise RuntimeError("Unable to load base Venture assembler")
base = importlib.util.module_from_spec(spec)
spec.loader.exec_module(base)

_original_prepare = base.prepare


def prepare(label: str, path: Path) -> str:
    doc = _original_prepare(label, path)
    if label == "Chapter Five":
        replacement = base.strip_scaffolding(
            base.read(base.ME / "11-1613-pay-table-section-iii-natural-compression.md")
        )
        doc = base.replace_section(doc, "## III. The Voice", replacement)
        # The replacement keeps the same section number, but normalise defensively.
        doc = base.renumber_sections(doc)
    return doc


base.prepare = prepare

if __name__ == "__main__":
    base.main()
