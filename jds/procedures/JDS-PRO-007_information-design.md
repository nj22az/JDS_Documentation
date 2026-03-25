# Information Design Standard

| | |
|---|---|
| **Document No.** | JDS-PRO-007 |
| **Revision** | D |
| **Date** | 2026-03-25 |
| **Status** | APPROVED |
| **Author** | Nils Johansson |

---

## 1. Purpose

This standard defines how information is visually presented in JDS documents. It draws on world-class information design traditions — the principles that make the best wayfinding systems, technical infographics, and engineering documents clear and effective.

The core philosophy:

> **How information is presented is inseparable from the information itself. A well-designed document is not a decorated document — it is a document where every visual element serves communication.**

## 2. The Seven Principles

| # | Principle | Meaning |
|---|-----------|---------|
| 1 | **Active Space — Emptiness is structure** | White space organises information. Never fill space for the sake of filling it. |
| 2 | **Compartment Design — The container is content** | Layout, format, and templates are engineering tools, not overhead. |
| 3 | **Visual Explanation — If you can't diagram it, you don't understand it** | Every report should contain at least one visual element. |
| 4 | **Colour is Language** | Every colour means something. Use it consistently. Never decoratively. |
| 5 | **Redundant Encoding** | Critical information in at least two channels: colour + text, icon + word. |
| 6 | **Reduce to Essence** | Remove every element that does not contribute to understanding. |
| 7 | **Craft Precision — Visible quality** | Alignment, spacing, and precision in documents reflect your engineering quality. |

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
- **Line height:** 1.4–1.5x the font size
- **Paragraph spacing:** 6–8pt between paragraphs
- **Maximum line length:** 75–85 characters (beyond this, the eye loses its way)

### 4.3 Font Rules

- Maximum 2 font families per document
- Sans-serif for headings, tables, labels, captions
- Monospace only for codes, reference numbers, and technical identifiers
- Recommended: Calibri (universal), Source Sans Pro (free, excellent), or Inter (modern)

## 5. Layout

### 5.1 Margins

- **Minimum:** 20mm all sides
- **Recommended:** 25mm left/right, 20mm top, 25mm bottom
- **Binding edge:** Add 10mm if document will be bound

### 5.2 Alignment

- Left-align body text (never justify — uneven word spacing disrupts reading rhythm)
- Right-align numbers in tables
- Left-align text in tables
- Centre short codes and status indicators
- **A misaligned element undermines the credibility of everything around it**

### 5.3 Compartment Layout

For one-page summaries, cover sheets, and project cards, use the compartment principle — self-contained sections that form a complete whole:

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
| **White/Off-white** | Background, breathing room | Active space — receptive space |

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

### 6.4 Logo Colour Variants by Document Category

The Johansson Engineering stamp logo appears in a category-specific colour on every PDF. This provides instant glance-level identification of document type — you can tell a procedure from a letter from across the room.

| Category | Logo Colour | Hex | Rationale |
|----------|------------|-----|-----------|
| QMS, PRO | Navy Blue | #1B3A5C | System governance, authority |
| RPT, MAN | Deep Teal | #2E6B8A | Technical execution, findings |
| DWG | Steel Blue | #4A90A4 | Drawings, models, CAD |
| PRJ | Project Blue | #3A7CA5 | Project documents |
| LOG | Forest Green | #3D8B6E | Logs, registers, records |
| COR, BLG | Heritage Red | #8B2D2D | Communication, published work |
| TSH, EXP | Warm Bronze | #6B5B3E | Administrative, time and cost |
| TMP | Neutral Gray | #5C5C5C | Templates (blank forms) |

**Rules:**

1. The logo SVG source is `jds/assets/logo.svg`. Colour variants are generated by `scripts/logo-variants.py`.
2. PDF generators (`md2pdf.py`, `md2letter.py`) automatically select the correct colour variant based on the document number.
3. The logo colour must always match the document category — never mix colours.
4. When printing in black and white, the category is still identified by the document number (redundant encoding, §6.2 rule 2).

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

