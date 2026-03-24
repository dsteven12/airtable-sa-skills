---
name: training-guide
description: "Generate a branded, print-ready HTML training guide from video transcripts, screen recordings, workflow descriptions, or Airtable interface screenshots. MANDATORY TRIGGERS: training guide, training materials, user guide, onboarding doc, how-to guide, workflow walkthrough, VTT, SRT, loom, screen recording, end-user documentation, step-by-step instructions. ALWAYS invoke this skill when the user provides transcripts, screenshots, or walkthrough descriptions and wants documentation for end users — even if they don't explicitly say 'training guide.' If the goal is teaching people how to USE a deployed Airtable app, this is the skill. Outputs a print-friendly HTML document organized by persona/role with numbered steps, annotated UI mock-ups, and contextual tips."
---

# Training Guide Generator

Generate branded, print-ready training guides from video transcripts, screen recording transcripts, workflow descriptions, or Airtable interface screenshots. Outputs an HTML document organized by user persona with step-by-step workflows, annotated UI mock-ups, and contextual tips.

## Prerequisites

**Before processing any input**, read these shared dependencies:
- **Read `structured-input/SKILL.md`** — contains the base XML input schema, normalization protocol, and extension pattern used across all doc-generating skills.
- **Read `doc-css-framework/SKILL.md`** — contains CSS variables, component classes, print CSS, brand detection logic, and language/tone rules.
- **Read `base-metadata-extractor/SKILL.md`** — if the training guide needs interface or schema data from a live base, this contains the MCP extraction steps and browser console scripts for interfaces.

Input parsing rules are defined in `structured-input`. Styling and print rules are defined in `doc-css-framework`. Data extraction logic is defined in `base-metadata-extractor`. This skill defines the **document structure, content extraction patterns, and training-specific components**.

## Input Types

This skill accepts any combination of:
- **Structured XML** — explicitly tagged input using the `<training-guide>` wrapper (see `structured-input/SKILL.md` for the base schema and extension pattern)
- **Video transcripts** (.txt, .vtt, .srt) — from Loom, Zoom, or screen recording tools
- **Screenshots** (images) — of the actual Airtable interface or application being documented
- **Workflow descriptions** — written or verbal descriptions of what each user role does
- **Airtable field/table schemas** — extracted via MCP (see `base-metadata-extractor`) or screenshots/descriptions

The most effective input is **transcript + screenshots together** — the transcript provides the workflow narrative and the screenshots provide the visual reference for building accurate mock UIs.

### Skill-Specific Extension Fields

Beyond the base schema (`client`, `solution`, `brand_color`, `stakeholders`, `content`), this skill accepts:

| Extension Field | When provided | When absent |
|-----------------|--------------|-------------|
| `<personas>` | Use as the exact persona list (skip inference from content) | Infer personas from transcript narration and content context |
| `<transcript_type>` | Optimize parsing for the specified format (loom, zoom, vtt, srt) | Auto-detect format from content structure |

## Process

### Step 0: Normalize Input

Follow the **Normalization Protocol** in `structured-input/SKILL.md`. Parse the input into the canonical object with: `client`, `solution`, `brand_primary`, `brand_accent`, `stakeholders`, `raw_content`, and extension fields (`personas`, `transcript_type`). This object is the single source of truth for all downstream steps.

### Step 1: Identify the Customer & Brand

Use the normalized `client` field if present. If `brand_primary` is already set from XML input, skip the web search and apply directly. Otherwise, follow the **Brand Color Detection** algorithm in `doc-css-framework/SKILL.md` to determine primary and accent colors.

If no customer brand is identified and no `brand_color` was provided, use these defaults:
- **Primary:** `#0A3161` (navy)
- **Accent:** `#7C3AED` (purple)
- **Light background:** `#E8EDF4`

### Step 2: Extract Personas

If the normalized object includes `personas` or `stakeholders`, use those as the starting persona list. Otherwise, identify distinct user personas from the content. Each persona represents a role with different workflows, permissions, and views of the system. Common patterns:

- **Data entry / submitter** — creates and submits records (e.g., Department Head)
- **Reviewer / approver** — reviews, edits, and approves submitted records (e.g., DCOO Reviewer)
- **Admin / coordinator** — manages the full lifecycle, compiles, generates outputs (e.g., Admin)
- **Viewer / consumer** — read-only access to dashboards or outputs (e.g., Commissioner)

For each persona, extract:
- **Label** — the role name as users know it
- **Icon** — an emoji representing the role
- **Color** — assign from the brand palette (primary for main roles, accent for secondary)
- **Description** — one sentence explaining what this persona does
- **Step count** — how many workflow steps they have

### Step 3: Extract Steps per Persona

Parse transcripts and screenshots to identify sequential workflow steps. Each step should capture:

| Field | Source | Description |
|-------|--------|-------------|
| **Title** | Transcript narration | Short, action-oriented title (e.g., "Filter to Your Department") |
| **Tab/Location** | Screenshots or transcript | Which interface tab or page this step occurs on |
| **Detail** | Transcript narration | 2-3 sentence description of what the user does and why |
| **UI Mock** | Screenshots | A simplified HTML recreation of what the user sees at this step |
| **Annotations** | Transcript + screenshots | Lettered callouts (A, B, C...) explaining specific UI elements |
| **Tip** | Transcript context | A practical tip or warning relevant to this step |

#### Step extraction from transcripts

Video transcripts follow a pattern where the narrator:
1. States what they're about to show ("So I want to take you through the department head flow")
2. Describes the UI they're looking at ("You have 3 tabs: completed, in review, and in progress")
3. Demonstrates an action ("I can create a new report")
4. Explains the outcome ("It will go ahead and mark this as in progress")
5. Provides context or caveats ("We want to make sure department heads don't have the ability to approve")

