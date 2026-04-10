#!/usr/bin/env python3
"""
JDS Vessel Classification & Inventory Generator

Classifies pressurised vessels per AFS 2017:3 (consolidated with AFS 2019:1,
AFS 2020:10, AFS 2022:2) and generates JDS-compliant inventory documents with
automatic risk classification and inspection interval calculation.

Usage:
    Interactive:  python3 scripts/jds-classify.py
    From CSV:     python3 scripts/jds-classify.py --csv vessels.csv [--output inventory.md]
    Quick check:  python3 scripts/jds-classify.py --quick --ps 11 --volume 1000

Part of JDS-PRJ-MEC-002 (Vessel Supervision System).
"""

import argparse
import csv
import sys
import os
from datetime import date, datetime

# ---------------------------------------------------------------------------
# Media classification database
# ---------------------------------------------------------------------------

MEDIA_GROUPS = {
    # Group 1 — Dangerous (explosive, flammable, toxic, oxidising per CLP)
    "lpg": 1, "propane": 1, "butane": 1, "ammonia": 1, "hydrogen": 1,
    "chlorine": 1, "acetylene": 1, "ethylene": 1, "methane": 1,
    "natural gas": 1, "oxygen": 1, "ethanol": 1, "methanol": 1,
    "toluene": 1, "benzene": 1, "co": 1, "carbon monoxide": 1,
    "sulphur dioxide": 1, "so2": 1, "fluorine": 1, "phosgene": 1,
    "vinyl chloride": 1, "ethylene oxide": 1, "hydrochloric acid": 1,
    # Group 2 — Non-dangerous (all other fluids)
    "compressed air": 2, "air": 2, "nitrogen": 2, "water": 2,
    "steam": 2, "co2": 2, "carbon dioxide": 2, "argon": 2,
    "helium": 2, "neon": 2, "krypton": 2, "xenon": 2,
    "hydraulic oil": 2, "mineral oil": 2, "glycol": 2,
    "r134a": 2, "r410a": 2, "r32": 2,
}

# ---------------------------------------------------------------------------
# Classification logic per AFS 2017:3
# ---------------------------------------------------------------------------

def lookup_fluid_group(medium):
    """Determine fluid group from medium name. Returns 1, 2, or None."""
    key = medium.strip().lower()
    return MEDIA_GROUPS.get(key, None)


def classify_vessel(ps, volume, fluid_group):
    """
    Classify a vessel per AFS 2017:3 based on PS, volume, and fluid group.

    Returns dict with: psv, risk_class, ped_category, intervals, inspector.
    """
    psv = ps * volume

    # Check minimum threshold: PS must exceed 0.5 bar
    if ps <= 0.5:
        return _result(psv, "Not in scope", "N/A",
                       "Below 0.5 bar — outside AFS 2017:3 scope")

    if fluid_group == 1:
        # Group 1 — dangerous fluids (lower thresholds)
        if psv > 3000:
            risk_class = "A"
            ped_cat = "IV"
        elif psv > 200:
            risk_class = "B"
            ped_cat = "III" if psv > 1000 else "II"
        elif psv > 50:
            risk_class = "Simple PV"
            ped_cat = "I"
        else:
            return _result(psv, "Not classified", "Art. 4.3",
                           "Below classification threshold (Group 1)")
    else:
        # Group 2 — non-dangerous fluids
        if psv > 10000:
            risk_class = "A"
            ped_cat = "IV"
        elif psv > 3000:
            risk_class = "A"
            ped_cat = "III"
        elif psv > 1000:
            risk_class = "B"
            ped_cat = "II"
        elif psv > 200:
            risk_class = "Below B"
            ped_cat = "I"
        elif psv > 50:
            risk_class = "Simple PV"
            ped_cat = "Art. 4.3"
        else:
            return _result(psv, "Not classified", "N/A",
                           "Below classification threshold (Group 2)")

    intervals = get_intervals(risk_class)
    inspector = get_inspector(risk_class)
    return {
        "psv": psv,
        "risk_class": risk_class,
        "ped_category": ped_cat,
        "intervals": intervals,
        "inspector": inspector,
        "note": None,
    }


