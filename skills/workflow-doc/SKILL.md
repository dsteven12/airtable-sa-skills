---
name: workflow-doc
description: "Generate a branded, print-ready HTML technical workflow document from call transcripts, meeting notes, or process descriptions. MANDATORY TRIGGERS: workflow doc, workflow diagram, user stories, ERD, data model, discovery call, meeting notes, transcript, process description, call recording, intake process. ALWAYS invoke this skill when processing any pre-build project input into a technical deliverable — even if the user just says 'here are my notes from the call' or pastes a transcript without explicitly asking for a workflow doc. If the input describes a process that needs to be built in Airtable and hasn't been built yet, this is the skill. Outputs a complete 7-section HTML document (Project Summary, User Stories, Workflow Diagrams, ERD, Workflow Data Design, AI Opportunities, Clarifying Questions) themed to the customer's brand colors and optimized for landscape PDF printing."
---

# Workflow Diagram Generator

Generate branded, professional technical workflow documents from call transcripts, meeting notes, or process descriptions. Outputs a complete, print-ready HTML document with Project Summary, User Stories, Workflow Diagrams, ERD, Workflow Data Design, AI Opportunities, and Clarifying Questions — themed to the customer's brand colors.

## Prerequisites

**Before processing any input**, read the shared dependencies:
- **Read `airtable-design-principles/SKILL.md`** — the canonical risk heuristics, linking strategy framework, automation design patterns, and naming conventions. Apply these when generating Clarifying Questions (Step 4) to surface architectural risks before the design is committed to.
- **Read `structured-input/SKILL.md`** — base XML input schema, normalization protocol, and extension pattern used across all doc-generating skills.
- **Read `doc-css-framework/SKILL.md`** — brand detection algorithm, component reference guide, print principles, and language/tone rules.
- **Read `doc-css-framework/references/css-components.md`** — the complete CSS code blocks to embed in the document's `<style>` tag.

- **Read `automation-architect/references/platform-reference.md`** — when the workflow describes automations, reference this for structural constraints (Terminal Block Rule, trigger selection guide, action limits) during the Design Principles Pass in Clarifying Questions.
- **Read `ai-opportunities/SKILL.md`** — the dual-layer framework (business impact + technical context pipeline) for identifying and documenting AI opportunities. Always generate Section 7 (AI Opportunities) using this framework — SAs are mandated to identify AI opportunities in every workflow document.

Input parsing rules are in `structured-input`. The CSS guide is in `doc-css-framework/SKILL.md` and the actual CSS code is in `doc-css-framework/references/css-components.md`. Design principles are in `airtable-design-principles`. Automation constraints are in `automation-architect/references/platform-reference.md`. AI opportunity analysis is in `ai-opportunities`. This skill only defines the **section structure, content extraction, and document-specific patterns**.

## Input Types

This skill accepts any of the following:
- **Structured XML** — explicitly tagged input using the `<workflow-doc>` wrapper (fastest, most precise — see `structured-input/SKILL.md` for the base schema)
- **Call transcripts** (.txt files) — extracts workflows, user stories, and data models from conversation
- **Meeting notes** — rough bullet points or free-form text describing a process
- **Direct description** — user describes the workflow verbally in chat

This skill uses the **base schema only** — no additional extension fields are needed beyond `<client>`, `<solution>`, `<brand_color>`, `<stakeholders>`, and `<content>`.

## Process

### Step 0: Normalize Input

Follow the **Normalization Protocol** in `structured-input/SKILL.md`. Parse the input into the canonical object with: `client`, `solution`, `brand_primary`, `brand_accent`, `stakeholders`, and `raw_content`. This object is the single source of truth for all downstream steps.

### Step 1: Identify the Customer & Brand

Use the normalized `client` field if present. If `brand_primary` is already set from XML input, skip the web search and apply directly. Otherwise, follow the **Brand Color Detection** algorithm in `doc-css-framework/SKILL.md` to determine primary and accent colors.

### Step 2: Extract Content for All Sections

Parse the input to build a complete technical document. Extract content for each section:

