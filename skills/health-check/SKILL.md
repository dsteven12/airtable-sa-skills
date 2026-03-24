---
name: health-check
description: "Generate a scalability and risk assessment document (.docx) for any Airtable base. MANDATORY TRIGGERS: health check, risk assessment, scalability, base audit, production readiness, pre-production, system health, scaling concerns, performance issues, is this ready, check this base. ALWAYS invoke this skill when evaluating an Airtable base for risks, scaling concerns, or production readiness — even if the user just says 'check this base' or 'is this ready for production.' Inspects the live base via Airtable MCP and outputs a branded Word document with severity matrices, risk analysis, automation architecture review, and a prioritized readiness checklist."
---

# Health Check Generator

Generate a scalability and risk assessment document for any Airtable base. This is a **forward-looking deliverable** — it identifies architectural patterns that may encounter constraints under production load and proposes mitigation strategies. It is not a utilization audit or cleanup checklist.

The output is a `.docx` file generated via `docx-js`. This skill does NOT depend on `doc-css-framework` (that is for HTML-based skills only).

## Prerequisites

**Before processing any input**, read these shared dependencies:
- **Read `airtable-design-principles/SKILL.md`** — the canonical risk heuristics (8 risk categories with inspection thresholds and mitigations), linking strategy framework, automation design patterns, and naming conventions. All risk analysis content is drawn from this reference. Use the **inspection thresholds** (absolute counts from MCP extraction), not the design-time thresholds.
- **Read `structured-input/SKILL.md`** — contains the base XML input schema, normalization protocol, and extension pattern used across all doc-generating skills.
- **Read `base-metadata-extractor/SKILL.md`** — contains all extraction logic: MCP schema extraction steps, browser console scripts for automations/interfaces, type ID mappings, troubleshooting, and auth details.
- **Read `automation-architect/references/platform-reference.md`** — when documenting Section 6 (Automation Architecture Notes), reference this for precise structural constraints (Terminal Block Rule, trigger/action types, limits like Find Records 1K cap, forEach 8K cap, AI 64K char limit).

Input parsing rules are defined in `structured-input`. Data extraction logic is defined in `base-metadata-extractor`. Risk definitions and mitigations are in `airtable-design-principles`. Automation structural constraints are in `automation-architect/references/platform-reference.md`. This skill defines the **severity scoring framework, document sections, and .docx generation patterns**.

Note: This skill does NOT depend on `doc-css-framework` (that is for HTML-based skills only).

## Overview

A health check evaluates an Airtable base's architecture against known platform behaviors and limits. It serves two audiences:

- **Partners/builders** — Understand where their design may hit scaling walls and what to monitor
- **Internal SA team** — Structured framework for technical reviews with consistent rigor across engagements

The assessment uses a **Likelihood × Impact × Detectability** severity framework to prioritize risks.

## Input Types

This skill accepts:
- **Structured XML** — explicitly tagged input using the `<health-check>` wrapper (see `structured-input/SKILL.md` for the base schema and extension pattern)
- **Freeform request** — user describes the base to inspect verbally or provides a base ID inline

### Skill-Specific Extension Fields

Beyond the base schema (`client`, `solution`, `brand_color`, `stakeholders`, `content`), this skill accepts:

| Extension Field | When provided | When absent |
|-----------------|--------------|-------------|
| `<base_id>` | Skip `search_bases` step; use directly for MCP calls | Ask user for base ID |
| `<partner_name>` | Use on cover page "Prepared for:" | Omit partner attribution |
| `<base_status>` | Frame analysis tone (pre-production vs production) | Ask user |
| `<expected_users>` | Factor into concurrency risk scoring | Estimate from schema complexity |
| `<planned_syncs>` | Factor into sync cascade risk analysis | Ask user or skip sync analysis |

## Process

### Step 0: Normalize Input

Follow the **Normalization Protocol** in `structured-input/SKILL.md`. Parse the input into the canonical object with: `client`, `solution`, `brand_primary`, `brand_accent`, `stakeholders`, `raw_content`, and extension fields (`base_id`, `partner_name`, `base_status`, `expected_users`, `planned_syncs`). This object is the single source of truth for all downstream steps.

### Step 0.5: Gather Remaining Clarifying Information

If the normalized object already provides clear values for the following, skip redundant questions. Otherwise, ask:

| Question | Required | Notes |
|----------|----------|-------|
| Customer name | Yes (if null in normalized object) | Used on cover page and headers |
| Partner name | No | e.g., "Prepared for: PartnerName" |
| Base ID | Yes (if null in normalized object) | Used for MCP inspection |
| Base status | Yes (if null in normalized object) | pre-production = forward-looking, production = diagnostic |
| Expected concurrent users | If known | Affects automation queue and computed field cascade risk |
| Planned syncs (cross-base) | If known | Affects sync cascade and inverse link risk |
| Provide automation/interface extraction? | Ask | Optional — deeper analysis if they run browser console scripts |

### Step 1: Inspect Base Schema via MCP

Follow the **Schema Extraction (MCP Connector)** steps in `base-metadata-extractor/SKILL.md`:

1. `search_bases` or `list_bases` to find the base (or use provided base ID directly)
2. `list_tables_for_base(baseId)` to get all tables and fields
3. `get_table_schema` for detailed field configs where needed (select options, linked tables, formula expressions)
4. `list_records_for_table` to sample data if record counts or field usage patterns are relevant

From the MCP data, extract and tabulate:

| Metric | How to Calculate |
|--------|-----------------|
| **Table count** | Count of tables returned |
| **Field count per table** | Count of fields in each table |
| **Link fields per table** | Fields where type = `multipleRecordLinks` |
| **Computed fields per table** | Fields where type in (`formula`, `multipleLookupValues`, `rollup`, `count`) |
| **Repeated slot patterns** | Fields matching numbered patterns (e.g., "Vendor Type 1", "Vendor Type 2"... "Vendor Type 8") — count distinct groups and slots per group |

**Key tables to flag:**
- Any table with **>200 fields** — wide table rendering and API payload concern
- Any table with **>50 computed fields** — recalculation cascade candidate
- Any table with **>100 link fields** — high fan-out on create/update/duplicate
- Any table with **>80% repeated slot fields** — horizontal scaling pattern (intentional, but document the trade-offs)

### Step 2: Analyze Schema for Risk Indicators

For each flagged table, evaluate:

1. **Computed field density**: `computed_fields / total_fields` — if >30%, flag cascade risk
2. **Link field density**: `link_fields / total_fields` — if >50%, flag inverse update cost
3. **Repeated field ratio**: `repeated_fields / total_fields` — if >40%, document the horizontal scaling trade-off
4. **Hub table detection**: Tables linked TO by many other tables (high in-degree) are cascade amplifiers
5. **Stale inverse link detection**: Fields named with "copy" patterns ("Table copy", "Table copy copy") indicate sync artifacts

### Step 3: Optional — Automation & Interface Extraction

If the user opts to provide deeper automation/interface data, present the extraction scripts from `base-metadata-extractor/SKILL.md`:

1. **Automations** — Present the **Automation Extraction** browser console script. Use the **Type ID Mappings** in `base-metadata-extractor` to interpret the output.
2. **Interfaces** — Present the **Interface Page Extraction** 2-part scripts if interface data is also desired.

Refer the user to the **Troubleshooting** section in `base-metadata-extractor` if they encounter issues running the scripts.

If the user declines, proceed with schema-only analysis. Note in the document that automation analysis is based on schema inference rather than direct inspection.

### Step 4: Identify and Evaluate Risks

Apply the **Risk Analysis Framework** below to each detected risk. Not every risk category will apply to every base — only include risks that are evidenced by the schema or extraction data.

### Step 5: Generate .docx

Use the **.docx Generation Reference** below to produce the output document. Save to the Cowork workspace folder (use the workspace path from your system context — it follows the pattern `/sessions/<session-id>/mnt/Work Brain/`) with naming convention:

```
[CustomerName]-Health-Check-[YYYY-MM-DD].docx
```

---

## Risk Analysis Framework

### Severity Calculation

Each risk is evaluated on three dimensions (each scored 1–4):

| Dimension | 1 | 2 | 3 | 4 |
|-----------|---|---|---|---|
| **Likelihood** | Unlikely | Possible | Likely | Very Likely |
| **Impact** | Minor UX lag | Moderate delays | Workflow disruption | Data integrity / silent failure |
| **Detectability** | Obvious (visible error) | Noticeable (agent reports) | Hidden (requires monitoring) | Silent (no indication of failure) |

**Overall Severity mapping:**

