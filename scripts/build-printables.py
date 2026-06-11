#!/usr/bin/env python3
"""Generate the printable fill-in templates for JDS-PRJ-GEN-001.

These are the "download and print at home" documents the book points to with QR
codes: the garage inventory, the tool lifetime journal, the hazardous-materials
log, a zone-map worksheet, the seasonal pass, and the continuous maintenance
program & log. A4, black ink, EN + SV.

Usage:
    python3 scripts/build-printables.py                 # English set
    python3 scripts/build-printables.py --lang sv        # Swedish set
"""

import sys
from pathlib import Path

import weasyprint

# --- Configuration (JDS-PRO-004 §3) --------------------------------------------

OUT = Path("projects/JDS-PRJ-GEN-001/04-production/printables")

CSS = """
@page { size: A4; margin: 16mm 14mm; }
* { box-sizing: border-box; }
body { font-family: Georgia, 'Liberation Serif', serif; color: #14233a; font-size: 10.5pt; }
h1 { font-size: 19pt; margin: 0 0 2mm; }
.intro { font-size: 9.5pt; color: #555; margin: 0 0 5mm; }
.brand { float: right; font-size: 8pt; letter-spacing: .1em; color: #8a8a8a; }
table { width: 100%; border-collapse: collapse; }
th, td { border: 0.6pt solid #888; padding: 2.4mm 2mm; text-align: left; vertical-align: top; }
th { background: #e9edf2; font-size: 9pt; }
td { height: 9mm; }
.fields td { height: 7mm; }
.fields th { width: 30%; background: #f3f5f8; }
.box { border: 0.8pt solid #888; height: 150mm; margin-top: 3mm; border-radius: 2px; }
.legend { font-size: 9.5pt; color: #444; margin-top: 3mm; }
ul.check { list-style: none; padding: 0; margin: 0; }
ul.check li { padding: 2.2mm 0; border-bottom: 0.4pt dotted #bbb; }
ul.check li::before { content: "\\2610"; font-size: 13pt; margin-right: 3mm; }
.note { font-size: 9pt; color: #555; margin-top: 4mm; }
h2 { font-size: 12pt; margin: 6mm 0 2mm; }
"""

