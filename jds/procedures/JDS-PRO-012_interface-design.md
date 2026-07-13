# Interface Design Standard (Software UI & HMI)

| | |
|---|---|
| **Document No.** | JDS-PRO-012 |
| **Revision** | D |
| **Date** | 2026-07-13 |
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

## 12. Apple Human Interface Guidelines Alignment

JDS interface design aligns with Apple's Human Interface Guidelines (HIG). The two share a lineage, and where they meet, JDS adopts Apple's conventions **for software UI** — while keeping the JDS palette, JDS English, and the safety primacy of §9.

### 12.1 Shared Foundations

| Apple HIG principle | JDS equivalent | What it means here |
|---------------------|----------------|--------------------|
| **Clarity** | Reduce to Essence + Craft Precision (PRO-007 §2) | Legible text at every size, precise alignment, unambiguous controls |
| **Deference** — content first, chrome recedes | Active Space — emptiness is structure | The interface gets out of the way; content and current state lead |
| **Depth** — layering conveys hierarchy | Compartment Design + corner geometry (§4, PRO-007 §15.4) | Elevation and layers show what contains what, used sparingly |

### 12.2 Adopted Conventions (Software UI)

- **System typography & Dynamic Type.** Use the system font (San Francisco via the `-apple-system` stack; the platform equivalent elsewhere). Respect the user's text-size / Dynamic Type setting — text scales without breaking layout, never fixed-pixel-only.
- **Adaptive, semantic colour with light & dark appearance.** The JDS palette stays the brand and status anchor (Navy / Steel / Signal Red / Amber / Forest Green), but each role resolves to a **light and a dark** value so the UI follows the system appearance. Colour still never carries meaning alone (§7).
- **Hit targets** of at least **44×44 pt** (HIG and §6 agree).
- **Iconography:** one consistent symbol set (SF Symbols on Apple platforms) whose weight matches the adjacent text; an icon always pairs with a label or accessible name.
- **Materials & elevation, sparingly:** translucency or elevation may signal layering (sheets, popovers) — never decoration, never at the cost of contrast (§8).
- **Meaningful motion:** transitions clarify origin and hierarchy; all motion is optional and honours Reduce Motion (§8).
- **Accessibility as a baseline:** screen-reader labels on every control, Dynamic Type, sufficient contrast, Reduce Motion and Reduce Transparency — requirements, not enhancements.

### 12.3 Where HIG Does Not Apply — HMI Safety Primacy

Apple HIG is a standard for consumer software. It does **not** govern safety-critical HMI. On any HMI or control surface (§9), the high-performance-HMI rules **prevail over HIG aesthetics**:

- No translucency, vibrancy, blur, or decorative depth between an operator and the process state.
- Normal state stays low-saturation grey-scale (§9.1); HIG's richer colour and materials are for office software, not control rooms.
- No motion that could mask or delay an alarm.

When the two conflict on an HMI, **§9 wins.** HIG informs the *software UI* layer; it never softens a safety surface.

### 12.4 Iconography — SF Symbols: When, Why, and Which

Apple's **SF Symbols** are the icon vocabulary for JDS software UI. An icon is a second recognition channel, not a decoration — it must earn its place.

**When to use a symbol**

1. For a **repeated action, object, or status** the user scans for (toolbar, list row, status chip) — a known symbol is recognised faster than a word is read (the Glance level, §4).
2. **Always paired with a text label.** The icon never stands alone for any meaningful action — this is Redundant Encoding (§7): novices read the label, experts recognise the symbol, screen readers use the label.
3. From **one consistent set only.** Do not mix icon families. The symbol's **weight matches the adjacent text** and it sits on the optical baseline.
4. Using the symbol's **conventional meaning.** Never repurpose a glyph to mean something else.

**When NOT to use a symbol**

- As decoration or to fill space (Reduce to Essence, §3).
- When a short, unambiguous word is clearer — do not iconise rare or abstract concepts.
- As the **only** indicator of a safety state (§9 — that is shape + colour + text, always).

**Why** — recognition at a glance, a learned vocabulary that stays consistent across every JDS tool, and lower cognitive load for repeated tasks.

