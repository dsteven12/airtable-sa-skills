---
name: automation-architect
description: "Design, specify, and validate Airtable automation workflows with structurally correct output. Use this skill whenever the user asks to design automations, think through automation logic, specify automation steps, review automation architecture, or debug automation structural issues. Triggers include: 'design an automation', 'automation spec', 'automation architecture', 'what automations do we need', 'walk me through the automations', 'automation deep dive', 'fix my automation', 'why is my automation not working', 'automation builder', 'conditional logic', 'repeating group', or any request involving Airtable automation triggers, actions, branching, or flow design. Also trigger proactively whenever a conversation involves building Airtable tables and the next logical step is defining automations. This skill ensures every automation spec respects Airtable's structural constraints (especially the Terminal Block Rule) and outputs in a consistent, scannable format."
---

# Automation Architect

Design structurally correct Airtable automations in a consistent, scannable output format. This skill exists because Airtable's automation builder has structural constraints that are easy to violate when designing on paper — especially the rule that **nothing can follow a Conditional or Repeating Group**.

## Consuming Skills

This skill is referenced by other Airtable skills when they need automation-specific guidance:
- `airtable-design-advisor` — defers to this skill for structural validation and output format when reviewing automation architecture (Section 4)
- `health-check` — references the platform reference for structural constraints when documenting automation architecture (Section 6)
- `technical-design-doc` — uses the structured spec format when documenting automations in the built solution (Section 5)
- `workflow-doc` — references this skill during the Design Principles Pass when automations are described in the proposed workflow

## Before You Start

1. **Read the platform reference** at `references/platform-reference.md` (sibling to this file) for the complete trigger/action catalog, structural constraints, and token scoping rules.
2. **Read `airtable-design-principles/SKILL.md`** for risk heuristics and automation design patterns (AI step design, state machine patterns, human-in-the-loop gates, audit trail fields).
3. If the automation involves linked records or fan-out concerns, also consult the Linking Strategy Framework in `airtable-design-principles`.

---

## The Terminal Block Rule

This is the single most important structural constraint in Airtable automations. Internalize it before designing anything:

> **No steps can be added after a Conditional or Repeating Group at the same nesting level.** A Conditional or Repeating Group is always the TERMINAL element in its scope. Once you branch, all subsequent logic must live INSIDE the branches.

This means:
- Sequential conditionals (A then B) are **impossible** — B must be nested inside A's branches
- Any logic that applies "regardless of which branch was taken" must be **duplicated into each branch** or **moved before the conditional**
- The automation is a tree that only deepens, never widens after a branch

**Pre-conditional hoisting:** If an action needs to happen regardless of which branch is taken, place it BEFORE the conditional — not after. This is the primary structural optimization.

---

## Design Process

When designing automations for an Airtable solution, follow this sequence:

### Step 1: Inventory the State Transitions

Before writing any automation specs, list every state transition in the system. For each:
- What field changes? (the trigger signal)
- Who/what causes the change? (user, automation, AI, button)
- What should happen next? (the actions)

This inventory becomes the automation list.

### Step 2: Check for Implicit Chains

Map any Create Record actions back to the trigger list. If Automation A creates a record in Table X, and Automation B triggers on record creation in Table X, document that chain explicitly. Add `Setup Complete` flag fields where needed (see Risk 4 in design principles).

### Step 3: Sketch the Tree (Before Detailing Actions)

For each automation, sketch the branching structure FIRST:
- What conditionals are needed?
- What is the nesting order? (outermost condition first)
- Where does duplication occur? (actions needed in multiple branches)

Only after the tree structure is valid should you fill in the action details.

### Step 4: Write the Spec in Output Format

Use the output format defined below. Every automation spec must pass the structural validator checklist before presenting to the user.

---

## Output Format

Every automation specification should use this format to ensure consistency and clarity. The format is designed to be:
- **Scannable** — you can see the full tree structure at a glance
- **Structurally explicit** — nesting depth is unambiguous
- **Token-traceable** — every dynamic reference shows where it comes from

