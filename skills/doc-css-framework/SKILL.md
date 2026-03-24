---
name: doc-css-framework
description: "Shared HTML/CSS framework for generating branded, print-ready Airtable documentation. Dependency read by doc-generating skills (workflow-doc, technical-design-doc, etc.) before they render HTML. Provides: brand color detection algorithm with Airtable fallback palette, complete CSS variable system, all component classes (section-header, cards, ERD, automations, interfaces, permissions matrix, etc.), tested landscape print CSS, and language/tone rules."
---

# Doc CSS Framework

Shared CSS framework, brand theming, print optimization, and language rules for all Airtable documentation skills. This file is **read by other skills at generation time** — it is not invoked directly.

**Consuming skills:** `workflow-doc`, `technical-design-doc`, and any future doc-generating skill should read this file before rendering HTML output.

---

## How to Use This Framework

1. **Read this file first** — for brand detection, the component reference guide, print principles, and language rules
2. **Then read `references/css-components.md`** — for the complete CSS code blocks to copy into your document's `<style>` tag

This two-file structure keeps the guide lean while making the full CSS available on demand. The references file has a table of contents — use it to jump to the section you need.

---

## 1. Brand Color Detection

Before generating any document, identify the customer's brand colors:

1. Extract the customer/company name from the input
2. Search the web for `"[Company Name] brand colors hex codes"` to find their primary and accent colors
3. If found: use their brand palette (primary for headers/actors, accent for decisions/highlights)
4. If not found: fall back to Airtable brand colors:

**Airtable Default Palette:**
| Variable | Role | Hex |
|----------|------|-----|
| Primary Blue | Headers, badges, buttons | `#2D7FF9` |
| Accent Yellow | Decision nodes, highlights | `#FCB400` |
| Secondary Teal | Links, secondary accents | `#18BFFF` |
| Accent Pink | Special callouts | `#FF08C2` |
| Error Red | Blocked states, errors | `#EF3061` |

Apply the detected (or fallback) colors to the `--primary` and `--accent` variables in the CSS.

---

## 2. CSS Variables Overview

The framework uses CSS custom properties for all brand-sensitive values. The variables you'll customize per document:

- `--primary` — replace with detected brand primary color
- `--primary-light` — auto-derive as 10% opacity tint of primary (or use `#E8F0FE` as default)
- `--primary-dark` — auto-derive as darkened primary (or use `#1B5FC4` as default)
- `--accent` — replace with detected brand accent color
- `--accent-light` — auto-derive as 10% opacity tint of accent (or use `#FEF8E1` as default)

### Typography Variables

The framework uses a split font pairing system. These are the defaults — do not change them unless specifically requested:

- `--font-heading` — **Plus Jakarta Sans** (geometric, clean, modern)
- `--font-body` — **Sora** (clean, slightly rounded sans-serif with natural warmth)
- `--heading-weight` — `500` (medium — intentionally light for a modern editorial feel)
- `--heading-spacing` — `0em` (default letter-spacing)

