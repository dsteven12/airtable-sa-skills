---
name: engagement-orchestrator
description: "Track and orchestrate multi-phase Airtable engagements across sessions. Manages three engagement types: customer engagements (Align → Design → Build → Deploy → Adopt), learning builds (compressed design → build → test → lessons), and base reviews (health-check → design-advisor → remediation). Acts as a phase checklist (tracks where you are, what's next, which skills to invoke) and a context broker (passes accumulated project context forward so skills don't start cold). MANDATORY TRIGGERS: new engagement, new project, start a project, where are we, what phase, engagement status, project status, kick off, technical scoping, base review. ALWAYS invoke when starting a new multi-session project, resuming work on an existing engagement, or asking about project status across any engagement type."
---

# Engagement Orchestrator

Track multi-phase Airtable engagements across sessions. Two jobs: (1) phase checklist — know where you are, what's next, which skills apply; (2) context broker — pass accumulated decisions, schema context, and deliverable references forward so each skill starts warm, not cold.

## Prerequisites

Read the project note from `01 - Projects/` for the engagement being orchestrated. The `<engagement>` block (defined below) is the source of truth for phase state and accumulated context.

---

## Engagement Types

### Type 1: Customer Engagement

Full Airtable professional services lifecycle. Follows the Align → Design → Build → Deploy → Adopt methodology. Each phase has defined entry criteria, skills, gates, and outputs.

**Pre-engagement note:** Technical Scoping happens in Pre-Sales before the SA/DC engagement begins. The SA may produce a preliminary workflow-doc during scoping. If one exists, reference it in the Align phase as starting context.

#### Phases

**ALIGN** (~1 week)
- Entry: Technical Scoping complete, customer assigned
- Focus: prep and review of scoping findings, walk customer through preliminary workflow-docs, deployment planning, go-live readiness confirmation
- Skills: `workflow-doc` (create or refine preliminary version from scoping notes)
- Gate: customer reviews Customer Solution Guide (in Solution Hub) + preliminary workflow-docs and provides feedback. Customer should not feel like we're starting from scratch.
- Outputs: customer-validated requirements, preliminary workflow-doc (v1), deployment approach
- Context captured: client name, brand colors, stakeholder names/roles, base ID (if created), key requirements, deployment timeline, personas identified

**DESIGN**
- Entry: Align gate passed (customer has reviewed and provided feedback)
- Focus: workflow discovery deep-dive, iterative review with customer
- Skills: `workflow-doc` (update with customer feedback — same doc evolves, not a new artifact), `airtable-design-advisor` (evaluate architecture decisions as they emerge)
- Gate: customer signs off on workflows and data model direction
- Outputs: finalized workflow-doc, approved schema design, linking strategy decisions, automation candidates identified
- Context captured: table names and relationships, linking strategy per relationship (Pattern 1-5), field inventory, automation candidates with trigger types, AI step candidates, risk flags from design-advisor, design decisions with rationale

**BUILD**
- Entry: Design gate passed (customer-approved workflows)
- Focus: build data model in Airtable, automations, interfaces
- Skills: `automation-architect` (detail automation specs), `ai-prompt-builder` (if AI steps present), `airtable-design-advisor` (as-needed during build for emerging questions)
- Sub-phase — Health Check (optional): run after build is finalized but BEFORE UAT. Catches design and scalability issues before users touch the base. Especially valuable on larger cross-functional builds where multiple tables, automations, and personas intersect — building for scale is a core pillar.
  - Skill: `health-check`
  - Context broker injects: table names, linking strategies, automation count, AI step count, expected record volumes
- Sub-phase — UAT: persona representatives test the build and provide feedback
- Gate: UAT feedback incorporated, code freeze
- Outputs: production-ready base, UAT feedback log, health check report (if run)
- Context captured: base ID, automation IDs, interface names, UAT feedback themes, health check findings (if run), final field count, final automation count

**DEPLOY**
- Entry: code freeze (build finalized after UAT)
- Focus: documentation and packaging — everything must be complete BEFORE go-live
- Skills: `technical-design-doc` (required), `training-guide` (optional — depends on engagement scope), `scaffold-extension` packaging (if custom extensions involved)
- Gate: all documentation complete and delivered to Solution Hub Resources
- Outputs: TDD, training guide (if applicable), extension code package (if applicable)
- Context captured: deliverable links, go-live date, training audience/scope

**ADOPT**
- Entry: customer goes live
- Focus: minor changes only — added filters, added fields, view adjustments
- Restrictions: data model changes heavily restricted unless it's just an added field
- Skills: none typically needed (lightweight manual work)
- Context captured: post-launch feedback themes, change requests logged

#### Customer Engagement — Optional Phases

These phases are included in the template but marked optional. The orchestrator tracks them but doesn't block progression if skipped:

- **Health Check** (in Build) — optional. Pre-UAT quality gate for design principles and base performance. Highest value on cross-functional enterprise builds where the data model spans multiple teams and scale matters early.
- **Training Guide** (in Deploy) — depends on engagement scope and whether the customer needs end-user documentation.
- **Extension Packaging** (in Deploy) — only if custom extensions were part of the build.

