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
    """Render a markdown document to a JDS-compliant PDF via md2pdf.py.

    Source and output are constrained to the repository (PRO-012 §5.3)."""
    args = [config.MD2PDF_SCRIPT, config.resolve_in_repo(md_rel_path)]
    if output_rel_path:
        args.append(config.resolve_in_repo(output_rel_path))
    return _run(args)


def generate_office(kind):
    """Generate an Excel workbook (timesheet | expense | mileage | all)."""
    return _run([config.OFFICE_SCRIPT, kind])


def classify_quick(ps, volume, medium="compressed air"):
    """Classify a single vessel to AFS 2017:3 — result text in `output`."""
    return _run([config.CLASSIFY_SCRIPT, "--quick",
                 "--ps", ps, "--volume", volume, "--medium", medium])


# The AFS 2017:3 supervision pipeline step -> its jds-classify.py flag.
SUPERVISION_STEPS = {
    "inventory": "--csv",      # source is a CSV of vessels
    "program": "--program",    # source is an inventory.md
    "round": "--round",        # source is a program.md
    "review": "--review",      # source is a program.md
}


def supervision(step, source_rel, output_rel, *, client=None, site=None,
                author=None, doc_no=None, round_type=None):
    """Run one supervision-pipeline step, reading and writing inside the repo.

    `step` is one of SUPERVISION_STEPS. `source_rel`/`output_rel` are
    repo-relative; both are validated against the repository boundary.
    """
    if step not in SUPERVISION_STEPS:
        raise ValueError(f"Unknown supervision step '{step}'")
    source = config.resolve_in_repo(source_rel)
    output = config.resolve_in_repo(output_rel)
    args = [config.CLASSIFY_SCRIPT, SUPERVISION_STEPS[step]]
    if step == "inventory":
        args += [str(source)]
    else:
        args += ["--from", str(source)]
    args += ["--output", str(output)]
    if client:
        args += ["--client", client]
    if site:
        args += ["--site", site]
    if author:
        args += ["--author", author]
    if doc_no:
        args += ["--doc-no", doc_no]
    if round_type and step == "round":
        args += ["--round-type", round_type]
    return _run(args)
