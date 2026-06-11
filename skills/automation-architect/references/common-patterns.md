# Common Automation Patterns

Reusable automation patterns for Airtable. Each pattern addresses a specific structural challenge.

## Pattern: Nested Routing (replaces sequential conditionals)

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

## Pattern: Pre-Conditional Hoisting

If an action applies regardless of which branch is taken, place it BEFORE the conditional:

```
[5] UPDATE RECORD — write common values (happens for ALL paths)
[6] CONDITIONAL: which specific path?
    ✅ YES → path-specific actions
    ❌ NO → other path-specific actions
```

This avoids duplicating the common action inside every branch.

## Pattern: Guard → Process → Route

The standard three-phase automation structure:

1. **Guard phase** (top-level sequential actions): Double-trigger guard, Find Records for context, input validation
2. **Process phase** (still sequential, before any conditional): AI processing, writing results back to the record
3. **Route phase** (conditional tree): Branch based on AI results, confidence, or classification

All guard and process actions are sequential at the top level. The route phase is a conditional tree that terminates the automation. This maximizes the "hoisted" actions and minimizes duplication.

## Pattern: Implicit Chain with Setup Flag

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

## Pattern: Status-Gate Trigger (State Machine)

Use "When record matches conditions" with a formula field that evaluates to a clean trigger string (e.g., `"Ready to Send"`). Gate the trigger on that formula field rather than raw status/checkbox combos. This prevents the automation from re-firing if unrelated fields are updated.

## Pattern: Batch Update via Find + forEach

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

## Pattern: Button-Triggered User Action (Interface)

```
Trigger: When a button is clicked
[1] UPDATE RECORD (Table)
    Summary: Capture who initiated and transition state
    Config:
      Initiated By = {{Trigger: User who took action → Name}}
      Status = "In Progress"
```

Remember: Interface must be published AFTER automation is turned on for the button to work.

## Pattern: Form → Notification → Categorize

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

## Pattern: Collaborator → Linked Record Sync (Hybrid Pattern 3)

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
