#!/usr/bin/env python3
"""JDS Validation Script — Automated quality checks for the documentation system.

Runs the JDS-PRO-005 quarterly audit checks programmatically:
- Registry vs filesystem consistency (no orphans, no phantoms)
- Document metadata completeness (header tables, revision history)
- Naming convention compliance
- Internal markdown link validation
- Cross-reference link validation
- Blog post front matter and structure
- Script configuration consistency (logo sizes, UNCONTROLLED COPY)
- Structure alignment with CLAUDE.md
- Status field consistency (CURRENT/SUPERSEDED/DRAFT/EXAMPLE)
- Logo and brand asset integrity

Usage:
    python3 scripts/jds-validate.py              # Full audit
    python3 scripts/jds-validate.py --quick       # Quick check (registry only)
    python3 scripts/jds-validate.py --fix         # Show suggested fixes
"""

import os
import re
import sys
import glob

REPO_ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
JDS_ROOT = os.path.join(REPO_ROOT, 'jds')
REGISTRY_PATH = os.path.join(JDS_ROOT, 'registry', 'document-register.md')
SCRIPTS_DIR = os.path.join(REPO_ROOT, 'scripts')

# JDS document number pattern
JDS_PATTERN = re.compile(r'JDS-([A-Z]{3})(?:-([A-Z]{3}))?-(\d{3})')

# Required metadata fields in JDS documents
REQUIRED_META = ['Document No.', 'Revision', 'Date', 'Status', 'Author']

# Valid JDS status values
VALID_STATUSES = {'CURRENT', 'APPROVED', 'DRAFT', 'SUPERSEDED', 'EXAMPLE', 'PUBLISHED', 'ARCHIVED'}

# Valid revision letters (JDS skips I, O, Q, S, X, Z)
VALID_REV_LETTERS = set('ABCDEFGHJKLMNPRTUVWY')

# JDS palette colours (PRO-007 §6.1)
JDS_PALETTE = {
    '#1B3A5C': 'Navy Blue (headings)',
    '#4A90A4': 'Steel Blue (subheadings)',
    '#8C8C8C': 'Warm Gray (metadata)',
}

# Logo requirements (CLAUDE.md)
LOGO_MIN_DOC_PT = 52    # Minimum logo size in documents
LOGO_MIN_LETTER_PT = 72  # Minimum logo size in letterheads


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


def safe_read(filepath):
    """Read a file safely with error handling. Returns content or None."""
    try:
        with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
            return f.read()
    except (IOError, OSError):
        return None


def parse_registry(result):
    """Parse the document register and return all registered doc numbers with their paths and revisions."""
    if not os.path.exists(REGISTRY_PATH):
        result.error('Document register not found at jds/registry/document-register.md')
        return {}

    content = safe_read(REGISTRY_PATH)
    if content is None:
        result.error('Could not read document register')
        return {}

    entries = {}
    # Match full registry table rows: | [JDS-XXX](path) | Title | Rev | Date | Status | Author |
    row_pattern = re.compile(
        r'\|\s*\[([^\]]+)\]\(([^)]+)\)\s*\|'   # doc_no and path
        r'[^|]*\|'                                # title
        r'\s*([A-Z]+)\s*\|'                       # revision
    )
    for match in row_pattern.finditer(content):
        doc_no = match.group(1)
        rel_path = match.group(2)
        rev = match.group(3)
        if JDS_PATTERN.search(doc_no):
            abs_path = os.path.normpath(
                os.path.join(os.path.dirname(REGISTRY_PATH), rel_path)
            )
            entries[doc_no] = {'path': abs_path, 'rev': rev}

    return entries


