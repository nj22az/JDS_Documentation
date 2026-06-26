# Interface Design Standard (Software UI & HMI)

| | |
|---|---|
| **Document No.** | JDS-PRO-012 |
| **Revision** | A |
| **Date** | 2026-06-26 |
| **Status** | APPROVED |
| **Author** | Nils Johansson |

---

## 1. Purpose

This standard defines how **interactive interfaces** look and behave under JDS — both software application interfaces (UI) and human-machine interfaces (HMI). It is the third design pillar, completing the set:

| Pillar | Standard | Governs |
|--------|----------|---------|
| **Code** | JDS-PRO-004 | How software is *written* — structure, naming, no dead code |
| **Document** | JDS-PRO-007 | How *documents and PDFs* look — typography, colour, layout |
| **Interface** | **JDS-PRO-012 (this)** | How *interactive screens* look and behave — UI and HMI |

A document is read. An interface is *operated*. The difference is feedback: the interface must answer, at every moment, "what state am I in, what can I do, and what just happened?"

## 2. Scope

Applies to every interactive interface produced under JDS:

- **Software UI** — application interfaces in `projects/software/JDS-PRJ-SFW-*` (web, desktop, CLI front-ends).
- **HMI** — operator panels, control screens, and equipment interfaces *designed or specified* in JDS engineering work (§9 governs these specifically).

Out of scope: document layout (PRO-007), code structure (PRO-004), and pure CLI tool output (covered by PRO-007 §15.6 for mascot voice).

## 3. Core Principle

> **An interface is a tool, not a destination. It makes the right action obvious, the current state unmistakable, and the wrong action hard.**

The seven JDS principles (PRO-007 §2) carry over directly: Active Space organises controls; Compartment Design groups them; Colour is Language; Redundant Encoding keeps meaning when colour fails; Reduce to Essence removes clutter; Craft Precision makes alignment and spacing visible quality.

## 4. The Three-Level Interaction Model

Every interface must work at three levels, mirroring the three-level reading system (PRO-007 §3):

| Level | Time | The user learns | Design requirement |
|-------|------|-----------------|-------------------|
| **Glance** | 0.5 s | What state is this in? Is anything wrong? | Status / alarm visible without interaction |
| **Scan** | 5 s | What can I do here? | Primary actions obvious, grouped, labelled |
| **Operate** | task | Full control, with confirmation it worked | Every action gives feedback |

If Glance and Scan fail, the operator hesitates — and in an HMI, hesitation is a hazard.

## 5. Interaction & Feedback Laws

1. **State is always visible.** The current state of the system (or document, or job) is shown on screen, never held only in the user's memory.
2. **Every action is acknowledged.** A control responds within ~100 ms (visual press, focus, or spinner). Operations longer than ~1 s show progress, not a frozen screen.
3. **Prevent the error, don't just report it.** Disable invalid actions, validate input inline, and constrain inputs so an impossible state cannot be entered.
4. **Reversible by default; confirm the irreversible.** Destructive or irreversible actions require explicit confirmation and are visually separated from routine ones. Offer undo wherever feasible.
5. **Forgiving recovery.** Every error message states what happened *and the way out*. No dead ends.

## 6. Layout & Typography for Screens

- **Font:** clean sans-serif (Gothic) for all UI text. Reserve serif for long-form reading surfaces only (e.g. a blog), never for controls.
- **Size:** UI body text **≥ 14px (≈10.5pt)**, never below 11px. Generous line-height **1.4–1.5** (PRO-007 §4.2).
- **Alignment:** left-align text; right-align numeric columns. **Never justify** (PRO-007 §5.2).
- **Compartment layout:** group controls by function with active space between groups; one primary action per view.
- **Target size:** pointer targets ≥ **24px**; touch targets ≥ **44px**; gloved/industrial targets ≥ **60px** (§9).
- **Consistent placement:** the primary action holds the same position across views; destructive actions are never adjacent to it.

## 7. Colour & Status Semantics

- Reuse the **JDS palette** (PRO-007 §6.1) unchanged: Navy/Steel build structure; Signal Red, Amber, and Forest Green carry status — and mean the *same thing* they mean in documents.
- **Never colour alone (Redundant Encoding).** Pair every status colour with text, an icon, or a shape, so the meaning survives colour-blindness, glare, and monochrome failure.
- **CUD-safe:** no pure red/green binary for pass/fail (PRO-007 §6.2). Use the muted JDS Signal Red / Forest Green and add a second channel.
- **Status indicator pattern:** coloured dot + word, exactly as PRO-007 §6.3 (`● CURRENT`, `● OVERDUE`, …).

