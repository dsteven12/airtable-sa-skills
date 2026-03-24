---
name: technical-design-doc
description: "Generate a branded, print-ready HTML technical design document for a completed Airtable application. MANDATORY TRIGGERS: technical design, design doc, TDD, system documentation, architecture doc, document this base, field specs, automation documentation, document the build, post-build documentation. ALWAYS invoke this skill when the user wants to document a completed Airtable application — even if they just say 'document this' or 'create docs for the base.' Uses the Airtable MCP connector to inspect the live base and produces an 8-section HTML document (Executive Summary, System Architecture, Data Model, Interface Design, Automations, Permissions, User Guide, Appendix) themed to the customer's brand colors."
---

# Technical Design Doc Generator

Generate a branded, print-ready HTML technical design document for a completed Airtable application. This is the **post-build deliverable** — it documents how the finalized solution works, how components connect, and how users interact with it. Serves as both the architecture reference and the end-user guide for the customer.

## Prerequisites

**Before processing any input**, read these shared dependencies:
- **Read `airtable-design-principles/SKILL.md`** — the canonical risk heuristics, linking strategy framework, automation design patterns, and naming conventions. Apply during Step 5 (Reconcile) to flag any design principle violations in the final built solution, and include a Design Principles Assessment in Section 8 (Appendix).
- **Read `structured-input/SKILL.md`** — base XML input schema, normalization protocol, and extension pattern used across all doc-generating skills.
- **Read `doc-css-framework/SKILL.md`** — brand detection algorithm, component reference guide, print principles, and language/tone rules.
- **Read `doc-css-framework/references/css-components.md`** — the complete CSS code blocks to embed in the document's `<style>` tag.
- **Read `base-metadata-extractor/SKILL.md`** — all extraction logic: MCP schema extraction steps, browser console scripts for automations/interfaces, type ID mappings, troubleshooting, and auth details.
- **Read `automation-architect/SKILL.md`** — when documenting Section 5 (Automations), use the structured spec output format (numbered action IDs with Y/N branch encoding, token references, Gotchas section) for complex automations. Reference `automation-architect/references/platform-reference.md` for precise trigger/action types and structural constraints.

Input parsing rules are in `structured-input`. The CSS guide is in `doc-css-framework/SKILL.md` and the CSS code is in `doc-css-framework/references/css-components.md`. Data extraction logic is in `base-metadata-extractor`. Design principles are in `airtable-design-principles`. Automation structural specs and format are in `automation-architect`. This skill only defines the **section structure, content organization, and document-specific patterns**.

## Input Types

This skill accepts any combination of:
- **Structured XML** — explicitly tagged input using the `<technical-design-doc>` wrapper (see `structured-input/SKILL.md` for the base schema and extension pattern)
- **Approved Workflow Doc** (.html) — the output from the `workflow-doc` skill, used as the foundation
- **Call transcripts / Meeting notes** (.txt) — original requirements context
- **Live Airtable base** — uses the Airtable MCP connector to inspect the actual built application

When the Airtable connector is available, always use it to verify and enrich the document with real schema data rather than relying solely on the workflow doc or transcript.

### Skill-Specific Extension Fields

Beyond the base schema (`client`, `solution`, `brand_color`, `stakeholders`, `content`), this skill accepts:

| Extension Field | When provided | When absent |
|-----------------|--------------|-------------|
| `<base_id>` | Skip `search_bases` step; use directly for MCP calls | Ask user or search by solution name |
| `<workflow_doc_path>` | Read file directly as foundation document | Ask user if a workflow doc exists |

## Process

### Step 0: Normalize Input

Follow the **Normalization Protocol** in `structured-input/SKILL.md`. Parse the input into the canonical object with: `client`, `solution`, `brand_primary`, `brand_accent`, `stakeholders`, `raw_content`, and extension fields (`base_id`, `workflow_doc_path`). This object is the single source of truth for all downstream steps.

### Step 1: Identify the Customer & Brand

Use the normalized `client` field if present. If `brand_primary` is already set from XML input, skip the web search and apply directly. Otherwise, follow the **Brand Color Detection** algorithm in `doc-css-framework/SKILL.md` to determine primary and accent colors.