def check_registry_vs_filesystem(result):
    """Check that registry entries match actual files and vice versa."""
    entries = parse_registry(result)
    if not entries:
        return

    result.ok(f'Document register contains {len(entries)} entries')

    # Check for phantom entries (registry entry but no file)
    for doc_no, info in entries.items():
        path = info['path']
        if os.path.exists(path):
            result.ok(f'{doc_no} → file exists')
        else:
            result.error(f'PHANTOM: {doc_no} registered but file missing: {path}')

    # Check registry Rev vs actual file Rev
    for doc_no, info in entries.items():
        path = info['path']
        reg_rev = info['rev']
        if not os.path.exists(path):
            continue
        # Skip templates — they contain placeholder metadata (DRAFT), not their own revision
        if doc_no.startswith('JDS-TMP-'):
            continue
        content = safe_read(path)
        if content is None:
            continue
        # Look for **Revision** | X or **Rev** | X in metadata table
        rev_match = re.search(r'\*\*Revision?\*\*\s*\|\s*([A-Z]+)', content)
        if not rev_match:
            # Try front matter style: revision: A
            rev_match = re.search(r'^revision:\s*([A-Z]+)', content, re.MULTILINE)
        if rev_match:
            file_rev = rev_match.group(1)
            if file_rev != reg_rev:
                rel = os.path.relpath(path, REPO_ROOT)
                result.error(
                    f'{doc_no}: registry says Rev {reg_rev} but file says Rev {file_rev} ({rel})'
                )

    # Check for orphan JDS files (file exists but not in registry)
    registered_paths = set(info['path'] for info in entries.values())
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
            content = safe_read(filepath)
            if content is None:
                result.error(f'Could not read: {filepath}')
                continue

            rel = os.path.relpath(filepath, REPO_ROOT)

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

            # Check Status field validity
            status_match = re.search(r'\*\*Status\*\*\s*\|\s*(\w+)', content)
            if status_match:
                status = status_match.group(1)
                if status not in VALID_STATUSES:
                    result.warn(f'{rel}: unusual Status value "{status}" (expected one of: {", ".join(sorted(VALID_STATUSES))})')

            # Check revision letter validity (skip templates with DRAFT placeholder)
            if 'JDS-TMP-' not in rel:
                rev_match = re.search(r'\*\*Revision?\*\*\s*\|\s*([A-Z]+)', content)
                if rev_match:
                    rev = rev_match.group(1)
                    if len(rev) == 1 and rev not in VALID_REV_LETTERS and rev != 'D':
                        # D is valid (not in skip list), double-check
                        result.warn(f'{rel}: revision letter "{rev}" is in the JDS skip list (I, O, Q, S, X, Z)')


def check_internal_links(result):
    """Validate that internal markdown links point to files that exist."""
    md_files = []
    for pattern in ['**/*.md']:
        md_files.extend(glob.glob(os.path.join(REPO_ROOT, pattern), recursive=True))

    # Exclude archive and safe-to-delete
    md_files = [f for f in md_files if '/archive/' not in f and '/safe-to-delete/' not in f]

    broken_count = 0
    checked_count = 0

    for filepath in md_files:
        content = safe_read(filepath)
        if content is None:
            continue

        rel_file = os.path.relpath(filepath, REPO_ROOT)
        file_dir = os.path.dirname(filepath)

        # Strip fenced code blocks and inline code to avoid false positives
        stripped = re.sub(r'```.*?```', '', content, flags=re.DOTALL)
        stripped = re.sub(r'`[^`]+`', '', stripped)

        # Find all markdown links [text](path) — skip URLs, anchors, and mailto
        links = re.findall(r'\[([^\]]*)\]\(([^)]+)\)', stripped)

        for link_text, link_path in links:
            # Skip external URLs, anchors, mailto, and template placeholders
            if link_path.startswith(('http://', 'https://', '#', 'mailto:')):
                continue
            if '[' in link_path or '{' in link_path:
                continue

            # Remove anchor from path
            clean_path = link_path.split('#')[0]
            if not clean_path:
                continue

            # Resolve relative to the file's directory
            target = os.path.normpath(os.path.join(file_dir, clean_path))
            checked_count += 1

            if not os.path.exists(target):
                broken_count += 1
                result.error(f'{rel_file}: broken link [{link_text}]({link_path}) → target not found')

    if broken_count == 0:
        result.ok(f'Internal links: {checked_count} links checked, all valid')
    else:
        result.error(f'Internal links: {broken_count} broken out of {checked_count} checked')