| Severity | Criteria |
|----------|----------|
| **Critical** | High Likelihood + High Impact + Low Detectability (silent failures under load) |
| **High** | High in 2 of 3 dimensions |
| **Medium** | Mixed — moderate across dimensions |
| **Low** | Low likelihood OR high detectability (easy to catch before damage) |

### Risk Category Reference

All risk category definitions — detection heuristics, descriptions, compounding factors, and mitigations — are in **`airtable-design-principles/SKILL.md`** under the "Risk Heuristics" section.

The eight risk categories are:
1. Computed Field Cascade
2. High-Cardinality Linked Records (Fan-Out)
3. Automation Queue Saturation
4. Implicit Automation Chains
5. Double-Trigger Risk
6. Button-Press Automation Contention
7. Sync Table Cascade
8. Configuration/Template Table Bottleneck

For each risk, use the **inspection thresholds** (absolute field/automation counts from MCP extraction), not the design-time thresholds. Only include risks that are evidenced by the base's schema or extraction data — no generic padding.

For each identified risk, generate a document section containing:
1. **Severity matrix table** (Likelihood / Impact / Detectability / Overall) — using the Severity Calculation framework above
2. **Description** — What the risk is, why it matters, how it manifests in this specific base
3. **Where it applies** — Specific tables, fields, or automations in this base (by name, from MCP data)
4. **Mitigation strategies** — Actionable bullet points drawn from the principles

---

## Document Sections

The output .docx should contain these sections in order:

### 1. Cover Page
- Document title: "Airtable Base Health Check"
- Subtitle: "Scalability & Risk Assessment"
- Customer name
- Partner name (if applicable): "Prepared for: [Partner]"
- Prepared by: "Airtable Solution Architecture"
- Date
- Base ID (italicized)
- Status badge: "Pre-Production" or "Production"

### 2. Purpose and Scope
- Assessment framework explanation (Likelihood × Impact × Detectability)
- Scope statement: what tables, automations, and patterns are included
- Disclaimer if automation/interface extraction was not provided

### 3. Base Architecture Overview
- **Table inventory table**: Table name, Fields, Links, Computed, Repeated, Role
- **Design context** (if horizontal scaling patterns detected): Explain WHY the pattern exists (interface form constraints, automation copy patterns, agent UX) and the trade-offs (fixed capacity, field count overhead, schema rigidity, automation duplication)
- Assessment paragraph: whether the design is appropriate given platform constraints

### 4. Scalability Risk Analysis
- One subsection per identified risk, each with:
  - Severity matrix table (4 columns)
  - Description paragraphs
  - "Where it applies" with specific table/field/automation references
  - Mitigation strategies as bullet points

### 5. Pre-Production Sync Hygiene (if applicable)
- Stale inverse link inventory table (Table, Stale Count, Pattern, Action)
- Cleanup process (numbered steps)
- Estimated cleanup scope

### 6. Automation Architecture Notes
- Consolidation feasibility assessment (what CAN and CANNOT be merged given Airtable constraints)
- Platform constraint reminders — reference `automation-architect/references/platform-reference.md` for precise constraints: Terminal Block Rule (nothing after conditionals/repeating groups), Find Records 1K limit with no sort and no linked field conditions, forEach 8K item limit, AI action 64K character limit, GMT timezone for all time evaluations
- Disabled automations disposition table (if any)
- If automation extraction data is available: validate structural correctness against the Terminal Block Rule and flag any anti-patterns from the automation-architect skill (sequential conditionals, actions after conditionals, sort-dependent Find Records, missing double-trigger guards)

### 7. Pre-Production Readiness Checklist
- Prioritized action table: #, Priority (Critical/High/Medium/Low), Action, Effort, Category
- Color-coded priority cells

### 8. Appendix
- Platform constraints referenced (bullet list)
- Methodology (data sources, tools used)
- Glossary (terms used in the document with plain-English definitions)

---

## .docx Generation Reference

### Technology

Use the `docx` npm package (docx-js) to generate Word documents programmatically:

```bash
npm install docx
```

### Page Setup

```javascript
const PAGE_WIDTH = 12240;  // 8.5 inches in DXA
const MARGINS = { top: 1440, right: 1440, bottom: 1440, left: 1440 };  // 1 inch each
const CONTENT_WIDTH = PAGE_WIDTH - MARGINS.left - MARGINS.right;  // 9360 DXA
```

### Airtable Brand Colors

