# CSS Components Reference

Complete CSS code blocks for all Airtable documentation components. Copy the entire contents of this file into your document's `<style>` tag, then replace `--primary` and `--accent` with the detected brand colors.

## Table of Contents

1. [CSS Variables & Base Styles](#1-css-variables--base-styles)
2. [Doc Header](#2-doc-header)
3. [Section Framework](#3-section-framework)
4. [Stats Bar](#4-stats-bar)
5. [Card Components](#5-card-components) — Persona, Module, Summary, Interface, Automation, Guide
6. [Flow Visualization](#6-flow-visualization)
7. [Detail Grids](#7-detail-grids)
8. [Data Model / ERD Components](#8-data-model--erd-components)
9. [Field & Data Tables](#9-field--data-tables)
10. [Permissions Matrix](#10-permissions-matrix)
11. [Appendix Components](#11-appendix-components)
12. [Workflow-Doc Specific Components](#12-workflow-doc-specific-components)
13. [Print CSS (Landscape PDF)](#13-print-css-landscape-pdf) ← tested, production-ready block

---

## 1. CSS Variables & Base Styles

Replace `--primary`, `--primary-light`, `--primary-dark`, `--accent`, and `--accent-light` with the detected brand colors. All other values are constants.

```css
:root {
  /* ── Brand Colors (replace with detected values) ── */
  --primary: #2D7FF9;
  --primary-light: #E8F0FE;
  --primary-dark: #1B5FC4;
  --accent: #FCB400;
  --accent-light: #FEF8E1;

  /* ── Semantic Colors (constants) ── */
  --success: #065F46;
  --success-light: #D1FAE5;
  --warning: #92400E;
  --warning-light: #FEF3C7;
  --error-red: #EF3061;
  --accent-teal: #18BFFF;
  --accent-pink: #FF08C2;

  /* ── Neutrals ── */
  --text: #1F2937;
  --text-muted: #6B7280;
  --bg: #FFFFFF;
  --bg-light: #F9FAFB;
  --border: #E5E7EB;

  /* ── Shared Tokens ── */
  --card-shadow: 0 1px 3px rgba(0,0,0,0.08), 0 1px 2px rgba(0,0,0,0.06);
  --radius: 8px;

  /* ── Typography ── */
  --font-heading: 'Plus Jakarta Sans', sans-serif;
  --font-body: 'Sora', sans-serif;
  --heading-weight: 500;
  --heading-spacing: 0em;
}

* { margin: 0; padding: 0; box-sizing: border-box; }

body {
  font-family: var(--font-body), -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
  color: var(--text);
  background: var(--bg-light);
  line-height: 1.6;
  -webkit-font-smoothing: antialiased;
}

.page {
  max-width: 1200px;
  margin: 0 auto;
  padding: 40px 32px;
}
```

---

## 2. Doc Header

The branded header at the top of every document.

```css
.doc-header {
  text-align: center;
  margin-bottom: 40px;
  padding: 32px 24px;
  background: linear-gradient(135deg, var(--primary) 0%, var(--primary-dark) 100%);
  border-radius: var(--radius);
  color: white;
}
.doc-header-badge {
  display: inline-block;
  padding: 4px 14px;
  background: var(--accent);
  color: white;
  border-radius: 12px;
  font-size: 11px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  margin-bottom: 12px;
}
.doc-header h1 {
  font-family: var(--font-heading);
  font-size: 28px;
  font-weight: var(--heading-weight);
  letter-spacing: var(--heading-spacing);
  margin-bottom: 6px;
}
.doc-header-sub {
  font-size: 14px;
  opacity: 0.85;
}
```

**HTML pattern:**
```html
<div class="doc-header">
  <div class="doc-header-badge">Document Type Label</div>
  <h1>Solution Name</h1>
  <div class="doc-header-sub">Customer Name — Description &nbsp;|&nbsp; Month Year</div>
</div>
```

---

## 3. Section Framework

Used for every numbered section in every document.

```css
.section-header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 8px;
  margin-top: 36px;
}
.section-number {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 36px;
  height: 36px;
  background: var(--primary);
  color: white;
  border-radius: 50%;
  font-weight: 700;
  font-size: 16px;
  flex-shrink: 0;
}
.section-title {
  font-family: var(--font-heading);
  font-size: 24px;
  font-weight: var(--heading-weight);
  letter-spacing: var(--heading-spacing);
  color: var(--text);
}
.section-intro {
  border-left: 3px solid var(--primary);
  padding: 12px 16px;
  background: var(--primary-light);
  border-radius: 0 var(--radius) var(--radius) 0;
  margin-bottom: 24px;
  font-size: 14px;
  color: var(--text-muted);
  line-height: 1.6;
}
.section-sub {
  font-family: var(--font-heading);
  font-size: 15px;
  font-weight: var(--heading-weight);
  color: var(--primary-dark);
  margin: 24px 0 12px 0;
  padding-bottom: 6px;
  border-bottom: 2px solid var(--primary-light);
}
```

**HTML pattern:**
```html
<div class="section-header">
  <span class="section-number">1</span>
  <h2 class="section-title">Section Name</h2>
</div>
<div class="section-intro">
  Brief description of this section's contents.
</div>
```

---

## 4. Stats Bar

Summary statistics displayed as horizontal chips.

```css
.stats-bar {
  display: flex;
  gap: 14px;
  margin-bottom: 24px;
  flex-wrap: wrap;
}
.stat-chip {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 16px;
  background: var(--bg);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  box-shadow: var(--card-shadow);
}
.stat-num {
  font-size: 26px;
  font-weight: 800;
  color: var(--primary);
  line-height: 1;
}
.stat-label {
  font-size: 11px;
  color: var(--text-muted);
  line-height: 1.3;
}
```

---

## 5. Card Components

### 5a. Persona Cards (Executive Summary / User Roles)

```css
.persona-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
  margin-bottom: 24px;
}
.persona-card {
  background: var(--bg);
  border: 1px solid var(--border);
  border-left: 4px solid var(--primary);
  border-radius: var(--radius);
  box-shadow: var(--card-shadow);
  padding: 16px 20px;
}
.persona-card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 8px;
}
.persona-name { font-family: var(--font-heading); font-size: 15px; font-weight: var(--heading-weight); color: var(--text); }
.persona-access {
  display: inline-block;
  padding: 2px 10px;
  border-radius: 12px;
  font-size: 10px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.06em;
}
.access-editor { background: var(--success-light); color: var(--success); }
.access-readonly { background: var(--primary-light); color: var(--primary); }
.access-owner { background: var(--warning-light); color: var(--warning); }
.persona-desc { font-size: 13px; color: var(--text-muted); margin-bottom: 8px; }
.persona-workflows { font-size: 12px; color: var(--text); line-height: 1.5; }
.persona-workflows strong {
  font-size: 10px;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  color: var(--text-muted);
}
```

### 5b. Module Cards (System Architecture)

```css
.module-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
  margin-bottom: 24px;
}
.module-card {
  background: var(--bg);
  border: 1px solid var(--border);
  border-left: 4px solid var(--accent);
  border-radius: var(--radius);
  box-shadow: var(--card-shadow);
  padding: 16px 20px;
}
.module-card h3 { font-family: var(--font-heading); font-size: 15px; font-weight: var(--heading-weight); color: var(--text); margin-bottom: 6px; }
.mod-purpose { font-size: 13px; color: var(--text-muted); margin-bottom: 8px; }
.mod-features-title {
  font-size: 10px; font-weight: 700; text-transform: uppercase;
  letter-spacing: 0.06em; color: var(--text-muted); margin-bottom: 4px;
}
.mod-features { padding-left: 16px; font-size: 12px; color: var(--text); margin-bottom: 8px; }
.mod-features li { margin-bottom: 2px; }
.mod-metric {
  font-size: 12px; color: var(--accent); font-weight: 600;
  border-top: 1px solid var(--border); padding-top: 6px;
}
```

**HTML pattern (module card):**
```html
<div class="module-card">
  <h3>Module Name</h3>
  <div class="mod-purpose"><strong>Purpose:</strong> One sentence.</div>
  <div class="mod-features-title">Key Features:</div>
  <ul class="mod-features">
    <li>Feature 1</li>
    <li>Feature 2</li>
  </ul>
  <div class="mod-metric"><strong>Metric:</strong> Measurable outcome</div>
</div>
```

### 5c. Summary Card (Warm amber callout)

```css
.summary-card {
  background: var(--accent-light);
  border: 1px solid #E2D9C0;
  border-radius: var(--radius);
  padding: 20px;
  margin-bottom: 24px;
}
.summary-card h3 { font-family: var(--font-heading); font-size: 14px; font-weight: var(--heading-weight); color: var(--warning); margin-bottom: 8px; }
.summary-card p { font-size: 13px; color: var(--text); line-height: 1.6; margin-bottom: 10px; }
```

Note: `.summary-card` is for prose callouts only — not for wrapping question categories. Clarifying question `.q-cat` blocks must be direct children of `.page` so they can break across pages naturally in print. Wrapping `.q-cat` blocks in a `.summary-card` creates a single tall container that cannot break, producing large whitespace gaps in the printed PDF.

### 5d. Interface Cards (Interface Design)

```css
.interface-card {
  background: var(--bg);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  box-shadow: var(--card-shadow);
  margin-bottom: 24px;
  overflow: hidden;
}
.interface-card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 14px 20px;
  border-bottom: 1px solid var(--border);
  background: var(--bg-light);
}
.interface-card-name { font-family: var(--font-heading); font-size: 16px; font-weight: var(--heading-weight); color: var(--text); }
.interface-badge {
  display: inline-flex; align-items: center; gap: 5px;
  font-size: 11px; font-weight: 600; text-transform: uppercase;
  letter-spacing: 0.05em; padding: 3px 10px; border-radius: 12px;
  background: var(--primary-light); color: var(--primary-dark);
}
.interface-card-body { padding: 20px; }
.interface-desc { font-size: 13px; color: var(--text-muted); margin-bottom: 14px; font-style: italic; }
```

### 5e. Automation Cards (Automations)

```css
.auto-card {
  background: var(--bg);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  box-shadow: var(--card-shadow);
  margin-bottom: 20px;
  overflow: hidden;
}
.auto-card-header {
  display: flex; align-items: center; justify-content: space-between;
  padding: 12px 20px; border-bottom: 1px solid var(--border); background: var(--bg-light);
}
.auto-card-name { font-size: 14px; font-weight: 600; color: var(--text); }
.auto-badge {
  display: inline-block; font-size: 10px; font-weight: 700;
  text-transform: uppercase; letter-spacing: 0.05em;
  padding: 3px 10px; border-radius: 12px;
}
.badge-active { background: var(--success-light); color: var(--success); }
.badge-inactive { background: #F3F4F6; color: #6B7280; }
.auto-card-body { padding: 16px 20px; }
```

### 5f. Guide Sections (User Guide)

```css
.guide-section {
  background: var(--bg);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  box-shadow: var(--card-shadow);
  margin-bottom: 20px;
  overflow: hidden;
}
.guide-section-header {
  padding: 12px 20px; border-bottom: 1px solid var(--border);
  background: var(--bg-light); font-family: var(--font-heading); font-size: 15px; font-weight: var(--heading-weight); color: var(--text);
}
.guide-section-body {
  padding: 16px 20px; font-size: 13px; line-height: 1.7; color: var(--text);
}
.guide-section-body h4 {
  font-family: var(--font-heading); font-size: 13px; font-weight: var(--heading-weight); color: var(--primary); margin: 14px 0 6px 0;
}
.guide-section-body h4:first-child { margin-top: 0; }
.guide-section-body ol, .guide-section-body ul { padding-left: 20px; margin-bottom: 8px; }
.guide-section-body li { margin-bottom: 4px; }
.guide-section-body p { margin-bottom: 8px; }
```

---

## 6. Flow Visualization (Automation Flows)

```css
.auto-flow {
  display: flex; align-items: stretch; gap: 0; flex-wrap: wrap; margin-bottom: 14px;
}
.flow-step { display: flex; align-items: center; gap: 0; }
.flow-node {
  padding: 8px 12px; border-radius: var(--radius); font-size: 11px;
  font-weight: 600; line-height: 1.4; text-align: center; min-width: 90px;
}
.flow-node-trigger { background: var(--primary); color: white; }
.flow-node-action {
  background: var(--primary-light); color: var(--primary-dark); border: 1px solid #C3D0E4;
}
.flow-node-decision {
  background: var(--warning-light); color: var(--warning); border: 1px solid #FDE68A;
}
.flow-arrow { display: flex; align-items: center; padding: 0 5px; color: var(--text-muted); font-size: 14px; }
```

**Workflow-doc specific flow nodes** (for workflow diagrams — actors, user actions, blocked states):
```css
.flow-node-actor { background: var(--primary-dark); color: white; }
.flow-node-user-action {
  background: var(--bg); color: var(--primary); border: 2px solid var(--primary);
}
.flow-node-system { background: var(--primary); color: white; }
.flow-node-blocked {
  background: #FEE2E2; color: #991B1B; border: 1px solid #FECACA;
}
```

---

## 7. Detail Grids

Shared 2-column detail layout used by automation cards, interface cards, and page details.

```css
.detail-grid {
  display: grid; grid-template-columns: 1fr 1fr; gap: 12px;
}
.detail-item {
  padding: 10px 14px; background: var(--bg-light);
  border-radius: var(--radius); border: 1px solid var(--border);
}
.detail-label {
  font-size: 10px; font-weight: 700; text-transform: uppercase;
  letter-spacing: 0.08em; color: var(--text-muted); margin-bottom: 3px;
}
.detail-value { font-size: 13px; color: var(--text); line-height: 1.5; }
.detail-full { grid-column: 1 / -1; }

.config-block {
  background: var(--bg-light); border: 1px solid var(--border);
  border-radius: 4px; padding: 8px 10px; margin-top: 4px;
  font-size: 11px; font-family: 'SF Mono', 'Fira Code', monospace;
  white-space: pre-wrap; word-break: break-word;
  color: var(--text-muted); max-height: 100px; overflow-y: auto;
}
```

---

## 8. Data Model / ERD Components

```css
.erd-container {
  background: var(--bg); border: 1px solid var(--border);
  border-radius: var(--radius); box-shadow: var(--card-shadow);
  padding: 20px; margin-bottom: 24px;
}
.erd-grid {
  display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-bottom: 20px;
}
.erd-table {
  background: var(--bg-light); border: 1px solid var(--border);
  border-radius: var(--radius); overflow: hidden;
}
.erd-table-header {
  background: var(--primary); color: white; padding: 8px 14px;
  font-family: var(--font-heading); font-size: 13px; font-weight: 600;
}
.erd-field-row {
  display: flex; align-items: center; justify-content: space-between;
  padding: 6px 14px; font-size: 12px; border-bottom: 1px solid var(--border);
}
.erd-field-row:last-child { border-bottom: none; }
.erd-field-name { font-weight: 600; color: var(--text); }
.erd-field-type {
  display: inline-block; padding: 1px 8px; border-radius: 4px;
  font-size: 10px; font-weight: 600;
}

/* Field type badges */
.type-pk { background: var(--primary); color: white; }
.type-fk { background: var(--accent); color: white; }
.type-text { background: #E5E7EB; color: #374151; }
.type-select { background: #DBEAFE; color: #1E40AF; }
.type-date { background: #D1FAE5; color: #065F46; }
.type-formula { background: #F3E8FF; color: #6B21A8; }
.type-attach { background: #FFE4E6; color: #9F1239; }
.type-collab { background: #FEF3C7; color: #92400E; }
.type-check { background: #E0F2FE; color: #075985; }
.type-number { background: #ECFDF5; color: #047857; }
.type-rich { background: #FDF4FF; color: #86198F; }

/* Relationships */
.erd-relationships {
  background: var(--bg-light); border: 1px solid var(--border);
  border-radius: var(--radius); padding: 14px 18px;
}
.erd-rel-title { font-family: var(--font-heading); font-size: 13px; font-weight: 600; color: var(--primary); margin-bottom: 8px; }
.rel-row {
  display: flex; align-items: center; gap: 8px; padding: 5px 0;
  font-size: 12px; border-bottom: 1px dashed var(--border);
}
.rel-row:last-child { border-bottom: none; }
.rel-table-name { font-weight: 700; color: var(--primary); }
.rel-arrow { color: var(--accent); font-weight: 700; }
.rel-type { font-size: 10px; color: var(--text-muted); font-style: italic; }
```

---

## 9. Field & Data Tables

```css
.field-table {
  width: 100%; border-collapse: collapse; font-size: 12px; margin-bottom: 16px;
}
.field-table thead th {
  background: var(--bg-light); padding: 8px 10px; text-align: left;
  font-size: 10px; font-weight: 700; text-transform: uppercase;
  letter-spacing: 0.06em; color: var(--text-muted);
  border-bottom: 2px solid var(--border);
}
.field-table tbody td {
  padding: 7px 10px; border-bottom: 1px solid var(--border); vertical-align: top;
}
.field-table .fname { font-weight: 600; color: var(--text); white-space: nowrap; }
```

### Page List Table (Interface Design)

```css
.page-list {
  width: 100%; border-collapse: collapse; font-size: 12px; margin-bottom: 16px;
}
.page-list thead th {
  background: var(--bg-light); padding: 7px 10px; text-align: left;
  font-size: 10px; font-weight: 700; text-transform: uppercase;
  letter-spacing: 0.06em; color: var(--text-muted);
  border-bottom: 2px solid var(--border);
}
.page-list tbody td {
  padding: 8px 10px; border-bottom: 1px solid var(--border); vertical-align: top;
}
.page-list .pname { font-weight: 600; color: var(--text); }

/* Page type badges */
.page-type-badge {
  display: inline-block; padding: 2px 8px; border-radius: 4px;
  font-size: 10px; font-weight: 600;
}
.ptype-dashboard { background: #DBEAFE; color: #1E40AF; }
.ptype-list { background: #F3E8FF; color: #6B21A8; }
.ptype-kanban { background: #FFE4E6; color: #9F1239; }
.ptype-grid { background: #E0F2FE; color: #075985; }
.ptype-record { background: #D1FAE5; color: #065F46; }
```

### Field Chips (Inline field display)

```css
.field-chips { display: flex; flex-wrap: wrap; gap: 5px; margin-top: 4px; }
.field-chip {
  display: inline-flex; align-items: center; gap: 3px;
  padding: 2px 8px; border-radius: 10px; font-size: 11px; font-weight: 500;
  background: var(--bg-light); border: 1px solid var(--border); color: var(--text);
}
.field-chip-type { font-size: 9px; color: var(--text-muted); }
```

---

## 10. Permissions Matrix (Access Model)

```css
.access-matrix {
  width: 100%; border-collapse: collapse; font-size: 12px; margin-bottom: 20px;
}
.access-matrix thead th {
  background: var(--primary); color: white; padding: 8px 10px;
  text-align: center; font-size: 11px; font-weight: 700;
}
.access-matrix thead th:first-child {
  text-align: left; background: var(--primary-dark);
}
.access-matrix tbody td {
  padding: 8px 10px; text-align: center; border-bottom: 1px solid var(--border);
  font-weight: 600; font-size: 11px;
}
.access-matrix tbody td:first-child {
  text-align: left; font-weight: 700; color: var(--text); background: var(--bg-light);
}
.perm-full { background: var(--primary); color: white; }
.perm-edit { background: var(--primary-light); color: var(--primary-dark); }
.perm-read { background: #F0F4F8; color: var(--text-muted); }
.perm-none { background: #F9FAFB; color: #D1D5DB; }
```

---

## 11. Appendix Components

```css
.changelog-table {
  width: 100%; border-collapse: collapse; font-size: 12px; margin-bottom: 20px;
}
.changelog-table thead th {
  background: var(--bg-light); padding: 8px 10px; text-align: left;
  font-size: 10px; font-weight: 700; text-transform: uppercase;
  letter-spacing: 0.06em; color: var(--text-muted);
  border-bottom: 2px solid var(--border);
}
.changelog-table tbody td {
  padding: 8px 10px; border-bottom: 1px solid var(--border); vertical-align: top;
}

.glossary-item { padding: 10px 0; border-bottom: 1px solid var(--border); }
.glossary-item:last-child { border-bottom: none; }
.glossary-term { font-family: var(--font-heading); font-size: 13px; font-weight: var(--heading-weight); color: var(--primary); }
.glossary-def { font-size: 13px; color: var(--text-muted); margin-top: 2px; }
```

---

## 12. Workflow-Doc Specific Components

These components are used by the `workflow-doc` skill (user stories, workflow diagrams, clarifying questions):

```css
/* Story Cards */
.story-card {
  background: var(--bg);
  border: 1px solid var(--border);
  border-left: 4px solid var(--primary);
  border-radius: var(--radius);
  box-shadow: var(--card-shadow);
  padding: 16px 20px;
  margin-bottom: 16px;
}

/* Workflow Cards */
.workflow-card {
  background: var(--bg-light);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 20px;
  margin-bottom: 20px;
}

/* WF Data Cards */
.wfdata-card {
  background: var(--bg);
  border: 1px solid var(--border);
  border-left: 4px solid var(--primary);
  border-radius: var(--radius);
  box-shadow: var(--card-shadow);
  padding: 16px 20px;
  margin-bottom: 16px;
}

/* Clarifying Question Blocks */
.q-cat { margin-bottom: 20px; }
.q-cat-title {
  font-family: var(--font-heading); font-size: 14px; font-weight: var(--heading-weight); color: var(--primary);
  margin-bottom: 8px; padding-bottom: 4px;
  border-bottom: 2px solid var(--primary-light);
}
.q-item {
  background: var(--bg); border: 1px solid var(--border);
  border-radius: var(--radius); padding: 12px 16px;
  margin-bottom: 8px; font-size: 13px; color: var(--text);
}
.q-context {
  margin-top: 6px; font-size: 12px; color: var(--text-muted);
  font-style: italic; border-top: 1px solid var(--border); padding-top: 6px;
}
```

---

## 13. Print CSS (Landscape PDF)

This is the tested, production-ready print block. Copy it in full into every generated document's `<style>` tag. The reasoning behind each rule is explained in `SKILL.md` Section 4.

```css
@media print {
  @page { size: landscape; margin: 0.4in 0.5in; }

  body {
    margin: 0; padding: 0;
    background: white !important;
    -webkit-print-color-adjust: exact !important;
    print-color-adjust: exact !important;
    color-adjust: exact !important;
  }

  .page { padding: 0; max-width: 100%; margin: 0; }

  /* ══════════════════════════════════════════════════════
     COVER PAGE: Title stands alone as page 1
     ══════════════════════════════════════════════════════ */
  .doc-header {
    -webkit-print-color-adjust: exact; print-color-adjust: exact;
    box-shadow: none;
    page-break-after: always;
    break-after: page;
  }

  /* ══════════════════════════════════════════════════════
     SECTIONS: Flow naturally, NO forced page breaks
     ══════════════════════════════════════════════════════ */
  .section {
    page-break-inside: auto;
    break-inside: auto;
    margin-bottom: 32px;
  }

  /* ══════════════════════════════════════════════════════
     HEADERS: Must stay with their following content
     ══════════════════════════════════════════════════════ */
  .section-header { page-break-after: avoid; break-after: avoid; }
  .section-sub { page-break-after: avoid; break-after: avoid; }
  h1, h2, h3, h4 { page-break-after: avoid; break-after: avoid; }

  /* .section-intro uses break-after: auto (not avoid) — adding avoid here causes
     the browser to stretch the intro box to fill the remaining page when the next
     element doesn't fit, creating large blank whitespace gaps. */
  .section-intro {
    break-inside: avoid;
    page-break-inside: avoid;
    break-after: auto;
    background: var(--primary-light) !important;
    border-left-color: var(--primary) !important;
    margin-bottom: 16px;
    padding: 8px 12px;
  }

  /* ══════════════════════════════════════════════════════
     COLOR PRESERVATION: Force all branded backgrounds
     ══════════════════════════════════════════════════════ */
  .doc-header { background: linear-gradient(135deg, var(--primary) 0%, var(--primary-dark) 100%) !important; }
  .doc-header-badge { background: var(--accent) !important; }
  .section-number { background: var(--primary) !important; }
  .erd-table-header { background: var(--primary) !important; }
  .access-matrix thead th { background: var(--primary) !important; }
  .access-matrix thead th:first-child { background: var(--primary-dark) !important; }
  .perm-full { background: var(--primary) !important; color: white !important; }
  .perm-edit { background: var(--primary-light) !important; }
  .persona-card { border-left-color: var(--primary) !important; }
  .module-card { border-left-color: var(--accent) !important; }
  .flow-node-trigger { background: var(--primary) !important; }
  .flow-node-decision { background: var(--warning-light) !important; }
  .badge-active { background: var(--success-light) !important; }
  .access-editor { background: var(--success-light) !important; }
  .access-readonly { background: var(--primary-light) !important; }
  .access-owner { background: var(--warning-light) !important; }
  .type-pk { background: var(--primary) !important; color: white !important; }
  .type-fk { background: var(--accent) !important; color: white !important; }
  .ptype-dashboard { background: #DBEAFE !important; }
  .ptype-list { background: #F3E8FF !important; }
  .ptype-kanban { background: #FFE4E6 !important; }
  .ptype-grid { background: #E0F2FE !important; }
  .ptype-record { background: #D1FAE5 !important; }

  /* ══════════════════════════════════════════════════════
     ALL CARDS: Never split across pages
     Both break-inside and page-break-inside are needed for
     cross-browser reliability across flex/grid contexts.
     ══════════════════════════════════════════════════════ */
  .persona-card, .module-card, .interface-card, .auto-card,
  .erd-table, .erd-relationships, .guide-section, .glossary-item,
  .summary-card, .detail-item, .ext-card, .dev-step,
  .warning-card, .tip-box, .caution-box, .stat-chip,
  .story-card, .workflow-card, .wfdata-card, .q-cat, .flow-step {
    -webkit-print-color-adjust: exact; print-color-adjust: exact;
    break-inside: avoid !important;
    page-break-inside: avoid !important;
    box-shadow: none !important;
  }

  /* ── Let tall containers break ── */
  .erd-container,
  .interface-card-body { break-inside: auto; }

  /* ══════════════════════════════════════════════════════
     STATS BAR: Flexbox row — all chips in one line
     ══════════════════════════════════════════════════════ */
  .stats-bar {
    display: flex !important;
    flex-wrap: wrap;
    gap: 12px;
  }
  .stats-bar .stat-chip {
    flex: 1 1 0;
    min-width: 120px;
  }

  /* ══════════════════════════════════════════════════════
     GRID → INLINE-BLOCK CONVERSION
     CSS Grid ignores break-inside: avoid on children.
     Convert to display: block parent + inline-block children
     at 48% width for 2-per-row landscape layout.
     ERD grid is the exception — stays as 3-across CSS grid.
     ══════════════════════════════════════════════════════ */

  /* Persona cards: 2 per row */
  .persona-grid { display: block !important; }
  .persona-grid .persona-card {
    display: inline-block; width: 48%; margin-right: 1.5%;
    margin-bottom: 16px; vertical-align: top;
    break-inside: avoid !important; page-break-inside: avoid !important;
  }

  /* Module cards: 2 per row */
  .module-grid { display: block !important; }
  .module-grid .module-card {
    display: inline-block; width: 48%; margin-right: 1.5%;
    margin-bottom: 16px; vertical-align: top;
    break-inside: avoid !important; page-break-inside: avoid !important;
  }

  /* Detail items: 2 per row */
  .detail-grid { display: block !important; }
  .detail-grid .detail-item {
    display: inline-block; width: 48%; margin-right: 1.5%;
    margin-bottom: 10px; vertical-align: top;
    break-inside: avoid !important; page-break-inside: avoid !important;
  }
  .detail-grid .detail-item.detail-full { display: block; width: 100%; }

  /* ERD grid: exception — stays as CSS grid at 3-across.
     ERD cards are compact enough that CSS grid works fine here. */
  .erd-grid {
    display: grid !important;
    grid-template-columns: repeat(3, 1fr) !important;
    gap: 16px;
  }

  /* Interface & automation cards: full-width stacked.
     These contain too much detail for side-by-side layout. */
  .interface-grid { display: block !important; }
  .interface-grid .interface-card {
    display: block; width: 100%; margin-bottom: 16px;
    break-inside: avoid !important; page-break-inside: avoid !important;
  }
  .auto-grid { display: block !important; }
  .auto-grid .auto-card {
    display: block; width: 100%; margin-bottom: 16px;
    break-inside: avoid !important; page-break-inside: avoid !important;
  }

  /* Long code blocks (appendix, source code): use orphans/widows to keep
     at least 8 lines together at page boundaries. */
  .appendix-skill { break-inside: auto; }
  .appendix-skill-header { break-after: avoid; }
  .appendix-skill-meta { break-after: avoid; }
  .appendix-skill-body { break-inside: auto; }
  .appendix-skill-body pre {
    white-space: pre-wrap;
    break-inside: auto;
    background: #1F2937 !important;
    color: #E5E7EB !important;
    padding-top: 12px;
    padding-bottom: 12px;
    line-height: 1.5;
    orphans: 8;
    widows: 8;
  }
  .code-block {
    background: #1F2937 !important;
    color: #E5E7EB !important;
  }

  /* Tighten spacing (~25% reduction) */
  .section-header { margin-top: 24px; }
  .auto-card { margin-bottom: 14px; }
  .interface-card { margin-bottom: 18px; }
}
```