def _result(psv, risk_class, ped_cat, note):
    return {
        "psv": psv,
        "risk_class": risk_class,
        "ped_category": ped_cat,
        "intervals": {"external": None, "internal": None, "pressure_test": None},
        "inspector": "N/A",
        "note": note,
    }


def get_intervals(risk_class):
    """Return inspection intervals in months per AFS 2017:3."""
    if risk_class == "A":
        return {"external": 24, "internal": 72, "pressure_test": 144}
    elif risk_class == "B":
        return {"external": 36, "internal": 72, "pressure_test": None}
    elif risk_class == "Below B":
        return {"external": 72, "internal": None, "pressure_test": None}
    else:
        return {"external": None, "internal": None, "pressure_test": None}


def get_inspector(risk_class):
    """Return who may inspect per AFS 2017:3."""
    if risk_class == "A":
        return "Accredited body"
    elif risk_class == "B":
        return "Accredited body (int.) / Own (ext.)"
    elif risk_class == "Below B":
        return "Own inspection"
    else:
        return "N/A"


# ---------------------------------------------------------------------------
# Date helpers
# ---------------------------------------------------------------------------

def add_months(d, months):
    """Add months to a date, clamping day to valid range."""
    month = d.month - 1 + months
    year = d.year + month // 12
    month = month % 12 + 1
    import calendar
    max_day = calendar.monthrange(year, month)[1]
    day = min(d.day, max_day)
    return date(year, month, day)


def parse_date(s):
    """Parse YYYY-MM-DD string to date, or return None."""
    if not s or s.lower() in ("none", "n/a", "-", ""):
        return None
    try:
        return datetime.strptime(s.strip(), "%Y-%m-%d").date()
    except ValueError:
        return None


def format_date(d):
    """Format date as YYYY-MM-DD or '—'."""
    return d.strftime("%Y-%m-%d") if d else "\u2014"


def calculate_next_due(last_date, interval_months):
    """Calculate next due date from last inspection and interval."""
    if not last_date or not interval_months:
        return None
    return add_months(last_date, interval_months)


# ---------------------------------------------------------------------------
# Interactive mode
# ---------------------------------------------------------------------------

def ask(prompt, default=None, required=True):
    """Ask user for input with optional default."""
    if default:
        prompt = f"{prompt} [{default}]: "
    else:
        prompt = f"{prompt}: "
    val = input(prompt).strip()
    if not val and default:
        return default
    if not val and required:
        print("  (required)")
        return ask(prompt.rstrip(": ").rstrip(f" [{default}]"), default, required)
    return val


def ask_float(prompt, default=None):
    """Ask for a float value."""
    while True:
        val = ask(prompt, str(default) if default else None)
        try:
            return float(val)
        except ValueError:
            print("  Please enter a number.")


def ask_yes_no(prompt, default="yes"):
    """Ask yes/no question."""
    val = ask(prompt, default).lower()
    return val in ("yes", "y", "true", "1")


