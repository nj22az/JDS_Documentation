Run a JDS self-enhancement pass — leave the repository better than you found it, following the JDS continuous-improvement cycle (CLAUDE.md → "Self-Improvement & Automation"). Use this when asked to improve, harden, or self-enhance the system, or as a closing pass after a work session.

The rule behind this skill: **every fix is applied at three levels — the instance, the root cause, and the guard that prevents recurrence.** A one-off fix that doesn't harden the system is incomplete.

## 1. Discover

Build a findings list from several angles (don't rely on one signal):

1. Run the validator: `python3 scripts/jds-validate.py`. Treat every `✗`/`⚠` as a finding.
2. Scan for smells the validator may not catch yet:
   - Documents in DRAFT that should be APPROVED; stale dates; missing revision-history rows.
   - Software (`projects/software/`): dead code, hardcoded values, files over 500 lines, unclear names, missing tests (JDS-PRO-004).
   - Interfaces (UI/HMI): non-conformance to JDS-PRO-012 (no visible focus, colour-only status, unconfirmed irreversible actions).
   - Broken or orphaned links; registry/file mismatches; duplicate numbers.
   - Templates or stylesheets that keep producing the same issue.
3. Note anything a future check *would* have caught but currently doesn't.

## 2. Triage

For each finding decide: fix now (small, < ~5 min, unambiguous) or log it. Anything that changes document identity, deletes content, or needs a human judgement call → **stop and ask the user** (AskUserQuestion), don't guess.

## 3. Apply the five-level protocol

For every finding you act on, work through as many of these as apply — this is the core of the skill:

1. **Fix the instance** — correct the document/file/code.
2. **Fix the root cause** — update the template, script, or stylesheet that produced it.
3. **Add automated detection** — add a check to `scripts/jds-validate.py` so it's caught next time. Prove the new check fires on a seeded example before trusting it.
4. **Improve the template/standard** — if a template or procedure led to the issue, update it.
5. **Update CLAUDE.md** — if guidance was unclear, clarify it so the issue can't recur.

## 4. Record

- Log larger corrective actions in `jds/registry/corrective-action-log.md` (use the next `CA-YYYY-NNN`, set status OPEN/CLOSED).
- Update the relevant CHANGELOG(s). System-level changes → `jds/CHANGELOG.md`; project changes → that project's CHANGELOG.
- If the system itself improved, bump the version in `jds/README.md` **and** `jds/CHANGELOG.md` (keep them in sync — the validator checks this).
- Register any new document in `jds/registry/document-register.md`.

## 5. Verify & commit

1. Re-run `python3 scripts/jds-validate.py` until it is clean (0 errors; warnings only where a human decision is pending and logged).
2. For software, run its tests (e.g. `python3 projects/software/<proj>/tests/test_core.py`).
3. Commit on the working branch with a clear message summarising what improved and which guard now prevents recurrence. Do **not** push to `main` without explicit user authorisation.

## Principle

Improve the system every session, never degrade it. Prefer adding a guard over fixing silently — the best outcome of finding a bug is a new check that makes that whole class of bug impossible to reintroduce.
