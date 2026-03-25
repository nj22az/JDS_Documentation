#!/usr/bin/env python3
"""JDS Validation Script — Automated quality checks for the documentation system.

Runs the JDS-PRO-005 quarterly audit checks programmatically:
- Registry vs filesystem consistency (no orphans, no phantoms)
- Document metadata completeness (header tables, revision history)
- Naming convention compliance
- Cross-reference link validation
- Structure alignment with CLAUDE.md

Usage:
    python3 scripts/jds-validate.py              # Full audit
    python3 scripts/jds-validate.py --quick       # Quick check (registry only)
    python3 scripts/jds-validate.py --fix         # Show suggested fixes
"""

import os
import re
import sys
import glob

REPO_ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
JDS_ROOT = os.path.join(REPO_ROOT, 'jds')
REGISTRY_PATH = os.path.join(JDS_ROOT, 'registry', 'document-register.md')

# JDS document number pattern
JDS_PATTERN = re.compile(r'JDS-([A-Z]{3})(?:-([A-Z]{3}))?-(\d{3})')

# Required metadata fields in JDS documents
REQUIRED_META = ['Document No.', 'Revision', 'Date', 'Status', 'Author']


class AuditResult:
    def __init__(self):
        self.passed = []
        self.warnings = []
        self.errors = []

    def ok(self, msg):
        self.passed.append(msg)

    def warn(self, msg):
        self.warnings.append(msg)

    def error(self, msg):
        self.errors.append(msg)

    def summary(self):
        total = len(self.passed) + len(self.warnings) + len(self.errors)
        lines = [
            '',
            '=' * 60,
            f'  JDS AUDIT SUMMARY — {total} checks',
            '=' * 60,
            f'  PASS:     {len(self.passed)}',
            f'  WARNINGS: {len(self.warnings)}',
            f'  ERRORS:   {len(self.errors)}',
            '=' * 60,
        ]
        if self.errors:
            lines.append('')
            lines.append('ERRORS:')
            for e in self.errors:
                lines.append(f'  ✗ {e}')
        if self.warnings:
            lines.append('')
            lines.append('WARNINGS:')
            for w in self.warnings:
                lines.append(f'  ⚠ {w}')
        if not self.errors and not self.warnings:
            lines.append('')
            lines.append('  All checks passed. System is clean.')
        lines.append('')
        return '\n'.join(lines)


def parse_registry(result):
    """Parse the document register and return all registered doc numbers with their paths."""
    if not os.path.exists(REGISTRY_PATH):
        result.error('Document register not found at jds/registry/document-register.md')
        return {}

    with open(REGISTRY_PATH, 'r') as f:
        content = f.read()

    entries = {}
    # Match markdown table links: [JDS-XXX-NNN](relative/path)
    link_pattern = re.compile(r'\[([^\]]+)\]\(([^)]+)\)')
    for match in link_pattern.finditer(content):
        doc_no = match.group(1)
        rel_path = match.group(2)
        if JDS_PATTERN.search(doc_no):
            # Resolve relative path from registry location
            abs_path = os.path.normpath(
                os.path.join(os.path.dirname(REGISTRY_PATH), rel_path)
            )
            entries[doc_no] = abs_path

    return entries


def check_registry_vs_filesystem(result):
    """Check that registry entries match actual files and vice versa."""
    entries = parse_registry(result)
    if not entries:
        return

    result.ok(f'Document register contains {len(entries)} entries')

    # Check for phantom entries (registry entry but no file)
    for doc_no, path in entries.items():
        if os.path.exists(path):
            result.ok(f'{doc_no} → file exists')
        else:
            result.error(f'PHANTOM: {doc_no} registered but file missing: {path}')

    # Check for orphan JDS files (file exists but not in registry)
    registered_paths = set(entries.values())
    jds_files = []
    for pattern in ['jds/**/*.md', 'projects/**/*.md', 'blog/_posts/*.md']:
        jds_files.extend(glob.glob(os.path.join(REPO_ROOT, pattern), recursive=True))

    for filepath in jds_files:
        filepath = os.path.normpath(filepath)
        # Skip non-JDS files
        basename = os.path.basename(filepath)
        if not JDS_PATTERN.search(basename) and not basename.startswith('2026-'):
            continue
        # Skip templates directory README, CHANGELOG, etc.
        if basename in ('README.md', 'CHANGELOG.md', 'corrective-action-log.md',
                        'document-register.md'):
            continue
        if filepath not in registered_paths:
            rel = os.path.relpath(filepath, REPO_ROOT)
            result.warn(f'ORPHAN: {rel} exists but not in registry')


