"""Paths and stable publishing constants for the reader content build."""

import os
import re
from pathlib import Path


def find_eic_root():
    """Locate the EIC project, with an explicit override for development copies."""
    configured = os.environ.get("EIC_ROOT")
    candidates = [Path(configured)] if configured else []
    candidates.append(Path(__file__).resolve().parents[2])
    for candidate in candidates:
        if (candidate / "manuscript" / "publishing-manifest.json").is_file():
            return candidate
    raise SystemExit(
        "Cannot locate EIC manuscript/publishing-manifest.json. "
        "Run inside the JDS project or set EIC_ROOT."
    )


APP = Path(__file__).resolve().parents[1]
EIC = find_eic_root()
MANUSCRIPT = EIC / "manuscript"
MANIFEST_PATH = MANUSCRIPT / "publishing-manifest.json"
HTML_ASSETS = EIC / "exports" / "html" / "assets"
ASSETS_JSON = HTML_ASSETS / "data" / "archive-assets.json"
COMPILED_MARKDOWN = EIC / "exports" / "the-front-row-seat.md"

OUT_DATA = APP / "src" / "data" / "content.json"
OUT_PUBLIC = APP / "public" / "assets"
OUT_OMNIBUS_CONFIG = APP / "public" / "omnibus-config.js"
INDEX_HTML = APP / "index.html"

NARRATIVE_ROLES = {"chapter", "interlude", "epilogue"}
SCENE_BREAK_PATTERN = re.compile(r"<hr\s*/?>")
FRONTMATTER_PATTERN = re.compile(r"\A---\s*\n(.*?)\n---\s*\n", re.S)
PORTRAIT_ASPECT_RATIO = 1.15
FALLBACK_EXCERPT_MAX_WORDS = 900
PUBLIC_ASSET_SUBDIRECTORIES = ("img", "generated")

# Stable hero selections for the illustrated edition. YAML hero metadata is also
# read when present; this map is the fallback for older exported headers.
HERO_FALLBACK = {
    "00-frontmatter": "front-row-seat-cover",
    "01-1603-the-boy-who-signed": "tom-maggie-paper",
    "02-1603-dutch-courage": "hendricks",
    "02-1626-the-man-who-came-back-wrong": "amboyna-massacre",
    "03-1696-the-price-of-a-man": "every-ganj-i-sawai",
    "04-1701-good-for-business": "wapping-old-stairs",
    "05-1757-a-soldiers-arithmetic": "plassey-clive-mir-jafar",
    "06-1770-what-mulvey-saw": "bengal-map-1776",
    "07-1774-too-big-to-sink": "boston-tea-party",
    "08-1790-forty-seven-days": "bligh-open-boat",
    "09-1839-what-pemberton-called-trade": "opium-destruction",
    "10-1858-what-harding-would-not-say": "east-india-house-1796",
    "11-1880-the-hell-ship": "cutty-sark-1871",
    "12-1888-the-watchmans-daughter": "liz-su-laundry",
    "13-1940-a-wardens-watch": "london-blitz",
    "14-2019-what-the-suit-didnt-see": "canary-wharf-west-india-docks",
    "appendix-0-authors-note": "eic-coat-of-arms",
    "appendix-1-timeline": "east-india-dock-1806",
    "appendix-2-bibliography": "east-india-house-1726",
}
