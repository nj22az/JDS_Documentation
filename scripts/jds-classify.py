#!/usr/bin/env python3
"""
JDS Vessel Classification & Inventory Generator

Classifies pressurised vessels per AFS 2017:3 (consolidated with AFS 2019:1,
AFS 2020:10, AFS 2022:2) and generates JDS-compliant inventory documents with
automatic risk classification and inspection interval calculation.

Document chain — each step reads the previous document and generates the next:

    INVENTORY  →  PROGRAM  →  ROUND  →  REVIEW
    (Step 1)      (Step 2)    (Step 3)   (Step 4)

Usage:
    Step 1 — Inventory:
      python3 scripts/jds-classify.py --csv vessels.csv --output inventory.md
      python3 scripts/jds-classify.py  (interactive)

    Step 2 — Supervision Program (from inventory):
      python3 scripts/jds-classify.py --program --from inventory.md

    Step 3 — Supervision Round (from program):
      python3 scripts/jds-classify.py --round --from program.md

    Step 4 — Annual Review (from program):
      python3 scripts/jds-classify.py --review --from program.md

    Quick classification:
      python3 scripts/jds-classify.py --quick --ps 11 --volume 1000

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
# Classification logic per AFS 2017:3 (4 Kap. §10, Bilaga 1)
# ---------------------------------------------------------------------------

# Media that trigger the Class B exemption in §10
# "Tryckkärl för luft och kvävgas" — air and nitrogen vessels that would
# be Class B shall NOT belong to any class.
AIR_NITROGEN_MEDIA = {"compressed air", "air", "nitrogen"}

# Refrigeration/heat pump media — Class B vessels exempt per §10
REFRIGERANT_MEDIA = {
    "r134a", "r410a", "r32", "r404a", "r407c", "r22", "r290", "r600a",
    "r717",  # ammonia is Group 1 but listed here for refrigeration context
}


def lookup_fluid_group(medium):
    """Determine fluid group from medium name. Returns 1, 2, or None."""
    key = medium.strip().lower()
    return MEDIA_GROUPS.get(key, None)


def is_air_or_nitrogen(medium):
    """Check if medium is air or nitrogen (exempt from Class B per §10)."""
    return medium.strip().lower() in AIR_NITROGEN_MEDIA


def is_refrigerant(medium):
    """Check if medium is a refrigerant (exempt from Class B per §10)."""
    return medium.strip().lower() in REFRIGERANT_MEDIA


def classify_vessel(ps, volume, fluid_group, medium=""):
    """
    Classify a vessel per AFS 2017:3 (4 Kap. §10) based on PS, volume,
    fluid group, and medium.

    Returns dict with: psv, risk_class, ped_category, driftprov_interval,
    examination_interval, inspector, note, exemptions.
    """
    psv = ps * volume
    medium_lower = medium.strip().lower()

    # Check minimum threshold: PS must exceed 0.5 bar
    if ps <= 0.5:
        return _result(psv, "Not in scope", "N/A",
                       "Below 0.5 bar — outside AFS 2017:3 scope")

    # Group 2a liquids at ≤65°C: no class (§10 last paragraph)
    # We can't fully check this without temperature, so skip for now

    if fluid_group == 1:
        # Group 1a — dangerous fluids (4 Kap. §10 table, gas column)
        if volume > 1 and ps > 0.5:
            if psv > 1000:
                risk_class = "A"
                ped_cat = "IV" if psv > 3000 else "III"
            else:
                risk_class = "B"
                ped_cat = "II"
        elif volume > 0.1 and volume <= 1 and ps > 200:
            risk_class = "A"
            ped_cat = "IV"
        elif psv > 50:
            risk_class = "B"
            ped_cat = "I"
        else:
            return _result(psv, "Not classified", "N/A",
                           "Below classification threshold (Group 1a)")
    else:
        # Group 2a — non-dangerous fluids (4 Kap. §10 table, gas column)
        if volume > 1 and ps > 0.5:
            if psv > 10000:
                risk_class = "A"
                ped_cat = "IV"
            elif psv > 1000:
                # Would be Class B, but check exemptions
                risk_class = "B"
                ped_cat = "II"
            elif psv > 200:
                risk_class = "Below threshold"
                ped_cat = "I"
                return _result(psv, "Below threshold", "I",
                               "PS×V 200-1000: below Class B threshold "
                               "for Group 2a gases")
            elif psv > 50:
                return _result(psv, "Below threshold", "Art. 4.3",
                               "PS×V 50-200: below classification")
            else:
                return _result(psv, "Not classified", "N/A",
                               "Below classification threshold (Group 2a)")
        elif volume > 0.1 and volume <= 1 and ps > 1000:
            risk_class = "A"
            ped_cat = "IV"
        else:
            return _result(psv, "Not classified", "N/A",
                           "Below classification threshold (Group 2a)")

    # Apply §10 exemptions for Class B vessels
    exemptions = []
    if risk_class == "B":
        if is_air_or_nitrogen(medium):
            exemptions.append("Air/nitrogen Class B exemption (§10)")
            return _result(psv, "Exempt (air/N2)", ped_cat,
                           "Air/nitrogen vessels: Class B exempt per "
                           "4 Kap. §10 — no periodic inspection required")
        if is_refrigerant(medium) and fluid_group == 2:
            exemptions.append("Refrigerant Class B exemption (§10)")
            return _result(psv, "Exempt (refrig.)", ped_cat,
                           "Refrigerant vessels (Group 2a): Class B exempt "
                           "per 4 Kap. §10 — no periodic inspection required")

    driftprov = get_driftprov_interval(risk_class, medium_lower)
    examination = get_examination_info(risk_class)
    inspector = get_inspector(risk_class)

    return {
        "psv": psv,
        "risk_class": risk_class,
        "ped_category": ped_cat,
        "driftprov_interval": driftprov,
        "examination_interval": examination,
        "intervals": {  # backward-compatible
            "external": driftprov,
            "internal": examination.get("base") if examination else None,
            "pressure_test": None,
        },
        "inspector": inspector,
        "note": None,
        "exemptions": exemptions,
    }


def _result(psv, risk_class, ped_cat, note):
    return {
        "psv": psv,
        "risk_class": risk_class,
        "ped_category": ped_cat,
        "driftprov_interval": None,
        "examination_interval": None,
        "intervals": {"external": None, "internal": None,
                      "pressure_test": None},
        "inspector": "N/A",
        "note": note,
        "exemptions": [],
    }


def get_driftprov_interval(risk_class, medium=""):
    """
    Return driftprov (operational test) base interval in months
    per Bilaga 1, §1.4.1.
    """
    if risk_class not in ("A", "B"):
        return None

    # Specific equipment types with 4-year interval
    if medium in AIR_NITROGEN_MEDIA:
        return 48  # 4 years — air, nitrogen, noble gas
    if medium in REFRIGERANT_MEDIA:
        return 48  # 4 years — refrigeration/heat pump
    if medium in ("argon", "helium", "neon", "krypton", "xenon"):
        return 48  # 4 years — noble gases
    if medium in ("lpg", "propane", "butane"):
        return 48  # 4 years — LPG storage

    # Default: "Övriga tryckkärl och vakuumkärl" = 2 years
    return 24  # 2 years


def get_examination_info(risk_class):
    """
    Return internal/external examination info per Bilaga 1, §2.2.
    Only Class A requires in- och utvändig undersökning.
    Returns dict with base interval and conditions, or None.
    """
    if risk_class != "A":
        return None

    return {
        "base": 48,  # 4 years (§2.2.2) — standard base interval
        "min": 6,    # 6 months (§2.2.5) — worst case
        "max": 120,  # 10 years (§2.2.8) — best case for vessels
        "max_cistern": 144,  # 12 years (§2.2.9) — cisterns only
        "note": "Condition-based: 4 years base, extendable to "
                "6/8/10 years by inspection body based on condition. "
                "Reducible to 2/1/0.5 years if condition deteriorates.",
    }


def get_intervals(risk_class):
    """Return inspection intervals in months (backward-compatible)."""
    if risk_class == "A":
        return {"external": 24, "internal": 48, "pressure_test": None}
    elif risk_class == "B":
        return {"external": 24, "internal": None, "pressure_test": None}
    else:
        return {"external": None, "internal": None, "pressure_test": None}


def get_inspector(risk_class):
    """Return who may inspect per AFS 2017:3."""
    if risk_class == "A":
        return "Accredited body (Type A)"
    elif risk_class == "B":
        return "Accredited body (Type A or B)"
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
# Markdown table parser — reads data from generated JDS documents
# ---------------------------------------------------------------------------

def parse_table_row(line):
    """Parse a markdown table row into a list of cell values."""
    line = line.strip()
    if line.startswith("|"):
        line = line[1:]
    if line.endswith("|"):
        line = line[:-1]
    return [cell.strip() for cell in line.split("|")]


def is_separator_row(line):
    """Check if a line is a markdown table separator (|---|---|)."""
    return all(c in "-| :" for c in line.strip())


def extract_tables(filepath):
    """Extract all markdown tables from a file as list of (headers, rows)."""
    with open(filepath, "r", encoding="utf-8") as f:
        lines = f.readlines()

    tables = []
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        # Look for table header: line with | that is followed by separator
        if (line.startswith("|") and i + 1 < len(lines)
                and is_separator_row(lines[i + 1])):
            headers = parse_table_row(line)
            i += 2  # skip header and separator
            rows = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                if not is_separator_row(lines[i]):
                    row = parse_table_row(lines[i])
                    # Pad row to match header length
                    while len(row) < len(headers):
                        row.append("")
                    rows.append(dict(zip(headers, row)))
                i += 1
            tables.append((headers, rows))
        else:
            i += 1
    return tables


def extract_metadata(filepath):
    """Extract JDS metadata block (key-value pairs) from a document."""
    meta = {}
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line.startswith("| **") and "|" in line[3:]:
                parts = parse_table_row(line)
                if len(parts) >= 2:
                    key = parts[0].replace("**", "").strip()
                    val = parts[1].replace("**", "").strip()
                    if key and val:
                        meta[key] = val
    return meta


def parse_inventory_file(filepath):
    """
    Parse a JDS inventory document and return vessel data.

    Returns (metadata_dict, list_of_vessel_dicts).
    """
    meta = extract_metadata(filepath)
    tables = extract_tables(filepath)

    # Build vessel dict by joining tables on Vessel ID
    vessels_by_id = {}

    for headers, rows in tables:
        for row in rows:
            vid = row.get("Vessel ID", "").strip()
            if not vid or vid.startswith("—") or vid == "":
                continue
            if vid not in vessels_by_id:
                vessels_by_id[vid] = {"vessel_id": vid}
            v = vessels_by_id[vid]

            # Identification table
            if "Description" in row:
                v["description"] = row.get("Description", "")
            if "Location" in row:
                v["location"] = row.get("Location", "")
            if "Manufacturer" in row:
                v["manufacturer"] = row.get("Manufacturer", "")
            if "Year" in row:
                v["year"] = row.get("Year", "")
            if "Serial No." in row:
                v["serial"] = row.get("Serial No.", "")

            # Technical data table
            if "PS (bar)" in row:
                try:
                    v["ps"] = float(row["PS (bar)"])
                except (ValueError, TypeError):
                    v["ps"] = 0
            if "Volume (L)" in row:
                try:
                    v["volume"] = float(row["Volume (L)"].replace(",", ""))
                except (ValueError, TypeError):
                    v["volume"] = 0
            if "Medium" in row:
                v["medium"] = row.get("Medium", "")

            # Classification table (handles both inventory and program formats)
            if "Risk Class" in row:
                rc = row.get("Risk Class", "").replace("**", "").strip()
                v["risk_class"] = rc
            if "Class" in row and "risk_class" not in v:
                rc = row.get("Class", "").replace("**", "").strip()
                if rc and rc not in ("", "Class"):
                    v["risk_class"] = rc
            if "Fluid Grp" in row:
                try:
                    v["fluid_group"] = int(row["Fluid Grp"])
                except (ValueError, TypeError):
                    v["fluid_group"] = 2
            if "PED Cat." in row:
                v["ped_category"] = row.get("PED Cat.", "")
            if "Inspector" in row:
                v["inspector"] = row.get("Inspector", "")

            # Inspection schedule table
            if "Ext. (mo)" in row:
                v["intervals"] = {
                    "external": _parse_int(row.get("Ext. (mo)")),
                    "internal": _parse_int(row.get("Int. (mo)")),
                    "pressure_test": _parse_int(row.get("Press. (mo)")),
                }
            if "Last Insp." in row:
                v["last_inspection"] = parse_date(row.get("Last Insp.", ""))
            if "Next Ext." in row:
                v["next_external"] = parse_date(row.get("Next Ext.", ""))

    # Ensure all vessels have required fields with defaults
    vessels = []
    for vid in sorted(vessels_by_id.keys()):
        v = vessels_by_id[vid]
        v.setdefault("description", "")
        v.setdefault("location", "")
        v.setdefault("manufacturer", "")
        v.setdefault("year", "")
        v.setdefault("serial", "")
        v.setdefault("ps", 0)
        v.setdefault("volume", 0)
        v.setdefault("medium", "")
        v.setdefault("risk_class", "")
        v.setdefault("fluid_group", 2)
        v.setdefault("ped_category", "")
        v.setdefault("inspector", "")
        # If intervals not parsed from table, derive from risk class
        if "intervals" not in v and v.get("risk_class"):
            v["intervals"] = get_intervals(v["risk_class"])
        v.setdefault("intervals",
                      {"external": None, "internal": None, "pressure_test": None})
        # If inspector not set, derive from risk class
        if not v.get("inspector") and v.get("risk_class"):
            v["inspector"] = get_inspector(v["risk_class"])
        v.setdefault("last_inspection", None)
        v.setdefault("next_external", None)
        v["psv"] = v["ps"] * v["volume"]
        vessels.append(v)

    return meta, vessels


def _parse_int(s):
    """Parse string to int, returning None for non-numeric."""
    if not s:
        return None
    s = s.strip().replace(",", "")
    if s in ("\u2014", "—", "-", "N/A", ""):
        return None
    try:
        return int(s)
    except ValueError:
        return None


def parse_program_file(filepath):
    """
    Parse a JDS supervision program document.

    Returns (metadata_dict, list_of_vessel_dicts).
    Reads the equipment register summary table from Section 2.
    """
    meta = extract_metadata(filepath)
    tables = extract_tables(filepath)

    vessels = []
    for headers, rows in tables:
        if "Vessel ID" in headers and "Class" in headers:
            for row in rows:
                vid = row.get("Vessel ID", "").strip()
                if not vid or vid.startswith("—"):
                    continue
                risk_class = row.get("Class", "").replace("**", "").strip()
                vessels.append({
                    "vessel_id": vid,
                    "description": row.get("Description", ""),
                    "location": row.get("Location", ""),
                    "risk_class": risk_class,
                    "medium": row.get("Medium", ""),
                    "ps": 0, "volume": 0, "psv": 0,
                    "fluid_group": 2,
                    "intervals": get_intervals(risk_class),
                })
            break  # use the first matching table

    return meta, vessels


# ---------------------------------------------------------------------------
# Check schedule definitions per risk class
# ---------------------------------------------------------------------------

CHECKS_DAILY = [
    ("Pressure gauge within normal range", "Visual reading"),
    ("Temperature within design limits", "Visual reading"),
    ("No audible leaks or unusual noise", "Listening"),
    ("Control system: no standing alarms", "Control panel check"),
]

CHECKS_WEEKLY = [
    ("No visible leaks at flanges, valves, fittings", "Walk-around visual"),
    ("Safety valves not gagged or blocked", "Visual check"),
    ("Drain valves functional (operate drain)", "Manual operation"),
    ("Condensate drainage working", "Visual / operate trap"),
]

CHECKS_MONTHLY = [
    ("External surface: no corrosion, dents, cracks", "Close visual"),
    ("Insulation intact, no moisture indicators", "Visual check"),
    ("Support and foundation integrity", "Visual check"),
    ("Safety valve seal intact", "Visual check"),
    ("Vessel access clear and safe", "Visual check"),
]

CHECKS_QUARTERLY = [
    ("Nameplate legible and not obscured", "Visual check"),
    ("Pressure switch function test", "Simulate / trip test"),
    ("Paint / coating condition", "Visual check"),
    ("Review open findings from previous rounds", "Register review"),
]

CHECKS_ANNUAL = [
    ("Safety valve function test (lift test)", "On-line or bench test"),
    ("Equipment register accuracy verification", "Compare to physical"),
    ("Competence records current", "Record review"),
    ("Formal inspection schedule review", "Inspection plan review"),
]


def get_check_schedule(risk_class):
    """Return which check categories apply to a risk class."""
    if risk_class == "A":
        return {
            "daily": CHECKS_DAILY,
            "weekly": CHECKS_WEEKLY,
            "monthly": CHECKS_MONTHLY,
            "quarterly": CHECKS_QUARTERLY,
            "annual": CHECKS_ANNUAL,
        }
    elif risk_class == "B":
        return {
            "daily": CHECKS_DAILY[:2],  # gauge + temp only
            "weekly": CHECKS_WEEKLY,
            "monthly": CHECKS_MONTHLY,
            "quarterly": CHECKS_QUARTERLY[:1] + CHECKS_QUARTERLY[2:3],
            "annual": CHECKS_ANNUAL,
        }
    elif risk_class == "Below B":
        return {
            "weekly": CHECKS_WEEKLY[:2],  # leak + safety valve
            "monthly": CHECKS_MONTHLY[:3],  # surface + insulation + support
            "annual": CHECKS_ANNUAL,
        }
    else:  # Simple PV, not classified
        return {
            "monthly": CHECKS_MONTHLY[:1],  # surface only
            "annual": CHECKS_ANNUAL[1:3],  # register + competence
        }


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
    result = classify_vessel(ps, volume, fluid_group, medium)

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

            result = classify_vessel(ps, volume, fluid_group, medium)
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

    result = classify_vessel(ps, volume, fluid_group, medium)

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

    # Next step
    w("## 9. Next Step")
    w()
    w("This inventory is **Step 1** of the Vessel Supervision System.")
    w()
    w("```")
    w("[INVENTORY]  →  PROGRAM  →  ROUND  →  REVIEW")
    w(" (you are       (next)")
    w("  here)")
    w("```")
    w()
    w("To generate the supervision program from this inventory, run:")
    w()
    w(f"```")
    w(f"python3 scripts/jds-classify.py --program "
      f"--from [this-file.md] --output [program.md]")
    w(f"```")
    w()
    w("The script will read this inventory and create a supervision "
      "program pre-filled with all vessels, risk-based check schedules, "
      "and inspection intervals.")
    w()
    w("---")
    w()

    # Revision history
    w("## Revision History")
    w()
    w("| Rev | Date | Author | Description |")
    w("|-----|------|--------|-------------|")
    w(f"| A | {today} | {author} "
      f"| Initial inventory \u2014 {len(vessels)} vessels classified |")

    return "\n".join(lines) + "\n"


# ---------------------------------------------------------------------------
# Program generator — Step 2 (reads inventory, generates program)
# Compliant with AFS 2017:3: 2 Kap. §6, 4 Kap. §§14-19, Bilaga 1
# ---------------------------------------------------------------------------

def generate_program_markdown(vessels, client, site, doc_no, author,
                              source_doc=""):
    """Generate a supervision program pre-filled from inventory data."""
    today = date.today().strftime("%Y-%m-%d")
    next_year = date.today().year + 1
    lines = []

    def w(line=""):
        lines.append(line)

    # Separate vessels by regulatory status
    class_ab = [v for v in vessels if v["risk_class"] in ("A", "B")]
    class_a = [v for v in vessels if v["risk_class"] == "A"]
    class_b = [v for v in vessels if v["risk_class"] == "B"]
    exempt = [v for v in vessels
              if v["risk_class"].startswith("Exempt")]
    below = [v for v in vessels
             if v["risk_class"] in ("Below threshold", "Simple PV",
                                    "Not classified", "Not in scope")]

    all_supervised = class_ab + exempt  # all that need some supervision
    has_daily = len(class_ab) > 0

    # Header
    w(f"# Supervision Program \u2014 {site}")
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
    w(f"| **Program ID** | SP-[NNN] |")
    w(f"| **Source** | {source_doc} |")
    w()
    w("---")
    w()

    # Document chain
    w("## 1. Document Chain")
    w()
    w("```")
    w("INVENTORY  \u2192  [PROGRAM]  \u2192  ROUND  \u2192  REVIEW")
    w("(Step 1)       (you are      (next)")
    w("                here)")
    w("```")
    w()
    w(f"**Source document:** {source_doc}")
    w()
    w("---")
    w()

    # Regulatory basis
    w("## 2. Regulatory Basis")
    w()
    w("This program satisfies the requirements of **AFS 2017:3** "
      "(consolidated with AFS 2019:1, AFS 2020:10, AFS 2022:2):")
    w()
    w("| Requirement | AFS 2017:3 | Status |")
    w("|------------|-----------|--------|")
    w("| Documented supervision routines | 4 Kap. \u00a717 | "
      "This document |")
    w("| Mandatory minimum checks (6 points) | 2 Kap. \u00a76 | "
      "Section 5 |")
    w("| Annual evaluation and revision | 4 Kap. \u00a717 | "
      "Section 12 |")
    w("| Assigned responsible person | 4 Kap. \u00a717 | "
      "Section 9 |")
    w("| Coordination person | 4 Kap. \u00a714 | "
      "Section 9 |")
    w("| Equipment register | 4 Kap. \u00a715 | "
      "Section 3 |")
    w("| Monitoring requirements | 4 Kap. \u00a716 | "
      "Section 4 |")
    w("| Recurring inspection schedule | 5 Kap., Bilaga 1 | "
      "Section 6 |")
    w("| Deviation reports | 4 Kap. \u00a719 | "
      "Section 10 |")
    w("| Lifetime journal | 4 Kap. \u00a718 | "
      "Section 11 |")
    w()
    w("> **Non-compliance sanction:** 10,000\u2013100,000 SEK for operating "
      "Class A/B equipment without documented supervision routines "
      "(4 Kap. \u00a717).")
    w()
    w("---")
    w()

    # Scope
    w("## 3. Equipment Register (4 Kap. \u00a715)")
    w()
    w(f"Register of all pressurised equipment at {site}:")
    w()
    w("| Vessel ID | Description | Location "
      "| Class | Medium | Inspector |")
    w("|-----------|-------------|----------"
      "|-------|--------|-----------|")
    for v in vessels:
        rc = v["risk_class"]
        insp = v.get("inspector", get_inspector(rc))
        w(f"| {v['vessel_id']} | {v.get('description', '')} "
          f"| {v.get('location', '')} "
          f"| **{rc}** | {v.get('medium', '')} | {insp} |")
    w()

    w(f"**Class A:** {len(class_a)} vessels "
      "(accredited inspection body required)")
    w(f"**Class B:** {len(class_b)} vessels")
    w(f"**Exempt (air/N2/refrigerant):** {len(exempt)} vessels "
      "(Class B exempt per 4 Kap. \u00a710)")
    w(f"**Below threshold:** {len(below)} vessels")
    w()
    w("---")
    w()

    # Monitoring requirements (§16)
    w("## 4. Monitoring Requirements (4 Kap. \u00a716)")
    w()
    if class_ab:
        w("Class A and B vessels must be **continuously monitored** "
          "(\u00a716). The operator must be able to immediately reach "
          "the vessel and determine if it is safe to remain pressurised.")
        w()
        w("If periodic monitoring is used instead (per documented risk "
          "assessment), the following must be documented:")
        w()
        w("1. How operators are alerted to safety-related alarms")
        w("2. The response time (inst\u00e4llelsetid) for safety-related alarms")
        w()
        w("| Vessel ID | Monitoring Type | Alarm System | Response Time |")
        w("|-----------|----------------|-------------|--------------|")
        for v in class_ab:
            w(f"| {v['vessel_id']} | Continuous / Periodic | "
              f"[Describe] | [Minutes] |")
        w()
    else:
        w("No Class A or B vessels \u2014 no mandatory monitoring "
          "requirements apply.")
        w()
    w("---")
    w()

    # Mandatory minimum checks (§6)
    w("## 5. Mandatory Supervision Checks (2 Kap. \u00a76)")
    w()
    w("AFS 2017:3 \u00a76 defines **six mandatory minimum checks**. "
      "Every supervision round must verify all six points:")
    w()
    w("| # | \u00a76 Requirement | Check | Method |")
    w("|---|--------------|-------|--------|")
    w("| 1 | Equipment functions satisfactorily | "
      "Pressure/temperature within range, no abnormal noise/vibration | "
      "Gauge reading, listening |")
    w("| 2 | No leaks have occurred | "
      "Check flanges, valves, fittings, weld joints | "
      "Visual walk-around |")
    w("| 3 | No harmful external or internal impact | "
      "Surface condition, insulation, supports, corrosion | "
      "Close visual inspection |")
    w("| 4 | No other faults or deviations | "
      "Safety devices, drainage, general condition | "
      "Functional check |")
    w("| 5 | Equipment correctly marked | "
      "Nameplates, valve tags, emergency stops legible | "
      "Visual check |")
    w("| 6 | Prescribed inspections carried out | "
      "Inspection certificate current, not overdue | "
      "Register review |")
    w()
    w("> These six points are the **legal minimum** per 2 Kap. \u00a76 "
      "and must be traceable in every supervision record.")
    w()
    w("---")
    w()

    # Supervision schedule
    w("## 6. Recurring Inspection Schedule (Bilaga 1)")
    w()
    if class_ab:
        w("### 6.1 Driftprov (Operational Test)")
        w()
        w("Base intervals per Bilaga 1, \u00a71.4.1. Actual interval "
          "determined by accredited inspection body at each inspection.")
        w()
        w("| Vessel ID | Class | Medium | Base Interval | Max |")
        w("|-----------|-------|--------|-------------|-----|")
        for v in class_ab:
            dp = v.get("driftprov_interval") or \
                get_driftprov_interval(v["risk_class"],
                                      v.get("medium", "").lower())
            dp_yr = f"{dp // 12} years" if dp else "\u2014"
            w(f"| {v['vessel_id']} | {v['risk_class']} "
              f"| {v.get('medium', '')} | {dp_yr} | 4 years |")
        w()
        w("**Extended interval (\u00a71.4.2):** Possible if safety equipment "
          "functioned at the two previous tests. Max 4 years.")
        w()
        w("**Shortened interval (\u00a71.4.3):** If safety equipment "
          "did NOT function, next interval is **halved**.")
        w()

        if class_a:
            w("### 6.2 Internal/External Examination (Class A only)")
            w()
            w("Condition-based interval determined by inspection body "
              "per Bilaga 1, \u00a72.2:")
            w()
            w("| Interval | Conditions |")
            w("|----------|-----------|")
            w("| 4 years | Base: not fire-affected, >5yr life, "
              "low crack risk, mild environment |")
            w("| 2 years | 4-year not met, but stable condition |")
            w("| 1 year | 2-year not met, but safe for 1 year |")
            w("| 6 months | 1-year not met, but safe for 6 months |")
            w("| 6 years | After clean 4-year, no fatigue/creep |")
            w("| 8 years | After 2 clean 4/6-year inspections |")
            w("| 10 years | After 2 progressively longer, clean |")
            w("| 12 years | Cisterns only, after clean 6-year |")
            w()
            w("| Vessel ID | Current Interval | Next Due |")
            w("|-----------|-----------------|----------|")
            for v in class_a:
                w(f"| {v['vessel_id']} | [Per inspection body] | "
                  f"[Expiry month] |")
            w()
    else:
        w("No Class A or B vessels \u2014 no mandatory recurring "
          "inspections required.")
        w()
    w("---")
    w()

    # Supervision round schedule
    w("## 7. Supervision Round Schedule")
    w()

    if has_daily:
        w("### 7.1 Daily / Per-Shift Checks")
        w()
        w(f"**Applies to:** "
          f"{', '.join(v['vessel_id'] for v in class_ab)}")
        w()
        w("| # | Check (\u00a76 ref) | Method |")
        w("|---|---------------|--------|")
        for i, (check, method) in enumerate(CHECKS_DAILY, 1):
            w(f"| {i} | {check} | {method} |")
        w()
        w("**Performed by:** [Name / role]")
        w("**Record:** Shift log")
        w()

        w("### 7.2 Weekly Checks")
        w()
        w(f"**Applies to:** "
          f"{', '.join(v['vessel_id'] for v in class_ab)}")
        w()
        w("| # | Check (\u00a76 ref) | Method |")
        w("|---|---------------|--------|")
        for i, (check, method) in enumerate(CHECKS_WEEKLY, 1):
            w(f"| {i} | {check} | {method} |")
        w()
        w("**Performed by:** [Name / role]")
        w("**Record:** Weekly check sheet")
        w()

    w("### 7.3 Monthly Checks (Formal Supervision Round)")
    w()
    w(f"**Applies to:** "
      f"{', '.join(v['vessel_id'] for v in all_supervised)}")
    w()
    w("| # | Check (\u00a76 ref) | Method |")
    w("|---|---------------|--------|")
    for i, (check, method) in enumerate(CHECKS_MONTHLY, 1):
        w(f"| {i} | {check} | {method} |")
    w()
    w("**Performed by:** [Name / role]")
    w("**Record:** Supervision round record (JDS-TMP-LOG-006)")
    w()

    if class_ab:
        w("### 7.4 Quarterly Checks")
        w()
        w(f"**Applies to:** "
          f"{', '.join(v['vessel_id'] for v in class_ab)}")
        w()
        w("| # | Check (\u00a76 ref) | Method |")
        w("|---|---------------|--------|")
        for i, (check, method) in enumerate(CHECKS_QUARTERLY, 1):
            w(f"| {i} | {check} | {method} |")
        w()
        w("**Performed by:** [Name / role]")
        w("**Record:** Supervision round record (JDS-TMP-LOG-006)")
        w()

    w("### 7.5 Annual Checks")
    w()
    w(f"**Applies to:** all vessels")
    w()
    w("| # | Check | Method |")
    w("|---|-------|--------|")
    for i, (check, method) in enumerate(CHECKS_ANNUAL, 1):
        w(f"| {i} | {check} | {method} |")
    w()
    w("**Performed by:** Program manager / competent person")
    w("**Record:** Annual review record (JDS-TMP-LOG-007)")
    w()
    w("---")
    w()

    # Per-vessel assignment
    w("## 8. Per-Vessel Check Assignment")
    w()
    w("| Vessel ID | Class | Daily | Weekly | Monthly | Quarterly | Annual |")
    w("|-----------|-------|-------|--------|---------|-----------|--------|")
    for v in vessels:
        rc = v["risk_class"]
        if rc in ("Not classified", "Not in scope"):
            w(f"| {v['vessel_id']} | {rc} | \u2014 | \u2014 "
              f"| \u2014 | \u2014 | \u2014 |")
            continue
        sched = get_check_schedule(rc)
        d = "Yes" if "daily" in sched else "\u2014"
        wk = "Yes" if "weekly" in sched else "\u2014"
        m = "Yes" if "monthly" in sched else "\u2014"
        q = "Yes" if "quarterly" in sched else "\u2014"
        a = "Yes" if "annual" in sched else "\u2014"
        w(f"| {v['vessel_id']} | **{rc}** "
          f"| {d} | {wk} | {m} | {q} | {a} |")
    w()
    w("---")
    w()

    # Personnel (§14, §17)
    w("## 9. Personnel and Responsibilities (4 Kap. \u00a714, \u00a717)")
    w()
    w("### 9.1 Assigned Roles")
    w()
    w("| Role | AFS Ref | Name | Responsibility |")
    w("|------|---------|------|---------------|")
    w("| **Coordination person** | 4 Kap. \u00a714 | [Name] | "
      "Plans and coordinates all work on Class A/B equipment |")
    w("| **Supervision responsible** | 4 Kap. \u00a717 | [Name] | "
      "Ensures supervision is carried out and documented |")
    w("| Daily/weekly supervisor | 2 Kap. \u00a76 | [Name] | "
      "Performs daily and weekly checks |")
    w("| Monthly supervisor | 2 Kap. \u00a76 | [Name] | "
      "Performs monthly formal rounds |")
    w("| Program manager | 4 Kap. \u00a717 | [Name] | "
      "Annual evaluation, revision, findings management |")
    w()
    w("### 9.2 Competence Requirements")
    w()
    w("All personnel must have documented competence per "
      "JDS-PRO-009. Competence records must be maintained and "
      "refreshed.")
    w()
    w("---")
    w()

    # Deviation reports (§19)
    w("## 10. Deviation Reports (4 Kap. \u00a719)")
    w()
    w("When Class A/B equipment is found to be damaged or "
      "deteriorated, a **deviation report** must be created containing:")
    w()
    w("| # | Required Content | Description |")
    w("|---|-----------------|-------------|")
    w("| 1 | Damage/deterioration | What was found |")
    w("| 2 | How discovered | Which observation or check |")
    w("| 3 | Date of discovery | When it was found |")
    w("| 4 | Action needed | What must be done |")
    w("| 5 | Cause | Root cause (if not obvious) |")
    w("| 6 | Date of action | When the repair/fix was completed |")
    w("| 7 | Reporter | Who made the report |")
    w()
    w("Deviation reports are managed per **JDS-PRO-008** "
      "(Corrective Action Procedure) and filed in the client's "
      "`findings/` folder.")
    w()
    w("### Severity Classification")
    w()
    w("| Severity | Definition | Action | Timeline |")
    w("|----------|-----------|--------|----------|")
    w("| **Critical** | Immediate safety risk "
      "| Out of service, escalate | Immediate |")
    w("| **Major** | Will deteriorate to critical "
      "| Plan repair, close monitoring | 30 days |")
    w("| **Minor** | Noted, no immediate risk "
      "| Monitor, plan maintenance | 90 days |")
    w("| **Observation** | Worth monitoring "
      "| Note, observe trend | Next round |")
    w()
    w("---")
    w()

    # Lifetime journal (§18)
    w("## 11. Lifetime Journal (4 Kap. \u00a718)")
    w()
    if class_ab:
        w("Class A/B equipment with limited lifetime must have a "
          "**journal showing remaining lifetime**. If parts have "
          "different lifetimes, each part must be tracked separately.")
        w()
        w("| Vessel ID | Limited Lifetime | Journal Ref | Notes |")
        w("|-----------|-----------------|-------------|-------|")
        for v in class_ab:
            w(f"| {v['vessel_id']} | Yes / No / Unknown | [Ref] | |")
        w()
        w("> Equipment that has reached its documented lifetime may "
          "only remain pressurised if an analysis demonstrating "
          "extended lifetime has been conducted and documented.")
    else:
        w("No Class A/B vessels \u2014 no lifetime journal required.")
    w()
    w("---")
    w()

    # Program review (§17)
    w("## 12. Program Review (4 Kap. \u00a717)")
    w()
    w("This program must be **evaluated and revised at least once "
      "per year** (4 Kap. \u00a717). Additional review triggers:")
    w()
    w("- Equipment added, removed, or modified")
    w("- Operating conditions changed significantly")
    w("- Regulatory requirements changed")
    w("- Significant finding or incident occurred")
    w("- Revision inspection (revisionskontroll) performed")
    w()
    w(f"**Next review due:** {next_year}-01-31")
    w()
    w("---")
    w()

    # Approval
    w("## 13. Approval")
    w()
    w("| | |")
    w("|---|---|")
    w("| **Prepared by** | [Name, role] |")
    w("| **Reviewed by** | [Name, role] |")
    w("| **Approved by** | [Operator/employer, role] |")
    w(f"| **Approval date** | {today} |")
    w(f"| **Next review due** | {next_year}-01-31 |")
    w()
    w("---")
    w()

    # Next step
    w("## 14. Next Step")
    w()
    w("```")
    w("INVENTORY  \u2192  [PROGRAM]  \u2192  ROUND  \u2192  REVIEW")
    w("                (done)      (next)")
    w("```")
    w()
    w("To generate a supervision round record:")
    w()
    w("```")
    w("python3 scripts/jds-classify.py --round "
      "--from [this-file.md] --output [round-YYYY-MM-DD.md]")
    w("```")
    w()
    w("---")
    w()

    # Revision history
    w("## Revision History")
    w()
    w("| Rev | Date | Author | Description |")
    w("|-----|------|--------|-------------|")
    w(f"| A | {today} | {author} "
      f"| Initial program \u2014 {len(vessels)} vessels, "
      f"compliant with AFS 2017:3 (verified against official PDF). "
      f"Auto-generated from {source_doc} |")

    return "\n".join(lines) + "\n"


# ---------------------------------------------------------------------------
# Round record generator — Step 3 (reads program, generates round)
# ---------------------------------------------------------------------------

def generate_round_markdown(vessels, client, site, doc_no, author,
                            source_doc="", round_type="Monthly"):
    """Generate a supervision round record pre-filled from program data."""
    today = date.today().strftime("%Y-%m-%d")
    lines = []

    def w(line=""):
        lines.append(line)

    in_scope = [v for v in vessels
                if v["risk_class"] not in
                ("Not classified", "Not in scope", "Simple PV", "")]

    w(f"# Supervision Round Record \u2014 {site}")
    w()
    w("| | |")
    w("|---|---|")
    w(f"| **Document No.** | {doc_no} |")
    w("| **Revision** | DRAFT |")
    w(f"| **Date** | {today} |")
    w("| **Status** | DRAFT |")
    w(f"| **Author** | {author} |")
    w("| **Project** | JDS-PRJ-MEC-002 |")
    w(f"| **Client** | {client} |")
    w(f"| **Site** | {site} |")
    w(f"| **Source** | {source_doc} |")
    w()
    w("---")
    w()

    # Workflow
    w("## 1. Document Chain")
    w()
    w("```")
    w("INVENTORY  →  PROGRAM  →  [ROUND]  →  REVIEW")
    w("                          (you are      (next,")
    w("                           here)        annual)")
    w("```")
    w()
    w(f"**Source program:** {source_doc}")
    w()
    w("---")
    w()

    # Round details
    w("## 2. Round Details")
    w()
    w("| | |")
    w("|---|---|")
    w(f"| **Round type** | {round_type} |")
    w(f"| **Round date** | {today} |")
    w("| **Start time** | HH:MM |")
    w("| **End time** | HH:MM |")
    w("| **Performed by** | [Name] |")
    w("| **Weather / conditions** | [Indoor / outdoor, temperature] |")
    w("| **Previous round date** | YYYY-MM-DD |")
    w("| **Open findings from previous** | [List or None] |")
    w()
    w("---")
    w()

    # General site checks
    w("## 3. General Site Checks")
    w()
    w("| # | Check Item | OK | Not OK | N/A | Notes |")
    w("|---|-----------|:--:|:------:|:---:|-------|")
    site_checks = [
        "Access to all vessels clear and safe",
        "Lighting adequate for inspection",
        "No unusual odours or sounds in area",
        "Housekeeping around vessels acceptable",
        "Emergency equipment accessible",
    ]
    for i, check in enumerate(site_checks, 1):
        w(f"| {i} | {check} | | | | |")
    w()
    w("---")
    w()

    # Per-vessel checks
    w("## 4. Per-Vessel Checks")
    w()

    for v in in_scope:
        rc = v["risk_class"]
        sched = get_check_schedule(rc)

        # Get the checks for this round type
        if round_type.lower() == "monthly":
            checks = sched.get("monthly", CHECKS_MONTHLY[:3])
        elif round_type.lower() == "quarterly":
            checks = sched.get("monthly", []) + sched.get("quarterly", [])
        else:
            checks = sched.get("monthly", CHECKS_MONTHLY[:3])

        w(f"### {v['vessel_id']} \u2014 {v.get('description', '')} "
          f"(Class {rc})")
        w()
        w("**Operating conditions at time of check:**")
        w()
        w("| Parameter | Reading | Normal Range | OK |")
        w("|-----------|---------|-------------|:--:|")
        w("| Pressure (bar) | | | |")
        w("| Temperature (\u00b0C) | | | |")
        w()
        w("**Supervision checks:**")
        w()
        w("| # | Check Item | OK | Not OK | N/A | Notes |")
        w("|---|-----------|:--:|:------:|:---:|-------|")
        for i, (check, method) in enumerate(checks, 1):
            w(f"| {i} | {check} | | | | |")
        w()

    w("---")
    w()

    # Safety device checks
    w("## 5. Safety Device Checks")
    w()
    w("| Device ID | Type | Protects | Check | Result | Notes |")
    w("|-----------|------|----------|-------|--------|-------|")
    for v in in_scope:
        dev_id = v["vessel_id"].replace("PV", "SV")
        w(f"| {dev_id} | Safety valve | {v['vessel_id']} "
          f"| Seal check | OK / Not OK | |")
    w()
    w("---")
    w()

    # Findings summary
    w("## 6. Findings Summary")
    w()
    w("| # | Vessel | Finding | Severity | Photo | Action |")
    w("|---|--------|---------|----------|-------|--------|")
    w("| 1 | | | Crit / Maj / Min / Obs | Y / N | |")
    w("| 2 | | | Crit / Maj / Min / Obs | Y / N | |")
    w("| 3 | | | Crit / Maj / Min / Obs | Y / N | |")
    w()

    w("### Corrective Actions Raised")
    w()
    w("| # | Finding | CA Ref. | Assigned To | Due Date |")
    w("|---|---------|---------|-------------|----------|")
    w("| 1 | | JDS-PRO-008 | | |")
    w()
    w("---")
    w()

    # Previous findings follow-up
    w("## 7. Previous Findings Follow-Up")
    w()
    w("| Finding Ref | Original Date | Description | Status |")
    w("|------------|---------------|-------------|--------|")
    w("| | | | Open / Closed |")
    w()
    w("---")
    w()

    # Round summary
    w("## 8. Round Summary")
    w()
    w("| | |")
    w("|---|---|")
    w(f"| **Total vessels inspected** | {len(in_scope)} |")
    w("| **Checks performed** | [N] |")
    w("| **Findings this round** | [N] |")
    w("| **Previous findings closed** | [N] |")
    w("| **Previous findings still open** | [N] |")
    w("| **Overall site condition** | Good / Acceptable / Needs attention |")
    w()
    w("---")
    w()

    # Sign-off
    w("## 9. Sign-Off")
    w()
    w("| | |")
    w("|---|---|")
    w("| **Inspected by** | [Name, signature] |")
    w(f"| **Date** | {today} |")
    w("| **Next scheduled round** | YYYY-MM-DD |")
    w("| **Reviewed by** | [Name, signature, date] |")
    w()
    w("---")
    w()

    # Next step
    w("## 10. Next Step")
    w()
    w("```")
    w("INVENTORY  →  PROGRAM  →  [ROUND]  →  REVIEW")
    w("                          (done)       (annual)")
    w("```")
    w()
    w("**After completing this round:**")
    w("1. File this record in the client's `rounds/` folder")
    w("2. Update the program register (JDS-LOG-MEC-005)")
    w("3. Raise corrective actions for any findings (JDS-PRO-008)")
    w("4. Generate the next round when scheduled:")
    w()
    w("```")
    w("python3 scripts/jds-classify.py --round "
      f"--from {source_doc} --output round-YYYY-MM-DD.md")
    w("```")
    w()
    w("---")
    w()

    # Revision history
    w("## Revision History")
    w()
    w("| Rev | Date | Author | Description |")
    w("|-----|------|--------|-------------|")
    w(f"| DRAFT | {today} | {author} | {round_type} supervision round |")

    return "\n".join(lines) + "\n"


# ---------------------------------------------------------------------------
# Annual review generator — Step 4 (reads program, generates review)
# ---------------------------------------------------------------------------

def generate_review_markdown(vessels, client, site, doc_no, author,
                             source_doc=""):
    """Generate an annual review pre-filled from program data."""
    today = date.today().strftime("%Y-%m-%d")
    year = date.today().year
    lines = []

    def w(line=""):
        lines.append(line)

    in_scope = [v for v in vessels
                if v["risk_class"] not in
                ("Not classified", "Not in scope", "Simple PV", "")]

    w(f"# Annual Supervision Program Review \u2014 {site}")
    w()
    w("| | |")
    w("|---|---|")
    w(f"| **Document No.** | {doc_no} |")
    w("| **Revision** | DRAFT |")
    w(f"| **Date** | {today} |")
    w("| **Status** | DRAFT |")
    w(f"| **Author** | {author} |")
    w("| **Project** | JDS-PRJ-MEC-002 |")
    w(f"| **Client** | {client} |")
    w(f"| **Site** | {site} |")
    w(f"| **Source** | {source_doc} |")
    w(f"| **Review period** | {year}-01-01 to {year}-12-31 |")
    w()
    w("---")
    w()

    # Workflow
    w("## 1. Document Chain")
    w()
    w("```")
    w("INVENTORY  →  PROGRAM  →  ROUND  →  [REVIEW]")
    w("                                     (you are")
    w("                                      here)")
    w("```")
    w()
    w(f"**Source program:** {source_doc}")
    w()
    w("This review closes the annual cycle. After completion, "
      "update the program and begin the next cycle.")
    w()
    w("---")
    w()

    # Round completion
    w("## 2. Program Execution Summary")
    w()
    has_daily = any(v["risk_class"] in ("A", "B") for v in in_scope)
    has_quarterly = any(v["risk_class"] in ("A", "B") for v in in_scope)

    w("### 2.1 Round Completion")
    w()
    w("| Round Type | Planned | Completed | Missed | Rate |")
    w("|-----------|---------|-----------|--------|------|")
    w("| Monthly | 12 | | | % |")
    if has_quarterly:
        w("| Quarterly | 4 | | | % |")
    w("| Annual | 1 | | | % |")
    w("| Special | \u2014 | | | \u2014 |")
    w()

    w("### 2.2 Findings Summary")
    w()
    w("| Severity | Raised | Closed | Open | Rate |")
    w("|----------|--------|--------|------|------|")
    w("| Critical | | | | % |")
    w("| Major | | | | % |")
    w("| Minor | | | | % |")
    w("| Observation | | | | % |")
    w("| **Total** | | | | **%** |")
    w()

    w("### 2.3 Recurring Findings")
    w()
    w("| Finding | Occurrences | Vessels | Root Cause | Action |")
    w("|---------|-------------|---------|-----------|--------|")
    w("| | | | Yes / No | |")
    w()
    w("---")
    w()

    # Equipment changes
    w("## 3. Equipment Changes")
    w()
    w("### 3.1 Current Register")
    w()
    w("| Vessel ID | Description | Class | Status |")
    w("|-----------|-------------|-------|--------|")
    for v in in_scope:
        w(f"| {v['vessel_id']} | {v.get('description', '')} "
          f"| {v['risk_class']} | In service |")
    w()

    w("### 3.2 Changes This Year")
    w()
    w("| Change | Vessel ID | Description | Date | Action |")
    w("|--------|-----------|-------------|------|--------|")
    w("| Added / Removed / Modified | | | | |")
    w()
    w("---")
    w()

    # Operating conditions
    w("## 4. Operating Condition Changes")
    w()
    w("| Change | Affected Vessels | Program Update |")
    w("|--------|-----------------|---------------|")
    w("| Pressure change | | Yes / No |")
    w("| Temperature change | | Yes / No |")
    w("| Medium change | | Yes / No |")
    w("| Duty cycle change | | Yes / No |")
    w()
    w("---")
    w()

    # Regulatory changes
    w("## 5. Regulatory Changes")
    w()
    w("| Regulation | Change | Impact |")
    w("|-----------|--------|--------|")
    w("| | | None / Update required |")
    w()
    w("---")
    w()

    # Personnel
    w("## 6. Personnel Review")
    w()
    w("| Name | Role | Competence Current | Refresher Due |")
    w("|------|------|-------------------|--------------|")
    w("| | Daily/weekly supervisor | Yes / No | YYYY-MM-DD |")
    w("| | Monthly/quarterly supervisor | Yes / No | YYYY-MM-DD |")
    w("| | Program manager | Yes / No | YYYY-MM-DD |")
    w()
    w("---")
    w()

    # Effectiveness
    w("## 7. Program Effectiveness")
    w()
    w("| Criterion | Rating | Evidence |")
    w("|----------|--------|---------|")
    w("| All scheduled rounds completed | Good / Acceptable / Poor | |")
    w("| Findings identified promptly | Good / Acceptable / Poor | |")
    w("| Corrective actions closed on time | Good / Acceptable / Poor | |")
    w("| No repeat critical findings | Good / Acceptable / Poor | |")
    w("| Equipment register current | Good / Acceptable / Poor | |")
    w("| Personnel competence maintained | Good / Acceptable / Poor | |")
    w("| Documentation complete | Good / Acceptable / Poor | |")
    w()
    w("**Overall effectiveness:** Good / Acceptable / Needs Improvement")
    w()
    w("---")
    w()

    # Improvements
    w("## 8. Improvement Actions")
    w()
    w("| # | Improvement | Reason | Owner | Target Date |")
    w("|---|-----------|--------|-------|-------------|")
    w("| 1 | | | | |")
    w("| 2 | | | | |")
    w()
    w("---")
    w()

    # Decision
    w("## 9. Program Update Decision")
    w()
    w("| | |")
    w("|---|---|")
    w("| **Program revision required?** | Yes / No |")
    w("| **Changes needed** | [Describe] |")
    w(f"| **New revision due by** | {year + 1}-01-31 |")
    w(f"| **Next annual review due** | {year + 1}-12-31 |")
    w()
    w("---")
    w()

    # Sign-off
    w("## 10. Sign-Off")
    w()
    w("| | |")
    w("|---|---|")
    w("| **Reviewed by** | [Name, role, signature] |")
    w(f"| **Date** | {today} |")
    w("| **Approved by** | [Operator representative, signature] |")
    w("| **Date** | |")
    w()
    w("---")
    w()

    # Next step
    w("## 11. Next Step")
    w()
    w("```")
    w("INVENTORY  →  PROGRAM  →  ROUND  →  [REVIEW]")
    w("                 ↑                    (done)")
    w("                 └──── update program, begin next cycle")
    w("```")
    w()
    w("**After completing this review:**")
    w("1. Update the supervision program if changes are needed (new revision)")
    w("2. Update the program register (JDS-LOG-MEC-005)")
    w("3. Update the equipment inventory if vessels changed")
    w("4. Begin the next annual cycle")
    w()
    w("---")
    w()

    # Revision history
    w("## Revision History")
    w()
    w("| Rev | Date | Author | Description |")
    w("|-----|------|--------|-------------|")
    w(f"| DRAFT | {today} | {author} | Annual review for {year} |")

    return "\n".join(lines) + "\n"


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def write_output(md, output_path, label):
    """Write markdown to file and print confirmation."""
    with open(output_path, "w") as f:
        f.write(md)
    print(f"\n{label} written to: {output_path}")


def main():
    parser = argparse.ArgumentParser(
        description="JDS Vessel Classification & Inventory Generator "
                    "(AFS 2017:3)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Document chain — each step reads the previous and generates the next:

  Step 1 — Inventory (from CSV or interactive):
    python3 scripts/jds-classify.py --csv vessels.csv --output inventory.md
    python3 scripts/jds-classify.py   (interactive)

  Step 2 — Supervision Program (reads inventory):
    python3 scripts/jds-classify.py --program --from inventory.md

  Step 3 — Supervision Round (reads program):
    python3 scripts/jds-classify.py --round --from program.md

  Step 4 — Annual Review (reads program):
    python3 scripts/jds-classify.py --review --from program.md

  Quick classification (standalone):
    python3 scripts/jds-classify.py --quick --ps 11 --volume 1000
    python3 scripts/jds-classify.py --quick --ps 25 --volume 200 --medium ammonia

CSV format (header row required):
  vessel_id,description,location,manufacturer,year,serial,ps_bar,ts_max_c,volume_l,medium,ce_marked,eu_doc,last_inspection,last_type
        """,
    )

    # Step 1: Inventory (existing)
    parser.add_argument("--csv", metavar="FILE",
                        help="Step 1: Read vessel data from CSV, "
                             "generate inventory")

    # Step 2: Program
    parser.add_argument("--program", action="store_true",
                        help="Step 2: Generate supervision program "
                             "from inventory (requires --from)")

    # Step 3: Round
    parser.add_argument("--round", action="store_true",
                        help="Step 3: Generate supervision round record "
                             "from program (requires --from)")
    parser.add_argument("--round-type", default="Monthly",
                        help="Round type: Monthly, Quarterly (default: Monthly)")

    # Step 4: Review
    parser.add_argument("--review", action="store_true",
                        help="Step 4: Generate annual review "
                             "from program (requires --from)")

    # Chain input
    parser.add_argument("--from", dest="from_file", metavar="FILE",
                        help="Source document for chain generation "
                             "(inventory for --program, program for "
                             "--round/--review)")

    # Quick classify
    parser.add_argument("--quick", action="store_true",
                        help="Quick single-vessel classification")
    parser.add_argument("--ps", type=float,
                        help="Design pressure in bar (for --quick)")
    parser.add_argument("--volume", type=float,
                        help="Volume in litres (for --quick)")
    parser.add_argument("--medium", default="compressed air",
                        help="Medium (default: compressed air)")

    # Common options
    parser.add_argument("--output", "-o", metavar="FILE",
                        help="Output markdown file")
    parser.add_argument("--client", default=None,
                        help="Client name")
    parser.add_argument("--site", default=None,
                        help="Site name")
    parser.add_argument("--doc-no", default="JDS-LOG-MEC-[NNN]",
                        help="JDS document number")
    parser.add_argument("--author", default="N. Johansson",
                        help="Author name")

    args = parser.parse_args()

    # --- Quick classify ---
    if args.quick:
        if not args.ps or not args.volume:
            parser.error("--quick requires --ps and --volume")
        quick_classify(args.ps, args.volume, args.medium)
        return

    # --- Step 2: Program from inventory ---
    if args.program:
        if not args.from_file:
            parser.error("--program requires --from <inventory.md>")
        if not os.path.exists(args.from_file):
            print(f"Error: Source file not found: {args.from_file}")
            sys.exit(1)

        print(f"Reading inventory: {args.from_file}")
        meta, vessels = parse_inventory_file(args.from_file)
        client = args.client or meta.get("Client", "Internal")
        site = args.site or meta.get("Site", "Site")

        print(f"  Found {len(vessels)} vessels")
        for v in vessels:
            print(f"    {v['vessel_id']}: {v['risk_class']} "
                  f"({v.get('description', '')})")

        md = generate_program_markdown(
            vessels, client, site, args.doc_no, args.author,
            source_doc=os.path.basename(args.from_file),
        )

        output = args.output or \
            f"program-{site.lower().replace(' ', '-')}.md"
        write_output(md, output, "Supervision program")
        print(f"\nNext step: python3 scripts/jds-classify.py --round "
              f"--from {output}")
        return

    # --- Step 3: Round from program ---
    if args.round:
        if not args.from_file:
            parser.error("--round requires --from <program.md>")
        if not os.path.exists(args.from_file):
            print(f"Error: Source file not found: {args.from_file}")
            sys.exit(1)

        print(f"Reading program: {args.from_file}")
        meta, vessels = parse_inventory_file(args.from_file)
        client = args.client or meta.get("Client", "Internal")
        site = args.site or meta.get("Site", "Site")

        print(f"  Found {len(vessels)} vessels for round record")

        md = generate_round_markdown(
            vessels, client, site, args.doc_no, args.author,
            source_doc=os.path.basename(args.from_file),
            round_type=args.round_type,
        )

        today_str = date.today().strftime("%Y-%m-%d")
        output = args.output or f"round-{today_str}.md"
        write_output(md, output, "Supervision round record")
        return

    # --- Step 4: Review from program ---
    if args.review:
        if not args.from_file:
            parser.error("--review requires --from <program.md>")
        if not os.path.exists(args.from_file):
            print(f"Error: Source file not found: {args.from_file}")
            sys.exit(1)

        print(f"Reading program: {args.from_file}")
        meta, vessels = parse_inventory_file(args.from_file)
        client = args.client or meta.get("Client", "Internal")
        site = args.site or meta.get("Site", "Site")

        print(f"  Found {len(vessels)} vessels for annual review")

        md = generate_review_markdown(
            vessels, client, site, args.doc_no, args.author,
            source_doc=os.path.basename(args.from_file),
        )

        year = date.today().year
        output = args.output or f"review-{year}.md"
        write_output(md, output, "Annual review")
        return

    # --- Step 1: Inventory from CSV ---
    if args.csv:
        if not os.path.exists(args.csv):
            print(f"Error: CSV file not found: {args.csv}")
            sys.exit(1)

        client = args.client or "Internal"
        site = args.site or "Site"
        vessels = read_csv(args.csv)
        print(f"Read {len(vessels)} vessels from {args.csv}")

        for v in vessels:
            print(f"  {v['vessel_id']}: PS\u00d7V = {v['psv']:,.0f} bar\u00b7L "
                  f"\u2192 {v['risk_class']}")

        md = generate_inventory_markdown(
            vessels, client, site, args.doc_no, args.author
        )

        output = args.output or \
            f"inventory-{site.lower().replace(' ', '-')}.md"
        write_output(md, output, "Inventory")
        print(f"\nNext step: python3 scripts/jds-classify.py --program "
              f"--from {output}")
        return

    # --- Default: interactive mode ---
    interactive_mode()


if __name__ == "__main__":
    main()
