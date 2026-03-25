# Swedish Pressure Vessel Regulations — Reference Summary

> **Rev A** | **CURRENT** | 2026-03-25 | N. Johansson

---

## Disclaimer

This document is a **practical reference summary** for working engineers. It does not replace the official regulatory texts. Always verify against the current published version of the regulations.

## Key Regulations

| Regulation | Full Name | What It Covers |
|-----------|-----------|---------------|
| **AFS 2017:3** | Användning och kontroll av trycksatta anordningar | Use and inspection of pressurised equipment — the main regulation for ongoing maintenance |
| **AFS 2016:1** | Tryckbärande anordningar | Design and manufacture of pressure equipment (PED implementation) |
| **PED 2014/68/EU** | Pressure Equipment Directive | EU directive for design and first placing on market |

**AFS 2017:3 is your primary regulation for ongoing maintenance programs.** It defines what to inspect, how often, and who may do it.

## Vessel Classification (AFS 2017:3)

Swedish regulations classify pressurised vessels into classes based on risk. The class determines the inspection requirements.

### Classification Factors

The class depends on:
1. **Pressure** (PS) — design pressure in bar
2. **Volume** (V) — internal volume in litres
3. **Medium** — what's inside (Group 1 = dangerous, Group 2 = non-dangerous)
4. **Product** — PS × V (pressure-volume product)

### Medium Groups

| Group | What It Means | Examples |
|-------|--------------|---------|
| **Group 1** | Dangerous fluids — explosive, flammable, toxic, oxidising | LPG, ammonia, hydrogen, chlorine |
| **Group 2** | All other fluids | Compressed air, nitrogen, water, steam |

### Classification Table — Simplified

For **Group 2 gases** (most common, e.g., compressed air):

| Class | PS × V (bar·L) | Typical Examples |
|-------|----------------|-----------------|
| **Class A** | > 10,000 | Large air receivers, industrial compressor tanks |
| **Class B** | 1,000 – 10,000 | Medium air receivers, hydraulic accumulators |
| **Class C** | 200 – 1,000 | Small pressure vessels |
| **Simple pressure vessel** | 50 – 200 | Very small receivers, expansion tanks |
| **Not classified** | < 50 | Below regulatory threshold |

**Note:** This is simplified. The exact classification follows the tables in AFS 2017:3 Chapter 3 and the PED categories. For Group 1 fluids, the thresholds are lower (more strict).

## Inspection Requirements by Class

| Class | Inspection Type | Interval | Who May Inspect |
|-------|----------------|----------|----------------|
| **Class A** | External inspection | 24 months | Ackrediterat kontrollorgan (e.g., DEKRA, Kiwa, RISE) |
| | Internal inspection | 72 months | Ackrediterat kontrollorgan |
| | Pressure test | 144 months | Ackrediterat kontrollorgan |
| **Class B** | External inspection | 36 months | Ackrediterat kontrollorgan OR egen kontroll (if approved) |
| | Internal inspection | 72 months | Ackrediterat kontrollorgan |
| **Class C** | External inspection | 72 months | Egen kontroll (own inspection) allowed |
| **Simple PV** | No mandatory periodic inspection | — | Owner's responsibility |

### Key Terms

| Swedish Term | English | Meaning |
|-------------|---------|---------|
| Ackrediterat kontrollorgan | Accredited inspection body | Third-party inspector (DEKRA, Kiwa, RISE, Bureau Veritas, etc.) |
| Egen kontroll | Own inspection | Inspection performed by the owner's own competent personnel |
| Fortlöpande tillsyn | Ongoing supervision | The owner's continuous responsibility to ensure safe operation |
| Driftprov | Operational test / functional test | Testing safety devices (relief valves, etc.) |

## Accredited Inspection Bodies in Sweden

| Organisation | Accreditation |
|-------------|--------------|
| DEKRA Industrial AB | SWEDAC accredited |
| Kiwa Sweden AB | SWEDAC accredited |
| RISE (Research Institutes of Sweden) | SWEDAC accredited |
| Bureau Veritas | SWEDAC accredited |
| TÜV Nord Sweden | SWEDAC accredited |

The latest list is available from SWEDAC (Swedish Board for Accreditation and Conformity Assessment).

## Owner Responsibilities (AFS 2017:3, Chapter 2)

As the owner/operator of pressurised equipment, you must:

1. **Maintain an inventory** of all pressurised equipment (→ equipment register)
2. **Classify** each vessel according to the regulation
3. **Ensure inspections** are performed on schedule by qualified persons
4. **Keep records** of all inspections, tests, repairs, and modifications
5. **Ensure ongoing supervision** — daily operational checks, maintenance
6. **Act on findings** — if an inspection reveals a defect, you must address it before returning the vessel to service
7. **Report incidents** — overpressure events, failures, or dangerous occurrences must be reported to Arbetsmiljöverket

## Safety Devices

Safety devices (relief valves, rupture discs, pressure switches) must be:

- **Tested regularly** — typically annually, but check the specific requirement
- **Set correctly** — relief pressure must not exceed the vessel's design pressure
- **Documented** — test results recorded with date, set pressure, and outcome

## Mapping to Equipment Register

When filling in the equipment register for a Swedish program:

| Register Column | Swedish-Specific Notes |
|----------------|----------------------|
| **Class** | Use Class A / B / C / Simple PV as defined above |
| **Inspection Interval** | Use the intervals from the table above |
| **Inspector** | Must be ackrediterat kontrollorgan for Class A and B (internal) |
| **Certificate Ref** | Reference the kontrollintyg (inspection certificate) number |

---

## Useful Links

- Arbetsmiljöverket (Swedish Work Environment Authority): AFS 2017:3 full text
- SWEDAC: List of accredited inspection bodies
- EU PED 2014/68/EU: Full directive text

*(Note: URLs not included — search for the regulation numbers above to find the official sources)*

---

## Revision History

| Rev | Date | Author | Description |
|-----|------|--------|-------------|
| A | 2026-03-25 | N. Johansson | Initial release — summary of AFS 2017:3 for working reference |
