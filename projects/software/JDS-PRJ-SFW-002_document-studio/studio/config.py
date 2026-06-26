"""Central configuration for JDS Document Studio.

Every constant the app relies on lives here (JDS-PRO-004 §3: no hardcoded values
scattered through logic). Paths are derived from the repository root, which is
discovered by walking up from this file until the JDS markers are found, so the
app keeps working if the repo is moved or cloned elsewhere.
"""

import os
import re
from pathlib import Path

# --- Repository discovery ---------------------------------------------------

# Markers that identify the JDS repository root (both must exist).
ROOT_MARKERS = ("jds", "scripts")


def find_repo_root(start=None):
    """Walk upward from `start` (or this file) until a directory holding all
    ROOT_MARKERS is found. Falls back to the env override JDS_REPO_ROOT."""
    override = os.environ.get("JDS_REPO_ROOT")
    if override:
        return Path(override).resolve()
    here = Path(start or __file__).resolve()
    for candidate in (here, *here.parents):
        if all((candidate / marker).is_dir() for marker in ROOT_MARKERS):
            return candidate
    raise RuntimeError(
        "Could not locate the JDS repository root (no parent has both "
        f"{ROOT_MARKERS}). Set JDS_REPO_ROOT to point at it."
    )


REPO_ROOT = find_repo_root()


def resolve_in_repo(rel_path):
    """Resolve a repo-relative path, refusing anything that escapes the repo.

    The single guard used everywhere Studio touches the filesystem (PRO-012 §5.3
    — prevent the invalid action). Reads REPO_ROOT at call time so tests can
    repoint it at a sandbox."""
    target = (REPO_ROOT / rel_path).resolve()
    if not target.is_relative_to(REPO_ROOT.resolve()):
        raise ValueError("path must stay inside the repository")
    return target


def today_iso():
    """Today's date as YYYY-MM-DD. One definition, shared by creator + editor."""
    from datetime import date
    return date.today().isoformat()


# Canonical JDS document-number pattern — defined once (JDS-PRO-004 §6) and
# imported wherever a number is matched, instead of re-spelling the regex.
DOC_NUMBER_RE = re.compile(r"JDS-[A-Z]{3}(?:-[A-Z]{3})?-\d{3}")
JDS_DIR = REPO_ROOT / "jds"
SCRIPTS_DIR = REPO_ROOT / "scripts"
TEMPLATES_DIR = JDS_DIR / "templates"
REGISTRY_PATH = JDS_DIR / "registry" / "document-register.md"

# --- JDS scripts the engine drives (single source of truth, never reimplemented) ---

VALIDATOR_SCRIPT = SCRIPTS_DIR / "jds-validate.py"
MD2PDF_SCRIPT = SCRIPTS_DIR / "md2pdf.py"
OFFICE_SCRIPT = SCRIPTS_DIR / "generate-office-docs.py"
CLASSIFY_SCRIPT = SCRIPTS_DIR / "jds-classify.py"

# --- JDS taxonomy (QMS-001) -------------------------------------------------

# Category code -> registry section heading it is filed under.
CATEGORY_SECTIONS = {
    "QMS": "Quality Management System (QMS)",
    "PRO": "Procedures (PRO)",
    "TMP": "Templates (TMP)",
    "RPT": "Reports (RPT)",
    "MAN": "Manuals (MAN)",
    "DWG": "Drawings (DWG)",
    "PRJ": "Project Documents (PRJ)",
    "TSH": "Timesheets (TSH)",
    "EXP": "Expenses (EXP)",
    "LOG": "Logs & Records (LOG)",
    "COR": "Correspondence (COR)",
    "BLG": "Blog Posts (BLG)",
}

# Engineering domain codes (QMS-001). A document number may omit the domain for
# system-level categories (e.g. JDS-PRO-001), so domain is always optional.
DOMAIN_CODES = (
    "MEC", "MAR", "AUT", "ELE", "PIP", "STR", "TST", "FAB", "THR", "SFW", "GEN",
)

# Revision letters JDS uses (skips I, O, Q, S, X, Z — QMS-001).
VALID_REV_LETTERS = "ABCDEFGHJKLMNPRTUVWY"

# Status values accepted in metadata blocks (mirrors jds-validate.py).
VALID_STATUSES = (
    "CURRENT", "APPROVED", "DRAFT", "SUPERSEDED", "EXAMPLE", "PUBLISHED", "ARCHIVED",
)

# Number of digits in the sequential part of a JDS number (e.g. 001).
NUMBER_WIDTH = 3

# --- Server -----------------------------------------------------------------

HOST = os.environ.get("JDS_STUDIO_HOST", "127.0.0.1")
PORT = int(os.environ.get("JDS_STUDIO_PORT", "8731"))
WEB_DIR = Path(__file__).resolve().parent.parent / "web"
