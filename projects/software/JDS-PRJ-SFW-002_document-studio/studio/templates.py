"""Template discovery and instantiation.

Studio never invents document layout — it reuses the blank templates in
``jds/templates/``. Instantiation fills the metadata block (Document No.,
Revision, Date, Status, Author) and the H1 title, leaving the body for the
author to complete. Only the metadata cells are rewritten, so the template's
content and structure pass through untouched.
"""

import re
from pathlib import Path

from . import config

# A metadata row in a template: | **Field** | value |
META_ROW_RE = re.compile(r"^\|\s*\*\*(?P<label>[^*]+?)\*\*\s*\|\s*(?P<value>.*?)\s*\|\s*$")

# Labels Studio fills in, mapped to the field name supplied by the caller.
META_FIELDS = {
    "Document No.": "doc_no",
    "Revision": "rev",
    "Date": "date",
    "Status": "status",
    "Author": "author",
}


def list_templates(templates_dir=None):
    """Return a sorted list of available templates as dicts.

    Each entry: {number, title, type, path} where `path` is relative to the
    repo root and `type` is the sub-folder (reports, logs, ...).
    """
    root = Path(templates_dir or config.TEMPLATES_DIR)
    found = []
    for path in sorted(root.rglob("*.md")):
        text = path.read_text(encoding="utf-8")
        found.append({
            "number": _first_number(path.name),
            "title": _first_heading(text) or path.stem,
            "type": path.parent.name,
            "path": str(path.relative_to(config.REPO_ROOT)),
        })
    return found


def _first_heading(text):
    for line in text.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return None


def _first_number(name):
    match = re.search(r"JDS-[A-Z]{3}(?:-[A-Z]{3})?-\d{3}", name)
    return match.group(0) if match else name


def instantiate(template_text, *, title, doc_no, rev, date, status, author):
    """Return document markdown with the H1 title and metadata block filled in."""
    values = {
        "doc_no": doc_no, "rev": rev, "date": date,
        "status": status, "author": author,
    }
    out_lines = []
    title_done = False
    for line in template_text.splitlines():
        if not title_done and line.startswith("# "):
            out_lines.append(f"# {title}")
            title_done = True
            continue
        meta = META_ROW_RE.match(line)
        if meta and meta.group("label") in META_FIELDS:
            field = META_FIELDS[meta.group("label")]
            out_lines.append(f"| **{meta.group('label')}** | {values[field]} |")
            continue
        out_lines.append(line)
    return "\n".join(out_lines) + "\n"