def interactive_classify_vessel():
    """Classify a single vessel interactively. Returns vessel dict or None."""
    print()
    vessel_id = ask("Vessel ID (e.g. PV-001)")
    description = ask("Description")
    location = ask("Location")
    manufacturer = ask("Manufacturer", required=False) or ""
    year = ask("Year of manufacture", required=False) or ""
    serial = ask("Serial number", required=False) or ""

    ps = ask_float("Design pressure PS (bar)")
    ts_max = ask("Max temperature TS (\u00b0C)", required=False) or ""
    volume = ask_float("Volume (litres)")

    medium = ask("Medium (e.g. compressed air, steam, ammonia)")
    fluid_group = lookup_fluid_group(medium)
    if fluid_group is None:
        print(f"\n  Medium '{medium}' not in database.")
        fg_input = ask("  Fluid group (1 = dangerous, 2 = non-dangerous)")
        fluid_group = 1 if fg_input.strip() == "1" else 2

    ce_marked = ask_yes_no("CE marked? (yes/no)", "yes")
    eu_doc = ask_yes_no("EU DoC on file? (yes/no)", "yes")

    last_insp_str = ask("Last inspection date (YYYY-MM-DD, or 'none')", "none",
                        required=False)
    last_inspection = parse_date(last_insp_str)
    last_type = ""
    if last_inspection:
        last_type = ask("Last inspection type (external/internal/pressure test)",
                        "external")

    # Classify
    result = classify_vessel(ps, volume, fluid_group)

    # Calculate next due dates
    next_external = calculate_next_due(last_inspection,
                                       result["intervals"]["external"])
    next_internal = calculate_next_due(last_inspection,
                                       result["intervals"]["internal"])
    next_pressure = calculate_next_due(last_inspection,
                                       result["intervals"]["pressure_test"])

    # Display result
    print()
    print("\u2500" * 54)
    print(f"  CLASSIFICATION RESULT \u2014 {vessel_id}")
    print("\u2500" * 54)
    print(f"  PS \u00d7 V:         {result['psv']:,.0f} bar\u00b7L")
    print(f"  Fluid Group:    {fluid_group} "
          f"({'Dangerous' if fluid_group == 1 else 'Non-dangerous'})")
    print(f"  PED Category:   {result['ped_category']}")
    print(f"  Risk Class:     {result['risk_class']}")
    print(f"  Inspector:      {result['inspector']}")
    if result["note"]:
        print(f"  Note:           {result['note']}")
    print()
    if result["intervals"]["external"]:
        print(f"  Inspection Intervals:")
        ext = result["intervals"]["external"]
        print(f"    External:       {ext} months"
              f" (next: {format_date(next_external)})")
        intr = result["intervals"]["internal"]
        if intr:
            print(f"    Internal:       {intr} months"
                  f" (next: {format_date(next_internal)})")
        pt = result["intervals"]["pressure_test"]
        if pt:
            print(f"    Pressure test:  {pt} months"
                  f" (next: {format_date(next_pressure)})")
    else:
        print("  No mandatory periodic inspection required.")
    print("\u2500" * 54)
    print()

    return {
        "vessel_id": vessel_id,
        "description": description,
        "location": location,
        "manufacturer": manufacturer,
        "year": year,
        "serial": serial,
        "ps": ps,
        "ts_max": ts_max,
        "volume": volume,
        "psv": result["psv"],
        "medium": medium,
        "fluid_group": fluid_group,
        "ped_category": result["ped_category"],
        "risk_class": result["risk_class"],
        "inspector": result["inspector"],
        "ce_marked": ce_marked,
        "eu_doc": eu_doc,
        "last_inspection": last_inspection,
        "last_type": last_type,
        "next_external": next_external,
        "next_internal": next_internal,
        "next_pressure": next_pressure,
        "intervals": result["intervals"],
        "note": result["note"],
    }


def interactive_mode():
    """Run interactive classification session."""
    print()
    print("=" * 54)
    print("  JDS Vessel Classification Tool")
    print("  AFS 2017:3 (consolidated)")
    print("=" * 54)
    print()
    print("Enter vessel data one at a time.")
    print("When done, type 'done' to generate the inventory.")
    print()

    vessels = []
    while True:
        try:
            vessel = interactive_classify_vessel()
            vessels.append(vessel)
        except (EOFError, KeyboardInterrupt):
            print("\n")
            break

        cont = ask("Add another vessel? (yes/no)", "yes")
        if cont.lower() not in ("yes", "y"):
            break

    if not vessels:
        print("No vessels entered. Exiting.")
        return

    # Ask for output details
    print()
    client = ask("Client name", "Internal")
    site = ask("Site name")
    doc_no = ask("Document number (e.g. JDS-LOG-MEC-006)", required=False) or "JDS-LOG-MEC-[NNN]"
    author = ask("Author", "N. Johansson")
    output_file = ask("Output file path", f"inventory-{site.lower().replace(' ', '-')}.md")

    md = generate_inventory_markdown(vessels, client, site, doc_no, author)

    with open(output_file, "w") as f:
        f.write(md)
    print(f"\nInventory written to: {output_file}")
    print(f"Vessels classified: {len(vessels)}")
    class_a = sum(1 for v in vessels if v["risk_class"] == "A")
    class_b = sum(1 for v in vessels if v["risk_class"] == "B")
    other = len(vessels) - class_a - class_b
    print(f"  Class A: {class_a}  |  Class B: {class_b}  |  Other: {other}")


