# Supervision Program Register

| | |
|---|---|
| **Document No.** | JDS-LOG-MEC-005 |
| **Revision** | A |
| **Date** | 2026-04-10 |
| **Status** | CURRENT |
| **Author** | N. Johansson |

---

## 1. Purpose

This register tracks every active supervision program created under the Vessel Supervision System (JDS-PRJ-MEC-002). It provides a single view of all programs, their status, and next review dates.

---

## 2. Active Programs

| Program ID | Client | Site | Vessels | Status | Issued | Next Review |
|-----------|--------|------|---------|--------|--------|-------------|
| — | — | — | — | — | — | — |

**Status codes:** ACTIVE / UNDER REVIEW / SUSPENDED / CLOSED

---

## 3. Program Summary

| Metric | Count |
|--------|-------|
| Total programs | 0 |
| Active | 0 |
| Under review | 0 |
| Suspended | 0 |
| Closed | 0 |

---

## 4. How to Use This Register

### Adding a New Program

1. Create the supervision program using JDS-TMP-LOG-005
2. Assign a unique program ID (format: `SP-[NNN]`, e.g., SP-001)
3. Add a row to the Active Programs table above
4. Set status to ACTIVE
5. Set Next Review to 12 months from issue date

### Updating a Program

1. After annual review (JDS-TMP-LOG-007), update the row:
   - Update Next Review date
   - If the program was revised, note the new revision in the supervision program document
2. If a program is suspended or closed, update the status

### Program ID Format

```
SP-001    ← Sequential number, unique across all clients
SP-002
SP-003
...
```

---

## 5. Overdue Reviews

| Program ID | Client | Site | Review Due | Days Overdue |
|-----------|--------|------|-----------|-------------|
| — | — | — | — | — |

> Review this table monthly. Any program overdue for review must be escalated to the operator.

---

## Revision History

| Rev | Date | Author | Description |
|-----|------|--------|-------------|
| A | 2026-04-10 | N. Johansson | Initial release — empty register, ready for first program |