#### A. Project Summary (Section 1)
- **Scope/Objective** — a narrative overview of what the solution does, who it serves, the access model
- **Core Modules** — identify 3–5 distinct functional modules. For each:
  - Module name
  - Purpose (1 sentence)
  - Key Features (3–5 bullet points)
  - Success Metric (1 measurable outcome)
- **Data Architecture** — brief prose about table structure, relationships, field patterns
- **Key Design Decisions** — notable architectural choices and their rationale

#### B. User Stories (Section 2)
For each workflow, extract user stories with:
- **Actor** — the user role (e.g., "Team Member", "Admin", "Manager")
- **Story** — "As a [role], I want [action], so that [benefit]"
- **Acceptance Criteria** — 3–5 testable conditions

#### C. Workflow Diagrams (Section 3)
For each identified workflow:
- **Workflow name** — descriptive title (e.g., "Creating a Team Engagement Post")
- **Actor** — the user role performing the workflow
- **Steps** — ordered list of actions with types:
  - `actor` — the starting user/role (dark primary color, white text)
  - `user-action` — manual action (white background, primary border)
  - `system` — automated action (primary color, white text)
  - `decision` — branching point (accent/gold styling)
  - `blocked` — error or denied end state (red styling)
- **Data tables** — which Airtable tables are read from or written to
- **Success metric** — measurable outcome if mentioned

#### D. Entity Relationship Diagram (Section 4)
- **Tables** — name, fields with types (PK, FK, text, single select, etc.)
- **Relationships** — table-to-table links with cardinality descriptions
- Present in a 2×2 grid for screen view, vertical stack for print

#### E. Workflow Data Design (Section 5)
For each workflow, show the data layer:
- **Tables used** — name, operation (Read/Create/Update), purpose, fields involved
- **Data flow** — arrow notation showing the data path
- **Permission logic** — access control rules if applicable
- **Success metric** — data-oriented metric

#### G. AI Opportunities (Section 6)
Follow the complete framework in `ai-opportunities/SKILL.md`. After extracting workflows and the data model (Steps 2A-2E), scan all workflows for AI-eligible steps. For each identified touchpoint:

1. **Identify mechanism** — Automation AI Action, AI Field, or Field Agent (see ai-opportunities Step 1)
2. **Map context pipeline** — what data does the step need, where does it live, how many hops (see ai-opportunities Step 2)
3. **Document output constraints** — target field types, format requirements, silent rejection risks
4. **Estimate iteration budget** — using task type heuristics and context complexity multiplier (see ai-opportunities Step 3)
5. **Write dual-layer content** — business layer (problem, solution, impact, effort, trade-offs, without-it) always visible; technical layer (context pipeline table, output constraints, iteration budget, evidence) in collapsible section (see ai-opportunities Step 4)
6. **Phase the recommendations** — group into Phase 1/2/3 with sequencing rationale (see ai-opportunities Step 5)
7. **Document design decisions** — frame as customer questions with plain-language + technical answers (see ai-opportunities Step 6)

If no AI-eligible steps are identified, include a brief section explaining why.

Append any AI-specific clarifying questions to Section 7 (see ai-opportunities Step 7).

#### H. Clarifying Questions (Section 7)
See Step 4 below for generation rules. Also include AI-specific clarifying questions from the ai-opportunities framework (Step 7 of that skill).

### Step 3: Detect Decision Points and Branching

**Auto-detect branching when the input contains:**
- Permission/role checks ("only managers can...", "if they have access...", "depending on their role...")
- Conditional logic ("if the status is X, then...", "when the field equals...", "based on whether...")
- Approval workflows ("needs to be approved by...", "if approved... if rejected...")
- Error/exception paths ("if it fails...", "when there's an error...", "if the record doesn't exist...")

**For each detected branch:**
- Create a `decision` node with the condition
- Create separate paths for each outcome (Yes/No, Approved/Rejected, etc.)
- Mark dead-end paths with "End of journey"
- Mark continuing paths with "continues below"

### Step 4: Generate Clarifying Questions

Generate clarifying questions when the input is ambiguous or incomplete. Always generate questions when:

**Implied branching (not explicit):**
- "They'd submit the form and it goes to their manager" → Does the manager approve/reject? What happens on rejection?
- "Users can see the dashboard" → Are there different views for different roles? Are some sections hidden?
- "The system sends a notification" → To whom? What channel? What if notification fails?

**Missing information:**
- No error/failure path mentioned → "What happens if [step] fails?"
- No permission model mentioned → "Who has access to perform [action]? Is this role-restricted?"
- Vague actor descriptions → "Who specifically performs this step? What role or title?"
- Unclear system behavior → "Is [action] manual or automated? What triggers it?"
- Missing data context → "Which table/fields does this read from or write to?"

**Standard clarifying question categories:**

1. **Permissions & Access:**
   - "Who is allowed to perform [action]? Is this restricted to specific roles?"
   - "What does a user see if they DON'T have permission?"

2. **Error & Exception Handling:**
   - "What happens if [step] fails or encounters an error?"
   - "Is there a fallback or retry mechanism?"
   - "Who gets notified if something goes wrong?"

3. **Branching & Conditions:**
   - "[condition] — does the workflow split here? What are the possible outcomes?"
   - "Is there an approval/review step before [action]?"
   - "Are there different paths based on [field/status/role]?"

4. **Data & Tables:**
   - "Which Airtable table stores [data object]?"
   - "Is [field] user-input or system-generated?"
   - "Does this create a new record or update an existing one?"

5. **Notifications & Triggers:**
   - "Who receives a notification when [event] happens?"
   - "What channel (email, Slack, in-app) is used for notifications?"
   - "Is this notification automated or manual?"

6. **Scope & Boundaries:**
   - "Where does this workflow start and end?"
   - "Is this a one-time action or repeatable?"
   - "Does this connect to any other workflows?"

**Design Principles Pass — apply before finalizing questions:**

After extracting the standard clarifying questions above, run one additional pass using `airtable-design-principles/SKILL.md`. For each risk heuristic and linking pattern, check whether the proposed data model as described triggers any design-time flags. If so, add a question to the appropriate category surfacing the concern — framed as a clarifying question, not a warning. Use the **design-time thresholds** (ratio-based).

Examples of principles-driven questions:
- If linked record relationships appear to be display-only (no rollups described): "The [Table] link to [Hub Table] appears to show [field] for display — is there also a need for rollups or aggregations from that link, or is it display-only?" *(surfaces Pattern 4 candidate)*
- If many automations are described: "How many automations are expected to be active at go-live? Are any of these triggered in sequence by agents?" *(surfaces queue saturation risk)*
- If Status fields drive automations: "Can [Status] be set by both agents and by other automations? If so, what prevents two automation runs from firing on the same record?" *(surfaces double-trigger risk)*
- If hub/reference tables are described with many linking entities: "How many [Entity] records are expected to link to a single [Hub] record at peak? This affects how we handle the linking strategy." *(surfaces fan-out risk)*

Only generate principles-driven questions when the design as described shows evidence of the risk. Do not generate generic platform warnings.

**IMPORTANT — Language rules for clarifying questions:**
- The section intro must read: "The following questions address open items, implied decision points, and areas that need clarification before finalizing the workflows and data model."
- Each question's context (`q-context`) should state the observation as a fact, NOT reference where it came from. Write "Each person manages their own projects, but Kim tracks all of them" — NOT "Transcript says each person manages their own projects."
- Follow all language/tone rules from `doc-css-framework/SKILL.md`.

### Step 5: Render the HTML Document

Generate a single HTML file containing ALL sections. Read `doc-css-framework/references/css-components.md` and copy its full contents into the document's `<style>` tag. Replace `--primary` and `--accent` CSS variables with the detected brand colors.

**Document structure:**