### Automation Header

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
AUTOMATION: [Name]
Table: [Table Name]
Trigger: [Trigger type] — [condition summary]
Purpose: [One sentence describing what this automation accomplishes]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### Action Format

Each action uses a structured block. Indentation (4 spaces per level) indicates nesting depth.

**Simple Action (no branching):**
```
[N] ACTION TYPE (Table)
    Summary: What this action does in plain English
    Config:
      Field = Value or {{token reference}}
    Outputs: token_name → description
```

**Conditional:**
```
[N] CONDITIONAL: description of what is being tested
    Condition: {{token}} operator value

    ✅ YES → [brief label for this path]
        [N.1] ACTION TYPE (Table)
            ...

    ❌ NO → [brief label for this path]
        [N.2] ACTION TYPE (Table)
            ...
```

**Repeating Group:**
```
[N] REPEATING GROUP: iterating over {{Action M: records}}

    Each iteration:
        [N.1] ACTION TYPE (Table)
            ...
```

### Nesting Depth Indicator

Each action's number reflects its position in the tree:
- `[1]`, `[2]`, `[3]` — top-level sequential actions
- `[3.Y.1]`, `[3.Y.2]` — actions inside the YES branch of Action 3
- `[3.Y.2.Y.1]` — action inside the YES branch of a conditional that's inside the YES branch of Action 3
- `[3.N.1]` — action inside the NO branch of Action 3

The Y/N suffix makes branch membership unambiguous when reading the flat list.

### Token Reference Convention

Always show where a dynamic value comes from:
- `{{Trigger: Field Name}}` — from the triggering record
- `{{[N]: output_name}}` — from Action N's output
- `{{[N.Y.2]: field}}` — from a specific action within a branch
- `{{[N]: First record: field}}` — from the first record in a Find Records result list (see below)

### Find Records Returns a List

Find Records always returns a list (array), even when Max records = 1. This important distinction has three key implications for every automation spec that uses Find Records:

1. **Token references must use "First record" syntax.** When referencing fields from a Find Records result, use `{{[N]: First record: Field Name}}` in specs. In the Airtable builder UI, the token picker shows these under a "First record" submenu within the Find Records action's output tokens.

2. **Conditionals checking "were records found" must check the list.** The correct check is whether the list has results (i.e., `{{[N]: First record: Record ID}}` is not empty). Do not reference Find Records output as if it were a single record.

3. **Processing multiple results requires a Repeating Group.** If the Find Records action may return more than one record and you need to act on each, pipe the result list into a Repeating Group. Referencing `{{[N]: First record: Field}}` outside a Repeating Group only gives you the first match — the rest are silently ignored.

When writing specs, always annotate Find Records outputs to make the list nature explicit:

```
[2] FIND RECORDS (Policy Library)
    Summary: Find the current active policy
    Config:
      Where: Current Policy = checked
      Max records: 1
    Outputs: records[] → list of matching records (expect 0 or 1)
    ↳ Use {{[2]: First record: Field Name}} to reference fields downstream
```

### Full Example

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
AUTOMATION: Example — Process Incoming Request
Table: Requests
Trigger: When record matches conditions — Status = "New"
Purpose: Validate the request, classify by priority, and route to the correct team queue.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[1] UPDATE RECORD (Requests)
    Summary: Double-trigger guard — immediately transition to processing state
    Config:
      Status = "Processing"
    Outputs: (none consumed downstream)

[2] FIND RECORDS (Configuration)
    Summary: Retrieve the active routing rules
    Config:
      Where: Active = checked
      Max records: 1
    Outputs: records[] → list of matching config records (expect 0 or 1)
    ↳ Use {{[2]: First record: Field}} to reference downstream

