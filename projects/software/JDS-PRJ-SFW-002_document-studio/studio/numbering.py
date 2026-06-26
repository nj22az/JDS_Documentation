"""Next-free JDS document number resolution.

A JDS number is a fixed prefix followed by a zero-padded sequential part, e.g.
``JDS-PRO-011`` (prefix ``JDS-PRO``) or ``JDS-RPT-MEC-005`` (prefix
``JDS-RPT-MEC``). To pick the next free number we look at BOTH the registry and
the files on disk, so a number is never reused even if a file was added without
being registered yet. The validator's duplicate-number check (CA-2026-008) is
the backstop that guarantees this stayed correct.
"""

import re

from . import config


def build_prefix(category, domain=None, template_type=None):
    """Assemble the number prefix from its parts.

    Examples:
        build_prefix("PRO")                  -> "JDS-PRO"
        build_prefix("RPT", domain="MEC")    -> "JDS-RPT-MEC"
        build_prefix("TMP", template_type="RPT") -> "JDS-TMP-RPT"
    """
    parts = ["JDS", category]
    if template_type:
        parts.append(template_type)
    if domain:
        parts.append(domain)
    return "-".join(parts)


def used_numbers(prefix, registry_text, filenames):
    """Return the set of sequential integers already taken for `prefix`.

    `registry_text` is the raw register markdown; `filenames` is an iterable of
    file basenames to scan. Matching is anchored so that prefix ``JDS-RPT`` does
    not accidentally swallow ``JDS-RPT-MEC`` numbers (the part after the number
    must not be another ``-XXX`` segment)."""
    # The sequential part, then a boundary that is not a continuation of the number.
    pattern = re.compile(
        re.escape(prefix) + r"-(\d{%d})(?![\dA-Za-z-])" % config.NUMBER_WIDTH
    )
    taken = set()
    for source in (registry_text or "", "\n".join(filenames)):
        for match in pattern.finditer(source):
            taken.add(int(match.group(1)))
    return taken


def next_number(prefix, registry_text, filenames):
    """Return the next free sequential integer for `prefix` (1 if none used)."""
    taken = used_numbers(prefix, registry_text, filenames)
    return max(taken) + 1 if taken else 1


def format_number(prefix, sequential):
    """Render a full JDS number, e.g. ("JDS-RPT-MEC", 5) -> "JDS-RPT-MEC-005"."""
    return f"{prefix}-{sequential:0{config.NUMBER_WIDTH}d}"