```
Document Structure:
├── Doc Header (brand badge, solution title, subtitle)
├── 1. Project Summary
│   ├── Section intro (scope/objective as merged narrative)
│   ├── Module Grid (2×2 cards: Purpose, Key Features, Success Metric)
│   └── Summary Card (Data Architecture + Key Design Decisions as prose)
├── 2. User Stories
│   ├── Section intro
│   └── Story Cards (actor badge, story text, acceptance criteria)
├── 3. Workflow Diagrams
│   ├── Section intro
│   └── Workflow Cards (horizontal flow nodes with arrows + legend)
├── 4. Entity Relationship Diagram
│   ├── Section intro
│   ├── ERD Grid (2×2 table cards with fields/types)
│   └── Relationships card
├── 5. Workflow Data Design
│   ├── Section intro
│   └── WF Data Cards (tables grid + data flow + permission logic + metric)
├── 6. AI Opportunities (framework from ai-opportunities/SKILL.md)
│   ├── Section intro
│   ├── Pipeline Overview (flow nodes showing AI touchpoints in context)
│   ├── Implementation Recommendation (phase matrix + narrative)
│   ├── Opportunity Cards (business layer visible, technical layer in <details>)
│   │   ├── Business: Problem, How It Works, Impact, Effort, Trade-offs, Without This
│   │   └── Technical (collapsible): AI Steps, Context Pipeline, Output Constraints, Iteration Budget, Evidence
│   └── Design Decisions (customer questions + plain-language answers + expandable technical rationale)
└── 7. Clarifying Questions
    ├── Section intro
    ├── Standard question categories (q-cat blocks, NOT wrapped in a summary-card)
    └── AI-specific questions (appended from ai-opportunities framework)
```

**Key CSS component reference (full CSS in doc-css-framework):**

| Component | Class | Purpose |
|-----------|-------|---------|
| Section title | `.section-header` | 24px bold primary color heading |
| Section description | `.section-intro` | Light branded callout with left border |
| Sub-section label | `.section-sub` | Gold accent with left border |
| Story card | `.story-card` | White card with primary left border |
| Workflow card | `.workflow-card` | Light gray rounded container |
| Flow node | `.flow-node` | Step badge (.actor, .action, .system, .decision) |
| ERD container | `.erd-container` | White card, 2×2 grid of table cards |
| WF Data card | `.wfdata-card` | White card with primary border |
| Module card | `.module-card` | White card with primary left border |
| Module grid | `.module-grid` | 2×2 CSS grid |
| Summary card | `.summary-card` | Warm amber card (for Data Architecture / Key Design Decisions only) |
| Question category | `.q-cat` | Group of questions under a category title |

**Module card HTML pattern:**
```html
<div class="module-grid">
    <div class="module-card">
        <h3>🎯 Module Name</h3>
        <div class="mod-purpose"><strong>Purpose:</strong> One-sentence description</div>
        <div class="mod-features-title">Key Features:</div>
        <ul class="mod-features">
            <li>Feature 1</li>
            <li>Feature 2</li>
            <li>Feature 3</li>
        </ul>
        <div class="mod-metric"><strong>Success Metric:</strong> Measurable outcome</div>
    </div>
    <!-- ... more module cards ... -->
</div>
```

**Clarifying Questions HTML pattern (NO wrapper div):**
```html
<div class="section-header">Clarifying Questions</div>
<div class="section-intro">The following questions address open items, implied decision points, and areas that need clarification before finalizing the workflows and data model.</div>

<div class="q-cat">
    <div class="q-cat-title">Permissions & Access</div>
    <div class="q-item">Question text here<div class="q-context">Factual context — no source references.</div></div>
</div>

<div class="q-cat">
    <div class="q-cat-title">Next Category</div>
    <!-- more q-items -->
</div>
```

Note: `.q-cat` blocks need to be direct children of `.page`, not wrapped in a `.summary-card`. The reason is that wrapping them creates a single tall container that can't break across pages, which produces large whitespace gaps in the printed PDF.

### Step 6: Print Optimization

The `@media print` block is in `doc-css-framework/references/css-components.md` Section 13 — include it in full. No additional print rules are needed for this document type.

### Step 7: Save and Present

- Save the HTML file as `[customer]-[solution-name]-full.html` to the Cowork workspace folder (use the workspace path from your system context — it follows the pattern `/sessions/<session-id>/mnt/Work Brain/`)
- Provide the computer:// link to the file
- Note that the document is print-optimized for landscape PDF (File → Print → Save as PDF)