[3] CONDITIONAL: Does the request have a description?
    Condition: {{Trigger: Description}} is not empty

    ✅ YES → Request has content, proceed with classification
        [3.Y.1] GENERATE WITH AI — Structured (Requests)
            Summary: Classify the request by priority and category
            Prompt: Classify this request: {{Trigger: Description}}
                    Routing rules: {{[2]: First record: rules_text}}
            Schema: { priority: string, category: string, confidence: number }
            Outputs: priority, category, confidence

        [3.Y.2] UPDATE RECORD (Requests)
            Summary: Write AI classification results to the request record
            Config:
              AI Priority = {{[3.Y.1]: priority}}
              AI Category = {{[3.Y.1]: category}}
              AI Confidence = {{[3.Y.1]: confidence}}

        [3.Y.3] CONDITIONAL: Is confidence high enough for auto-routing?
            Condition: {{[3.Y.1]: confidence}} ≥ 0.8

            ✅ YES → Auto-route to team
                [3.Y.3.Y.1] UPDATE RECORD (Requests)
                    Summary: Mark as classified and set team assignment
                    Config:
                      Status = "Classified"
                      Assigned Team = (lookup from routing config by category)

            ❌ NO → Flag for human triage
                [3.Y.3.N.1] UPDATE RECORD (Requests)
                    Summary: Flag for manual review due to low AI confidence
                    Config:
                      Status = "Needs Triage"
                      Flag for Review = checked

    ❌ NO → Request is empty, mark as failed
        [3.N.1] UPDATE RECORD (Requests)
            Summary: Cannot process a request with no description
            Config:
              Status = "Failed — No Description"
```

### What makes this format work:

1. **The header** gives you the automation's identity in 4 lines — table, trigger, purpose.
2. **Numbered action IDs** with Y/N path encoding let you trace any action's exact position in the tree without counting indentation levels.
3. **Summary lines** in plain English mean you can read just the summaries to understand the flow, then drill into Config for implementation detail.
4. **Token references** with action IDs (`{{[3.Y.1]: priority}}`) make data flow explicit — you can trace where every value originates.
5. **Conditionals are visually distinct** with the ✅/❌ markers and labeled paths.
6. **The tree only deepens, never widens** — you can verify structural correctness by checking that nothing appears after a CONDITIONAL or REPEATING GROUP at the same indentation level.

---

## Structural Validator Checklist

Before presenting any automation spec, review each of these. If any check fails, restructure before outputting.

- [ ] **Terminal Block Rule**: No action appears at the same indentation level after a CONDITIONAL or REPEATING GROUP
- [ ] **Pre-conditional hoisting**: Any action that needs to happen regardless of branch outcome is placed BEFORE the conditional, not duplicated inside branches (unless it genuinely differs per branch)
- [ ] **Token scope**: No action references a token from a sibling branch (tokens inside YES are not available in NO, and vice versa)
- [ ] **Token ordering**: No action references a token from an action that hasn't executed yet (references only point backward/upward in the tree)
- [ ] **Cross-table token access**: No action references a linked record or multi-collaborator field's nested values via the token picker without verification. If the spec relies on expanding a linked record field or multi-collaborator field, flag it — these show "No valid nested options" in the builder. Replace with a Find Records step, lookup field, or Script action. (See Known Token Limitations in platform-reference.md.)
- [ ] **Find Records by Record ID**: No Find Records action filters by Record ID — it's not available in the conditions UI. Use a unique field (`is` operator), a `RECORD_ID()` formula field, or a Script action instead.
- [ ] **Find Records → linked record write**: Any spec that writes a Find Records result to a linked record field uses the Find Records → Repeating Group → Update Record pattern, not a direct token reference.
- [ ] **Double-trigger guard**: If the trigger watches a status field, the FIRST action transitions that field to a processing state
- [ ] **Find Records list tokens**: All downstream references to Find Records output use `{{[N]: First record: Field}}` syntax — never bare `{{[N]: Field}}`
- [ ] **Find records without sort**: No Find Records action relies on sort order — uses explicit flag fields instead
- [ ] **Implicit chain awareness**: Any Create Record action notes whether it may trigger another automation
- [ ] **Consolidation check**: If a separate automation exists only because Automation A creates a record that Automation B needs to process, evaluate folding B's logic into A. Eliminates cross-table token issues, saves automation budget (50/base limit), and removes an implicit chain.
- [ ] **AI structured output**: All AI actions use structured JSON schema output, not free text
- [ ] **AI output schema is flat**: Structured data schemas are represented as flat key/type/description tables — no nested JSON. Airtable's UI defines schemas as flat rows (key name, type dropdown, description), not nested objects.
- [ ] **Confidence gating**: AI classification results route through a confidence check before auto-routing
- [ ] **Email body format**: Any Send Email action describes the body as rich text paragraphs, not inline strings with `\n` escape sequences. The Airtable email builder uses a rich text editor — escape sequences render literally.

---

## Automation Suite Summary

When presenting multiple automations for a solution, start with a suite overview before the individual specs:

```
┌─────────────────────────────────────────────────┐
│          AUTOMATION SUITE: [Solution Name]       │
├─────────────────────────────────────────────────┤
│                                                  │
│  1. [Automation Name]                            │
│     Trigger: [type] — [condition]                │
│     Actions: [count] │ Depth: [max nesting]      │
│     Chain: [→ Automation N if implicit chain]     │
│                                                  │
│  2. [Automation Name]                            │
│     Trigger: [type] — [condition]                │
│     Actions: [count] │ Depth: [max nesting]      │
│     Chain: standalone                             │
│                                                  │
│  Implicit Chains:                                │
│  • Auto 1 → creates Review → may trigger Auto 3  │
│                                                  │
└─────────────────────────────────────────────────┘
```

This gives a bird's-eye view before diving into individual specs. The chain mapping is critical — it surfaces the invisible dependencies between automations.

---

## Common Patterns

### Pattern: Nested Routing (replaces sequential conditionals)

When you need to route to one of N paths (e.g., Legal Hold / Senior Review / Standard Review), you cannot use N sequential conditionals. Instead, nest them:

```
CONDITIONAL: Is it path A?
├── YES → handle A
└── NO →
    CONDITIONAL: Is it path B?
    ├── YES → handle B
    └── NO → handle C (default/fallback)