def check_blog_posts(result):
    """Validate blog post structure, front matter, and JDS metadata."""
    posts_dir = os.path.join(REPO_ROOT, 'blog', '_posts')
    if not os.path.isdir(posts_dir):
        result.warn('blog/_posts/ directory not found')
        return

    posts = glob.glob(os.path.join(posts_dir, '*.md'))
    if not posts:
        result.warn('No blog posts found in blog/_posts/')
        return

    for filepath in sorted(posts):
        content = safe_read(filepath)
        if content is None:
            result.error(f'Could not read blog post: {filepath}')
            continue

        rel = os.path.relpath(filepath, REPO_ROOT)
        basename = os.path.basename(filepath)

        # Check Jekyll front matter exists
        if not content.startswith('---'):
            result.error(f'{rel}: missing Jekyll front matter (must start with ---)')
            continue

        # Parse front matter
        fm_match = re.match(r'^---\s*\n(.*?)\n---', content, re.DOTALL)
        if not fm_match:
            result.error(f'{rel}: malformed Jekyll front matter')
            continue

        front_matter = fm_match.group(1)

        # Check required front matter fields
        required_fm = ['layout', 'title', 'date']
        for field in required_fm:
            if not re.search(rf'^{field}:', front_matter, re.MULTILINE):
                result.error(f'{rel}: missing front matter field: {field}')

        # Check layout is 'post'
        layout_match = re.search(r'^layout:\s*(\S+)', front_matter, re.MULTILINE)
        if layout_match and layout_match.group(1) != 'post':
            result.warn(f'{rel}: layout is "{layout_match.group(1)}", expected "post"')

        # Check filename follows Jekyll convention: YYYY-MM-DD-slug.md
        if not re.match(r'\d{4}-\d{2}-\d{2}-.+\.md$', basename):
            result.warn(f'{rel}: filename does not follow YYYY-MM-DD-slug.md convention')

        # Check JDS metadata present (table or front matter jds_no)
        has_jds_meta = (
            'JDS-BLG' in content
            or re.search(r'^jds_no:', front_matter, re.MULTILINE)
        )
        if not has_jds_meta:
            result.warn(f'{rel}: no JDS-BLG document number found')

        result.ok(f'{rel}: blog post structure valid')

    # Check _config.yml exists
    config_path = os.path.join(REPO_ROOT, 'blog', '_config.yml')
    if os.path.exists(config_path):
        config = safe_read(config_path)
        if config:
            if 'baseurl' not in config:
                result.warn('blog/_config.yml: missing baseurl setting')
            else:
                result.ok('blog/_config.yml: baseurl configured')
    else:
        result.warn('blog/_config.yml not found')