**Which** — the canonical mapping (use these SF Symbol names; render at the text's weight):

| JDS action / object | SF Symbol | Notes |
|---------------------|-----------|-------|
| New document | `doc.badge.plus` | Primary create action |
| Document (generic) | `doc.text` | A document/record |
| Generate PDF | `arrow.down.doc` | Render/export |
| Validate / audit | `checkmark.seal` | Run `jds-validate.py` |
| Master register / list | `list.bullet.clipboard` | The document register |
| Document number / identity | `number` | JDS number field |
| Search / find | `magnifyingglass` | Find a document |
| Edit | `pencil` | Modify existing |
| Revision / supersede | `arrow.triangle.2.circlepath` | New revision |
| Reference / cross-link | `link` | Link to another doc |
| Settings | `gearshape` | Configuration |
| Guide Note / Doc mascot | `archivebox` | Doc, the filing cabinet (§11) |
| Timesheet | `clock` | Office doc (TSH) |
| Expense | `creditcard` | Office doc (EXP) |
| Mileage | `car` | Office doc (EXP mileage) |
| 3D model / drawing | `cube` | DWG category |
| Project | `folder` | PRJ category |
| Correspondence | `envelope` | COR category |
| Equipment / inventory | `wrench.and.screwdriver` | LOG category |

**Status symbols** — an optional icon channel beside the dot + word of PRO-007 §6.3 (never replacing it):

| Status | SF Symbol | Colour |
|--------|-----------|--------|
| CURRENT | `checkmark.circle.fill` | Forest Green |
| DRAFT | `circle.dashed` | Amber |
| IN REVIEW | `clock` | Steel Blue |
| OVERDUE | `exclamationmark.circle.fill` | Signal Red |
| SUPERSEDED / ARCHIVED | `archivebox` | Warm Gray |

**Platform note.** On Apple platforms, render these SF Symbols directly by name. On the web or other platforms (e.g. Document Studio), use an **open icon that mirrors the same meaning** — a matching inline SVG at the text's weight. This table defines the *meaning*, not a specific font; the meaning stays constant across platforms.

**HMI exception.** On HMI and control surfaces, iconography follows §9 — standardised, unambiguous, function-first symbols (industry / ISA conventions), never decorative consumer glyphs. SF Symbols are for software UI, not the control surface.

## 13. Long-Form Book Reader Pattern

This pattern governs literary, editorial, archival, and other sustained-reading interfaces. It connects the book typography of `md2book.py` with responsive web readers without making the screen imitate paper mechanically. The content remains primary; page furniture exists only to preserve place and hierarchy.

### 13.1 Information Hierarchy

Every reader must express the following levels in this order. A level may be omitted when the work does not use it, but levels must not be swapped or visually flattened.

| Level | Role | Typical expression |
|-------|------|--------------------|
| **Collection** | Names the complete work or omnibus | Contents title; left-page running head |
| **Book** | Identifies the self-contained volume | Book numeral, volume title, date range |
| **Chapter** | Names the current reading unit | Chapter number, title, year; right-page running head |
| **Section** | Marks an internal movement or scene | Quiet subheading or scene ornament |
| **Body** | Carries the narrative | Serif reading face, controlled measure and leading |
| **Figure** | Supports a specific narrative moment | Image placed after its text anchor with a concise caption |

Controls, navigation, and settings use the system sans-serif. Narrative body text may use a serif face. Metadata is quieter than content through size, weight, spacing, and tone—not colour alone.

### 13.2 Responsive Reading Modes

The reader has two modes driven by available width, not device identity:

- **Continuous mode:** one column in DOM order for narrow screens, enlarged text, zoom, and assistive technology. No blank pages, running heads, folios, or artificial page breaks are exposed.
- **Facing-page mode:** two equal page compartments on wide screens, joined by a centred spine. Both pages share height within a spread, outer margins are equal, and the reading order remains left then right.

The layout must return to continuous mode before either page becomes narrower than a comfortable reading measure. A project may tune the breakpoint, but it must be a named design token rather than a scattered literal value.

### 13.3 Running Heads, Footers, and Folios

Use conventional book furniture consistently:

| Position | Content | Alignment |
|----------|---------|-----------|
| **Verso (left) header** | Collection or omnibus title | Outer edge |
| **Recto (right) header** | Chapter number and chapter title | Outer edge |
| **Footer centre** | Book number, book title or subtitle, and period/year | Centre |
| **Footer outer corner** | Folio (page number) | Outside edge |

Running furniture is orientation, not decoration. It uses the UI face, small type, restrained letter spacing, and a fine rule. Suppress it on blank pages and, where the chapter title is already dominant, on formal chapter-opening pages. Do not repeat it in continuous mode.

### 13.4 Page Composition

- Keep the two page columns equal; do not alternate arbitrary text/image card arrangements between spreads.
- Balance page density while preserving paragraph and scene order. Never split a heading from the first block it introduces.
- Treat figures as substantial blocks during pagination so an image cannot silently overflow its page.
- Place each illustration immediately after the narrative beat it depicts. A plate gallery at the end is supplementary, not a substitute for contextual placement.
- Use captions to add interpretive context, not to repeat the alt text.
- Keep the centred spine, outer margins, rules, shadows, and page numbers uniform across the book.

### 13.5 Accessibility and Interaction

- The DOM remains in logical reading order even when CSS presents paired pages.
- Page wrappers and decorative furniture must not interrupt screen-reader prose. Running heads and repeated footers are hidden from assistive technology.
- Real heading elements define structure; visual styling never substitutes for semantic levels.
- Page turning must not be the only way to advance. Scrolling, keyboard navigation, and direct chapter navigation remain available.
- Page-turn motion is optional, never required, and honours Reduce Motion (§8).
- User text-size settings may increase page height or trigger continuous mode; text must never be clipped to preserve a paper-like rectangle.

### 13.6 Reuse Contract

Implementations expose named content fields—`collectionTitle`, `bookLabel`, `bookTitle`, `chapterLabel`, `chapterTitle`, and `period`—and named layout tokens for the breakpoint, spread width, page padding, rule colour, and page surface. Project-specific titles and measurements must not be hard-coded into pagination logic. The Front-Row Seat Chapter One reader is the web reference implementation; `scripts/md2book.py` is the print reference implementation.

## 14. Self-Check Before Release

- [ ] Glance level works — state/status visible without interaction
- [ ] Primary action is obvious and consistently placed
- [ ] Every action gives feedback within ~100 ms; long actions show progress
- [ ] Invalid actions are prevented, not just reported
- [ ] Irreversible actions are confirmed and visually separated
- [ ] Colour is never the only encoding; contrast meets WCAG AA
- [ ] Fully keyboard-operable with a visible focus indicator
- [ ] (Software UI) System font; text scales with Dynamic Type; light & dark appearance supported (§12)
- [ ] (Software UI) Icons are from one set, paired with a label, and used per the §12.4 mapping — never decorative or alone
- [ ] (Book reader) Collection → book → chapter → section → body → figure hierarchy is visible and semantic (§13.1)
- [ ] (Book reader) Wide screens use equal facing pages; narrow screens preserve one continuous DOM reading order (§13.2)
- [ ] (Book reader) Running heads, footer metadata, and outside folios follow §13.3 and disappear in continuous mode
- [ ] (Book reader) Illustrations are anchored to their narrative beat and counted in page composition (§13.4)
- [ ] (HMI) Normal = grey-scale; colour reserved for the abnormal
- [ ] (HMI) Alarms ranked, actionable, multi-channel; safety actions guarded
- [ ] (HMI) No HIG decoration — no translucency, vibrancy, or motion on the safety surface (§12.3)

## 15. Conformance

Software UIs conform to this standard at code review (alongside the PRO-004 code audit). **JDS-PRJ-SFW-002 (Document Studio)** is the reference implementation: its web UI follows §6–§8, §10–§12. HMI specifications produced for clients cite §9 as the governing standard.

---

## Revision History

| Rev | Date | Author | Description |
|-----|------|--------|-------------|
| A | 2026-06-26 | Nils Johansson | Initial release — the third design pillar (interface). Three-level interaction model, interaction & feedback laws, screen typography/layout, colour & status semantics, accessibility, a full HMI section (situational awareness, alarm discipline, safety-critical actions, physical environment), component conventions, and the Doc mascot boundary for safety-critical surfaces. |
| B | 2026-06-26 | Nils Johansson | Added §12 Apple HIG Alignment — maps Clarity/Deference/Depth to JDS and adopts HIG conventions for software UI (system typography & Dynamic Type, adaptive semantic colour with light/dark appearance, 44pt targets, SF Symbols-style iconography, materials/motion). §12.3 establishes HMI safety primacy: HIG aesthetics never override the §9 safety rules on a control surface. Self-check and Conformance updated. |
| C | 2026-06-26 | Nils Johansson | Added §12.4 Iconography — SF Symbols: when, why, and which. Defines the rules for icon use (recognition channel, always with a label, one set, conventional meaning), a canonical action/object → SF Symbol mapping table and a status-symbol table, the web/other-platform equivalent rule, and the HMI exception. Self-check item added. |
| D | 2026-07-13 | Nils Johansson | Added §13 Long-Form Book Reader Pattern. Defines the reusable collection → book → chapter → section → body → figure hierarchy; responsive continuous and facing-page modes; conventional running heads, footer metadata and outside folios; page-composition and illustration-anchoring rules; accessibility requirements; and a reuse contract shared by web readers and `md2book.py`. |
