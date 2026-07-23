#!/usr/bin/env python3
"""Fix the redundant/invisible year display in the Front-Row Seat reader.

1. Contents overview: merge the year into the (visible) kicker label line so
   each row reads "CHAPTER ONE · 1603", and drop the faint right-edge year span.
2. Chapter page: strip the redundant leading bold-year <p> from every epigraph
   (the grey metadata year under the title already carries it once; the
   attribution date is kept as a natural citation).

Operates in place on the bundle file passed as the argument.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

bundle_path = Path(sys.argv[1])
s = bundle_path.read_text(encoding="utf-8")

# --- Fix 1: overview kicker carries the year; remove the faint standalone span.
kicker_old = '{className:"toc-kicker",children:n.kicker}'
kicker_new = '{className:"toc-kicker",children:n.year?n.kicker+" · "+n.year:n.kicker}'
assert s.count(kicker_old) == 1, "toc-kicker anchor not unique"
s = s.replace(kicker_old, kicker_new, 1)

year_span = 'n.year&&w.jsx("span",{className:"toc-year",children:n.year}),'
assert s.count(year_span) == 1, "toc-year span not unique"
s = s.replace(year_span, "", 1)

# --- Fix 2: strip the leading bold-year <p> from every epigraph blockquote.
epi_pat = re.compile(
    r'(epigraph:`<blockquote>\n)<p><strong>[0-9]{4}(?:–[0-9]{4})?</strong></p>\n'
)
s, n_epi = epi_pat.subn(r"\1", s)

bundle_path.write_text(s, encoding="utf-8")
print(f"overview kicker merged: 1, faint year span removed: 1")
print(f"epigraph bold-year lines stripped: {n_epi}")