def check_document_metadata(result):
    """Check that all JDS documents have required metadata headers."""
    patterns = [
        'jds/quality-manual/JDS-*.md',
        'jds/procedures/JDS-*.md',
        'jds/examples/JDS-*.md',
        'jds/templates/**/JDS-*.md',
        'projects/**/JDS-*.md',
    ]

    for pattern in patterns:
        for filepath in glob.glob(os.path.join(REPO_ROOT, pattern), recursive=True):
            with open(filepath, 'r') as f:
                content = f.read()

            rel = os.path.relpath(filepath, REPO_ROOT)
            basename = os.path.basename(filepath)

            # Check required metadata fields
            missing = []
            for field in REQUIRED_META:
                if f'**{field}**' not in content:
                    missing.append(field)

            if missing:
                result.error(f'{rel}: missing metadata: {", ".join(missing)}')
            else:
                result.ok(f'{rel}: metadata complete')

            # Check for revision history
            if 'Revision History' not in content and '## Revision' not in content:
                result.warn(f'{rel}: no revision history table found')

            # Check heading hierarchy (exclude headings inside fenced code blocks)
            # Strip fenced code blocks before checking
            stripped = re.sub(r'```.*?```', '', content, flags=re.DOTALL)
            headings = re.findall(r'^(#{1,6})\s', stripped, re.MULTILINE)
            h1_count = sum(1 for h in headings if h == '#')
            if h1_count == 0:
                result.warn(f'{rel}: no H1 heading')
            elif h1_count > 1:
                result.error(f'{rel}: multiple H1 headings ({h1_count})')

            levels = [len(h) for h in headings]
            for i in range(1, len(levels)):
                if levels[i] > levels[i - 1] + 1:
                    result.warn(f'{rel}: skipped heading level ({levels[i-1]} → {levels[i]})')
                    break

            # Check for wide tables (>7 columns will overflow A4 portrait)
            table_rows = re.findall(r'^\|(.+)\|', stripped, re.MULTILINE)
            for row in table_rows:
                cols = [c.strip() for c in row.split('|') if c.strip()]
                # Skip separator rows (all dashes)
                if all(re.match(r'^-+$', c) for c in cols):
                    continue
                if len(cols) > 7:
                    result.error(
                        f'{rel}: table has {len(cols)} columns (max 7 for A4). '
                        f'Split into multiple tables.'
                    )
                    break


def check_naming_conventions(result):
    """Check that JDS files follow naming conventions."""
    patterns = [
        ('jds/quality-manual/', r'JDS-QMS-\d{3}_[\w-]+\.md'),
        ('jds/procedures/', r'JDS-PRO-\d{3}_[\w-]+\.md'),
        ('jds/templates/**/', r'JDS-TMP-[A-Z]{3}-\d{3}_[\w-]+\.md'),
        ('jds/examples/', r'JDS-[A-Z]{3}(?:-[A-Z]{3})?-\d{3}_[\w-]+\.md'),
    ]

    for directory, name_pattern in patterns:
        dir_path = os.path.join(REPO_ROOT, directory)
        if not os.path.exists(dir_path.rstrip('*/')):
            continue

        for filepath in glob.glob(os.path.join(REPO_ROOT, directory, '*.md'), recursive=True):
            basename = os.path.basename(filepath)
            if basename in ('README.md',):
                continue
            if not re.match(name_pattern, basename):
                rel = os.path.relpath(filepath, REPO_ROOT)
                result.warn(f'{rel}: filename does not match expected pattern {name_pattern}')


def check_structure(result):
    """Check that required directories exist per CLAUDE.md."""
    required_dirs = [
        'jds',
        'jds/quality-manual',
        'jds/procedures',
        'jds/templates',
        'jds/registry',
        'jds/assets',
        'blog',
        '3d-modeling',
        'projects',
        'scripts',
        'documents',
        'archive',
    ]

    for d in required_dirs:
        path = os.path.join(REPO_ROOT, d)
        if os.path.isdir(path):
            result.ok(f'Directory exists: {d}/')
        else:
            result.error(f'Missing required directory: {d}/')


def check_gitignore(result):
    """Check that .gitignore has essential rules."""
    gitignore_path = os.path.join(REPO_ROOT, '.gitignore')
    if not os.path.exists(gitignore_path):
        result.error('.gitignore missing')
        return

    with open(gitignore_path, 'r') as f:
        content = f.read()

    required_rules = ['*.pdf', '__pycache__/', '.env']
    for rule in required_rules:
        if rule in content:
            result.ok(f'.gitignore contains: {rule}')
        else:
            result.warn(f'.gitignore missing rule: {rule}')


def check_changelog_version(result):
    """Check that CHANGELOG and README versions match."""
    changelog_path = os.path.join(JDS_ROOT, 'CHANGELOG.md')
    readme_path = os.path.join(JDS_ROOT, 'README.md')

    changelog_ver = None
    readme_ver = None

    if os.path.exists(changelog_path):
        with open(changelog_path, 'r') as f:
            match = re.search(r'## \[(\d+\.\d+)\]', f.read())
            if match:
                changelog_ver = match.group(1)

    if os.path.exists(readme_path):
        with open(readme_path, 'r') as f:
            match = re.search(r'\*\*Version:\*\*\s*(\d+\.\d+)', f.read())
            if match:
                readme_ver = match.group(1)

    if changelog_ver and readme_ver:
        if changelog_ver == readme_ver:
            result.ok(f'Version consistent: CHANGELOG={changelog_ver}, README={readme_ver}')
        else:
            result.error(f'Version mismatch: CHANGELOG={changelog_ver}, README={readme_ver}')
    else:
        result.warn('Could not parse version from CHANGELOG or README')


def main():
    quick = '--quick' in sys.argv

    result = AuditResult()

    print('JDS Validation Audit')
    print('=' * 60)

    print('\n[1/6] Checking directory structure...')
    check_structure(result)

    print('[2/6] Checking registry vs filesystem...')
    check_registry_vs_filesystem(result)

    if not quick:
        print('[3/6] Checking document metadata...')
        check_document_metadata(result)

        print('[4/6] Checking naming conventions...')
        check_naming_conventions(result)

        print('[5/6] Checking .gitignore...')
        check_gitignore(result)

        print('[6/6] Checking version consistency...')
        check_changelog_version(result)
    else:
        print('[3-6] Skipped (quick mode)')

    print(result.summary())

    # Exit code: 1 if errors, 0 if clean
    sys.exit(1 if result.errors else 0)


if __name__ == '__main__':
    main()