### Step 2: Gather Clarifying Information

If the normalized object already provides clear values for the following, skip redundant questions. Otherwise, ask:

1. **Customer Name** — confirm from normalized `client` field, or ask if null
2. **Target Personas** — use normalized `stakeholders` if provided, or ask. Offer common options:
   - Executive Leadership
   - Administrative Staff
   - Department Managers
   - Field Workers / Frontline Staff
   - External Stakeholders
   - (Let the user specify custom roles)
3. **Interfaces & Automations** — ask whether the user wants to extract and document real interface and automation data from the live base (strongly recommended), or rely on inferred data from the schema alone

### Step 3: Extract Base Schema via MCP

Follow the **Schema Extraction (MCP Connector)** steps in `base-metadata-extractor/SKILL.md`:

1. `search_bases` or `list_bases` to find the base
2. `list_tables_for_base` to get all tables and fields
3. `get_table_schema` for detailed field configs (select options, linked tables, formulas)
4. `list_records_for_table` to sample data and understand field usage

Extract from the live base:
- Finalized table names and field configurations (types, options, descriptions)
- Linked record relationships (actual FK connections)
- Views and their filter/sort/group configurations

#### From the Workflow Doc (if provided):
- Project scope/objective
- Module definitions
- User personas/actors
- Workflow sequences
- Original ERD design
- Data design patterns

#### From Transcripts/Notes (if provided):
- Business context and requirements rationale
- User persona details and workflows
- Success criteria and metrics
- Any decisions or constraints discussed

### Step 4: Extract Automation & Interface Data (Strongly Recommended)

**The Airtable MCP connector does not expose automations or interface page layouts.** To get real data, follow the extraction instructions in `base-metadata-extractor/SKILL.md`:

1. **Automations** — Present the **Automation Extraction** browser console script from `base-metadata-extractor`. Tell the user to run it and paste the JSON output.
2. **Interfaces** — Present the **Interface Page Extraction** 2-part browser console scripts from `base-metadata-extractor`. User runs Part 1 (discovery) then Part 2 (fetch layouts).

Use the **Type ID Mappings** and **Interface Element Type Reference** tables in `base-metadata-extractor` to interpret the raw data.

If the user cannot or declines to run the browser scripts, proceed with schema-only analysis. Note in the document that automation and interface sections are based on schema inference rather than direct inspection.

### Step 5: Reconcile and Merge

Compare all data sources against the actual built base:
- Note any fields, tables, or views that were added during build but weren't in the original design
- Note any design elements that were modified during implementation
- Resolve naming differences (the built base is the source of truth for names)
- Fill in implementation details the workflow doc didn't capture (field options, formula logic, automation timing)
- Cross-reference automation triggers/actions with the table schema to identify which tables each automation operates on

**Design Principles Pass — apply the inspection thresholds from `airtable-design-principles/SKILL.md`:**

After reconciling, run a pass against the built schema using the Risk Heuristics and Linking Strategy Framework. Use the **inspection thresholds** (absolute counts from MCP data). Flag any violations found:

- **Risk flags** — Note which risk categories are triggered and at what severity. These findings will be documented in Section 8 (Appendix) under Design Principles Assessment. If risks are severe (Critical or High), surface a callout in the relevant section of the document (e.g., in Section 5: Automations if queue saturation is detected).
- **Linking strategy mismatches** — Note any linked record fields that appear to be display-only (Pattern 5 candidates) or hub links with high fan-out potential (Pattern 4 candidates).
- **Naming convention violations** — Note any AI-generated or automation-written fields that don't follow the `AI ` prefix or `[Cache]` suffix conventions.

Do not turn the TDD into a risk assessment — that is the health-check's job. These findings go in the Appendix and serve as forward-looking recommendations, not the body of the document.

### Step 6: Generate Document Sections

The Technical Design Doc has the following structure:

---

#### Section 1: Executive Summary
- **Solution Overview** — what was built, who it serves, the business problem it solves
- **Scope** — what's included and what's explicitly out of scope
- **User Personas** — role cards for each user type with their access level and primary use cases