def check_script_consistency(result):
    """Validate that PDF scripts follow JDS brand and design requirements."""

    # Check logo assets exist (PNG source + SVG vector)
    logo_png = os.path.join(REPO_ROOT, 'jds', 'assets', 'logo.png')
    logo_svg = os.path.join(REPO_ROOT, 'jds', 'assets', 'logo.svg')

    if os.path.exists(logo_png):
        result.ok('Logo PNG exists: jds/assets/logo.png')
        if os.path.getsize(logo_png) < 100:
            result.error('Logo PNG appears empty or corrupt (< 100 bytes)')
    else:
        result.error('Logo PNG missing: jds/assets/logo.png')

    if os.path.exists(logo_svg):
        result.ok('Logo SVG exists: jds/assets/logo.svg')
    else:
        result.warn('Logo SVG missing: jds/assets/logo.svg (run: python3 scripts/logo-variants.py)')

    # Check logo colour variants
    variants_dir = os.path.join(REPO_ROOT, 'jds', 'assets', 'logo-variants')
    if os.path.isdir(variants_dir):
        variants = [f for f in os.listdir(variants_dir) if f.endswith('.svg')]
        if variants:
            result.ok(f'Logo variants: {len(variants)} colour variants in logo-variants/')
        else:
            result.warn('Logo variants directory exists but is empty')
    else:
        result.warn('Logo variants directory missing (run: python3 scripts/logo-variants.py)')

    # Check md2pdf.py
    md2pdf_path = os.path.join(SCRIPTS_DIR, 'md2pdf.py')
    if os.path.exists(md2pdf_path):
        content = safe_read(md2pdf_path)
        if content:
            # Check UNCONTROLLED COPY marking
            if 'UNCONTROLLED COPY' in content:
                result.ok('md2pdf.py: UNCONTROLLED COPY marking present')
            else:
                result.error('md2pdf.py: missing UNCONTROLLED COPY marking (JDS-PRO-005 §6)')

            # Check logo size >= 52pt
            logo_size_match = re.search(r'\.logo-header\s+img\s*\{[^}]*width:\s*(\d+)pt', content, re.DOTALL)
            if not logo_size_match:
                # Try alternate CSS pattern
                logo_size_match = re.search(r'logo.*?width:\s*(\d+)pt', content, re.DOTALL)
            if logo_size_match:
                size = int(logo_size_match.group(1))
                if size >= LOGO_MIN_DOC_PT:
                    result.ok(f'md2pdf.py: logo size {size}pt >= {LOGO_MIN_DOC_PT}pt minimum')
                else:
                    result.error(f'md2pdf.py: logo size {size}pt < {LOGO_MIN_DOC_PT}pt minimum')
            else:
                result.warn('md2pdf.py: could not determine logo size — verify manually')

            # Check border-radius not applied to logo (CA-2026-002)
            # Look for border-radius near logo CSS
            logo_css = re.search(r'\.logo-header.*?\}.*?\}', content, re.DOTALL)
            if logo_css and 'border-radius' in logo_css.group(0):
                result.error('md2pdf.py: border-radius applied to logo (CA-2026-002 — stamp must not be squished)')
            else:
                result.ok('md2pdf.py: no border-radius on logo')

            # Check page numbering
            if 'counter(page)' in content and 'counter(pages)' in content:
                result.ok('md2pdf.py: page numbering (Page N of M) present')
            else:
                result.warn('md2pdf.py: missing page numbering (Page N of M)')

            # Check running header (doc title on page 2+)
            if 'string(doc-title)' in content or '@top-center' in content:
                result.ok('md2pdf.py: running header present')
            else:
                result.warn('md2pdf.py: missing running header on continuation pages')
    else:
        result.error('md2pdf.py not found in scripts/')

    # Check md2letter.py
    md2letter_path = os.path.join(SCRIPTS_DIR, 'md2letter.py')
    if os.path.exists(md2letter_path):
        content = safe_read(md2letter_path)
        if content:
            # Check logo size >= 72pt for letterhead
            letter_logo_match = re.search(r'\.letterhead\s+img\s*\{[^}]*width:\s*(\d+)pt', content, re.DOTALL)
            if not letter_logo_match:
                letter_logo_match = re.search(r'letterhead.*?img.*?width:\s*(\d+)pt', content, re.DOTALL)
            if letter_logo_match:
                size = int(letter_logo_match.group(1))
                if size >= LOGO_MIN_LETTER_PT:
                    result.ok(f'md2letter.py: logo size {size}pt >= {LOGO_MIN_LETTER_PT}pt minimum')
                else:
                    result.error(f'md2letter.py: logo size {size}pt < {LOGO_MIN_LETTER_PT}pt minimum')
            else:
                result.warn('md2letter.py: could not determine logo size — verify manually')

            # Check font embedding
            if '@font-face' in content or 'font-face' in content:
                result.ok('md2letter.py: font embedding configured')
            else:
                result.warn('md2letter.py: no @font-face rules found')
    else:
        result.warn('md2letter.py not found in scripts/')


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

    content = safe_read(gitignore_path)
    if content is None:
        result.error('Could not read .gitignore')
        return

    required_rules = ['*.pdf', '__pycache__/', '.env']
    for rule in required_rules:
        if rule in content:
            result.ok(f'.gitignore contains: {rule}')
        else:
            result.warn(f'.gitignore missing rule: {rule}')

    # Check safe-to-delete exception exists
    if '!safe-to-delete/' in content:
        result.ok('.gitignore: safe-to-delete/ PDF exception present')


def check_changelog_version(result):
    """Check that CHANGELOG and README versions match."""
    changelog_path = os.path.join(JDS_ROOT, 'CHANGELOG.md')
    readme_path = os.path.join(JDS_ROOT, 'README.md')

    changelog_ver = None
    readme_ver = None

    if os.path.exists(changelog_path):
        content = safe_read(changelog_path)
        if content:
            match = re.search(r'## \[(\d+\.\d+)\]', content)
            if match:
                changelog_ver = match.group(1)

    if os.path.exists(readme_path):
        content = safe_read(readme_path)
        if content:
            match = re.search(r'\*\*Version:\*\*\s*(\d+\.\d+)', content)
            if match:
                readme_ver = match.group(1)

    if changelog_ver and readme_ver:
        if changelog_ver == readme_ver:
            result.ok(f'Version consistent: CHANGELOG={changelog_ver}, jds/README={readme_ver}')
        else:
            result.error(f'Version mismatch: CHANGELOG={changelog_ver}, jds/README={readme_ver}')
    else:
        result.warn('Could not parse version from CHANGELOG or jds/README')

    # Also check root README version
    root_readme = os.path.join(REPO_ROOT, 'README.md')
    if os.path.exists(root_readme):
        content = safe_read(root_readme)
        if content:
            match = re.search(r'\*\*JDS Version:\*\*\s*(\d+\.\d+)', content)
            if match:
                root_ver = match.group(1)
                if changelog_ver and root_ver != changelog_ver:
                    result.error(f'Root README version {root_ver} != CHANGELOG {changelog_ver}')
                else:
                    result.ok(f'Root README version consistent: {root_ver}')