## Example Usage

**User provides structured XML input:**
```xml
<workflow-doc>
  <client>Hilton</client>
  <solution>Team Engagement Hub</solution>
  <brand_color primary="#1E4380" accent="#B09A61" />
  <stakeholders>Team Member, Manager, HR Admin</stakeholders>
  <content><![CDATA[
    [transcript or notes here]
  ]]></content>
</workflow-doc>
```
**Skill does:**
1. Reads `structured-input/SKILL.md` for the input parsing protocol
2. Reads `doc-css-framework/SKILL.md` for the shared CSS framework
3. Normalizes input (per structured-input protocol) — client: "Hilton", brand colors set directly, stakeholders pre-defined
4. Skips web search entirely (brand colors provided)
4. Extracts project scope, 4 modules, user stories (using specified stakeholder roles), workflows, ERD, data design
5. Identifies ambiguous areas → generates clarifying questions (scrubbed of source references)
6. Renders complete 7-section branded HTML document
7. Presents the file link

**User says:** "Here's the transcript from my call with Hilton. Can you generate the workflow doc?" *(freeform)*
**Skill does:**
1. Reads `structured-input/SKILL.md` for the input parsing protocol
2. Reads `doc-css-framework/SKILL.md` for the shared CSS framework
3. Normalizes input (per structured-input protocol) — infers client: "Hilton" from context, brand colors null
3. Searches for Hilton brand colors → applies #1E4380 / #B09A61
4. Extracts project scope, 4 modules, user stories, workflows, ERD, data design
5. Identifies ambiguous areas → generates clarifying questions (scrubbed of source references)
6. Renders complete 7-section branded HTML document
7. Presents the file link

**User says:** "Generate a workflow doc for a new customer's intake process" *(no client info)*
**Skill does:**
1. Reads `structured-input/SKILL.md` for the input parsing protocol
2. Reads `doc-css-framework/SKILL.md` for the shared CSS framework
3. Normalizes input (per structured-input protocol) — client: null, brand colors null
3. Falls back to Airtable brand colors (#2D7FF9 / #FCB400)
4. Extracts all available content into the 7-section structure
5. Renders document with Airtable blue theming

## Output Checklist

Before presenting the file, verify:
- [ ] `airtable-design-principles/SKILL.md` was read before generating Clarifying Questions
- [ ] Design principles pass completed — design-time risk flags checked against the proposed data model
- [ ] Principles-driven questions added where evidence of risk exists (not as generic warnings)
- [ ] `structured-input/SKILL.md` was read before input parsing
- [ ] Input was normalized into the canonical object (Step 0) per structured-input protocol
- [ ] `doc-css-framework/SKILL.md` was read before generating HTML
- [ ] `doc-css-framework/references/css-components.md` was read and its contents copied into `<style>` tag
- [ ] All 7 sections present in correct order
- [ ] `ai-opportunities/SKILL.md` was read before generating Section 6
- [ ] AI touchpoints identified across all three mechanisms (Automation, AI Field, Field Agent)
- [ ] Each opportunity has both business layer (visible) and technical layer (collapsible)
- [ ] Implementation recommendation includes phasing with rationale
- [ ] AI-specific clarifying questions appended to Section 7
- [ ] Project Summary has module cards (2×2 grid) with Purpose, Key Features, Success Metric
- [ ] Scope/Objective merged into the Project Summary section intro
- [ ] No "transcript", "auto-generated", "notes", or source-revealing language anywhere
- [ ] Clarifying question contexts state facts, not sources
- [ ] `.q-cat` blocks are direct children of `.page` (not wrapped in `.summary-card`)
- [ ] Print CSS from `css-components.md` Section 13 included in full
- [ ] ERD grid switches to 3-across in print (not converted to block like other grids)
- [ ] Section is called "Workflow Data Design" (not "Workflow + Data Integration")
- [ ] Brand colors applied consistently across all components
- [ ] File saved to Cowork workspace folder (not `/mnt/outputs/`)