```javascript
const AIRTABLE_BLUE = "2D7FF9";   // Primary — section headings, cover page
const AIRTABLE_DARK = "1A1A2E";   // Body text
const GRAY_LIGHT = "F5F5F5";      // Alternating row backgrounds
const GRAY_MED = "E0E0E0";        // Borders, dividers
const GRAY_TEXT = "666666";        // Secondary text, metadata
const WHITE = "FFFFFF";            // Header cell text
const RED_ALERT = "EF3061";       // Critical severity
const YELLOW_WARN = "FCB400";     // High severity
const ORANGE_MED = "FFE0B2";      // Medium severity
const GREEN_LOW = "E8F5E9";       // Low severity
```

### Heading Styles

```javascript
paragraphStyles: [
  { id: "Heading1", run: { size: 36, bold: true, font: "Arial", color: AIRTABLE_BLUE },
    paragraph: { spacing: { before: 360, after: 200 } } },
  { id: "Heading2", run: { size: 28, bold: true, font: "Arial", color: AIRTABLE_DARK },
    paragraph: { spacing: { before: 240, after: 160 } } },
  { id: "Heading3", run: { size: 24, bold: true, font: "Arial", color: AIRTABLE_DARK },
    paragraph: { spacing: { before: 200, after: 120 } } },
]
```

### Severity Badge Cells

Use color-coded table cells for severity ratings:

```javascript
function severityCell(level, width) {
  const map = {
    "Critical": { fill: RED_ALERT, color: WHITE },
    "High": { fill: YELLOW_WARN, color: AIRTABLE_DARK },
    "Medium": { fill: ORANGE_MED, color: AIRTABLE_DARK },
    "Low": { fill: GREEN_LOW, color: AIRTABLE_DARK },
  };
  // ... return TableCell with shading and centered bold text
}
```

### Common Helper Functions

Build these reusable helpers:

- `headerCell(text, width)` — Blue background, white bold text
- `dataCell(text, width, opts)` — Standard data cell with optional bold/color
- `severityCell(level, width)` — Color-coded severity badge
- `spacer(pts)` — Empty paragraph for vertical spacing
- `heading(text, level)` — Section heading
- `para(text, opts)` — Body paragraph with optional formatting
- `multiRunPara(runs)` — Paragraph with mixed bold/normal text
- `bullet(text)` — Bulleted list item
- `bulletMulti(runs)` — Bulleted list item with mixed formatting

### Document Structure

```javascript
const doc = new Document({
  styles: { /* heading styles above */ },
  numbering: { config: [
    { reference: "bullets", levels: [{ level: 0, format: LevelFormat.BULLET, text: "•" }] },
    { reference: "numbers", levels: [{ level: 0, format: LevelFormat.DECIMAL, text: "%1." }] },
  ]},
  sections: [
    { /* Cover page — no header/footer */ },
    { /* Main content — with header/footer, page numbers */ },
  ],
});
```

### Output

```javascript
// Save to the Cowork workspace folder (get the path from your system context)
// System context provides the current session path following the pattern: /sessions/<session-id>/mnt/Work Brain/
const WORKSPACE = `<workspace-path-from-system-context>`;
const OUTPUT = `${WORKSPACE}/${customerName}-Health-Check-${date}.docx`;
Packer.toBuffer(doc).then(buffer => {
  fs.writeFileSync(OUTPUT, buffer);
});
```

---

## Output Checklist

Before presenting the document to the user, verify:

- [ ] `structured-input/SKILL.md` was read before input parsing
- [ ] Input was normalized into the canonical object (Step 0) per structured-input protocol
- [ ] `base-metadata-extractor/SKILL.md` was read before extracting data
- [ ] Schema extracted via MCP (`list_tables_for_base` + `get_table_schema`)
- [ ] Cover page has correct customer name, partner name, date, base ID, and status
- [ ] Table inventory matches MCP data (table count, field counts)
- [ ] Every risk section has a severity matrix + description + mitigation strategies
- [ ] Risk sections only include risks evidenced by this base's schema (no generic padding)
- [ ] If horizontal scaling detected: Design Context section explains WHY and documents trade-offs
- [ ] Pre-production checklist is prioritized (Critical → High → Medium → Low)
- [ ] Appendix includes platform constraints and glossary
- [ ] File saved to the Cowork workspace folder with correct naming convention (not `/mnt/outputs/`)
- [ ] No references to "transcripts", "call recordings", or source materials in customer-facing text