def check_corrective_action_log(result):
    """Check that the corrective action log is well-formed."""
    ca_log_path = os.path.join(JDS_ROOT, 'registry', 'corrective-action-log.md')
    if not os.path.exists(ca_log_path):
        result.warn('Corrective action log not found')
        return

    content = safe_read(ca_log_path)
    if content is None:
        result.error('Could not read corrective action log')
        return

    # Check for Next number tracker
    if 'Next number' in content or 'next number' in content.lower():
        result.ok('Corrective action log: next number tracker present')
    else:
        result.warn('Corrective action log: missing "Next number" tracker')

    # Check that all CAs have a status (OPEN or CLOSED)
    ca_headers = re.findall(r'###\s+CA-\d{4}-\d{3}\s*—\s*(.*)', content)
    for header in ca_headers:
        if 'CLOSED' not in header.upper() and 'OPEN' not in header.upper():
            result.warn(f'CA entry missing status: {header}')

    result.ok(f'Corrective action log: {len(ca_headers)} entries found')


def check_claude_md(result):
    """Check that CLAUDE.md exists and references key system components."""
    claude_path = os.path.join(REPO_ROOT, 'CLAUDE.md')
    if not os.path.exists(claude_path):
        result.error('CLAUDE.md not found in repository root')
        return

    content = safe_read(claude_path)
    if content is None:
        result.error('Could not read CLAUDE.md')
        return

    # Check for key sections that should be present
    required_sections = [
        ('JDS Documentation System', 'Document numbering reference'),
        ('jds-validate.py', 'Validator reference'),
        ('Table Design Rules', 'Table width rules'),
        ('Logo', 'Logo and brand rules'),
    ]

    for keyword, description in required_sections:
        if keyword in content:
            result.ok(f'CLAUDE.md: {description} present')
        else:
            result.warn(f'CLAUDE.md: missing {description} ({keyword})')


def main():
    quick = '--quick' in sys.argv
    show_fix = '--fix' in sys.argv

    result = AuditResult()

    print('JDS Validation Audit')
    print('=' * 60)

    print('\n[1/10] Checking directory structure...')
    check_structure(result)

    print('[2/10] Checking registry vs filesystem...')
    check_registry_vs_filesystem(result)

    if not quick:
        print('[3/10] Checking document metadata...')
        check_document_metadata(result)

        print('[4/10] Checking naming conventions...')
        check_naming_conventions(result)

        print('[5/10] Checking internal links...')
        check_internal_links(result)

        print('[6/10] Checking blog posts...')
        check_blog_posts(result)

        print('[7/10] Checking script consistency...')
        check_script_consistency(result)

        print('[8/10] Checking .gitignore...')
        check_gitignore(result)

        print('[9/10] Checking version consistency...')
        check_changelog_version(result)

        print('[10/10] Checking system integrity...')
        check_corrective_action_log(result)
        check_claude_md(result)
    else:
        print('[3-10] Skipped (quick mode)')

    print(result.summary())

    if show_fix and (result.errors or result.warnings):
        print('SUGGESTED FIXES:')
        print('-' * 40)
        for e in result.errors:
            if 'missing metadata' in e:
                print(f'  → Add JDS metadata table to file (see JDS-TMP-RPT-001 for format)')
            elif 'broken link' in e:
                print(f'  → Update or remove the broken link: {e}')
            elif 'PHANTOM' in e:
                print(f'  → Either create the missing file or remove the registry entry')
            elif 'registry says Rev' in e:
                print(f'  → Update either the registry or file metadata to match')
            elif 'table has' in e:
                print(f'  → Split wide table into multiple tables with shared ID column')
            elif 'Version mismatch' in e or 'version' in e.lower():
                print(f'  → Sync version numbers across README.md, jds/README.md, CHANGELOG.md')
            elif 'UNCONTROLLED COPY' in e:
                print(f'  → Add "UNCONTROLLED COPY" to @top-right CSS in md2pdf.py')
            elif 'logo size' in e.lower():
                print(f'  → Increase logo width to meet minimum (52pt docs, 72pt letters)')
            elif 'border-radius' in e:
                print(f'  → Remove border-radius from logo CSS (stamp must not be squished)')
        for w in result.warnings:
            if 'ORPHAN' in w:
                print(f'  → Register the orphan file in jds/registry/document-register.md')
            elif 'front matter' in w:
                print(f'  → Add Jekyll front matter (layout, title, date) to blog post')
        print()

    # Exit code: 1 if errors, 0 if clean
    sys.exit(1 if result.errors else 0)


if __name__ == '__main__':
    main()