Map these narration patterns to step fields:
- Pattern 1 → new step title
- Pattern 2 → UI mock content + annotations
- Pattern 3 → step detail
- Pattern 4 → step detail (outcome)
- Pattern 5 → tip

#### Step extraction from screenshots

Screenshots provide the visual accuracy for mock UIs. For each screenshot:
1. Identify the interface tab shown (from the tab navigation bar)
2. Note specific UI elements: buttons, dropdowns, status badges, KPI cards, lists
3. Capture exact labels, badge text, and color coding
4. Note the layout pattern: list view, record detail, dashboard, editor

### Step 4: Build UI Mocks

For each step, create a simplified HTML mock that mirrors what the user sees. The mock should be recognizable but not a pixel-perfect reproduction. Include:

**Navigation bar** — show the 5 interface tabs (or however many exist) with the active tab highlighted in the persona's color.

**Key UI patterns to replicate:**

| Pattern | When to use | Elements |
|---------|------------|----------|
| **List with cards** | Report lists, section lists | Cards with title, status badges, date badges, action buttons |
| **KPI dashboard** | Status overview pages | Grid of colored number cards with labels |
| **Editor/builder** | Report creation/editing | Progress bar, section headers, line items with action icons, add buttons |
| **Filter + tabs** | Filtered list views | Dropdown filter, status tabs with counts |
| **Record picker** | Compilation views | "Included" and "Available" sections with add/remove |
| **Digest/output** | Generated report views | Branded card with KPIs, summary text, navigation links |
| **Confirmation dialog** | Delete/submit confirmations | Warning icon, message, cancel/confirm buttons |
| **Flow diagram** | Multi-step processes | Numbered circles with connecting lines and descriptions |

**Badge styles** — use consistent CSS classes:
- `.green` — Completed, Submitted, Generated (green background, dark green text)
- `.purple` — Digest Generated, Digest Available (purple background)
- `.gray` — metadata (submitted by, dates, section counts)
- `.yellow` — In Progress, Started dates (yellow background)
- `.red` — In Review, urgent items (red background)
- `.navy` — brand-specific elements

**Button styles:**
- Primary (filled, brand color) — main actions: Submit, Create, Review, Manage
- Outline — secondary actions: Save Draft, View Details, View Digest
- Danger (red outline) — destructive: Remove, Delete

### Step 5: Write Annotations

For each mock UI, identify 3-5 key elements that need explanation. Assign letters (A, B, C, D, E) and write concise, one-sentence descriptions. Annotations should answer "what is this and why does it matter?"

Good annotation: `"Department filter — only shows departments with active (In Progress or In Review) reports."`
Bad annotation: `"This is the filter dropdown."`

### Step 6: Write Tips

Each step should have one contextual tip. Tips fall into categories:
- **Permissions/access** — "You will NOT see an Approve button. Only DCOOs can move to Completed."
- **Performance** — "The filter only shows active departments to keep the list manageable."
- **Workflow context** — "After approval, the report becomes available for Admin compilation."
- **Safety/warnings** — "Once confirmed, deleted items are gone permanently."
- **Shortcuts** — "Click a KPI card to reveal department contacts for follow-up emails."

## Document Structure

The output HTML document uses this structure:

```
Cover Page (brand-colored header)
├── Title: "[System Name] — Training Guide"
├── Subtitle: "Step-by-step workflows for each role"
│
Persona Tabs (sticky navigation, screen only — hidden in print)
│
For each Persona:
├── Persona Header (icon, name, description, step count)
│
├── Step 1 Card
│   ├── Step Header (number, title, tab badge)
│   ├── Detail paragraph
│   ├── Mock UI
│   ├── Annotations (A, B, C...)
│   └── Tip box
│
├── Step 2 Card
│   └── ...
│
└── Step N Card
    └── ...
│
Footer
```

### Print Optimization

The HTML must include these print-specific CSS rules:

```css
@media print {
  body { background: white; font-size: 10pt; }
  .no-print { display: none !important; }
  .page-break { page-break-before: always; }
  .avoid-break { page-break-inside: avoid; }
  .step-card { page-break-inside: avoid; }
  .cover-page { page-break-after: always; }
  .persona-header { page-break-after: avoid; }
  @page { margin: 0.6in 0.5in; size: letter; }
}
```

Key print rules:
- Step cards must not split across pages (`page-break-inside: avoid`)
- Each persona section starts on a new page (`page-break-before: always` on persona dividers)
- The cover page gets its own page
- Persona tabs are hidden in print (all personas print sequentially)
- Mock UIs should have visible borders in print (background colors may not print)

### Screen Behavior

On screen, the document should:
- Show persona tabs as sticky navigation at the top
- Only display the active persona's steps (hide others)
- Allow switching between personas via tab clicks
- Use JavaScript `showPersona()` function to toggle visibility

In print, all personas display sequentially with page breaks between them.

## Output

Save the final HTML to the Cowork workspace folder (use the workspace path from your system context — it follows the pattern `/sessions/<session-id>/mnt/Work Brain/`) with a descriptive filename like `[system-name]-training-guide.html`.

The output should be a single self-contained HTML file with:
- Embedded CSS (no external stylesheets except Google Fonts)
- Minimal JavaScript (only for persona tab switching)
- All mock UIs built with HTML/CSS (no images or external dependencies)
- Print-ready formatting that produces clean PDFs when printed from browser

## Reference

For a complete working example of this skill's output, see `references/example-structure.md` which documents the component patterns and HTML structure used in the Montgomery County Weekly Reports training guide.