**User Persona card pattern:**
Each persona gets a card showing:
- Role name and icon
- Description (1-2 sentences)
- Access level (Owner, Editor, Commenter, Read-only)
- Primary workflows they perform
- Key views they use

---

#### Section 2: System Architecture
- **Architecture Overview** — high-level diagram showing how the base's tables, interfaces, and automations connect
- **Module Breakdown** — each functional module with:
  - Purpose
  - Tables involved
  - Interfaces involved
  - Automations involved
  - How it connects to other modules
- **Integration Points** — any external connections (syncs, Slack, email, other Airtable bases)

---

#### Section 3: Data Model (Finalized ERD)
- **Table Inventory** — every table with:
  - Table name
  - Purpose (1 sentence)
  - Record count category (if sampled: "~50 records", "empty - ready for use")
  - Primary field
- **Field Specifications** — for each table, a detailed field listing:
  - Field name
  - Field type (Single line text, Single select, Linked record, Formula, etc.)
  - Configuration details (select options, linked table target, formula expression, etc.)
  - Required/Optional
  - Description / business purpose
- **Relationship Map** — table-to-table connections with:
  - Source table -> Target table
  - Link field name
  - Relationship type (one-to-many, many-to-many)
  - Lookup/Rollup fields that depend on each link
- **Key Formulas & Rollups** — document any non-trivial calculated fields with their logic explained in plain English

Present field specifications as styled HTML tables within each table's card. Use the ERD visual pattern from `doc-css-framework` (table cards with field rows showing PK/FK/type badges) but with expanded detail.

---

#### Section 4: Interface Design
For each Airtable Interface in the solution (use REAL data from Step 4 when available):
- **Interface name** and purpose
- **Layout type** — dashboard, inbox, list, grid, custom extension, etc.
- **Target persona(s)** — which user roles use this interface
- **Elements** — what components are on the page (charts, big numbers, grids, extensions, pivot tables)
- **Key interactions** — what users can do (filter, edit, create, submit, drill down)
- **Permissions / Filters** — static filters (e.g., current user), editability settings
- **Connected data** — which tables power this interface
- **Custom Extensions** — if the page includes a block installation, document the extension name, scope, and tables it manages

Use a card-per-interface layout with detail grids showing properties.

---

#### Section 5: Automations
For each automation in the solution (use REAL data from Step 4 when available):
- **Automation name**
- **Deployment status** — deployed (active) or not deployed (configured but inactive)
- **Trigger** — what event starts it (record created, field updated, scheduled time, button press, etc.)
- **Actions** — step-by-step what happens (send email, update record, create record, run script, AI generate, etc.)
- **Decisions** — any conditional branching, fan-out, or reducer logic
- **Target persona** — who benefits or is affected
- **Module** — which functional module this automation belongs to

Present automations in a timeline/flow format: Trigger -> Action 1 -> Action 2 -> ...
Use `.auto-card` with `.auto-flow` components. Show `.badge-active` for deployed and `.badge-inactive` for not deployed.

---

#### Section 6: Permissions & Access Model
- **Access Level Matrix** — a table showing each persona x each table/interface with their permission level
- **Field-Level Permissions** — any fields that are hidden or read-only for certain roles
- **View Filters** — views that are role-scoped (e.g., "My Tasks" filtered to current user)
- **Interface Permissions** — which interfaces each persona can access
- **Static Filters** — document any `staticFilters` from the interface data (e.g., filtering by `dynamicCurrentUserEmail`)

Present the access matrix as a styled HTML table with colored cells (use `.access-matrix` and `.perm-*` classes from `doc-css-framework`):
- Full access: primary color
- Read-only: light primary
- No access: light gray
- Conditional: accent color with note

---

#### Section 7: User Guide
For each persona, provide a usage walkthrough:
- **Getting Started** — how to access the base/interfaces
- **Common Tasks** — step-by-step for their primary workflows (reference the workflow diagrams)
- **Tips & Best Practices** — field entry guidance, naming conventions, when to use which view
- **FAQ** — anticipated questions based on the solution's complexity

Write this section in clear, non-technical language. The audience is the end user, not the SA.

