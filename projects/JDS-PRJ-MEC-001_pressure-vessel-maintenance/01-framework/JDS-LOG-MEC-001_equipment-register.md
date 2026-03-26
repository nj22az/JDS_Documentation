# Equipment Register — Pressure Vessels

| | |
|---|---|
| **Document No.** | JDS-LOG-MEC-001 |
| **Revision** | A |
| **Date** | 2026-03-25 |
| **Status** | CURRENT |
| **Author** | N. Johansson |

---

## What Is This?

This is the master inventory of all pressurised vessels under your maintenance program. Every vessel gets one row. This register is the **single source of truth** for what equipment exists, what condition it's in, and when it needs attention.

It works like a lifecycle record — each piece of equipment is tracked from installation to retirement, with every inspection and status change recorded in one place.

## How to Use This Register

1. **Add a new vessel** — Fill in one row per vessel. Every field matters.
2. **Update after inspection** — After each inspection, update the "Last Inspection" and "Next Inspection" columns.
3. **Review quarterly** — Check that no vessel has passed its next inspection date without action.
4. **Revision** — When you add or remove vessels, create a new revision (A → B → C).

---

## Equipment Register

### Column Definitions

Before filling in the register, here's what each column means:

| Column | What to write | Example |
|--------|--------------|---------|
| **Vessel ID** | Your unique identifier for this vessel. Use a logical system. | PV-001 |
| **Description** | What it is, in plain language | Compressed air receiver |
| **Location** | Where it is physically installed | Machine hall, bay 3 |
| **Manufacturer** | Who made it (from the nameplate) | Atlas Copco |
| **Year** | Year of manufacture (from the nameplate) | 2018 |
| **Serial No.** | Manufacturer's serial number | AC-2018-44521 |
| **Design Pressure** | Maximum allowable pressure (from nameplate) | 11 bar |
| **Design Temp** | Maximum allowable temperature | 200°C |
| **Volume** | Internal volume in litres | 500 L |
| **Medium** | What's inside the vessel | Compressed air |
| **Class** | Regulatory classification (see regulations folder) | Class A / B / C |
| **Inspection Interval** | How often it must be inspected (from regulations) | 24 months |
| **Last Inspection** | Date of most recent inspection | 2025-06-15 |
| **Next Inspection** | When the next inspection is due | 2027-06-15 |
| **Inspector** | Who performed the last inspection | DEKRA / Kiwa / Internal |
| **Certificate Ref** | Reference number of the inspection certificate | DEKRA-2025-12345 |
| **Status** | Current operational status | IN SERVICE / OUT OF SERVICE / DECOMMISSIONED |
| **Notes** | Anything important — defects found, repairs pending, etc. | Minor corrosion noted on weld seam |

---

### The Register

*Copy the tables below and fill in your vessels. Add rows as needed. All tables are linked by Vessel ID.*

#### Table 1 — Vessel Identification

| Vessel ID | Description | Location | Manufacturer | Year | Serial No. | Status |
|-----------|-------------|----------|-------------|------|-----------|--------|
| PV-001 | *Air receiver* | *Machine hall* | *Atlas Copco* | *2018* | *AC-44521* | *IN SERVICE* |
| | | | | | | |
| | | | | | | |

#### Table 2 — Design Parameters

| Vessel ID | Design Pressure | Design Temp | Volume | Medium | Class |
|-----------|----------------|-------------|--------|--------|-------|
| PV-001 | *11 bar* | *200°C* | *500 L* | *Air* | *B* |
| | | | | | |
| | | | | | |

#### Table 3 — Inspection Tracking

| Vessel ID | Insp. Interval | Last Inspection | Next Inspection | Inspector | Certificate Ref | Notes |
|-----------|---------------|----------------|----------------|-----------|----------------|-------|
| PV-001 | *24 months* | *2025-06-15* | *2027-06-15* | *DEKRA* | *DK-2025-123* | *Example row — replace with real data* |
| | | | | | | |
| | | | | | | |

---

## Vessel ID Naming Convention

Use a consistent naming system for vessel IDs. Suggested format:

```
[TYPE]-[NUMBER]
```

| Type Code | Meaning | Example |
|-----------|---------|---------|
| PV | Pressure Vessel (general) | PV-001 |
| AR | Air Receiver | AR-001 |
| HE | Heat Exchanger | HE-001 |
| ST | Steam Vessel | ST-001 |
| BL | Boiler | BL-001 |
| AC | Accumulator (hydraulic) | AC-001 |
| CY | Cylinder (gas) | CY-001 |

If you manage multiple sites, add a site prefix:

```
[SITE]-[TYPE]-[NUMBER]
Example: MALMO-AR-001 (Air receiver #1 at Malmö site)
```

## Status Definitions

| Status | Meaning | Action |
|--------|---------|--------|
| **IN SERVICE** | Vessel is operational and compliant | Maintain inspection schedule |
| **OUT OF SERVICE** | Vessel is not currently in use but still installed | Still requires periodic inspection in most jurisdictions |
| **REPAIR PENDING** | Defect found, awaiting repair | Schedule repair before next use |
| **DECOMMISSIONED** | Permanently removed from service | Document the removal, update register |

## Inspection Overdue Alert

Any vessel where today's date is **past the Next Inspection date** is overdue. Overdue vessels must be:

1. Taken out of service immediately (or risk assessed)
2. Inspection scheduled as soon as possible
3. Flagged in the Notes column: **"OVERDUE — [action taken]"**

---

## Adapting This Register for Different Countries

This register is **country-neutral**. The columns work everywhere. What changes between countries:

| What changes | Where it's defined |
|---|---|
| How "Class" is determined | `02-regulations/[country]/` |
| What the inspection intervals are | `02-regulations/[country]/` |
| Who is qualified to inspect | `02-regulations/[country]/` |
| What certificates are required | `02-regulations/[country]/` |

The register itself stays the same. Only the values in the Class, Inspection Interval, and Inspector columns change based on which country's rules apply.

---

## Revision History

| Rev | Date | Author | Description |
|-----|------|--------|-------------|
| A | 2026-03-25 | N. Johansson | Initial release — framework template with examples and naming convention |