## 8. Accessibility (Non-Negotiable)

- Contrast meets **WCAG 2.1 Level AA** (PRO-007 §11.3).
- Fully **keyboard-operable**; focus order is logical and the **focus indicator is always visible**.
- Every control has a programmatic **label** (a placeholder is not a label).
- Honour the user's **reduced-motion** preference; motion is never required to understand state.

## 9. HMI — Human-Machine Interfaces

HMIs are interfaces to physical processes and equipment. They are **safety-critical**, and the rules here are stricter than for office software. They draw on high-performance HMI practice (the principles behind ISA-101 and the alarm standard IEC 62682 / ISA-18.2), stated in JDS English.

### 9.1 Situational Awareness First

The screen answers **"is the process normal?"** in one glance. Normal running state is shown in **low-saturation grey-scale**; saturated colour is **reserved for the abnormal**. A screen that is "all grey" means "all well" — colour draws the eye only where attention is needed.

### 9.2 Alarm Discipline

- Every alarm is **ranked by priority** and shown with colour **+ shape + text** (never colour alone).
- An alarm is raised only when an **operator action is required** — no alarm flood, no decorative alerts.
- Provide controlled **alarm shelving** (temporarily silencing a known alarm) with an audit trail. Suppressed alarms remain visible as suppressed.

### 9.3 Safety-Critical Actions

- Commands that move equipment or change process state are **guarded**: two-step or explicit confirmation, with the consequence stated.
- **Fail-safe defaults:** on loss of input or signal, the interface defaults to the safe state, not the last command.
- No destructive or hazardous action is ever **one mis-tap away** from a routine one.

### 9.4 Physical Environment

- Readable in **direct sunlight and low light**; contrast minimums exceed office UI.
- Targets sized for **gloved hands** (§6, ≥ 60px) and tolerant of vibration and motion.
- **No decoration** — no gratuitous animation, gradients, or skeuomorphism on a control surface. Precision over polish.
- **Redundant encoding is mandatory**, not optional: operators may be colour-blind, and a degraded display may be monochrome.

## 10. Component Conventions

- **Buttons:** primary (filled Navy), secondary (outlined Steel), destructive (Signal Red, separated). Consistent across the app.
- **Forms:** labelled controls, inline validation, the primary action disabled until the form is valid.
- **Tables:** reuse the document table semantics — Navy header, subtle zebra shading, left-aligned text, right-aligned numbers (PRO-007 §7.3).
- **Callouts:** the same marker family as documents — Warning / Done / Note (PRO-007 §15).

## 11. The Doc Mascot in Interfaces

Guide Notes from **Doc** (PRO-007 §15) are welcome in **software UIs** for onboarding, help, and reassurance — one or two, never crowding the task.

They are **prohibited on HMI and any safety-critical surface.** Nothing cute belongs between an operator and an alarm. On a control screen, the only voice is the precise state of the process.

## 12. Self-Check Before Release

- [ ] Glance level works — state/status visible without interaction
- [ ] Primary action is obvious and consistently placed
- [ ] Every action gives feedback within ~100 ms; long actions show progress
- [ ] Invalid actions are prevented, not just reported
- [ ] Irreversible actions are confirmed and visually separated
- [ ] Colour is never the only encoding; contrast meets WCAG AA
- [ ] Fully keyboard-operable with a visible focus indicator
- [ ] (HMI) Normal = grey-scale; colour reserved for the abnormal
- [ ] (HMI) Alarms ranked, actionable, multi-channel; safety actions guarded

## 13. Conformance

Software UIs conform to this standard at code review (alongside the PRO-004 code audit). **JDS-PRJ-SFW-002 (Document Studio)** is the reference implementation: its web UI follows §6–§8 and §10–§11. HMI specifications produced for clients cite §9 as the governing standard.

---

## Revision History

| Rev | Date | Author | Description |
|-----|------|--------|-------------|
| A | 2026-06-26 | Nils Johansson | Initial release — the third design pillar (interface). Three-level interaction model, interaction & feedback laws, screen typography/layout, colour & status semantics, accessibility, a full HMI section (situational awareness, alarm discipline, safety-critical actions, physical environment), component conventions, and the Doc mascot boundary for safety-critical surfaces. |