---

#### Section 8: Appendix
- **Change Log** — differences between the workflow doc design and final build (if workflow doc was provided)
- **Design Principles Assessment** — results of the design principles pass from Step 5. List any risk flags identified (with severity), any linking strategy mismatches, and any naming convention gaps. Frame these as forward-looking recommendations, not defects. If no violations were found, include a brief positive confirmation ("The solution follows Airtable design principles. No structural risks were identified at current scale."). This subsection keeps the body of the TDD clean while ensuring the SA's architectural judgment is documented.
- **Glossary** — Airtable-specific terms explained for non-technical users (e.g., "Linked Record", "Rollup", "Interface")
- **Support & Contact** — placeholder for SA contact info and Airtable support resources

---

### Step 7: Render the HTML Document

Generate a single HTML file. Read `doc-css-framework/references/css-components.md` and copy its full contents into the document's `<style>` tag. Replace `--primary` and `--accent` CSS variables with the detected brand colors.

**Key CSS component reference (full CSS in `doc-css-framework/references/css-components.md`):**

| Component | Class | Purpose |
|-----------|-------|---------|
| Persona card | `.persona-card` | User role card with icon, description, access level |
| Persona grid | `.persona-grid` | 2x2 or 2x3 grid of persona cards |
| Field spec table | `.field-table` | Styled table showing field name, type, config, description |
| Access matrix | `.access-matrix` | Colored permission grid (personas x tables) |
| Automation card | `.auto-card` | Trigger -> Condition -> Actions flow |
| Interface card | `.interface-card` | Interface description with layout, permissions, data |
| Guide section | `.guide-section` | User-friendly walkthrough per persona |
| Change log | `.changelog-table` | Before/after comparison table |
| Glossary | `.glossary-item` | Term + definition pairs |
| Page list | `.page-list` | Interface pages with type badges |
| Detail grid | `.detail-grid` | Key-value layout for interface/automation details |

### Step 8: Print Optimization

The `@media print` block is in `doc-css-framework/references/css-components.md` Section 13 — include it in full and the document will print correctly. The print CSS already encodes all the patterns below, but understanding the reasoning helps when a document has unusual layout needs:

**Cover page:** The `.doc-header` gets `page-break-after: always; break-after: page;` so it renders as a standalone title page. Executive Summary begins on page 2.

**Section flow:** Sections flow naturally — no `page-break-before: always` on `.section` elements. That rule creates full blank pages of whitespace. The cover page is the only element that gets a forced break.

**Grid-to-inline-block:** CSS Grid ignores `break-inside: avoid` on its children, so grids need converting for print: persona, module, and detail grids become `display: block` parents with `display: inline-block` children at `48% width` (2-per-row landscape layout).

**ERD grid exception:** ERD cards are compact enough that 3-across CSS grid works reliably — leave it as `grid-template-columns: repeat(3, 1fr)` in print.

**Interface and automation cards:** These go full-width (`display: block; width: 100%`) in print because they contain too much detail for side-by-side layout.

**Stats bar:** Use `flex: 1 1 0` on stat chips so all chips fit in one row.

**Dual break properties:** Both `break-inside: avoid !important` and `page-break-inside: avoid !important` are needed on every card for cross-browser reliability.

### Step 9: Save and Present

- Save as `[customer]-[solution-name]-technical-design.html`
- Save the file to the Cowork workspace folder (use the workspace path from your system context — it follows the pattern `/sessions/<session-id>/mnt/Work Brain/`)
- Provide the computer:// link
- Note it's optimized for landscape PDF via Print → Save as PDF
- Recommend the user print to PDF immediately and review the output before considering the TDD complete

### Step 10: Print PDF Review

After the user prints to PDF, offer to review the output for common issues:

**What to check:**
- Title page standalone (page 1 should only be the cover)
- No massive whitespace gaps between sections
- Cards not splitting across pages
- Persona/module cards displaying 2-per-row (not 1-per-row or 3-per-row)
- ERD tables displaying 3-across
- Stats bar chips all in one row
- Brand colors preserved (backgrounds not stripped to white)
- Section headers attached to their following content (not orphaned at page bottom)