T = {
    "en": {
        "brand": "THE GARAGE RESET",
        "inventory": {
            "title": "Garage Inventory",
            "intro": "List what you keep and where it lives — one line per item or box. "
                     "This doubles as your insurance and theft record: add serial numbers "
                     "and photograph anything valuable.",
            "cols": ["Item / box", "Zone", "Qty", "Serial / value", "Location & notes"],
            "rows": 26,
        },
        "lifetime": {
            "title": "Tool & Equipment Lifetime Journal",
            "intro": "One sheet per machine or major tool. Keep it with the manual. "
                     "A serviced, documented tool lasts longer and is worth more.",
            "fields": [("Tool / machine", ""), ("Make & model", ""), ("Serial no.", ""),
                       ("Bought (date)", ""), ("Price", ""),
                       ("Manual & receipt kept?", "  ☐ yes   ☐ no"),
                       ("Photographed for insurance?", "  ☐ yes   ☐ no")],
            "cols": ["Date", "Service / repair / note", "By", "Cost"],
            "rows": 14,
        },
        "hazmat": {
            "title": "Hazardous-Materials Log",
            "intro": "Fuel, paint, solvent, oil, batteries, gas. Keep the list short — "
                     "only what you'll use in a season (see chapter 5).",
            "cols": ["Product", "Type", "Qty", "Bought", "Use-by", "Disposed (date)"],
            "rows": 20,
            "note": "Store flammables low and cool; propane outdoors only. Take anything "
                    "dried, unlabeled, or unknown to the hazardous-waste drop-off.",
        },
        "zone": {
            "title": "Zone-Map Worksheet",
            "intro": "Sketch your garage from above and mark the five zones. Plan the car "
                     "in first, then build everything around its clearances.",
            "legend": "1 Car · 2 Tools · 3 Garden · 4 Seasonal · 5 Recycling — "
                      "often-used near the door and the light; rarely-used high and far back.",
        },
        "seasonal": {
            "title": "Spring / Fall Garage Pass",
            "intro": "Twice a year, tied to the tire swap. Tick as you go.",
            "items": ["Swap the seasonal zone (tires, cushions, etc.)",
                      "Sort while things are in your hands — used it last season?",
                      "Haul the 'lose' pile out the same day",
                      "Check the hazard corner — dried paint, stale fuel out",
                      "Test the fire extinguisher gauge (in the green)",
                      "Test smoke / CO alarms",
                      "Check lighting works for the season ahead",
                      "Update the inventory and lifetime journals",
                      "Refill the consumables you're low on",
                      "Book the next pass in the calendar"],
        },
        "program": {
            "title": "Continuous Maintenance Program & Log",
            "intro": "The garage stays in order on a rhythm, not a rescue. Keep this where "
                     "you'll see it, and sign the log so the whole house can share it.",
            "sched": [["Weekly · 10 min", "Put things back · recycling out · wipe the bench"],
                      ["Monthly · 15 min", "Scan for new clutter · extinguisher gauge · note low consumables"],
                      ["Spring & Fall · ½ day", "Seasonal swap + Sort + hazard check (use the seasonal sheet)"],
                      ["Yearly · 1–2 h", "Walk the inventory · update journals · photograph valuables · test alarms & GFCI"]],
            "log_cols": ["Date", "What was done", "Done by"],
            "rows": 16,
        },
    },
    "sv": {
        "brand": "STÄDA I GARAGET",
        "inventory": {
            "title": "Garageinventering",
            "intro": "Skriv upp vad du behåller och var det bor — en rad per sak eller låda. "
                     "Listan fungerar också som försäkrings- och stöldregister: lägg till "
                     "serienummer och fotografera det värdefulla.",
            "cols": ["Sak / låda", "Zon", "Antal", "Serienr / värde", "Plats & noteringar"],
            "rows": 26,
        },
        "lifetime": {
            "title": "Livslängdsjournal för verktyg & maskiner",
            "intro": "Ett blad per maskin eller större verktyg. Förvara det med manualen. "
                     "Ett servat och dokumenterat verktyg håller längre och är värt mer.",
            "fields": [("Verktyg / maskin", ""), ("Märke & modell", ""), ("Serienr", ""),
                       ("Köpt (datum)", ""), ("Pris", ""),
                       ("Manual & kvitto sparat?", "  ☐ ja   ☐ nej"),
                       ("Fotat för försäkring?", "  ☐ ja   ☐ nej")],
            "cols": ["Datum", "Service / reparation / notering", "Av", "Kostnad"],
            "rows": 14,
        },
        "hazmat": {
            "title": "Logg för farligt och brandfarligt",
            "intro": "Bränsle, färg, lösningsmedel, olja, batterier, gasol. Håll listan kort — "
                     "bara det du gör av med på en säsong (se kapitel 5).",
            "cols": ["Produkt", "Typ", "Mängd", "Köpt", "Bäst före", "Lämnad (datum)"],
            "rows": 20,
            "note": "Förvara brandfarligt lågt och svalt; gasol endast utomhus. Lämna det som "
                    "är intorkat, omärkt eller okänt på miljöstationen. I Sverige får du förvara "
                    "ca 25 liter bensin hemma utan tillstånd (MSB).",
        },
        "zone": {
            "title": "Arbetsblad: zonkarta",
            "intro": "Rita garaget ovanifrån och märk ut de fem zonerna. Planera in bilen "
                     "först och bygg allt annat runt dess mått.",
            "legend": "1 Bil · 2 Verktyg · 3 Trädgård · 4 Säsong · 5 Återvinning — "
                      "ofta-zoner nära porten och ljuset; sällan-zoner högt och längst in.",
        },
        "seasonal": {
            "title": "Vår- och höstgenomgång",
            "intro": "Två gånger om året, kopplat till däckbytet. Bocka av efter hand.",
            "items": ["Vänd säsongszonen (däck, dynor m.m.)",
                      "Sortera medan sakerna är i händerna — använd förra säsongen?",
                      "Kör ut 'lämna'-högen samma dag",
                      "Gå igenom gifthörnan — torkad färg, gammalt bränsle ut",
                      "Kontrollera brandsläckarens visare (i det gröna)",
                      "Testa brand- och CO-varnare",
                      "Se till att belysningen fungerar inför säsongen",
                      "Uppdatera inventeringen och livslängdsjournalerna",
                      "Fyll på förbrukningsvaror du har ont om",
                      "Boka nästa genomgång i kalendern"],
        },
        "program": {
            "title": "Löpande underhållsprogram & logg",
            "intro": "Garaget hålls i ordning på en rytm, inte med en räddningsaktion. Häng "
                     "det här synligt och signera loggen så att hela huset kan dela på det.",
            "sched": [["Varje vecka · 10 min", "Ställ tillbaka · återvinning ut · torka bänken"],
                      ["Varje månad · 15 min", "Spana efter ny röra · släckarvisare · notera tomma förråd"],
                      ["Vår & höst · ½ dag", "Säsongsbyte + Sortera + gifthörna (använd säsongsbladet)"],
                      ["Varje år · 1–2 h", "Gå igenom inventeringen · uppdatera journaler · fota värdesaker · testa varnare & jordfelsbrytare"]],
            "log_cols": ["Datum", "Vad som gjordes", "Av vem"],
            "rows": 16,
        },
    },
}