```

If each path also needs a shared sub-check (e.g., auto-renewal detection), that sub-check must be duplicated inside each path's branch. This is the cost of the Terminal Block Rule.

### Pattern: Pre-Conditional Hoisting

If an action applies regardless of which branch is taken, place it BEFORE the conditional:

```
[5] UPDATE RECORD — write common values (happens for ALL paths)
[6] CONDITIONAL: which specific path?
    ✅ YES → path-specific actions
    ❌ NO → other path-specific actions
```

This avoids duplicating the common action inside every branch.

### Pattern: Guard → Process → Route

The standard three-phase automation structure:

1. **Guard phase** (top-level sequential actions): Double-trigger guard, Find Records for context, input validation
2. **Process phase** (still sequential, before any conditional): AI processing, writing results back to the record
3. **Route phase** (conditional tree): Branch based on AI results, confidence, or classification

All guard and process actions are sequential at the top level. The route phase is a conditional tree that terminates the automation. This maximizes the "hoisted" actions and minimizes duplication.

### Pattern: Implicit Chain with Setup Flag

When Automation A creates a record that triggers Automation B:

**Automation A** (the creator):
```
[N] CREATE RECORD (Target Table)
    Config:
      ...fields...
      Setup Complete = unchecked     ← signals "B hasn't run yet"
    ⚠️  IMPLICIT CHAIN: This triggers Automation B
```

**Automation B** (the initializer):
```
Trigger: When record matches conditions — Setup Complete = unchecked
[1] ...initialization actions...
[N] UPDATE RECORD
    Config:
      Setup Complete = checked       ← signals "B has finished"