## 8. The Craft Precision Standard

> **The quality of your documentation is the visible surface of the quality of your engineering.**

A client who receives a report with inconsistent formatting, misaligned tables, and unclear hierarchy will question the quality of the engineering itself. Conversely, a report with clean layout, clear hierarchy, and meaningful visuals communicates professional integrity.

This is not about making things "pretty." It is about **precision made visible.**

### 8.1 Self-Check Before Issue

Before issuing any document, verify:

- [ ] Headings follow the 4-level hierarchy consistently
- [ ] Text is left-aligned, numbers are right-aligned
- [ ] Colour is used meaningfully, not decoratively
- [ ] Active space separates sections clearly
- [ ] At least one visual element is present (for reports)
- [ ] Status block is complete and colour-coded
- [ ] The document works at all three reading levels (glance, scan, read)

## 9. Grid System & Vertical Rhythm

### 9.1 The Baseline Unit

All vertical spacing derives from a **base unit of 6pt** (the paragraph spacing). This creates a consistent rhythm throughout the document.

| Spacing | Value | Use |
|---------|-------|-----|
| **1 unit** | 6pt | Paragraph spacing, list item gap |
| **2 units** | 12pt | Between heading and first paragraph |
| **3 units** | 18pt | Above H2 sections |
| **2.5 units** | 15pt | Above H3 subsections |
| **4 units** | 24pt | Major section breaks |

**Rule:** Never use arbitrary spacing values. Every gap must be a multiple (or half-multiple) of 6pt.

### 9.2 Horizontal Grid

Body text occupies the full text width. The metadata identity block occupies 55–75% of text width, left-aligned. Tables default to 100% width unless semantically inappropriate (e.g., short lookup tables).

### 9.3 Content Density

**Every page should carry meaningful content.** If a page is more than 40% empty (excluding the final page), restructure. White space is intentional structure (active space), not leftover gap.

## 10. Page Architecture

### 10.1 Page Zones

Every page has five zones, separated by thin rules:

```
┌─────────────────────────────────────────────┐
│ HEADER: Doc No  |  Title  |  UNCONTROLLED   │  ← 7pt, Warm Gray
├─────────────────────────────────────────────┤  ← 0.25pt rule
│                                             │
│                 BODY ZONE                   │
│                                             │
├─────────────────────────────────────────────┤  ← 0.25pt rule
│ FOOTER: Rev     |  Page N of M  |  Date     │  ← 7pt, Warm Gray
└─────────────────────────────────────────────┘
```

### 10.2 First Page (Title Page Zone)

Page 1 has a distinctive treatment:

1. **Document number** in header (top-left, Navy, bold)
2. **H1 title** — largest text on the page, Navy, underlined
3. **Identity strip** — compact metadata table (55–75% width), not full-width
4. **No running title** in header (title is visible in body)
5. Content begins immediately after identity strip — no wasted space

### 10.3 Continuation Pages

Pages 2+ include the running document title in the top-centre header. This satisfies the glance-level reading requirement: any loose page can be identified in 0.5 seconds.

## 11. Micro-Typography

### 11.1 Letter-Spacing (Tracking)

| Element | Tracking | Reason |
|---------|----------|--------|
| H1 title | -0.3pt | Tighter headlines feel authoritative |
| Uppercase labels | +0.5pt | Small caps need air to breathe |
| Body text | Default (0) | System font handles this |
| Footer/header | +0.3pt | Small text needs looser tracking |

### 11.2 Font Weight Discipline

| Level | Weight | Numeric |
|-------|--------|---------|
| H1 | Bold | 700 |
| H2 | Bold | 700 |
| H3 | SemiBold | 600 |
| H4 | SemiBold Italic | 600 |
| Body | Regular | 400 |
| Strong/emphasis | SemiBold | 600 |
| Metadata labels | SemiBold | 600 |
| Headers/footers | Regular | 400 |

