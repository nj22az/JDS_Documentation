"""Document creation orchestration — the heart of Studio.

Ties together numbering, templates, and the registry to perform the one action
the app exists for: turn a blank template into a numbered, registered JDS
document on disk. Pure with respect to side effects except the two writes at the
end (the new document file and the appended registry row).
"""

import os
import re
from pathlib import Path

from . import config, numbering, registry, templates


def slugify(title):
    """Turn a title into a filename-safe slug, e.g. 'Pump Test' -> 'pump-test'."""
    slug = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")
    return slug or "document"


def _scan_filenames():
    """All JDS markdown basenames on disk (registry-independent collision guard)."""
    names = []
    for sub in ("jds", "projects"):
        for path in (config.REPO_ROOT / sub).rglob("*.md"):
            names.append(path.name)
    return names


def preview_number(category, domain=None, template_type=None, registry_text=None):
    """Compute the next free doc number without writing anything."""
    prefix = numbering.build_prefix(category, domain, template_type)
    text = registry_text if registry_text is not None else registry.read_text()
    seq = numbering.next_number(prefix, text, _scan_filenames())
    return numbering.format_number(prefix, seq)


def create_document(*, template_rel_path, target_dir, title, category,
                    author, domain=None, template_type=None, status="DRAFT",
                    rev="A", date=None):
    """Create a numbered, registered document. Returns a summary dict.

    `target_dir` is relative to the repo root (e.g. 'jds/procedures'). The
    registry link is stored relative to the registry file, matching existing rows.
    """
    if category not in config.CATEGORY_SECTIONS:
        raise ValueError(f"Unknown category '{category}'")
    if domain and domain not in config.DOMAIN_CODES:
        raise ValueError(f"Unknown domain '{domain}'")
    if status not in config.VALID_STATUSES:
        raise ValueError(f"Invalid status '{status}'")
    date = date or _today()

    registry_text = registry.read_text()
    doc_no = preview_number(category, domain, template_type, registry_text)

    # Build the document body from the template.
    template_text = (config.REPO_ROOT / template_rel_path).read_text(encoding="utf-8")
    body = templates.instantiate(
        template_text, title=title, doc_no=doc_no, rev=rev,
        date=date, status=status, author=author,
    )

    # Write the new file.
    filename = f"{doc_no}_{slugify(title)}.md"
    abs_dir = config.REPO_ROOT / target_dir
    abs_dir.mkdir(parents=True, exist_ok=True)
    abs_path = abs_dir / filename
    if abs_path.exists():
        raise FileExistsError(f"{abs_path} already exists")
    abs_path.write_text(body, encoding="utf-8")

    # Append the registry row (link relative to the registry file location).
    rel_for_registry = os.path.relpath(abs_path, config.REGISTRY_PATH.parent)
    new_registry = registry.append_entry(
        registry_text, category, doc_no, rel_for_registry, title,
        rev, date, status, author,
    )
    registry.write_text(new_registry)

    return {
        "doc_no": doc_no,
        "path": str(abs_path.relative_to(config.REPO_ROOT)),
        "registry_link": rel_for_registry,
    }


def _today():
    """ISO date string. Isolated so tests can monkeypatch it deterministically."""
    from datetime import date as _date
    return _date.today().isoformat()