def rows_html(n, cols):
    cell = "".join("<td></td>" for _ in cols)
    return "".join(f"<tr>{cell}</tr>" for _ in range(n))


def header(t):
    return f'<div class="brand">{t["brand"]}</div>'


def table_form(t, f):
    head = "".join(f"<th>{c}</th>" for c in f["cols"])
    note = f'<p class="note">{f["note"]}</p>' if f.get("note") else ""
    return (f'{header(t)}<h1>{f["title"]}</h1><p class="intro">{f["intro"]}</p>'
            f'<table><thead><tr>{head}</tr></thead><tbody>{rows_html(f["rows"], f["cols"])}'
            f'</tbody></table>{note}')


def lifetime_form(t, f):
    fields = "".join(f'<tr><th>{k}</th><td>{v}</td></tr>' for k, v in f["fields"])
    head = "".join(f"<th>{c}</th>" for c in f["cols"])
    return (f'{header(t)}<h1>{f["title"]}</h1><p class="intro">{f["intro"]}</p>'
            f'<table class="fields"><tbody>{fields}</tbody></table>'
            f'<h2>Service log</h2><table><thead><tr>{head}</tr></thead>'
            f'<tbody>{rows_html(f["rows"], f["cols"])}</tbody></table>')


def zone_form(t, f):
    return (f'{header(t)}<h1>{f["title"]}</h1><p class="intro">{f["intro"]}</p>'
            f'<div class="box"></div><p class="legend">{f["legend"]}</p>')


def seasonal_form(t, f):
    items = "".join(f"<li>{i}</li>" for i in f["items"])
    return (f'{header(t)}<h1>{f["title"]}</h1><p class="intro">{f["intro"]}</p>'
            f'<ul class="check">{items}</ul>')


def program_form(t, f):
    sched = "".join(f"<tr><th>{a}</th><td>{b}</td></tr>" for a, b in f["sched"])
    head = "".join(f"<th>{c}</th>" for c in f["log_cols"])
    return (f'{header(t)}<h1>{f["title"]}</h1><p class="intro">{f["intro"]}</p>'
            f'<table class="fields"><tbody>{sched}</tbody></table>'
            f'<h2>Maintenance log</h2><table><thead><tr>{head}</tr></thead>'
            f'<tbody>{rows_html(f["rows"], f["log_cols"])}</tbody></table>')


BUILDERS = {"inventory": table_form, "lifetime": lifetime_form, "hazmat": table_form,
            "zone": zone_form, "seasonal": seasonal_form, "program": program_form}


def main():
    args = sys.argv[1:]
    lang = args[args.index("--lang") + 1] if "--lang" in args else "en"
    t = T[lang]
    out_dir = OUT / lang
    out_dir.mkdir(parents=True, exist_ok=True)
    for slug, builder in BUILDERS.items():
        html = f"<html><head><meta charset='utf-8'></head><body>{builder(t, t[slug])}</body></html>"
        path = out_dir / f"{slug}.pdf"
        weasyprint.HTML(string=html).write_pdf(str(path), stylesheets=[weasyprint.CSS(string=CSS)])
        print(f"Built {path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
