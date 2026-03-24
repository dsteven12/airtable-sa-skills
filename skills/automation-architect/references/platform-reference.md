# Airtable Automations — Platform Reference

Complete reference for Airtable automation triggers, actions, structural constraints, and dynamic values. This is the ground-truth document that the automation-architect skill reads when it needs to verify a structural claim or look up an action's capabilities.

Sources: Airtable support documentation (getting-started-with-airtable-automations, automation-triggers, automation-actions), plus field-tested corrections from production builds.

---

## Table of Contents

1. [Structural Constraints](#structural-constraints)
2. [Trigger Types](#trigger-types)
3. [Trigger Selection Guide](#trigger-selection-guide)
4. [Action Types](#action-types)
5. [Action Selection Guide](#action-selection-guide)
6. [Advanced Logic](#advanced-logic)
7. [Dynamic Values (Token References)](#dynamic-values)
8. [Limits and Quotas](#limits-and-quotas)
9. [Implicit Behaviors](#implicit-behaviors)

---

## Structural Constraints

These are the hard rules of the Airtable automation builder. They cannot be worked around.

### The Terminal Block Rule

**CRITICAL: No steps can be added after a Conditional block or a Repeating Group block.** A Conditional or Repeating Group is always the LAST element at its nesting level. Once you branch, you never rejoin.

This means:
- If Action 3 is a Conditional, there is no Action 4 at the same level. Period.
- All subsequent logic must live INSIDE the branches of that Conditional.
- The same applies to Repeating Groups — nothing follows them.

### Nesting Rules

- A Conditional can only be created INSIDE an existing Conditional branch (or at the top level if it's the first/only conditional in the automation).
- You CAN have multiple sequential actions BEFORE a Conditional within a branch — the Conditional just has to be the LAST thing.
- There is no limit documented on nesting depth, but deep nesting (4+ levels) becomes very hard to maintain in the UI.

### What IS allowed within a branch

Inside a YES or NO branch of a Conditional (or inside a Repeating Group iteration), you can have:
1. One or more sequential Actions (Update record, Create record, Send email, etc.)
2. Followed by AT MOST ONE Conditional or Repeating Group (which must be the last element)

Example of valid structure:
```
Conditional (is text empty?)
├── YES:
│   Action: Update record
│   Action: Send email
│   Conditional (is priority high?)     ← LAST element in this branch
│   ├── YES: Action: Create record
│   └── NO: (empty)
└── NO:
    Action: Update record               ← only action, no conditional needed
```

Example of INVALID structure:
```
Conditional (is text empty?)
├── YES: Action: Update record
└── NO: Action: Update record
Action: Send email                      ← ILLEGAL — nothing can follow a Conditional
```

### Action Groups

Action Groups let you visually organize sequential actions, but they do NOT bypass the Terminal Block Rule. An Action Group containing a Conditional still makes that group the last element at its level.

---

## Trigger Types

### Record-Based Triggers

| Trigger | Fires When | Table Scope | Key Config | Downstream Tokens |
|---------|-----------|-------------|------------|-------------------|
| **When record matches conditions** | A record is created or updated to match ALL specified conditions | Single table | Field conditions (field, operator, value) | All fields on the triggering record |
| **When record created** | Any new record is created in the table | Single table | None (fires on all creates) | All fields on the new record |
| **When record updated** | A specific field changes value | Single table | Select which field(s) to watch | All fields on the record, plus previous field values |
| **When record enters view** | A record appears in a filtered view (new record that matches, or existing record updated to match) | Single table + view | Select a view | All fields on the record |

### Time-Based Triggers

| Trigger | Fires When | Key Config |
|---------|-----------|------------|
| **At a scheduled time** | On a cron-like schedule | Interval (every N minutes/hours/days), specific time, specific days |
| **When date field value is reached** | The current time passes a date stored in a field | Select a date field, optional offset (e.g., 3 days before) |

### External Triggers

| Trigger | Fires When | Key Config |
|---------|-----------|------------|
| **When webhook received** | An external HTTP POST hits the automation's webhook URL | Webhook URL (auto-generated) |
| **When form submitted** | A record is created via an Airtable form view | Select a form view |
| **When a button is clicked** | A user clicks a Button field in the table | Select a button field |

### Critical Trigger Behaviors

**Always surface these when designing automations:**

1. **Triggers require a change of state.** Records already matching conditions when the automation is first turned on will NOT fire. The record must transition INTO the matching state while the automation is active.

2. **"When record updated" does NOT fire on record creation.** If you need to catch both creates and updates, use "When record matches conditions" instead.

3. **"When record enters view" is fragile.** If someone changes the view's filter while the automation is active, the trigger conditions silently change. Always recommend locking the view. Prefer "When record matches conditions" as the self-contained alternative.

4. **"When record matches conditions" is the preferred trigger for state-machine patterns.** It fires on both creation and update, is self-contained (no view dependency), and the conditions are visible directly in the automation.

5. **Automations run on GMT.** Date/time conditions and scheduled triggers use GMT. For non-UTC timezones, use formula-based date adjustment fields or manually offset scheduled times.

6. **Button trigger context:** Button automations run in the context of the clicked record. They are user-initiated and feel synchronous (the user waits for completion feedback via spinner). Heavy processing belongs in a "When record matches conditions" automation triggered by a status change the button sets.

7. **Interface button requirement:** The interface must be published AFTER the automation is turned on for button triggers to work in interfaces.

---

## Trigger Selection Guide

Quick decision matrix for choosing the right trigger:

| Scenario | Recommended Trigger | Why |
|----------|-------------------|-----|
| Record created programmatically (form, automation) | When record created | Simplest; fires on all creates |
| Record created manually by a user | When record matches conditions | Safer — gate on a specific condition, not just existence |
| Condition becomes true on existing record | When record matches conditions | Only trigger that catches existing records transitioning into a state |
| State machine / status-based workflow | When record matches conditions | Self-contained, no view dependency, fires on status transition |
| Driving from a pre-existing filtered view | When record enters view | Only if the view already exists and is locked; prefer "matches conditions" otherwise |
| User-initiated action from interface | When a button is clicked | Direct user intent; interface must be published |
| Time-based batch processing | At a scheduled time | Pair with Find records + Repeating Group for batch operations |
| External system pushes data in | When webhook received | External service POSTs to the auto-generated URL |
| Watching specific fields for updates | When record updated | Select the exact field(s) to watch; does NOT fire on creation |
| Form submission workflow | When a form is submitted | Tied to a specific form view |

---

## Action Types

### Record Actions

| Action | What It Does | Output Tokens | Key Constraints |
|--------|-------------|---------------|-----------------|
| **Create record** | Creates a new record in any table in the same base | Record ID + all set fields | Can trigger other automations ("When record created", "When record matches conditions") — this creates implicit chains |
| **Update record** | Updates fields on a specific record | Updated field values | Record must be identified by ID (from trigger, Find records, or a previous action) |
| **Find records** | Searches a table for records matching conditions | Array of matching records (fields accessible per record) | Max **1,000** records returned. **No sort capability** — records return in undefined order. **Linked record fields NOT supported in conditions** — use formula/rollup workarounds. Use explicit flag fields (e.g., `Current Policy = checked`) instead of sort + first-record patterns |
| **Delete record** | Deletes a specific record | None | Irreversible. The record ID must be known. |

**Find records — critical constraints:**
- **1,000 record limit** per action. If more than 1,000 match, only 1,000 are returned (in undefined order).
- **No sort capability.** There is no reliable way to sort results within Find records. If you need "the most recent" or "the current" record, use an explicit boolean flag field (e.g., `Is Current`) rather than sorting by date and taking the first result.
- **Linked record fields NOT supported in conditions.** You cannot filter by "Linked Table → Field". Workaround: create a formula or rollup field that surfaces the linked value as a text/number field, then filter on that formula field.

### Communication Actions

| Action | What It Does | Key Config |
|--------|-------------|------------|
| **Send email** | Sends an email via Airtable's mail service | To, Subject, Body (supports dynamic values and rich text). Supports CC, BCC, From name, Reply-to via "Show more options." **Requires a valid email address in the "To" field** — missing/invalid emails cause failed runs. |
| **Send Slack message** | Posts to a Slack channel or DM | Requires Slack integration. Dynamic channel routing: use a field containing the channel name prefixed with `#`. Multiple user email tokens separated by commas send individual DMs (not a group DM). |
| **Send Slack actionable message** | Posts a message with approve/reject buttons | Requires Slack integration. User response is captured as a token for downstream conditional logic. |
| **Send Microsoft Teams message** | Posts to a Teams channel | Requires Teams integration |

### AI Actions

| Action | What It Does | Output Tokens | Key Constraints |
|--------|-------------|---------------|-----------------|
| **Generate text (AI)** | Sends a prompt to an AI model and returns free-form text | Single text output | Prompt + referenced field content must stay under **64,000 characters** |
| **Generate structured data (AI)** | Sends a prompt with a JSON schema and returns structured data | Each schema key becomes a separately referenceable token | Supports up to **4 levels** of array/object nesting in the schema. Same 64K character limit. AI output can feed downstream actions including Repeating Groups. |

**Structured AI output is strongly preferred.** Each key in the JSON schema becomes its own dynamic token that downstream actions can reference individually (e.g., `{{Action 4: risk_verdict}}`). Free-text output requires brittle parsing logic.

**AI credit cost:** Every AI action consumes credits from a pooled monthly budget. Cost scales with input volume, model power, and output volume. Models tagged "Low cost" in the UI consume fewer credits. Lower-powered models support ~12,000 words (query + response); higher-powered models support ~90,000 words. Responses exceeding the limit are silently truncated. Low-powered models cannot reliably handle complex tool-calling prompts — they cause errors ("Unknown error while using tools with the agent"). Use direct imperative prompt language with lower-tier models.

**Available models by provider (as of March 2026):**
- **OpenAI:** GPT-4.1 *(default)*, GPT-4.1 mini ᴸᶜ, GPT-5.2, GPT-5.1, GPT-5, GPT-5 mini ᴸᶜ, GPT-5 nano ᴸᶜ, o3, o4-mini, GPT-4o, GPT-4o mini ᴸᶜ, o3-mini
- **Anthropic:** Claude 4.5 Sonnet, Claude 4 Sonnet, Claude 3.7 Sonnet, Claude 3.5 Sonnet, Claude 4.6 Opus, Claude 4.5 Opus, Claude 4.5 Haiku ᴸᶜ, Claude 3.5 Haiku ᴸᶜ
- **Meta:** Llama 3.3 70B ᴸᶜ, Llama 4 Maverick 17B ᴸᶜ, Llama 4 Scout 17B ᴸᶜ, Llama 3.1 8B ᴸᶜ, Llama 3.3 70B (on IBM) ᴸᶜ
- **Mistral AI:** Mistral Large 3, Ministral 3 14B ᴸᶜ, Ministral 3 8B ᴸᶜ
- **Google:** Gemini 3 Flash, Gemini 3 Pro, Gemini 2.5 Flash, Gemini 2.5 Pro, Gemini 2.5 Flash Lite ᴸᶜ
- **IBM:** Granite 3 8B ᴸᶜ
- **Amazon:** Nova Pro, Nova Premier, Nova Lite ᴸᶜ, Nova Micro ᴸᶜ

*(ᴸᶜ = "Low cost" tagged in the UI)*

For detailed model selection guidance by task type (including performance notes), see `ai-prompt-builder/SKILL.md` → Model Selection Matrix.

### Script and Integration Actions

| Action | What It Does | Key Constraints |
|--------|-------------|-----------------|
| **Run a script** | Executes JavaScript with access to `base`, `input`, `output` objects | 30-second timeout. Can exceed Find records limits by fetching via the Airtable API inside the script. Input/output variables must be explicitly declared. Can return arrays usable as Repeating Group input. |
| **Send webhook** | Sends an HTTP request to an external URL | GET/POST/PUT/PATCH/DELETE. Response available as token. |
| **Create/Update in external service** | Jira, Salesforce, Google Sheets, etc. | Varies by connected integrations |

**Script action power moves:**
- Scripts can query tables via `base.getTable().selectRecordsAsync()` — bypasses the Find records 1,000 limit
- Scripts have `input.config()` for receiving dynamic values from previous actions
- Scripts have `output.set()` for passing values to subsequent actions
- Scripts can perform complex logic that would otherwise require multiple conditional branches
- Add try/catch — uncaught errors fail silently

---

## Action Selection Guide

Quick decision matrix for choosing the right action:

| Need | Action | Notes |
|------|--------|-------|
| Write field values to the triggering record | Update record | Reference trigger record ID |
| Create a new child/related record | Create record | ⚠️ Can trigger other automations |
| Query records matching conditions | Find records | 1,000 max; no linked fields in conditions |
| Loop over a list of records and act on each | Repeating Group (forEach) | 8,000 item limit; disables Test button |
| Notify a person via email | Send email | Requires valid email in To field |
| Post to Slack channel or DM | Send Slack message | Dynamic channel via `#channel-name` field |
| Slack message with approve/reject | Send Slack actionable message | Response captured as downstream token |
| Run custom JavaScript logic | Run a script | 30s timeout; can bypass Find records limits |
| Generate text content via AI | Generate text (AI) | 64K character prompt limit |
| Generate structured JSON output via AI | Generate structured data (AI) | 4 levels nesting; 64K limit |
| Branch based on conditions | Conditional logic | Terminal Block Rule applies |
| Send data to external system | Send webhook | HTTP method + payload |

---

## Advanced Logic

### Conditional

- Creates a YES / NO branch based on a condition
- Condition evaluates a dynamic value from a previous action or trigger field
- Supports operators: equals, does not equal, contains, is empty, is not empty, greater than, less than, etc.
- **MUST be the last element at its nesting level** (Terminal Block Rule)
- You can nest Conditionals inside Conditional branches to create decision trees
- The NO branch can be left empty (no actions) — this is valid and common

### Repeating Group (forEach)

- Iterates over an array (typically the results of a Find records action or AI structured data array output)
- Each iteration has access to the current record's fields
- **MUST be the last element at its nesting level** (Terminal Block Rule)
- Actions inside a Repeating Group execute once per record in the result set
- Cannot nest a Repeating Group inside another Repeating Group
- **8,000 item limit** per input list
- **"Test automation" button is disabled** once a Repeating Group is added — all steps must be tested individually
- Counts as **1 automation run** regardless of how many iterations execute

### Action Group

- Visual container for organizing related actions — does NOT change execution behavior
- Actions inside an Action Group execute sequentially, same as if they weren't grouped
- Useful for collapsing sections of a long automation in the builder UI
- Does NOT bypass the Terminal Block Rule

---

## Dynamic Values

Dynamic values (tokens) reference outputs from the trigger or any previous action. They appear as pills in the UI and use the format:

```
{{Trigger: Field Name}}
{{Action N: Output Name}}
{{Action N: Record ID}}
```

### Token availability rules:
- Tokens from the **trigger** are available to ALL actions
- Tokens from **Action N** are available to Actions N+1, N+2, ... (any action that comes after, at the same or deeper nesting level)
- Tokens from inside a **Conditional branch** are NOT available outside that branch
- Tokens from inside a **Repeating Group** are NOT available outside the group
- **Find records** tokens: when Find records returns multiple records, referencing `{{Action N: Field}}` gives the value from the FIRST record only. To process all records, use a Repeating Group.
- **Button trigger special token:** "User who took action" provides ID, Name, and Email of the user who clicked the button.

### Token scope with nesting:
Actions at the top level of the automation provide tokens to everything. Actions inside a branch provide tokens only to subsequent actions in that same branch (or deeper).

### Known Token Limitations

The token picker has hard limitations on which fields can be expanded. These are platform constraints — not configuration issues. Designing around them is a core automation architecture skill.

**1. Linked record fields show "No valid nested options."**
When a trigger fires on Table A and Table A has a linked record field pointing to Table B, the token picker does NOT let you expand that link to access Table B's fields. You cannot reference `{{Trigger: Linked Field → Table B Field}}`. This applies to both trigger tokens and action output tokens where the source field is a linked record.

**Workarounds:**
- Add a Find Records step to query Table B directly (but note: Find Records cannot filter by Record ID — use a unique field with the `is` operator, or a formula field that surfaces the Record ID as text)
- Consolidate logic into the automation that already has the source data in scope (fold the downstream automation into the upstream one)
- Add lookup/formula fields on Table A that surface the Table B values you need — these are expandable in the token picker

**2. Multi-collaborator fields show "No valid nested options."**
Same behavior as linked records. A multi-collaborator field cannot be expanded to access individual user names, emails, or IDs in the token picker. Single collaborator fields expand normally (→ Name, Email, ID).

**Workarounds:**
- Use a Script action that reads the multi-collaborator field via `getCellValue()` and processes each collaborator programmatically
- If only one collaborator is expected, switch to a single collaborator field

**3. Find Records cannot filter by Record ID.**
Record ID is not available as a filterable field in the Find Records conditions UI. You cannot say "find the record with ID recXYZ123."

**Workarounds:**
- Filter by a unique field (primary field with `is` operator)
- Add a formula field `RECORD_ID()` that surfaces the ID as text, then filter on that formula field
- Use a Script action with `selectRecordsAsync()` and filter by ID programmatically

**4. Find Records results require Repeating Group for linked record field writes.**
Update Record may not reliably consume a Find Records result to set a linked record field via direct token reference. The standard pattern: Find Records → Repeating Group → Update Record inside the loop. With Max records = 1, the loop executes exactly once. With 0 results, it skips (correct behavior for "no match found").

**Impact on automation design:**
These limitations are the primary reason to consolidate automations (keep data access within the automation that already has the tokens) and to use Script actions when the token picker cannot provide the data path you need. Always verify token availability in the builder before committing to a cross-table automation design.

---

## Limits and Quotas

| Limit | Value | Notes |
|-------|-------|-------|
| Automation runs per month | Varies by plan (Free: limited, Team: 25,000, Business: 100,000, Enterprise: 500,000) | Counted per base |
| Actions per automation | No hard documented max, but 25+ actions indicates the automation should likely be split | Deep nesting makes debugging difficult |
| Find records max results | **1,000 records** | If more than 1,000 match, only 1,000 are returned (undefined order) |
| Repeating Group max items | **8,000 items** | Input list capped at 8,000; exceeding this silently truncates |
| AI prompt + field content | **64,000 characters** | Prompt text + all referenced field values combined; applies regardless of model |
| AI structured data nesting | **4 levels** | Array/object nesting in JSON schema |
| AI word limit (low-cost models) | **~12,000 words** | Combined query + response. Exceeding this silently truncates the response |
| AI word limit (high-powered models) | **~90,000 words** | Combined query + response. Exceeding this silently truncates the response |
| AI credits (Free plan) | **500/user/month** | Editor+ only. Cannot purchase additional — must upgrade |
| AI credits (Team plan) | **10,000/user/month** | Pooled across workspace. Credit packs available for overage |
| AI credits (Business/Enterprise) | **Contact Sales** | Pooled across organization. Credit packs via Sales rep |
| Script action timeout | **30 seconds** | Scripts exceeding this are terminated |
| Webhook payload size | Varies | Large payloads may be truncated |
| Concurrent automation runs | Limited per-base concurrency | Not publicly documented; queue-based processing |

---

## Implicit Behaviors

These are behaviors that are not errors but are easy to miss:

1. **Triggers require a state change.** Records already matching conditions when the automation is turned on will NOT fire. The record must transition into the matching state while the automation is active.

2. **Create record triggers other automations.** If Automation A creates a record in Table X, and Automation B triggers on "When record created" in Table X, Automation B will fire. This chain is invisible in the builder.

3. **Update record can re-trigger the same automation.** If an automation triggers on "Status = X" and one of its actions updates Status back to X on a different record, a new run fires for that record.

4. **Automation runs are asynchronous.** When a trigger fires, the run is queued. Under load, there may be seconds to minutes of delay before execution begins.

5. **Failed actions don't roll back previous actions.** If Action 5 of 8 fails, Actions 1-4 have already executed and their effects persist. There is no transaction/rollback mechanism.

6. **AI actions can fail silently.** If the AI model returns an error or times out, the action may produce empty/null outputs. Downstream actions that reference those tokens will receive empty values without an explicit error.

7. **Button automations show a spinner.** The user sees a loading state until the automation completes. Long automations (10+ seconds) create a poor UX for button triggers.

8. **Failed run notifications go to the last editor of the automation.** Not the creator, not the base owner — the person who most recently edited the automation. Document this for clients during handoff.

9. **Automations run on GMT.** All date/time evaluations use GMT. This affects scheduled triggers, date field comparisons, and NOW() timestamps in formulas used as trigger conditions.

10. **"When record updated" does NOT fire on record creation.** This is a common misconception. New records only trigger "When record created" or "When record matches conditions."