```

### Pattern: Status-Gate Trigger (State Machine)

Use "When record matches conditions" with a formula field that evaluates to a clean trigger string (e.g., `"Ready to Send"`). Gate the trigger on that formula field rather than raw status/checkbox combos. This prevents the automation from re-firing if unrelated fields are updated.

### Pattern: Batch Update via Find + forEach

```
Trigger: At a scheduled time
[1] FIND RECORDS (Target Table)
    Config:
      Where: Status = "Pending Batch" (or use a locked view)
      Max records: 1000
[2] REPEATING GROUP: iterating over {{[1]: records}}
    Each iteration:
        [2.1] UPDATE RECORD (Target Table)
            Config:
              Status = "Processed"
              Processed At = NOW()
```

Note: Lock the view used in Find records to prevent accidental condition drift.

### Pattern: Button-Triggered User Action (Interface)

```
Trigger: When a button is clicked
[1] UPDATE RECORD (Table)
    Summary: Capture who initiated and transition state
    Config:
      Initiated By = {{Trigger: User who took action → Name}}
      Status = "In Progress"
```

Remember: Interface must be published AFTER automation is turned on for the button to work.

### Pattern: Form → Notification → Categorize

```
Trigger: When a form is submitted
[1] SEND EMAIL
    Summary: Confirmation to submitter
    Config:
      To: {{Trigger: Email}}
[2] UPDATE RECORD
    Summary: Tag submission source
    Config:
      Source = "Form"
      Submission Type = (based on form fields)
[3] SEND SLACK MESSAGE
    Summary: Notify team channel
    Config:
      Channel: #intake-queue
      Message: New submission from {{Trigger: Name}}
```

### Pattern: Collaborator → Linked Record Sync (Hybrid Pattern 3)

One automation per Hybrid link. Keeps the Collaborator field (operational — notifications, interface filtering) in sync with a Linked Record field (analytical — rollups, reporting).

**Single collaborator variant** (standard — use this by default):

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
AUTOMATION: Sync [Field Name] → [People Link Field]
Table: [Entity Table]
Trigger: When record updated — watch [Collaborator Field]
Purpose: Keep the linked People record in sync with the collaborator field for reporting rollups.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[1] FIND RECORDS (People)
    Summary: Find the People record matching the collaborator's email
    Config:
      Where: Email contains {{Trigger: [Collaborator Field] → Email}}
      Max records: 1
    Outputs: records[] → list of matching People records (expect 0 or 1)
    ↳ Use {{[1]: First record: Field}} to reference downstream

[2] REPEATING GROUP: iterating over {{[1]: records}}

    Each iteration:
        [2.1] UPDATE RECORD ([Entity Table])
            Summary: Set the linked People record on the entity
            Config:
              [People Link Field] = {{[2]: Record ID}}
```

Three steps, portable to any Hybrid link. The Repeating Group is required because Find Records results don't reliably write to linked record fields via direct token reference. With Max records = 1, the loop runs once. With 0 results (collaborator not in People table), it skips — correct behavior.

**Multi-collaborator variant** (requires Script action):

When the collaborator field allows multiple users, the token picker shows "No valid nested options" — you cannot expand to get individual emails. Use a Script action instead:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
AUTOMATION: Sync [Multi-Collaborator Field] → [People Link Field]
Table: [Entity Table]
Trigger: When record updated — watch [Multi-Collaborator Field]
Purpose: Sync all collaborators to linked People records for team reporting.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[1] RUN A SCRIPT
    Summary: Read collaborator emails, match against People table, write linked records
    Input variables:
      recordId = {{Trigger: Record ID}}
    Script logic:
      1. Get the trigger record from [Entity Table] via selectRecordsAsync()
      2. Read [Multi-Collaborator Field] → array of {id, email, name}
      3. Query People table, match by email
      4. Update [People Link Field] with all matched People record IDs
    Outputs: (none — script writes directly)
