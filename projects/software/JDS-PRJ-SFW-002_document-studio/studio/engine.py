"""Thin wrappers around the existing JDS command-line scripts.

Studio deliberately does NOT reimplement PDF rendering, validation, or Excel
generation — those already live in ``scripts/`` and are the single source of
truth (JDS-PRO-004 §6: shared logic lives in one place). The engine just shells
out to them with the repo's own Python interpreter and returns structured
results for the API to surface.
"""

import subprocess
import sys

from . import config


def _run(args):
    """Run a script under the current interpreter; return a result dict."""
    completed = subprocess.run(
        [sys.executable, *[str(a) for a in args]],
        cwd=str(config.REPO_ROOT),
        capture_output=True,
        text=True,
    )
    return {
        "ok": completed.returncode == 0,
        "returncode": completed.returncode,
        "output": (completed.stdout + completed.stderr).strip(),
    }


def run_validator(quick=False):
    """Run jds-validate.py and return its result (output includes Doc's line)."""
    args = [config.VALIDATOR_SCRIPT]
    if quick:
        args.append("--quick")
    return _run(args)


def generate_pdf(md_rel_path, output_rel_path=None):
    """Render a markdown document to a JDS-compliant PDF via md2pdf.py."""
    args = [config.MD2PDF_SCRIPT, config.REPO_ROOT / md_rel_path]
    if output_rel_path:
        args.append(config.REPO_ROOT / output_rel_path)
    return _run(args)


def generate_office(kind):
    """Generate an Excel workbook (timesheet | expense | mileage | all)."""
    return _run([config.OFFICE_SCRIPT, kind])