**Common fixes:**
| Symptom | Cause | Fix |
|---------|-------|-----|
| Massive whitespace between sections | `page-break-before: always` on `.section` | Remove it — sections should flow naturally |
| Cards splitting across pages | CSS Grid parent | Convert to `display: block` + `inline-block` children |
| Section header orphaned at page bottom | Missing `break-after: avoid` | Add `page-break-after: avoid; break-after: avoid;` to `.section-header` |
| Stats bar wrapping to 2 rows | Fixed-width chips | Use `flex: 1 1 0` instead of fixed widths |
| Brand colors missing in print | Browser strips backgrounds | Add `!important` to all branded background rules in `@media print` |
| Section-intro stretching to fill page | `break-after: avoid` on `.section-intro` | Use `break-after: auto` instead |

## Example Usage

**User says:** "Here's the workflow doc we approved and the base is called 'Hilton Task Management'. Generate the technical design doc."
**Skill does:**
1. Reads `structured-input/SKILL.md` for the input parsing protocol
2. Reads `doc-css-framework/SKILL.md` for the shared CSS framework
3. Reads `base-metadata-extractor/SKILL.md` for extraction logic
4. Normalizes input (per structured-input protocol) — infers client: "Hilton", base_id: null
5. Asks clarifying questions (confirms customer name, personas, interfaces/automations extraction)
4. Reads the workflow doc HTML
5. Uses Airtable MCP: `search_bases("Hilton Task Management")` → `list_tables_for_base(baseId)` → `get_table_schema` for detailed field configs
6. Provides the user with automation + interface extraction scripts from `base-metadata-extractor`
7. Waits for user to paste the extraction results
8. Reconciles all data sources
9. Generates all 8 sections with real field names, automation details, and permissions
10. Renders branded HTML document
11. Presents the file link

## Output Checklist

Before presenting the file, verify:
- [ ] `airtable-design-principles/SKILL.md` was read before the Reconcile step
- [ ] Design principles pass completed using inspection thresholds (absolute counts from MCP data)
- [ ] Risk flags, linking mismatches, and naming violations documented in Appendix Section 8
- [ ] No risk content polluting the main body sections (body stays clean; Appendix holds the assessment)
- [ ] `structured-input/SKILL.md` was read before input parsing
- [ ] Input was normalized into the canonical object (Step 0) per structured-input protocol
- [ ] `doc-css-framework/SKILL.md` was read before generating HTML
- [ ] `base-metadata-extractor/SKILL.md` was read before extracting data
- [ ] Clarifying questions asked only for fields not already provided via structured input
- [ ] Schema extracted via MCP (`list_tables_for_base` + `get_table_schema`)
- [ ] Automation extraction script offered and results received (or noted as schema-inferred)
- [ ] Interface extraction scripts offered and results received (or noted as schema-inferred)
- [ ] All 8 sections present in correct order
- [ ] User personas match the roles identified in the workflows
- [ ] Data Model reflects the ACTUAL built base (via MCP), not just the design doc
- [ ] Field specifications include types, configs, and business purpose
- [ ] Automations documented with REAL trigger → action flow data when available
- [ ] Interface Design documented with REAL page layout data when available
- [ ] Permissions matrix is complete (every persona x every table/interface)
- [ ] User Guide is written in non-technical language
- [ ] No "transcript", "auto-generated", or source-revealing language anywhere
- [ ] Print CSS from doc-css-framework included in full
- [ ] Brand colors applied consistently
- [ ] Change Log notes any differences between design and final build
- [ ] Cover page renders as standalone page 1 (title only)
- [ ] No `page-break-before: always` on any `.section` element
- [ ] Grid-to-inline-block conversion applied for persona, module, and detail grids in print CSS
- [ ] ERD grid uses `repeat(3, 1fr)` in print (NOT converted to block)
- [ ] All cards use both `break-inside: avoid !important` AND `page-break-inside: avoid !important`
- [ ] File saved to the Cowork workspace folder (not `/mnt/outputs/` — that path does not exist)
- [ ] User reviewed printed PDF output before delivery
