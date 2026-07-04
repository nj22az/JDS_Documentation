#!/usr/bin/env python3
import html
import json
import re
import ssl
import time
import urllib.parse
import urllib.request
from pathlib import Path
from html.parser import HTMLParser


ROOT = Path(__file__).resolve().parents[1]
IMG_DIR = ROOT / "assets" / "img"
DATA_DIR = ROOT / "assets" / "data"
USER_AGENT = "FrontRowSeatVisualEdition/1.0 (local static-book project)"


ASSETS = [
    {
        "id": "prospect-of-whitby",
        "title": "Prospect of Whitby, Wapping",
        "commons_title": "File:Prospect of Whitby, Wapping - geograph.org.uk - 4162020.jpg",
        "caption": "The Prospect of Whitby on Wapping Wall, the book's fixed room beside the Thames.",
        "alt": "Exterior view of the Prospect of Whitby pub beside the Thames.",
    },
    {
        "id": "east-indiaman-cirencester",
        "title": "East Indiaman off St Helena",
        "commons_title": "File:East Indiaman Cirencester off St Helena 1795.jpg",
        "caption": "An East Indiaman under sail: the kind of vessel that turns the book's paper contracts into distance, cargo, and risk.",
        "alt": "A large East Indiaman sailing ship at sea under full sail.",
    },
    {
        "id": "english-east-indiaman",
        "title": "An English East Indiaman",
        "commons_title": "File:An English East Indiaman RMG BHC1011.tiff",
        "caption": "A Company-era merchant ship shown as maritime power rather than romance.",
        "alt": "An English East Indiaman painted in profile on open water.",
    },
    {
        "id": "eic-coat-of-arms",
        "title": "East India Company coat of arms",
        "commons_title": "File:Coat of arms of the East India Company.svg",
        "caption": "The corporate mark behind many of the book's ledgers, voyages, and silences.",
        "alt": "The coat of arms of the East India Company.",
    },
    {
        "id": "east-india-house-1726",
        "title": "East India House, Leadenhall Street",
        "commons_title": "File:Gezicht op de Leadenhall Street, met rechts het East India House, te Londen The house occupied by the East India Company in Leadenhall Street, as refaced in 1726 (titel op object), RP-P-2018-2131.jpg",
        "caption": "East India House on Leadenhall Street, where distant violence became minutes, orders, and dividends.",
        "alt": "Historic print of Leadenhall Street with East India House.",
    },
    {
        "id": "east-india-house-1796",
        "title": "Front of the East India House",
        "commons_title": "File:Gezicht op het East India House, te Londen Front of the East India House, Leadenhall Street, as rebuilt in 1796 (titel op object), RP-P-2018-2132.jpg",
        "caption": "The later East India House facade: respectable architecture for an extraction machine.",
        "alt": "Historic print of the front of East India House in Leadenhall Street.",
    },
    {
        "id": "surat-map-1730",
        "title": "Map of Surat, 1730",
        "commons_title": "File:Map of Surat 1730.jpg",
        "caption": "Surat, one of the Company's early Indian footholds, drawn as a trading city before the forts hardened.",
        "alt": "Historic map of Surat from 1730.",
    },
    {
        "id": "surat-warehouse",
        "title": "Company warehouse at Surat",
        "commons_title": "File:Dutch East India Company's warehouse and living quarters in Surat.jpg",
        "caption": "A European company warehouse at Surat: trade made architectural and permanent.",
        "alt": "Historic drawing of a European company warehouse and living quarters in Surat.",
    },
    {
        "id": "amboyna-massacre",
        "title": "Amboyna",
        "commons_title": "File:Amboyna.jpg",
        "caption": "Amboyna enters the book as trauma, paperwork, and a pivot away from the Spice Islands.",
        "alt": "Historic image connected to the Amboyna massacre.",
    },
    {
        "id": "amboyna-fort",
        "title": "Fort Victoria, Amboyna",
        "commons_title": "File:AmboynaFort1655.jpg",
        "caption": "Amboyna's fortifications: the wall behind the word 'factory' when trade turns coercive.",
        "alt": "Seventeenth-century view of Fort Victoria at Amboyna.",
    },
    {
        "id": "every-ganj-i-sawai",
        "title": "Every engaging the Great Mughal's ship",
        "commons_title": "File:Every engaging the Great Mogul's Ship.jpg",
        "caption": "The raid on the Ganj-i-Sawai made piracy, empire, and Company trade answer to the same court of consequences.",
        "alt": "An engraving of Henry Every's ship attacking the Great Mughal's ship.",
    },
    {
        "id": "captain-every",
        "title": "Captain Every",
        "commons_title": "File:Captain Every (Works of Daniel Defoe).png",
        "caption": "Henry Every as print culture made him: a wanted man becoming a marketable image.",
        "alt": "Old printed portrait of Captain Every.",
    },
    {
        "id": "captain-kidd-hanging",
        "title": "Captain Kidd hanging",
        "commons_title": "File:Captain Kidd hanging.jpg",
        "caption": "Kidd's execution turns legal ambiguity into public theatre on the Wapping foreshore.",
        "alt": "Historic illustration of Captain Kidd being hanged.",
    },
    {
        "id": "captain-kidd-portrait",
        "title": "Captain Kidd",
        "commons_title": "File:Kidd compressed.jpg",
        "caption": "Kidd's printed face outlived the missing papers and the snapped rope.",
        "alt": "Old portrait print of Captain William Kidd.",
    },
    {
        "id": "plassey-clive-mir-jafar",
        "title": "Clive and Mir Jafar after Plassey",
        "commons_title": "File:Robert Clive and Mir Jafar after the Battle of Plassey, 1757 by Francis Hayman.jpg",
        "caption": "Plassey as imperial painting: a transaction dressed as victory.",
        "alt": "Painting of Robert Clive meeting Mir Jafar after the Battle of Plassey.",
    },
    {
        "id": "bengal-map-1776",
        "title": "Bengal and Bihar map, 1776",
        "commons_title": "File:1776 Rennell - Dury Wall Map of Bihar and Bengal, India - Geographicus - BaharBengal-dury-1776.jpg",
        "caption": "Bengal mapped for revenue, movement, and rule after the Company became a governing power.",
        "alt": "Eighteenth-century map of Bengal and Bihar.",
    },
    {
        "id": "famine-relief-engraving",
        "title": "Famine relief engraving",
        "commons_title": "File:Distressed Natives Going to the Relief Works - The Graphic 1874.jpg",
        "caption": "A later public-domain famine engraving, used as visual context rather than a direct image of Bengal in 1770.",
        "alt": "Engraving of distressed people going to famine relief works.",
    },
    {
        "id": "east-india-dock-1806",
        "title": "East India Dock, 1806",
        "commons_title": "File:East India dock 1806.jpg",
        "caption": "The dock system as imperial infrastructure: cargo, customs, and state power made local.",
        "alt": "Historic print of the East India Dock in London.",
    },
    {
        "id": "east-india-company-docks-1844",
        "title": "East India Company docks, 1844",
        "commons_title": "File:East India Company docks.jpg",
        "caption": "The East India Company docks in 1844: the river converted into managed imperial intake.",
        "alt": "Historic illustration of the East India Company docks in London.",
    },
    {
        "id": "east-india-export-dock",
        "title": "East India Export Dock, 1843",
        "commons_title": "File:East India Export Dock (1843).jpg",
        "caption": "The export dock made the Company's world visible from London's river edge.",
        "alt": "Historic print of the East India Export Dock in London.",
    },
    {
        "id": "boston-tea-party",
        "title": "Boston Tea Party",
        "commons_title": "File:Boston Tea Party-Cooper.jpg",
        "caption": "The tea hoard leaves Wapping's ledgers and returns as politics in Boston harbour.",
        "alt": "Historic illustration of men throwing tea chests into Boston Harbor.",
    },
    {
        "id": "tea-chest-caddies",
        "title": "Tea chest with caddies",
        "commons_title": "File:Tea chest with tea caddies MET DT2933.jpg",
        "caption": "Tea as a domestic luxury with a global account underneath it.",
        "alt": "An antique tea chest with tea caddies.",
    },
    {
        "id": "tea-chest-met",
        "title": "Tea chest",
        "commons_title": "File:Tea Chest MET 121779.jpg",
        "caption": "The commodity made small enough to sit on a table, though the route behind it spans oceans.",
        "alt": "An antique tea chest.",
    },
    {
        "id": "bligh-open-boat",
        "title": "Bligh's open boat",
        "commons_title": "File:Bligh open boat.jpg",
        "caption": "Bligh's launch compresses distance, rationing, discipline, and survival into twenty-three feet.",
        "alt": "Historic illustration of Bligh and men in an open boat at sea.",
    },
    {
        "id": "breadfruit-tree",
        "title": "Breadfruit tree",
        "commons_title": "File:Breadfruit tree.jpg",
        "caption": "Breadfruit: the plant behind the Bounty's voyage, and behind the plantation arithmetic it served.",
        "alt": "Botanical drawing of a breadfruit tree.",
    },
    {
        "id": "fuchsia-denticulata",
        "title": "Fuchsia denticulata",
        "commons_title": "File:Fuchsia denticulata.jpg",
        "caption": "The fuchsia thread gives the book one living inheritance not built on extraction.",
        "alt": "Botanical illustration of fuchsia flowers.",
    },
    {
        "id": "fuchsia-botanical",
        "title": "Fuchsia botanical plate",
        "commons_title": "File:Nfnz d127 fuchsia procumbens and alsiosma macrophylla.jpg",
        "caption": "A botanical fuchsia plate for the plant that keeps reappearing as a quiet counter-ledger.",
        "alt": "Botanical plate including a fuchsia plant.",
    },
    {
        "id": "opium-destruction",
        "title": "Destruction of opium, 1839",
        "commons_title": "File:Destruction of opium in 1839.jpg",
        "caption": "Lin's destruction of seized opium marks the moment a commercial triangle becomes a shooting war.",
        "alt": "Historic image of opium being destroyed in 1839.",
    },
    {
        "id": "cinchona-bark",
        "title": "Cinchona bark",
        "commons_title": "File:The cinchona barks (PL. V) BHL6677295.jpg",
        "caption": "Cinchona bark, quinine, and gin: the medicinal edge of empire's daily rituals.",
        "alt": "Botanical plate showing cinchona bark.",
    },
    {
        "id": "fighting-temeraire",
        "title": "The Fighting Temeraire",
        "commons_title": "File:The Fighting Temeraire, JMW Turner, National Gallery.jpg",
        "caption": "Turner's Temeraire belongs to the same river world as the book: sail, smoke, nostalgia, and industrial replacement.",
        "alt": "J. M. W. Turner's painting of the Fighting Temeraire being tugged to be broken up.",
    },
    {
        "id": "gin-lane",
        "title": "Gin Lane",
        "commons_title": "File:William Hogarth - Gin Lane.jpg",
        "caption": "Gin Lane brings the drink's social cost into the book's longer argument about appetite and profit.",
        "alt": "William Hogarth's engraving Gin Lane.",
    },
    {
        "id": "cutty-sark-1871",
        "title": "Cutty Sark, 1871",
        "commons_title": "File:Cutty Sark, 1871.jpg",
        "caption": "Cutty Sark in her prime, before speed, violence, and obsolescence enter the chapter's account.",
        "alt": "Painting of the Cutty Sark sailing ship.",
    },
    {
        "id": "cutty-sark-photo",
        "title": "Cutty Sark",
        "commons_title": "File:StateLibQld 1 145051 Cutty Sark (ship).jpg",
        "caption": "The clipper as remembered by photography: famous, practical, and already becoming heritage.",
        "alt": "Historic photograph of the Cutty Sark sailing ship.",
    },
    {
        "id": "whitechapel-murders-map",
        "title": "Whitechapel murders map",
        "commons_title": "File:Whitechapel murders.jpg",
        "caption": "A public-domain map of the Whitechapel murder sites, included for geography, not spectacle.",
        "alt": "Historic map showing Whitechapel murder sites.",
    },
    {
        "id": "booth-whitechapel",
        "title": "Booth map of Whitechapel",
        "commons_title": "File:Booth map of Whitechapel.jpg",
        "caption": "Booth's poverty map turns streets into social categories, a different kind of ledger.",
        "alt": "Charles Booth poverty map of Whitechapel.",
    },
    {
        "id": "london-blitz",
        "title": "London Blitz",
        "commons_title": "File:London Blitz 791940.jpg",
        "caption": "The docks burning in 1940: the imperial engine room made target and ruin.",
        "alt": "London docks burning during the Blitz.",
    },
    {
        "id": "bombing-density-map",
        "title": "Bombing density map",
        "commons_title": "File:Map of the density of bombing, London region, to October 1941 (HO193-45) (29282975318).jpg",
        "caption": "Bombing mapped as a clerk might map damage: dots, density, and a city under arithmetic.",
        "alt": "Map of bombing density in the London region to October 1941.",
    },
    {
        "id": "canary-wharf-west-india-docks",
        "title": "Canary Wharf and West India Docks",
        "commons_title": "File:Canary Wharf - West India Docks - North Dock - geograph.org.uk - 7987785.jpg",
        "caption": "Modern finance rising from the West India Docks: the old machine in glass and steel.",
        "alt": "Canary Wharf towers seen from West India Docks.",
    },
    {
        "id": "wapping-old-stairs",
        "title": "Wapping Old Stairs",
        "commons_title": "File:Wapping Old Stairs - geograph.org.uk - 4161993.jpg",
        "caption": "The stairs and foreshore keep the book tied to mud, tide, and everyday access to the river.",
        "alt": "Wapping Old Stairs leading down toward the Thames.",
    },
    {
        "id": "mughal-gold",
        "title": "Jahangir weighing Prince Khurram",
        "commons_title": "File:Jahangir weighing prince Khurram (later Shah Jahan) against gold and silver in the presence of Mahabat Khan and Khan Jahan..jpg",
        "caption": "Mughal gold, sovereignty, and scale: a courtly counter-image to Wapping's reward arithmetic.",
        "alt": "Mughal miniature of Jahangir weighing Prince Khurram against gold and silver.",
    },
]


class TextExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.parts = []

    def handle_data(self, data):
        self.parts.append(data)

    def text(self):
        return re.sub(r"\s+", " ", html.unescape(" ".join(self.parts))).strip()


def clean(value):
    if not value:
        return ""
    parser = TextExtractor()
    parser.feed(str(value))
    return parser.text()


def slug_ext(url, content_type=""):
    path = urllib.parse.urlparse(url).path
    name = urllib.parse.unquote(path.rsplit("/", 1)[-1])
    ext = Path(name).suffix.lower()
    if ext in {".jpg", ".jpeg", ".png", ".webp", ".gif"}:
        return ".jpg" if ext == ".jpeg" else ext
    if "png" in content_type:
        return ".png"
    if "webp" in content_type:
        return ".webp"
    return ".jpg"


def request_json(url):
    ctx = ssl._create_unverified_context()
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=40, context=ctx) as response:
        return json.load(response)


def download(url, out):
    ctx = ssl._create_unverified_context()
    content_type = ""
    data = b""
    for attempt in range(2):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
            with urllib.request.urlopen(req, timeout=80, context=ctx) as response:
                content_type = response.headers.get("Content-Type", "")
                data = response.read()
            break
        except urllib.error.HTTPError as error:
            if error.code != 429 or attempt == 1:
                print(f"skipping download after HTTP {error.code}: {url}", flush=True)
                return None
            time.sleep(10)
    if not data:
        return None
    ext = slug_ext(url, content_type)
    if out.suffix != ext:
        out = out.with_suffix(ext)
    out.write_bytes(data)
    return out