---

### Type 2: Learning Build

Compressed customer phases without the ceremony. For internal skill development, demo bases, and pattern exploration (like the AI Workflows Learning Lab).

#### Phases

**SCOPE**
- Entry: learning objective defined
- Focus: define what patterns to exercise, customer scenario framing, target tables and automations
- Skills: `airtable-design-advisor` (optional — for deliberate design principle practice)
- Outputs: scope definition in project note, target patterns listed
- Context captured: learning objectives, fictional customer context, target patterns, design principles to exercise

**DESIGN + BUILD** (combined)
- Entry: scope defined
- Focus: interactive schema design → build in Airtable → iterate
- Skills: `airtable-design-advisor` (during design decisions), `automation-architect` (when detailing automations), `ai-prompt-builder` (if AI steps)
- Outputs: working base, automation specs (captured in project note, not formal deliverable)
- Context captured: table names, linking strategies, automation specs, AI prompts, platform discoveries, design tradeoffs made

**TEST + LEARN**
- Entry: build complete enough to exercise target patterns
- Focus: test with sample data, exercise edge cases, capture learnings
- Skills: none required — testing is manual
- Outputs: lessons captured in the learning base's lessons table, skill adaptation opportunities identified
- Context captured: what worked, what broke, platform constraints discovered, skill gaps identified

No formal deliverables required. The "documentation" is the lessons table in the base and the session log in the project note.

---

### Type 3: Base Review

Enters the lifecycle mid-stream. Used when evaluating an existing base for risks, optimization, or production readiness.

#### Phases

**ASSESS**
- Entry: base ID provided (existing base)
- Focus: inspect the base for scalability, design, and performance risks
- Skills: `health-check` (primary), `airtable-design-advisor` (for interpreting findings)
- Outputs: health check report (.docx), risk inventory with severity ratings
- Context captured: base ID, table count, field count, automation count, risk findings by severity, top 3 remediation priorities

**REMEDIATE** (optional — only if assessment surfaces actionable risks)
- Entry: assessment complete, risks identified that warrant changes
- Focus: design and implement fixes for flagged risks
- Skills: `airtable-design-advisor` (evaluate remediation options), `automation-architect` (if automation changes needed)
- Gate: remediation changes approved by base owner
- Outputs: updated base, change log
- Context captured: changes made, risks mitigated, remaining accepted risks

**VERIFY** (optional — only if remediation was done)
- Entry: remediation complete
- Focus: re-run health check to confirm improvements
- Skills: `health-check` (re-run)
- Outputs: updated health check report, before/after comparison
- Context captured: risk score delta, remaining findings

---

## Engagement State Block

The orchestrator reads and writes an `<engagement>` block in the project's `01 - Projects/` note. This is the canonical state store — no separate files.

### Format

```xml
<engagement type="customer|learning|review" status="[current phase]" started="YYYY-MM-DD">
<client>[Client name or "Internal" for learning builds]</client>
<base_id>[Airtable base ID, when known]</base_id>

<phases>
  <phase name="align" status="complete|in-progress|pending|skipped" skill="workflow-doc">
    <output>[[Link to deliverable or note]]</output>
    <context>
      Key decisions, table names, linking strategies, risk flags —
      whatever the next phase needs to start warm.
      Format: key: value pairs, one per line.
    </context>
  </phase>

  <phase name="design" status="pending" skill="workflow-doc, airtable-design-advisor">
    <!-- context accumulates as the phase progresses -->
  </phase>

  <!-- ... remaining phases ... -->
</phases>
</engagement>
```

### State Rules

1. **One phase is `in-progress` at a time.** The orchestrator presents the current phase prominently and shows what's next.
2. **Phases advance manually.** The orchestrator doesn't auto-advance. When you say "we're done with Design" or "move to Build," the orchestrator updates the state.
3. **Phases can be skipped.** Mark as `skipped` with a reason. The orchestrator adjusts the checklist.
4. **Context accumulates.** Each phase's `<context>` block grows as decisions are made. The orchestrator appends, never overwrites.
5. **The engagement block lives in the project note.** Alongside session logs, decisions, and next steps. One source of truth.

---

## Context Broker Behavior

When a skill is invoked during an active engagement, the orchestrator's context broker injects accumulated context from prior phases. The injection format:

```
ENGAGEMENT CONTEXT (auto-injected by orchestrator)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Client: [name]
Engagement type: [customer | learning | review]
Current phase: [phase name]
Base ID: [if known]

Prior phase context:
  [Align] tables: Content, Reviews, Team Members
  [Align] personas: writers (8), editors (3), managing editor (1)
  [Design] linking: Pattern 3 (Hybrid) on Author, Pattern 2 on Content→Reviews
  [Design] risks flagged: Risk 1 (computed field cascade), Risk 5 (double-trigger)
  [Design] automations identified: 4 (AI pipeline, state routing, sync, notifications)

Deliverable references:
  Workflow doc: [[Client — Workflow Doc]]
  Automation specs: [[Client — Automation Specs]] (or inline in project note)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### What gets injected per skill

| Skill invoked | Context injected |
|---------------|-----------------|
| `workflow-doc` | Client name, brand colors, personas, prior version reference (same doc evolves) |
| `airtable-design-advisor` | Table names, linking strategies decided so far, risk flags from prior phases, automation candidates |
| `automation-architect` | Full table/field inventory, linking strategies, AI step candidates, design-advisor risk flags |
| `ai-prompt-builder` | Automation spec (step numbers, trigger tokens, downstream conditionals), table/field names, content types |
| `health-check` | Base ID, table names, expected record volumes, automation count, known risk flags |
| `technical-design-doc` | Base ID, client name, brand colors, all prior phase context (this is the comprehensive doc) |
| `training-guide` | Base ID, client name, personas, interface names, workflow summaries |

### Context depth: summary + references

Each phase's context block contains:
- **Summary lines** (key: value pairs) — enough to orient the skill without reading full prior outputs. 10-20 lines per phase.
- **Deliverable references** (wikilinks) — pointers to the actual artifacts for when the skill needs the full detail.

---

## Orchestrator Invocation Patterns

### Starting a new engagement

User says: "Starting a new customer engagement for Acme Corp" or "New project — Hilton M&L" or "Let's kick off technical scoping for State of Florida"

Orchestrator:
1. Asks engagement type (customer / learning / base review) if not obvious from context
2. Creates or locates the project note in `01 - Projects/`
3. Writes the initial `<engagement>` block with the appropriate phase template
4. Presents the phase checklist with the first phase marked `in-progress`
5. Lists the skills relevant to the first phase

### Resuming an engagement

User says: "Where are we with Acme Corp?" or "Let's pick up the Hilton build" or "What phase am I in?"

Orchestrator:
1. Reads the project note's `<engagement>` block
2. Presents current phase status, accumulated context summary, and what's next
3. If a skill is relevant to the current phase, suggests invoking it with the accumulated context

### Advancing a phase

User says: "Design is done, let's move to Build" or "Customer approved the workflows" or "We're in code freeze"

Orchestrator:
1. Marks the current phase `complete`
2. Advances to the next phase (marks `in-progress`)
3. Presents the new phase's focus, skills, and entry context
4. Updates the project note's `<engagement>` block

### Capturing context

After any skill produces output during an engagement, the orchestrator appends to the current phase's `<context>` block. This happens conversationally — when decisions are made, when schemas are designed, when risks are flagged.

User doesn't need to explicitly say "save this context." The orchestrator watches for:
- Table names and field decisions
- Linking strategy choices (Pattern 1-5)
- Risk flags from design-advisor
- Automation specs from automation-architect
- AI step decisions
- Customer feedback themes
- Deliverable completion

---

## Phase Checklist Display

When presenting engagement status, use this format:

```
ENGAGEMENT: [Client Name] ([type])
Started: [date] | Current phase: [phase]
Base: [base ID or "not yet created"]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Align — workflow-doc v1 delivered, customer reviewed
✅ Design — 3 tables, 4 automations, Pattern 3 on Author
▶  Build — automation specs in progress (2 of 4 detailed)
   ○ Health Check (optional, recommended pre-UAT)
   ○ UAT
☐ Deploy — TDD, training guide (optional)
☐ Adopt
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Next skill: automation-architect (2 automations remaining)
Context available: tables, linking strategy, 2 completed specs
```

Status markers:
- ✅ complete
- ▶ in-progress
- ○ sub-phase (within current phase)
- ☐ pending
- ⊘ skipped

---

## Relationship to Other Skills

This skill does NOT replace any existing skill. It orchestrates them.

- **Invokes nothing automatically.** It tells you which skill to use next and provides the context for that skill. You invoke the skill manually.
- **Reads project notes.** The `<engagement>` block in `01 - Projects/` is the state store.
- **Writes project notes.** Phase transitions and context accumulation update the engagement block.
- **Works with the vault bootstrap.** The `_context.md` file references active engagements. The orchestrator keeps them in sync.

### Skill dependency direction

```
engagement-orchestrator
├── reads: project notes (01 - Projects/)
├── writes: engagement blocks in project notes
├── suggests: which skill to invoke next
└── injects: accumulated context into skill invocations

All other skills remain independent.
The orchestrator is an overlay, not a dependency.
```

---

## Validation Checklist

Before presenting engagement status or advancing a phase:

- [ ] Project note exists in `01 - Projects/` with an `<engagement>` block
- [ ] Current phase status is accurate (check session logs for work done since last update)
- [ ] Context block for completed phases has summary lines + deliverable references
- [ ] Optional phases are marked with their optionality (not silently dropped)
- [ ] Phase advancement has a clear reason (gate passed, user confirmed, or explicit skip)
- [ ] `_context.md` reflects the engagement's current status