# ---------------------------------------------------------------------------
# CSV mode
# ---------------------------------------------------------------------------

CSV_FIELDS = [
    "vessel_id", "description", "location", "manufacturer", "year", "serial",
    "ps_bar", "ts_max_c", "volume_l", "medium", "ce_marked", "eu_doc",
    "last_inspection", "last_type",
]


def read_csv(path):
    """Read vessel data from CSV. Returns list of vessel dicts."""
    vessels = []
    with open(path, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            ps = float(row.get("ps_bar", 0))
            volume = float(row.get("volume_l", 0))
            medium = row.get("medium", "").strip()
            fluid_group = lookup_fluid_group(medium)
            if fluid_group is None:
                fg = row.get("fluid_group", "2").strip()
                fluid_group = 1 if fg == "1" else 2

            result = classify_vessel(ps, volume, fluid_group)
            last_inspection = parse_date(row.get("last_inspection", ""))

            next_ext = calculate_next_due(last_inspection,
                                          result["intervals"]["external"])
            next_int = calculate_next_due(last_inspection,
                                          result["intervals"]["internal"])
            next_pt = calculate_next_due(last_inspection,
                                         result["intervals"]["pressure_test"])

            ce = row.get("ce_marked", "yes").strip().lower() in \
                ("yes", "y", "true", "1")
            doc = row.get("eu_doc", "yes").strip().lower() in \
                ("yes", "y", "true", "1")

            vessels.append({
                "vessel_id": row.get("vessel_id", "").strip(),
                "description": row.get("description", "").strip(),
                "location": row.get("location", "").strip(),
                "manufacturer": row.get("manufacturer", "").strip(),
                "year": row.get("year", "").strip(),
                "serial": row.get("serial", "").strip(),
                "ps": ps,
                "ts_max": row.get("ts_max_c", "").strip(),
                "volume": volume,
                "psv": result["psv"],
                "medium": medium,
                "fluid_group": fluid_group,
                "ped_category": result["ped_category"],
                "risk_class": result["risk_class"],
                "inspector": result["inspector"],
                "ce_marked": ce,
                "eu_doc": doc,
                "last_inspection": last_inspection,
                "last_type": row.get("last_type", "").strip(),
                "next_external": next_ext,
                "next_internal": next_int,
                "next_pressure": next_pt,
                "intervals": result["intervals"],
                "note": result["note"],
            })
    return vessels


# ---------------------------------------------------------------------------
# Quick classify mode
# ---------------------------------------------------------------------------

def quick_classify(ps, volume, medium="compressed air"):
    """Quick single-vessel classification to stdout."""
    fluid_group = lookup_fluid_group(medium)
    if fluid_group is None:
        print(f"Unknown medium '{medium}'. Assuming Group 2 (non-dangerous).")
        fluid_group = 2

    result = classify_vessel(ps, volume, fluid_group)

    print()
    print("=" * 50)
    print("  VESSEL CLASSIFICATION (AFS 2017:3)")
    print("=" * 50)
    print(f"  PS:             {ps} bar")
    print(f"  Volume:         {volume} L")
    print(f"  Medium:         {medium}")
    print(f"  PS \u00d7 V:         {result['psv']:,.0f} bar\u00b7L")
    print(f"  Fluid Group:    {fluid_group} "
          f"({'Dangerous' if fluid_group == 1 else 'Non-dangerous'})")
    print(f"  PED Category:   {result['ped_category']}")
    print(f"  Risk Class:     {result['risk_class']}")
    print(f"  Inspector:      {result['inspector']}")
    if result["note"]:
        print(f"  Note:           {result['note']}")
    print()
    if result["intervals"]["external"]:
        print(f"  Inspection Intervals:")
        print(f"    External:       {result['intervals']['external']} months")
        if result["intervals"]["internal"]:
            print(f"    Internal:       "
                  f"{result['intervals']['internal']} months")
        if result["intervals"]["pressure_test"]:
            print(f"    Pressure test:  "
                  f"{result['intervals']['pressure_test']} months")
    else:
        print("  No mandatory periodic inspection required.")
    print("=" * 50)


# ---------------------------------------------------------------------------
# Markdown inventory generator
# ---------------------------------------------------------------------------

def yn(val):
    return "Yes" if val else "No"


def fmt_months(m):
    return f"{m}" if m else "\u2014"


def generate_inventory_markdown(vessels, client, site, doc_no, author):
    """Generate a complete JDS inventory document from classified vessels."""
    today = date.today().strftime("%Y-%m-%d")
    lines = []

    def w(line=""):
        lines.append(line)

    # Header
    w(f"# Equipment Inventory \u2014 {site}")
    w()
    w("| | |")
    w("|---|---|")
    w(f"| **Document No.** | {doc_no} |")
    w("| **Revision** | A |")
    w(f"| **Date** | {today} |")
    w("| **Status** | CURRENT |")
    w(f"| **Author** | {author} |")
    w("| **Project** | JDS-PRJ-MEC-002 |")
    w(f"| **Client** | {client} |")
    w(f"| **Site** | {site} |")
    w()
    w("---")
    w()

    # Purpose
    w("## 1. Purpose")
    w()
    w(f"This register is the master inventory of all pressurised vessels at "
      f"{site}. Classification, risk class, and inspection intervals have been "
      f"**automatically calculated** per AFS 2017:3 (consolidated) using "
      f"`jds-classify.py`.")
    w()
    w("---")
    w()

    # Summary
    class_a = [v for v in vessels if v["risk_class"] == "A"]
    class_b = [v for v in vessels if v["risk_class"] == "B"]
    below_b = [v for v in vessels if v["risk_class"] == "Below B"]
    simple = [v for v in vessels if v["risk_class"] == "Simple PV"]
    not_cl = [v for v in vessels if v["risk_class"] in
              ("Not classified", "Not in scope")]

    w("## 2. Classification Summary")
    w()
    w("| Risk Class | Count | Inspection Regime |")
    w("|-----------|-------|-------------------|")
    w(f"| **Class A** | {len(class_a)} | "
      f"Accredited body: ext. 24 mo, int. 72 mo, press. test 144 mo |")
    w(f"| **Class B** | {len(class_b)} | "
      f"Accredited (int.) / own (ext.): ext. 36 mo, int. 72 mo |")
    w(f"| **Below B** | {len(below_b)} | Own inspection: ext. 72 mo |")
    w(f"| **Simple PV** | {len(simple)} | No mandatory periodic inspection |")
    w(f"| **Not classified** | {len(not_cl)} | Below regulatory threshold |")
    w(f"| **Total** | **{len(vessels)}** | |")
    w()
    w("---")
    w()

    # Table 1: Identification
    w("## 3. Vessel Identification")
    w()
    w("| Vessel ID | Description | Location | Manufacturer | Year | Serial No. |")
    w("|-----------|-------------|----------|-------------|------|-----------|")
    for v in vessels:
        w(f"| {v['vessel_id']} | {v['description']} | {v['location']} "
          f"| {v['manufacturer']} | {v['year']} | {v['serial']} |")
    w()
    w("---")
    w()

    # Table 2: Technical data
    w("## 4. Technical Data")
    w()
    w("| Vessel ID | PS (bar) | TS max (\u00b0C) "
      "| Volume (L) | PS\u00d7V (bar\u00b7L) | Medium |")
    w("|-----------|---------|-------------|"
      "-----------|--------------|--------|")
    for v in vessels:
        ts = v["ts_max"] if v["ts_max"] else "\u2014"
        w(f"| {v['vessel_id']} | {v['ps']:.1f} | {ts} "
          f"| {v['volume']:.0f} | {v['psv']:,.0f} | {v['medium']} |")
    w()
    w("---")
    w()

    # Table 3: Classification (auto-generated)
    w("## 5. Regulatory Classification (Auto-Generated)")
    w()
    w("> Classification calculated automatically by `jds-classify.py` "
      "per AFS 2017:3.")
    w()
    w("| Vessel ID | Fluid Grp | PED Cat. "
      "| Risk Class | Inspector | CE | DoC |")
    w("|-----------|----------|----------"
      "|-----------|-----------|----|----|")
    for v in vessels:
        w(f"| {v['vessel_id']} | {v['fluid_group']} "
          f"| {v['ped_category']} | **{v['risk_class']}** "
          f"| {v['inspector']} | {yn(v['ce_marked'])} "
          f"| {yn(v['eu_doc'])} |")
    w()
    w("---")
    w()

    # Table 4: Inspection schedule (auto-generated)
    w("## 6. Inspection Schedule (Auto-Generated)")
    w()
    w("> Intervals and next due dates calculated automatically "
      "from classification and last inspection.")
    w()
    w("| Vessel ID | Ext. (mo) | Int. (mo) "
      "| Press. (mo) | Last Insp. | Next Ext. | Next Int. |")
    w("|-----------|----------|----------"
      "|------------|-----------|----------|----------|")
    for v in vessels:
        ext_mo = fmt_months(v["intervals"]["external"])
        int_mo = fmt_months(v["intervals"]["internal"])
        pt_mo = fmt_months(v["intervals"]["pressure_test"])
        last = format_date(v["last_inspection"])
        next_e = format_date(v.get("next_external"))
        next_i = format_date(v.get("next_internal"))
        w(f"| {v['vessel_id']} | {ext_mo} | {int_mo} | {pt_mo} "
          f"| {last} | {next_e} | {next_i} |")
    w()

    # Overdue warning
    today_d = date.today()
    overdue = []
    for v in vessels:
        if v.get("next_external") and v["next_external"] < today_d:
            overdue.append((v["vessel_id"], "External", v["next_external"]))
        if v.get("next_internal") and v["next_internal"] < today_d:
            overdue.append((v["vessel_id"], "Internal", v["next_internal"]))
        if v.get("next_pressure") and v["next_pressure"] < today_d:
            overdue.append((v["vessel_id"], "Pressure test",
                            v["next_pressure"]))

    if overdue:
        w()
        w("### OVERDUE INSPECTIONS")
        w()
        w("| Vessel ID | Type | Was Due | Days Overdue |")
        w("|-----------|------|---------|-------------|")
        for vid, typ, due in overdue:
            days = (today_d - due).days
            w(f"| {vid} | {typ} | {format_date(due)} | **{days}** |")
        w()

    w()
    w("---")
    w()

    # Safety devices (placeholder)
    w("## 7. Safety Devices")
    w()
    w("| Device ID | Type | Protects | Set Pressure (bar) "
      "| Last Test | Next Test |")
    w("|-----------|------|----------|------------------- "
      "|-----------|-----------|")
    for v in vessels:
        if v["risk_class"] in ("A", "B", "Below B"):
            dev_id = v["vessel_id"].replace("PV", "SV")
            w(f"| {dev_id} | Safety valve | {v['vessel_id']} "
              f"| | | |")
    w()
    w("---")
    w()

    # Documentation checklist — split into groups of 6 (max 7 columns)
    w("## 8. Documentation Checklist")
    w()
    checks = [
        "Registered in inventory",
        "Nameplate photo on file",
        "EU DoC on file",
        "Risk class confirmed",
        "Safety devices documented",
        "Current certificate on file",
    ]
    max_per_table = 6  # 6 vessels + 1 Check column = 7 columns max
    for i in range(0, len(vessels), max_per_table):
        chunk = vessels[i:i + max_per_table]
        if len(vessels) > max_per_table:
            first_id = chunk[0]["vessel_id"]
            last_id = chunk[-1]["vessel_id"]
            w(f"### Vessels {first_id} to {last_id}")
            w()
        header = "| Check |"
        sep = "|-------|"
        for v in chunk:
            header += f" {v['vessel_id']} |"
            sep += "---|"
        w(header)
        w(sep)
        for check in checks:
            row = f"| {check} |"
            for v in chunk:
                row += " |"
            w(row)
        w()
    w("---")
    w()

    # Revision history
    w("## Revision History")
    w()
    w("| Rev | Date | Author | Description |")
    w("|-----|------|--------|-------------|")
    w(f"| A | {today} | {author} "
      f"| Initial inventory — {len(vessels)} vessels classified |")

    return "\n".join(lines) + "\n"


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="JDS Vessel Classification & Inventory Generator "
                    "(AFS 2017:3)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  Interactive mode:
    python3 scripts/jds-classify.py

  Quick classification:
    python3 scripts/jds-classify.py --quick --ps 11 --volume 1000
    python3 scripts/jds-classify.py --quick --ps 25 --volume 200 --medium ammonia

  From CSV file:
    python3 scripts/jds-classify.py --csv vessels.csv --output inventory.md
    python3 scripts/jds-classify.py --csv vessels.csv --client "ACME" --site "Workshop"

CSV format (header row required):
  vessel_id,description,location,manufacturer,year,serial,ps_bar,ts_max_c,volume_l,medium,ce_marked,eu_doc,last_inspection,last_type
        """,
    )

    parser.add_argument("--quick", action="store_true",
                        help="Quick single-vessel classification")
    parser.add_argument("--ps", type=float,
                        help="Design pressure in bar (for --quick)")
    parser.add_argument("--volume", type=float,
                        help="Volume in litres (for --quick)")
    parser.add_argument("--medium", default="compressed air",
                        help="Medium (default: compressed air)")

    parser.add_argument("--csv", metavar="FILE",
                        help="Read vessel data from CSV file")
    parser.add_argument("--output", "-o", metavar="FILE",
                        help="Output markdown file")
    parser.add_argument("--client", default="Internal",
                        help="Client name (for CSV mode)")
    parser.add_argument("--site", default="Site",
                        help="Site name (for CSV mode)")
    parser.add_argument("--doc-no", default="JDS-LOG-MEC-[NNN]",
                        help="JDS document number")
    parser.add_argument("--author", default="N. Johansson",
                        help="Author name")

    args = parser.parse_args()

    if args.quick:
        if not args.ps or not args.volume:
            parser.error("--quick requires --ps and --volume")
        quick_classify(args.ps, args.volume, args.medium)

    elif args.csv:
        if not os.path.exists(args.csv):
            print(f"Error: CSV file not found: {args.csv}")
            sys.exit(1)

        vessels = read_csv(args.csv)
        print(f"Read {len(vessels)} vessels from {args.csv}")

        for v in vessels:
            print(f"  {v['vessel_id']}: PS\u00d7V = {v['psv']:,.0f} bar\u00b7L "
                  f"\u2192 {v['risk_class']}")

        md = generate_inventory_markdown(
            vessels, args.client, args.site, args.doc_no, args.author
        )

        output = args.output or f"inventory-{args.site.lower().replace(' ', '-')}.md"
        with open(output, "w") as f:
            f.write(md)
        print(f"\nInventory written to: {output}")

    else:
        interactive_mode()


if __name__ == "__main__":
    main()