### 11.3 Contrast Ratios (Accessibility)

All text must meet **WCAG 2.1 Level AA** minimum contrast:

| Element | Colour | Background | Ratio | Pass? |
|---------|--------|------------|-------|-------|
| Body text (#222) | Dark gray | White | 16.8:1 | AA |
| H1/H2 (#1B3A5C) | Navy | White | 10.2:1 | AA |
| H3 (#4A90A4) | Steel Blue | White | 4.6:1 | AA |
| Metadata (#8C8C8C) | Warm Gray | White | 3.5:1 | AA Large |
| Table header (#1B3A5C) | Navy | #f0f3f6 | 9.4:1 | AA |

**Rule:** Never use light text on light backgrounds. Warm Gray (#8C8C8C) is the lightest permissible text colour, and only for metadata and annotations at 7pt+ sizes.

## 12. Figure & Table Conventions

### 12.1 Sequential Numbering

All figures and tables should be referenced in text before they appear:
- **Tables:** "Table 1", "Table 2", etc. (or "Table 3.1" for section-numbered documents)
- **Figures:** "Figure 1", "Figure 2", etc.

The metadata identity strip at the top of every document is **not** counted in table numbering — it is part of the document's identity, not its content.

### 12.2 Revision History Table

The revision history table at the end of every document has a **distinct visual treatment** from data tables — it uses the same compact, borderless style as the metadata identity strip. This signals "this is document metadata" rather than "this is technical data."

## 13. Emptiness & Receptivity

> **"Emptiness is not the absence of content but the presence of potential."**

This section codifies the philosophical distinction between **minimalism** (removing things) and **emptiness** (creating receptive space). In JDS documents:

- White space is not "unused" — it is **active structure** that guides the eye
- A page with 30% white space is not wasting paper — it is **breathing**
- The margin is not a border — it is a **frame** that gives the content meaning
- The gap between sections is not empty — it is the **active space** that separates ideas

JDS designs documents the way engineers design spaces — with intention in every absence.

## 14. Automation & Consistency

### 14.1 PDF Generation

All JDS documents are converted to PDF using `scripts/md2pdf.py`, which enforces every rule in this standard automatically. The stylesheet is the single source of truth for visual presentation — authors write content in markdown and the system handles design.

### 14.2 What the System Enforces Automatically

| Rule | How it's enforced |
|------|-------------------|
| Typography hierarchy | CSS heading styles |
| Colour palette | CSS colour definitions |
| Page layout & margins | @page rules |
| Header/footer content | Metadata extraction + @page margin boxes |
| Table styling | CSS table rules |
| Vertical spacing | CSS margin/padding |
| Font selection | CSS font-family stack |
| UNCONTROLLED COPY marking | @page top-right content |

### 14.3 What Authors Must Verify

| Check | Method |
|-------|--------|
| Single H1 per document | Visual review |
| No skipped heading levels | Visual review |
| Metadata header complete | Pre-flight checklist |
| Revision history present | Pre-flight checklist |
| Visual content in reports | Pre-flight checklist |
| Three-level readability | Craft precision self-check |

---

## Revision History

| Rev | Date | Author | Description |
|-----|------|--------|-------------|
| A | 2026-03-25 | Nils Johansson | Initial release — typography, colour system, layout principles, visual standards, compartment layout, craft precision philosophy |
| B | 2026-03-25 | Nils Johansson | Added grid system (§9), page architecture (§10), micro-typography (§11), figure/table conventions (§12), emptiness philosophy (§13), automation rules (§14) |
| C | 2026-03-25 | Nils Johansson | Added §6.4 Logo Colour Variants — category-specific logo colours for glance-level document identification. SVG logo and automated variant generation. |
| D | 2026-03-25 | Nils Johansson | Language authority update — all terminology now JDS English. Japanese loan words replaced with JDS-owned terms (Active Space, Compartment Design, Visual Explanation, Craft Precision). |