def main():
    IMG_DIR.mkdir(parents=True, exist_ok=True)
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    titles = [asset["commons_title"] for asset in ASSETS]
    pages = {}
    for index in range(0, len(titles), 20):
        batch = titles[index : index + 20]
        params = urllib.parse.urlencode(
            {
                "action": "query",
                "format": "json",
                "titles": "|".join(batch),
                "prop": "imageinfo",
                "iiprop": "url|mime|extmetadata",
                "iiurlwidth": "1024",
            }
        )
        data = request_json("https://commons.wikimedia.org/w/api.php?" + params)
        pages.update(data.get("query", {}).get("pages", {}))
        time.sleep(1.5)

    by_title = {page.get("title"): page for page in pages.values()}
    manifest = []

    for asset in ASSETS:
        page = by_title.get(asset["commons_title"])
        if not page or "missing" in page:
            print(f"missing: {asset['commons_title']}")
            continue
        imageinfo = (page.get("imageinfo") or [{}])[0]
        meta = imageinfo.get("extmetadata", {})
        source_url = imageinfo.get("descriptionurl", "")
        image_url = imageinfo.get("thumburl") or imageinfo.get("url", "")
        base = IMG_DIR / asset["id"]
        existing = list(IMG_DIR.glob(asset["id"] + ".*"))
        if existing:
            local_path = existing[0]
        else:
            local_path = download(image_url, base)
            if local_path is None:
                print(f"skipped: {asset['id']}", flush=True)
                continue
            time.sleep(4.0)

        manifest.append(
            {
                "id": asset["id"],
                "title": asset["title"],
                "caption": asset["caption"],
                "alt": asset["alt"],
                "file": local_path.relative_to(ROOT).as_posix(),
                "source_url": source_url,
                "commons_title": asset["commons_title"],
                "license": clean(meta.get("LicenseShortName", {}).get("value")),
                "usage_terms": clean(meta.get("UsageTerms", {}).get("value")),
                "creator": clean(meta.get("Artist", {}).get("value")),
                "credit": clean(meta.get("Credit", {}).get("value")),
                "date": clean(meta.get("DateTimeOriginal", {}).get("value")),
                "attribution_required": clean(meta.get("AttributionRequired", {}).get("value")),
            }
        )
        print(f"fetched: {asset['id']} -> {local_path.relative_to(ROOT)}", flush=True)

    generated = {
        "id": "front-row-seat-cover",
        "title": "The Front-Row Seat cover illustration",
        "caption": "AI-generated painted cover illustration: Wapping, the Thames, old timber, ships in mist, and low historic riverside buildings across the water.",
        "alt": "Painted historical illustration of a Thames riverside pub at dusk with old ships in mist and low historic buildings across the water.",
        "file": "assets/generated/front-row-seat-cover.png",
        "source_url": "",
        "license": "Generated image",
        "usage_terms": "Generated for this project",
        "creator": "OpenAI image generation",
        "credit": "Prompted and curated for this static HTML edition.",
        "date": "2026",
        "attribution_required": "false",
        "prompt": "Painted historical book-cover illustration of the Prospect of Whitby / Wapping Wall atmosphere at dusk, period-only Thames riverside, no text, no portraits, muted river palette, old ships in mist and low historic buildings across the Thames.",
    }
    author_photo = {
        "id": "prospect-of-whitby-night-author",
        "title": "Prospect of Whitby at night",
        "caption": "The Prospect of Whitby after dark: the living room of the book seen as a present-day threshold into its older river history.",
        "alt": "Black-and-white night photograph of the Prospect of Whitby exterior on a wet Wapping street.",
        "file": "assets/img/prospect-of-whitby-night-author.png",
        "source_url": "",
        "source_note": "Private photograph supplied by the author.",
        "license": "Author-owned photograph",
        "usage_terms": "Used with permission for this edition",
        "creator": "Author photograph",
        "credit": "Private photograph supplied by the author.",
        "date": "Unknown",
        "attribution_required": "false",
    }
    manifest.insert(0, generated)
    manifest.insert(1, author_photo)

    (DATA_DIR / "archive-assets.json").write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
