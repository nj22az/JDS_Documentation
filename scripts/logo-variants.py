#!/usr/bin/env python3
"""Generate colour variants of the JDS logo SVG for different document categories.

JDS-PRO-007 §6 — Colour is Language (Principle #4):
Each document category gets a distinctive colour variant of the Johansson Engineering
stamp logo. This provides instant glance-level identification of document type.

Usage:
    python3 scripts/logo-variants.py              # Generate all variants
    python3 scripts/logo-variants.py --category PRO  # Generate one variant

The SVG source (logo.svg) must exist in jds/assets/. All variants are written to
jds/assets/logo-variants/.
"""

import os
import re
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.normpath(os.path.join(SCRIPT_DIR, '..'))
ASSETS_DIR = os.path.join(REPO_ROOT, 'jds', 'assets')
SVG_SOURCE = os.path.join(ASSETS_DIR, 'logo.svg')
VARIANTS_DIR = os.path.join(ASSETS_DIR, 'logo-variants')

# ─────────────────────────────────────────────────────────────────────────────
# JDS Document Category Colour Map
#
# Design rationale (PRO-007 §6 + Tokyo Metro principle):
# - Each colour carries meaning consistent with JDS palette
# - Categories grouped by function: governance (navy), execution (teal/green),
#   communication (warm tones), reference (neutrals)
# ─────────────────────────────────────────────────────────────────────────────

CATEGORY_COLOURS = {
    # System governance — Navy Blue (authority)
    'QMS':  {'hex': '#1B3A5C', 'name': 'Navy Blue',      'meaning': 'System governance, authority'},
    'PRO':  {'hex': '#1B3A5C', 'name': 'Navy Blue',      'meaning': 'Procedures, rules'},

    # Engineering execution — Steel Blue / Teal
    'RPT':  {'hex': '#2E6B8A', 'name': 'Deep Teal',      'meaning': 'Reports, findings'},
    'DWG':  {'hex': '#4A90A4', 'name': 'Steel Blue',     'meaning': 'Drawings, models, CAD'},
    'PRJ':  {'hex': '#3A7CA5', 'name': 'Project Blue',   'meaning': 'Project documents'},
    'MAN':  {'hex': '#2E6B8A', 'name': 'Deep Teal',      'meaning': 'Manuals, guides'},
    'LOG':  {'hex': '#3D8B6E', 'name': 'Forest Green',   'meaning': 'Logs, registers, records'},

    # Communication — Warm tones
    'COR':  {'hex': '#8B2D2D', 'name': 'Heritage Red',   'meaning': 'Correspondence, letters'},
    'BLG':  {'hex': '#8B2D2D', 'name': 'Heritage Red',   'meaning': 'Blog posts, published articles'},

    # Administrative — Warm neutrals
    'TSH':  {'hex': '#6B5B3E', 'name': 'Warm Bronze',    'meaning': 'Timesheets, time tracking'},
    'EXP':  {'hex': '#6B5B3E', 'name': 'Warm Bronze',    'meaning': 'Expenses, cost tracking'},
    'TMP':  {'hex': '#5C5C5C', 'name': 'Neutral Gray',   'meaning': 'Templates (blank forms)'},

    # Default — Classic black (for uncoloured use)
    'DEFAULT': {'hex': '#000000', 'name': 'Black', 'meaning': 'Default, uncoloured'},
}

# ─────────────────────────────────────────────────────────────────────────────
# Engineering Domain Colour Accents (optional, for DWG/RPT/LOG with domain)
# These can be used as a secondary accent when domain distinction matters.
# ─────────────────────────────────────────────────────────────────────────────

DOMAIN_COLOURS = {
    'MEC': {'hex': '#4A90A4', 'name': 'Steel Blue'},
    'MAR': {'hex': '#1B3A5C', 'name': 'Navy Blue'},
    'AUT': {'hex': '#5B8C5A', 'name': 'Automation Green'},
    'ELE': {'hex': '#D4A017', 'name': 'Electric Gold'},
    'PIP': {'hex': '#7B5B3A', 'name': 'Pipe Bronze'},
    'STR': {'hex': '#6B6B6B', 'name': 'Steel Gray'},
    'TST': {'hex': '#8B5E3C', 'name': 'Instrument Brown'},
    'FAB': {'hex': '#C85A17', 'name': 'Workshop Orange'},
    'THR': {'hex': '#8B2D2D', 'name': 'Thermal Red'},
    'SFW': {'hex': '#3A7CA5', 'name': 'Digital Blue'},
    'GEN': {'hex': '#5C5C5C', 'name': 'Neutral Gray'},
}


def generate_variant(svg_content, fill_colour, output_path):
    """Replace all fill colours in the SVG with the target colour."""
    # Replace fill="#000000" with the new colour
    variant = svg_content.replace('fill="#000000"', f'fill="{fill_colour}"')

    # Also replace any inline style fills
    variant = re.sub(
        r'fill:\s*#000000',
        f'fill: {fill_colour}',
        variant
    )

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(variant)


def main():
    # Check source exists
    if not os.path.exists(SVG_SOURCE):
        print(f'ERROR: SVG source not found: {SVG_SOURCE}')
        print('Run vtracer to convert logo.png to logo.svg first.')
        sys.exit(1)

    # Read source SVG
    with open(SVG_SOURCE, 'r', encoding='utf-8') as f:
        svg_content = f.read()

    # Create variants directory
    os.makedirs(VARIANTS_DIR, exist_ok=True)

    # Check for single category mode
    single = None
    if '--category' in sys.argv:
        idx = sys.argv.index('--category')
        if idx + 1 < len(sys.argv):
            single = sys.argv[idx + 1].upper()

    # Generate category variants
    generated = 0
    for cat, info in CATEGORY_COLOURS.items():
        if single and cat != single:
            continue

        filename = f'logo-{cat.lower()}.svg'
        output_path = os.path.join(VARIANTS_DIR, filename)
        generate_variant(svg_content, info['hex'], output_path)
        size_kb = os.path.getsize(output_path) / 1024
        print(f'  {cat:8s} → {filename:25s} {info["hex"]}  {info["name"]:20s} ({size_kb:.0f} KB)')
        generated += 1

    # Generate domain variants (optional)
    if not single or single == 'DOMAINS':
        for dom, info in DOMAIN_COLOURS.items():
            filename = f'logo-domain-{dom.lower()}.svg'
            output_path = os.path.join(VARIANTS_DIR, filename)
            generate_variant(svg_content, info['hex'], output_path)
            generated += 1

        print(f'\n  + {len(DOMAIN_COLOURS)} domain variants generated')

    print(f'\nTotal: {generated} logo variants in jds/assets/logo-variants/')

    # Print colour reference table
    if not single:
        print('\n' + '=' * 65)
        print('  JDS LOGO COLOUR REFERENCE — PRO-007 §6')
        print('=' * 65)
        print(f'  {"Category":<10} {"Colour":<20} {"Hex":<10} {"Meaning"}')
        print('-' * 65)
        for cat, info in CATEGORY_COLOURS.items():
            if cat == 'DEFAULT':
                continue
            print(f'  {cat:<10} {info["name"]:<20} {info["hex"]:<10} {info["meaning"]}')
        print()


if __name__ == '__main__':
    main()