```

Key difference: the Script action bypasses the token picker entirely by reading field values via `getCellValue()` and writing via `updateRecordAsync()`. Pass only the Record ID through `input.config()` — don't try to pass the unexpandable multi-collaborator field.

**When to use which:**
- Single collaborator field → standard Find Records pattern (no code required)
- Multi-collaborator field → Script action (token picker can't expand multi-collaborator)
- If the People table doesn't exist yet → evaluate whether you actually need Pattern 3, or if Pattern 1 (pure Collaborator) is sufficient

---

## Anti-Patterns to Flag

When reviewing or designing automations, pay attention to these patterns:

1. **Sequential conditionals** — Two conditional blocks at the same nesting level. Restructure as nested conditionals.
2. **Actions after a conditional** — Any action at the same level following a conditional block. Move it before the conditional or inside every branch.
3. **Sort-dependent Find Records** — Relying on sort order in Find Records to get "the latest" or "the current" record. Use explicit flag fields.
4. **Free-text AI output** — AI actions returning unstructured text that requires parsing. Use structured JSON schema.
5. **Missing double-trigger guard** — An automation that triggers on a status value but doesn't immediately transition that value as its first action.
6. **Unbounded Repeating Groups** — Iterating over Find Records results without a Max Records limit. Always set a ceiling.
7. **Cross-branch token references** — Referencing `{{[3.Y.1]: value}}` from inside the NO branch of Action 3. Tokens from YES are not available in NO.
8. **Linked record fields in Find Records conditions** — Find Records does not support linked record fields in its condition filters. Use a formula/rollup field that surfaces the linked value as text/number instead.
9. **Missing GMT offset** — Date/time conditions or scheduled triggers without accounting for GMT. Remember that all automation time evaluations run in GMT.
10. **Fragile view-based triggers** — Using "When record enters view" without locking the view. A filter change can silently change the trigger conditions.
11. **Infinite loop risk** — An automation action that updates the same field/value the trigger watches may re-trigger itself on another record (or the same record via a chain).
12. **Find Records treated as single record** — Referencing `{{[N]: Field}}` instead of `{{[N]: First record: Field}}` from a Find Records action. Remember that Find Records always returns a list and the "First record" token accessor is required even when Max records = 1.

---

## Automation Design Checklist

Before finalizing any automation design, confirm ALL of these:

- [ ] Trigger is the right type for the use case (use Trigger Selection Guide in platform reference)
- [ ] A state-change mechanism exists (record won't be stuck in a triggered state forever)
- [ ] GMT offset addressed if any date/time conditions or scheduled triggers are involved
- [ ] Find Records outputs referenced with "First record" token syntax (Find Records always returns a list)
- [ ] Linked record fields avoided in Find Records conditions (use formula alternatives)
- [ ] forEach loops verified to stay under 8,000 item limit
- [ ] Locked view used if trigger is "When record enters view"
- [ ] Infinite loop risk checked (does any action step re-trigger the same or another automation unintentionally?)
- [ ] Failed run notification documented — last editor of the automation receives them
- [ ] AI prompt size verified to stay under 64,000 characters (prompt + all referenced field values)
- [ ] All structural validator checks pass (Terminal Block Rule, token scope, etc.)

---

## Gotchas Section

When outputting automation specs, include a Gotchas / Design Notes section after the action tree to surface important considerations:

```
Gotchas / Design Notes:
• [Any trigger-specific warnings — GMT, state-change requirement, view locking]
• [Any action-specific limits — Find Records 1K cap, forEach 8K cap, AI 64K char limit]
• [Any implicit chain risks — which Create Record actions may trigger other automations]
• [Any token scope concerns — values that aren't available where you'd expect]
• [Interface publishing requirement if button triggers are used]
```

This is where the platform reference knowledge becomes practical advice and should be included whenever presenting automation specs.

---

## AI Prompt Design Patterns

For AI prompt design guidance — including when to use automation AI vs Omni AI fields, structured output schema design, prompt engineering patterns, and prompt size estimation — read `references/ai-prompt-patterns.md`.
