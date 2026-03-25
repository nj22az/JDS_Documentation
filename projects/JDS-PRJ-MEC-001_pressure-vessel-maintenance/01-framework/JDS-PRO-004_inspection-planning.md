# Inspection Planning Procedure

| | |
|---|---|
| **Document No.** | JDS-PRO-004 |
| **Revision** | A |
| **Date** | 2026-03-25 |
| **Status** | CURRENT |
| **Author** | N. Johansson |

---

## What Is This?

This procedure describes how to plan and schedule inspections for pressurised vessels. It's the second step after building your equipment register — once you know what you have, you plan when to inspect it.

## The Inspection Cycle

Every pressure vessel follows the same basic cycle, regardless of country:

```
INVENTORY → PLAN → INSPECT → REPORT → UPDATE REGISTER → PLAN NEXT
    ↑                                                        │
    └────────────────────────────────────────────────────────┘
```

1. **Inventory** — Know what vessels you have (equipment register)
2. **Plan** — Schedule inspections based on intervals and due dates
3. **Inspect** — Perform the inspection (internal, external, pressure test)
4. **Report** — Document findings (JDS-RPT category)
5. **Update** — Update the equipment register with results and next date
6. **Repeat** — The cycle never stops as long as the vessel is in service

## Inspection Types

Most regulatory frameworks recognise these inspection types:

| Type | What it covers | Typical method |
|------|---------------|---------------|
| **External inspection** | Visual check of the outside — corrosion, leaks, supports, safety devices | Visual, surface NDT |
| **Internal inspection** | Check inside the vessel — corrosion, cracks, deposits, wall thickness | Visual, UT wall thickness, NDT |
| **Pressure test** | Verify the vessel can safely hold pressure | Hydrostatic test (water) or pneumatic test |
| **Functional test** | Verify safety devices work — relief valves, gauges, interlocks | Operational test, bench test |

Which types apply and how often depends on the country's regulations. See the `02-regulations/` folder for specifics.

## How to Build an Inspection Schedule

### Step 1: Export Due Dates from the Equipment Register

Go through the equipment register and list every vessel with its next inspection date:

| Vessel ID | Description | Next Inspection | Type Required |
|-----------|-------------|----------------|---------------|
| PV-001 | Air receiver | 2027-06-15 | External + Internal |
| PV-002 | Hydraulic accumulator | 2026-09-01 | External |
| HE-001 | Heat exchanger | 2026-12-01 | Internal |

### Step 2: Group by Quarter

Organise inspections into quarterly blocks for workload planning:

| Quarter | Vessels Due | Count |
|---------|------------|-------|
| Q1 (Jan-Mar) | — | 0 |
| Q2 (Apr-Jun) | — | 0 |
| Q3 (Jul-Sep) | PV-002 | 1 |
| Q4 (Oct-Dec) | HE-001 | 1 |

### Step 3: Book Inspectors

For inspections that require an accredited third party (most countries require this for higher-class vessels):

- Book the inspector **at least 3 months ahead**
- Confirm the inspector is accredited for the vessel type and country
- Ensure access to the vessel (isolation, draining, cleaning if internal)

### Step 4: Prepare the Vessel

Before inspection day:

| Task | Lead Time | Responsible |
|------|-----------|-------------|
| Notify operations that vessel will be taken offline | 2 weeks | Maintenance planner |
| Isolate and depressurise the vessel | Day before | Operations |
| Drain and clean (if internal inspection) | Day before | Maintenance |
| Remove insulation (if required for external) | Day before | Maintenance |
| Prepare previous inspection reports for the inspector | 1 week | Document controller |

### Step 5: After the Inspection

1. Receive the inspection report/certificate from the inspector
2. File the report as `JDS-RPT-MEC-NNN` in the active program folder
3. Update the equipment register:
   - Last Inspection → today's date
   - Next Inspection → calculate from the interval
   - Certificate Ref → new certificate number
   - Notes → any findings or actions required
4. Log the update in the project CHANGELOG
5. If defects were found, create an action item and track to completion

## Inspection Calendar Template

Use this calendar to plan the full year at a glance:

| Month | Vessels Due | Type | Inspector | Status |
|-------|------------|------|-----------|--------|
| January | | | | |
| February | | | | |
| March | | | | |
| April | | | | |
| May | | | | |
| June | | | | |
| July | | | | |
| August | | | | |
| September | | | | |
| October | | | | |
| November | | | | |
| December | | | | |

## Overdue Management

If an inspection is overdue:

| Overdue by | Action |
|-----------|--------|
| 0-30 days | Schedule immediately. Vessel may continue in service if risk assessed. |
| 30-90 days | Vessel should be taken out of service until inspected. Notify responsible person. |
| 90+ days | Vessel **must** be taken out of service. May require re-certification before returning to service. |

**Note:** Specific rules vary by country. Always check the regulatory requirements in `02-regulations/`.

---

## Revision History

| Rev | Date | Author | Description |
|-----|------|--------|-------------|
| A | 2026-03-25 | N. Johansson | Initial release — inspection planning framework |
