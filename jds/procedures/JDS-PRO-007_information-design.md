# Information Design Standard

| | |
|---|---|
| **Document No.** | JDS-PRO-007 |
| **Revision** | A |
| **Date** | 2026-03-25 |
| **Status** | APPROVED |
| **Author** | Nils Johansson |

---

## 1. Purpose

This standard defines how information is visually presented in JDS documents. It draws primarily on the Japanese information design tradition — the same principles that make Tokyo Metro maps, Japanese wayfinding systems, and technical infographics world-leading in clarity.

The core philosophy:

> **How information is presented is inseparable from the information itself. A well-designed document is not a decorated document — it is a document where every visual element serves communication.**

## 2. The Seven Principles

| # | Principle | Origin | Meaning |
|---|-----------|--------|---------|
| 1 | **Ma (間) — Emptiness is structure** | Japanese | White space organises information. Never fill space for the sake of filling it. |
| 2 | **Bento — The container is content** | Japanese | Layout, format, and templates are engineering tools, not overhead. |
| 3 | **Zukai — If you can't diagram it, you don't understand it** | Japanese | Every report should contain at least one visual element. |
| 4 | **Colour is language** | Tokyo Metro | Every colour means something. Use it consistently. Never decoratively. |
| 5 | **Redundant encoding** | Japanese wayfinding | Critical information in at least two channels: colour + text, icon + word. |
| 6 | **Reduce to essence** | Kenya Hara / MUJI | Remove every element that does not contribute to understanding. |
| 7 | **Craft is visible** | Monozukuri | Alignment, spacing, and precision in documents reflect your engineering quality. |

## 3. The Three-Level Reading System

Every document must work at three reading levels:

| Level | Time | What the reader gets | Design requirement |
|-------|------|---------------------|-------------------|
| **Glance** | 0.5 seconds | What is this? What is its status? | Document number, title, and status indicator visible from arm's length |
| **Scan** | 5 seconds | What does it cover? Key findings? | Clear headings, key data callouts, summary block, visual elements |
| **Read** | Minutes | Full comprehension | Well-structured body text, tables, detailed data |

If Level 1 and Level 2 fail, Level 3 will never be reached — the reader gives up or misnavigates.

## 4. Typography

### 4.1 Heading Hierarchy (4 Levels Maximum)

| Level | Use | Size | Style |
|-------|-----|------|-------|
| H1 | Document title | 18–22pt | Bold |
| H2 | Major sections | 14–16pt | Bold, line below |
| H3 | Subsections | 12–13pt | Bold |
| H4 | Sub-subsections | 11–12pt | Bold italic |

**If you need a fifth level, your document structure is too deep. Restructure.**

### 4.2 Body Text

- **Size:** 10–11pt (never smaller than 9pt, even for notes)
- **Line height:** 1.4–1.5x the font size (this is the ma between lines)
- **Paragraph spacing:** 6–8pt between paragraphs
- **Maximum line length:** 75–85 characters (beyond this, the eye loses its way)

### 4.3 Font Rules

- Maximum 2 font families per document
- Sans-serif for headings, tables, labels, captions
- Monospace only for codes, reference numbers, and technical identifiers
- Recommended: Calibri (universal), Source Sans Pro (free, excellent), or Inter (modern)

## 5. Layout

### 5.1 Margins (The Frame of Ma)

- **Minimum:** 20mm all sides
- **Recommended:** 25mm left/right, 20mm top, 25mm bottom
- **Binding edge:** Add 10mm if document will be bound

### 5.2 Alignment

- Left-align body text (never justify — uneven word spacing disrupts reading rhythm)
- Right-align numbers in tables
- Left-align text in tables
- Centre short codes and status indicators
- **A misaligned element undermines the credibility of everything around it**

### 5.3 The Bento Box Layout

For one-page summaries, cover sheets, and project cards, use the bento principle — self-contained compartments that form a complete whole:

```
┌────────────────────────────────┬──────────────────┐
│ DOCUMENT IDENTITY              │ STATUS BLOCK     │
│ Number, title, project         │ Rev, status,     │
│                                │ date, author     │
├────────────────────────────────┼──────────────────┤
│                                │                  │
│ MAIN CONTENT                   │ KEY DATA         │
│ (largest compartment —         │ Bullet points,   │
│  the "main dish")              │ key metrics,     │
│                                │ critical values  │
│                                │                  │
├────────────────────────────────┴──────────────────┤
│ ACTIONS / RECOMMENDATIONS / NEXT STEPS            │
├───────────────────────────────────────────────────┤
│ VISUAL: Diagram, chart, map, or photograph        │
└───────────────────────────────────────────────────┘
```

Each compartment works independently. A reader can go directly to KEY DATA without reading the main content.

## 6. Colour System

### 6.1 The JDS Colour Palette

| Colour | Use | Meaning |
|--------|-----|---------|
| **Navy Blue** | Primary headings, document identity | Authority, primary information |
| **Steel Blue** | Secondary headings, cross-references | Supporting information |
| **Signal Red** | Warnings, overdue items, critical findings | Immediate attention required |
| **Amber** | Cautions, approaching deadlines, monitor items | Warning, review needed |
| **Forest Green** | Approved, complete, current, satisfactory | Proceed, no action needed |
| **Warm Gray** | Metadata, references, notes, archived | Supporting, non-critical |
| **White/Off-white** | Background, breathing room | Ma — receptive space |

### 6.2 Colour Rules

1. **Every colour must mean something.** If a colour appears, a reader should be able to ask "what does this colour mean?" and get a consistent answer.
2. **Never use colour as the only encoding.** Always pair colour with text or an icon (for accessibility and photocopy safety).
3. **Maximum 3 colours per page** (excluding black and white). More creates visual noise.

### 6.3 Document Status Indicators

```
● CURRENT    (green)   — Active, approved document
● DRAFT      (amber)   — In preparation, not yet approved
● IN REVIEW  (blue)    — Awaiting review/approval
● SUPERSEDED (gray)    — Replaced by newer revision
● OVERDUE    (red)     — Past scheduled review date
● ARCHIVED   (gray)    — No longer in active use
```

The colour dot provides glance-level information. The word provides redundant encoding. Neither alone is sufficient.

## 7. Visual Content Requirements

### 7.1 Minimum Visual Content

- Every report (RPT) over 3 pages must contain at least one diagram, chart, or annotated photograph
- Every procedure (PRO) involving physical work should include step photographs
- Every project README should include a visual element (diagram, render, or status overview)

### 7.2 Diagram Standards

| Line type | Meaning |
|-----------|---------|
| Solid line | Direct connection or flow |
| Dashed line | Indirect relationship or reference |
| Arrow | Direction of flow or causation |
| Bold/double line | Primary or critical connection |

### 7.3 Data Presentation

- Present inspection data as **colour-mapped diagrams** where possible (spatial context makes data meaningful)
- Use **progress bars** for equipment status and running hours (instantly understood)
- When presenting before/after data, use **side-by-side visual comparison**
- Always include **threshold lines** on charts — a measurement without a standard is meaningless
- Tables: subtle alternating row shading, generous cell padding, units in header only

## 8. The Monozukuri Standard

> **The quality of your documentation is the visible surface of the quality of your engineering.**

A client who receives a report with inconsistent formatting, misaligned tables, and unclear hierarchy will question the quality of the engineering itself. Conversely, a report with clean layout, clear hierarchy, and meaningful visuals communicates professional integrity.

This is not about making things "pretty." It is about **precision made visible.**

### 8.1 Self-Check Before Issue

Before issuing any document, verify:

- [ ] Headings follow the 4-level hierarchy consistently
- [ ] Text is left-aligned, numbers are right-aligned
- [ ] Colour is used meaningfully, not decoratively
- [ ] White space (ma) separates sections clearly
- [ ] At least one visual element is present (for reports)
- [ ] Status block is complete and colour-coded
- [ ] The document works at all three reading levels (glance, scan, read)

---

## Revision History

| Rev | Date | Author | Description |
|-----|------|--------|-------------|
| A | 2026-03-25 | Nils Johansson | Initial release — typography, colour system, layout principles, visual standards, bento box layout, monozukuri philosophy |
