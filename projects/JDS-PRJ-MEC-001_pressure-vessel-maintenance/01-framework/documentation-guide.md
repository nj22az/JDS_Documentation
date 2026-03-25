# Documentation Guide — What Records to Keep and Why

> **JDS-MAN-MEC-001** | **Rev A** | **CURRENT** | 2026-03-25 | N. Johansson

---

## What Is This?

This guide explains what documentation you must maintain for a pressure vessel maintenance program. Good documentation isn't bureaucracy — it's your proof of compliance and your protection if something goes wrong.

## The Golden Rule

> **If it's not documented, it didn't happen.**

Every inspection, every repair, every modification, every test — must be on paper (or in this system). When a regulator asks "show me your records", you need to be able to produce them within minutes.

## Required Documents Per Vessel

Every pressure vessel in your program should have the following documents available:

### At Commissioning (when first put into service)

| Document | What it is | Where to get it | JDS Category |
|----------|-----------|-----------------|-------------|
| **Manufacturer's data sheet** | Nameplate data, design parameters, materials | From the manufacturer | Reference (keep in `references/`) |
| **CE Declaration of Conformity** | Confirms the vessel meets PED requirements | From the manufacturer | Reference |
| **Design drawings** | Technical drawings of the vessel | From the manufacturer | DWG |
| **Strength calculations** | Proof that the vessel is designed to withstand its rated pressure | From the manufacturer | Reference |
| **Material certificates** | What materials the vessel is made from (e.g., EN 10204 3.1) | From the manufacturer | Reference |
| **Welding documentation** | WPS, WPQR, welder qualifications | From the manufacturer | Reference |
| **Pressure test certificate** | Factory pressure test results | From the manufacturer | Reference |
| **Risk assessment** | Identifies hazards and controls | You or the manufacturer | RPT |
| **Equipment register entry** | Vessel added to the inventory | You | LOG |

### During Service (ongoing)

| Document | When created | How often | JDS Category |
|----------|-------------|-----------|-------------|
| **Inspection reports** | After each inspection | Per inspection interval | RPT |
| **Inspection certificates** | Issued by accredited inspector | Per inspection interval | Reference |
| **Repair reports** | When repairs are performed | As needed | RPT |
| **Modification records** | When the vessel is modified | As needed | RPT |
| **Safety valve test records** | After each safety valve test | Typically annually | LOG |
| **Equipment register updates** | After each inspection or status change | Ongoing | LOG |
| **Incident reports** | If anything goes wrong (leak, overpressure, failure) | As needed | RPT |

### At Decommissioning (when removed from service)

| Document | What it is | JDS Category |
|----------|-----------|-------------|
| **Decommissioning record** | Date, reason, method of making safe | RPT |
| **Equipment register update** | Status changed to DECOMMISSIONED | LOG |

## How Long to Keep Records

| Record type | Minimum retention | Why |
|---|---|---|
| Manufacturer documentation | **Lifetime of the vessel** | May be needed for re-certification or incident investigation |
| Inspection reports & certificates | **Lifetime of the vessel** | Proves compliance history |
| Repair & modification records | **Lifetime of the vessel** | Affects future inspections and design limits |
| Decommissioning records | **10 years after decommissioning** | Regulatory requirement in most jurisdictions |

**In JDS, retention is simple:** Everything stays in the Git repository forever. Git never forgets.

## Filing Structure for Active Programs

When you run a real client program, organise their files like this:

```
03-active-programs/
└── client-name/
    ├── equipment-register.md         ← Their filled-in inventory
    ├── inspection-calendar.md        ← Their annual plan
    ├── vessel-files/                 ← One subfolder per vessel
    │   ├── PV-001/
    │   │   ├── manufacturer-docs/    ← Datasheet, CE cert, drawings
    │   │   ├── inspections/          ← JDS-RPT inspection reports
    │   │   └── repairs/              ← JDS-RPT repair reports
    │   ├── PV-002/
    │   │   └── ...
    │   └── HE-001/
    │       └── ...
    └── correspondence/               ← Client communication
```

## Quick Checklist: Is My Documentation Complete?

For each vessel, can you answer YES to all of these?

- [ ] Is it in the equipment register with all fields filled?
- [ ] Do you have the manufacturer's data sheet and CE declaration?
- [ ] Do you know the regulatory class and inspection interval?
- [ ] Are all past inspection reports on file?
- [ ] Is the next inspection date in the future (not overdue)?
- [ ] Are all safety valve tests documented?
- [ ] Are all repairs and modifications documented?

If any answer is NO, that's your next action item.

---

## Revision History

| Rev | Date | Author | Description |
|-----|------|--------|-------------|
| A | 2026-03-25 | N. Johansson | Initial release — documentation requirements and filing structure |