**Google Fonts import line** (include in every document's `<head>`):
```html
<link href="https://fonts.googleapis.com/css2?family=Sora:wght@300;400;500;600&family=Plus+Jakarta+Sans:wght@400;500;600;700&family=JetBrains+Mono:wght@400&display=swap" rel="stylesheet">
```

**Usage rules:**
- All `h1`, `h2`, `h3`, `h4`, `.section-title`, `.story-title`, `.q-cat-title`, card heading elements → `font-family: var(--font-heading); font-weight: var(--heading-weight);`
- Body, paragraphs, list items, descriptions → inherit from `body { font-family: var(--font-body) }`
- Structural labels (badges, metric labels, uppercase captions) → keep `font-weight: 600–700` for visual hierarchy, but still use `var(--font-body)`
- ERD table headers → `font-weight: 600` (slightly heavier than content headings for table contrast)
- Monospace elements (field types, code) → `JetBrains Mono`

All other variables (neutrals, semantic colors, shadows) are constants — copy them unchanged from `references/css-components.md` Section 1.

---

## 3. Component Reference Guide

When planning the HTML structure of a document, use this table to select the right component class:

| Need | Component | Class |
|------|-----------|-------|
| Numbered section heading | Section header | `.section-header` + `.section-number` |
| Section description callout | Section intro | `.section-intro` |
| Sub-section label | Section sub | `.section-sub` |
| User role card | Persona card | `.persona-card` in `.persona-grid` |
| Functional module card | Module card | `.module-card` in `.module-grid` |
| Automation trigger→action | Auto card + flow | `.auto-card` + `.auto-flow` |
| Interface overview | Interface card | `.interface-card` |
| User walkthrough | Guide section | `.guide-section` |
| Warm callout | Summary card | `.summary-card` |
| Key-value detail pairs | Detail grid | `.detail-grid` + `.detail-item` |
| Stats at section top | Stats bar | `.stats-bar` + `.stat-chip` |
| Table schema visual | ERD table | `.erd-table` in `.erd-grid` |
| Table relationships | Relationship list | `.erd-relationships` |
| Field specifications | Field table | `.field-table` |
| Permissions grid | Access matrix | `.access-matrix` |
| Page listing | Page list | `.page-list` |
| Inline field display | Field chips | `.field-chips` + `.field-chip` |
| Code/template preview | Config block | `.config-block` |
| Design changes | Changelog | `.changelog-table` |
| Term definitions | Glossary | `.glossary-item` |
| User story | Story card | `.story-card` |
| Workflow diagram | Workflow card | `.workflow-card` |
| Data design card | WF data card | `.wfdata-card` |
| Clarifying questions | Question category | `.q-cat` + `.q-item` |

Full CSS for every component is in `references/css-components.md`.

---

## 4. Print Optimization Principles

The print CSS in `references/css-components.md` Section 7 is the production-ready `@media print` block — copy it in full. Here's the reasoning behind its design, so you can make good decisions when a document has unusual layout needs:

**Section flow:** Sections should flow naturally into one another. The only element that gets a forced page break is the cover page (`.doc-header`), which becomes a standalone title page. Adding `page-break-before: always` to section elements creates full blank pages of whitespace — a very common mistake that's hard to spot without printing.

**CSS Grid and page breaks:** CSS Grid containers ignore `break-inside: avoid` on their children, meaning child cards will split across pages regardless of that property. The solution is to convert grid parents to `display: block` in print, with children as `display: inline-block` at 48% width. This gives a 2-per-row landscape layout while letting the browser honor break constraints on each card. The ERD grid is the one exception — ERD table cards are compact enough that 3-across CSS grid works reliably.

**Cross-browser card preservation:** Both `break-inside: avoid !important` and `page-break-inside: avoid !important` are needed on every card element. Chrome's behavior across flex and grid contexts requires both properties to be reliable.

**Section-intro whitespace trap:** Avoid adding `break-after: avoid` to `.section-intro`. When the element immediately following the intro doesn't fit on the same page, the browser stretches the intro box to fill the remaining space — producing a large blank area. Use `break-after: auto` instead.

**Color preservation:** Browsers strip background colors from printed pages by default. All branded backgrounds need `-webkit-print-color-adjust: exact` and the `@media print` equivalents with `!important` to survive.

---

## 5. Language & Tone Rules

All doc-generating skills must follow these rules to ensure documents read as if the SA authored them directly:

1. **Never reference sources.** Never use "transcript", "call recording", "meeting notes", "auto-generated", or any language that reveals the source material or generation process.

2. **Clarifying question contexts** should state observations as facts, not cite their origin. Write "Each person manages their own projects, but Kim tracks all of them" — not "The transcript says each person manages their own projects."

3. **Technical sections** (Data Model, Automations, Permissions) — precise and specific. Use exact field names, table names, formula syntax.

4. **User Guide sections** — plain, friendly language for non-technical users. Avoid Airtable jargon without explanation.

5. **Executive Summary** — concise, business-focused. No technical jargon.

---

## Reference Files

- **`references/css-components.md`** — Complete CSS code blocks for all components and the full `@media print` block. Read this file and copy its contents into your document's `<style>` tag, then replace `--primary` and `--accent` with the detected brand colors.
