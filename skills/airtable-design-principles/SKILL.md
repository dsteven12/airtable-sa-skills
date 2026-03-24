---
name: airtable-design-principles
description: "Shared Airtable design principles and architectural standards used across all Airtable-related skills. Read by airtable-design-advisor (pre-build review), automation-architect (automation structural specs and AI prompt design), health-check (post-build risk assessment), workflow-doc (design steering), and technical-design-doc (design violation flags). Contains: Risk Heuristics (8 categories), Linking Strategy Framework (5 patterns), Automation Design Patterns, and Naming Conventions."
---

# Airtable Design Principles

Canonical design standards and architectural knowledge for Airtable solution architecture. This is a **shared reference — not a standalone skill**. It is read by other skills to ensure consistent design guidance across the full engagement lifecycle.

**Consuming skills and how they use this file:**
- `airtable-design-advisor` — applies all sections proactively during pre-build design review
- `automation-architect` — applies Automation Design Patterns and AI Step Design when specifying automation workflows; extends with platform-specific structural constraints (Terminal Block Rule, trigger/action reference)
- `health-check` — applies Risk Heuristics to a live base as a post-build assessment
- `workflow-doc` — uses Risk Heuristics and Linking Strategy to surface design concerns in the Clarifying Questions section
- `technical-design-doc` — uses all sections to flag violations in the final built solution and document design decisions in the Appendix

---

## Risk Heuristics

Eight platform risk patterns that manifest under production load. Each has two detection modes:

- **Design-time threshold** — used when evaluating a *proposed* architecture (ratios, cardinality patterns, planned counts)
- **Inspection threshold** — used when evaluating a *live base* via MCP schema extraction (absolute field/automation counts)

Apply only the risks that are evidenced by the design or base being reviewed. Do not generate generic warnings.

---

### Risk 1: Computed Field Cascade

**Design-time flag:** Computed field density exceeds 30% of total fields on any table (formulas, lookups, rollups, counts).

**Inspection flag:** Any table with >50 computed fields, OR any multi-hop lookup chain (A → B → C recalculations crossing table boundaries).

**What happens:** Every record edit triggers recalculation of all computed fields on that record, plus propagation to any table with lookups or rollups pointing at it. Under concurrent editing (5+ users), recalculation queues back up — causing stale formula values for seconds to minutes. Silent degradation: no error is thrown, fields just return old values.

**Compounding factors:**
- Repeated slot patterns (Rate 1–8, Total 1–8) — each slot multiplies the recalculation surface
- Multi-hop lookups (A → B → C) — chain recalculations cascade across tables
- Automations that write back to fields with downstream lookups (can create cascade loops)
- Agents making rapid sequential edits — each triggers a full recalc pass

**Mitigations:**
- Monitor formula lag during UAT with concurrent users before go-live
- Audit multi-hop lookup chains — flatten with automation-written cache fields where source data rarely changes
- Replace display-only lookups (showing one field from a linked record) with the Flat Field pattern (see Linking Strategy Framework, Pattern 4)
- Avoid automations that write to computed field trigger fields in tight loops

---

### Risk 2: High-Cardinality Linked Records (Fan-Out)

**Design-time flag:** A "hub" record (reference/lookup table) will be linked to by many entity records — airports, people, vendor types, policies, configurations.

**Inspection flag:** Any table with >100 link fields, OR reference tables linked TO by many entity tables (high in-degree hub detected via `multipleRecordLinks` field density across the schema).

**What happens:** When a record is created, duplicated, or updated, Airtable updates the inverse link on every linked record. A policy record linked to by 1,000 contracts: updating that policy cascades inverse updates to 1,000 contract records. Silent — no visible error, just slowdown that accumulates as data grows.

**Compounding factors:**
- Tables with >100 link fields amplify cost per operation
- Native record duplication on high-link tables is especially expensive (triggers fan-out for every link)
- Hub tables linked from multiple entity tables compound across all entity types simultaneously

**Mitigations:**
- Treat hub tables as read-mostly — schedule bulk edits during off-hours
- Use script-based record creation instead of native duplication for high-link-count tables
- Flatten display-only links to automation-written text fields (Pattern 4)
- Use Script actions to bypass token picker limitations when automations need to traverse high-cardinality links or multi-collaborator fields (see Script Action Escape Hatches below)
- Monitor hub record edit performance over time — degradation is gradual and silent

---

### Risk 3: Automation Queue Saturation

**Design-time flag:** >30 planned automations, OR any single automation with >10 actions, OR multiple record-creation triggers that can fire simultaneously, OR button-press automations that agents trigger in rapid succession.

**Inspection flag:** >30 deployed automations confirmed via automation extraction, OR individual automations with sequential Update Record steps totaling >9 actions, OR multiple scheduled automations set to the same trigger time.

**What happens:** Airtable processes automation runs with limited per-base concurrency. When many automations trigger simultaneously, the queue backs up. Button-press automations feel sluggish; scheduled automations may overlap with agent-triggered ones.

**Key patterns to flag:**
- Long automation chains (15+ actions) — single point of failure, no retry; any action failing halts all downstream steps silently
- Multiple scheduled automations running at the same minute — they queue, not parallelize
- Button-press automations that agents trigger in rapid succession (e.g., Copy RFP + Copy Requirements + Copy UDIDs)
- Custom Script actions that query multiple tables via `selectRecordsAsync` — each query competes for throughput

**Mitigations:**
- Stagger scheduled automations by 5–10 minutes
- Add status/feedback fields (`Processing`, `Complete`, `Failed`) so automation progress is visible
- Add try/catch to Custom Script actions — uncaught errors fail silently
- Consolidate related button presses into a single script-based automation
- Monitor automation run history weekly for duration creep

---

### Risk 4: Implicit Automation Chains

**Design-time flag:** Multiple "When record created" automations across related tables, especially when other automations also create records in those tables.

**Inspection flag:** Automation extraction shows multiple "record created" triggers across tables that are linked, combined with "create record" actions in other automations — forming an invisible chain.

**What happens:** One automation's Create Record action triggers another automation's "When record created" trigger. This chain is invisible in the automation builder. If the downstream automation fails (rate limit, API error), the record exists but its default field values are never populated. The upstream automation shows as "successful" — the failure is completely hidden.

**Mitigations:**
- Document all implicit chains — map which automations trigger which via record creation
- Add "Setup Complete" flag fields that creation automations set at the end of their run
- Build audit views filtered to records where the setup flag is unchecked + creation date > 5 minutes ago

---

### Risk 5: Double-Trigger Risk

**Design-time flag:** An automation triggers on a field change (e.g., Status = "Pending Review") where the same field could be set by multiple paths, by user action, or by another automation.

**Inspection flag:** Automations with "field changes to [specific value]" triggers on Status fields that are also agent-editable (not automation-only).

**What happens:** Two automation runs fire for the same record, creating duplicate downstream records, duplicate emails, or duplicate AI calls. Often caused by agents who set a status value, the automation starts processing, and the agent (or another automation) sets the same value again before the first run completes.

**Mitigation:** Immediately flip the trigger field to a transitional value ("Processing") as the **first action** in the automation — this prevents a second trigger from firing while the automation runs.

---

### Risk 6: Button-Press Automation Contention

**Design-time flag:** >10 planned button-press automations, OR families of related buttons that agents would logically trigger in sequence.

**Inspection flag:** >10 button-press automations confirmed via automation extraction, OR groups of 3+ thematically related buttons on the same table.

**What happens:** When an agent presses 3 related buttons in rapid succession (e.g., "Copy RFP", "Copy Requirements", "Copy UDIDs"), each queues a separate automation run. Under concurrent usage — multiple agents doing this for different records — the queue backs up. Heavy automations (9+ sequential Update Record actions) consume disproportionate rate budget.

**Mitigations:**
- Combine related button presses into a single script-based "Initialize" automation
- Add visual feedback (status fields) for long-running button automations
- Evaluate whether sequential Update Record steps can be replaced with a single script action

---

### Risk 7: Sync Table Cascade

**Design-time flag:** Cross-base syncs are planned.

**Inspection flag:** Fields named with "copy" patterns ("Table copy", "Table copy copy", "Table 2 copy") — these are stale sync artifact inverse links. Any table with >20 inverse link fields warrants inspection.

**What happens:** Each sync connection creates inverse link fields on the source table. If syncs are recreated during development, old inverses persist as live bidirectional relationships. Every record edit triggers relationship checks across all of them — including stale ones nobody is using.

**Mitigations:**
- Maintain a sync registry — document every sync connection with source base, target base, synced fields, and creation date
- Sync only the specific fields the target base actually needs (not full tables)
- Audit and delete stale inverse links before go-live (verify no formulas/lookups depend on them first)
- Avoid automations on synced record changes in target bases — use scheduled polling instead

---

### Risk 8: Configuration/Template Table Bottleneck

**Design-time flag:** A table intended as a "template" or "configuration" hub has a very high number of link fields (>50 planned), and many entity tables are planned to look up from it.

**Inspection flag:** Any table with >150 link fields that functions as a hub referenced by multiple entity tables via lookups.

**What happens:** The configuration table is the source of truth feeding values to multiple entity tables via lookups. Any edit to a configuration record triggers recalculation cascades across every table that looks up from it. If configurations are edited frequently or during peak usage, the cascade amplifies across the full entity hierarchy.

**Mitigations:**
- Treat configuration tables as read-mostly (edit during off-hours)
- Minimize live lookups from configuration tables — write values once via automation instead
- Document which tables depend on which configuration fields so the blast radius of any edit is understood

---

## Linking Strategy Framework

For every linked record relationship in a design, evaluate it against these five patterns and apply the most appropriate one. The goal is to match the linking strategy to the actual use case — **not to default to linked records everywhere.**

---

### Pattern 1: Collaborator Field

**Use when:** The linked entity is an Airtable user, and the primary use is notification, @mention, interface filtering ("show me my records"), or permission scoping.

**Why it matters:** No inverse link is created — zero fan-out cost. Native Airtable identity system handles notifications without automation.

**Limit:** Only works for actual Airtable users. Cannot store rich metadata, external stakeholders, or non-user People records.

**Ideal for:** Task assignment, record ownership, notification routing, filtering interfaces to current user.

---

### Pattern 2: Linked Record (Pure)

**Use when:** The relationship is analytical or structural — you need rollups, lookups, or aggregate views across the link. The linked table has rich metadata that needs to stay live (not cached). Cardinality is bounded (the hub record will never accumulate thousands of entity records linking to it).

**Avoid when:** The table is a high-volume hub (thousands of entities linking to a small set of reference records). Fan-out cost accumulates silently over time.

---

### Pattern 3: Hybrid (Collaborator + Linked Record)

**Use when:** You need both operational speed (native notifications, @mentions, interface filtering) AND analytical depth (rollups, team-level reporting, rich People metadata).

**How it works:** Two fields serve different purposes on the same record:
- `Assigned To [Collaborator]` — operational field, native Airtable identity, zero fan-out
- `Assignee Record [Link → People]` — analytical field, used for reporting, team rollups, rich metadata

**Trade-off:** Two fields to maintain. Drift risk if one updates without the other. Requires a sync automation to keep them aligned.

**Sync automation (required):** The Collaborator field is the source of truth (users set it via interface). An automation watches the Collaborator field and updates the Linked Record field to match. The implementation depends on the collaborator field type:
- **Single collaborator** → Find Records (match email on People table) → Repeating Group → Update Record. Three steps, no code. This is the default.
- **Multi-collaborator** → Script action. The token picker cannot expand multi-collaborator fields ("No valid nested options"), so a Script reads the collaborator array via `getCellValue()` and matches against the People table programmatically.

See the Collaborator Sync pattern in `automation-architect/SKILL.md` for full automation specs.

**This is the right pattern when:** Assignment needs to appear in Airtable notifications AND you need team-level reporting (records per person/team).

---

### Pattern 4: Flat Field (Automation-Written Cache)

**Use when:** A linked record is used only for display (showing a name, email, or status) and the linked table is a hub with high fan-out potential. Replace the link with an automation-written text field that stores the display value. Zero inverse link. No cascade.

**Trade-off:** Two-source-of-truth risk if the source record changes. Acceptable when the source data rarely changes (reference tables, People profiles, configuration values).

**This is the right pattern when:** Linking to a hub record only to show one or two fields (e.g., "Vendor Name", "Policy Version") with no rollups or aggregations needed from that link.

---

### Pattern 5: Display-Only Link → Candidate for Flattening

**Flag for review:** Any linked record field where the only usage is looking up 1–2 display fields on the linked record, with no rollups or aggregations pointing back. These are candidates to convert to Pattern 4 if performance becomes a concern at scale.

---

## Automation Design Patterns

### AI Step Design

- **Use automation AI actions, not AI fields, for deterministic one-time processing.** AI fields recalculate whenever their trigger condition is met (every time the record is opened or a dependency changes). Automation AI actions run exactly once on trigger. For contract review, data extraction, or classification — always use automation AI actions.
- **Always use structured output (JSON schema) for AI steps.** Free-text AI output requires brittle parsing logic. Structured output maps each value directly to a specific Airtable field.
- **Separate AI steps by concern when possible.** A single AI step producing 8+ outputs is elegant but fragile — if the prompt is too long, the model underperforms on specific outputs. Consider splitting: one step for classification (risk verdict, score, recommended action) and one for extraction (compliance gaps, key dates, summary). Trade-off: doubles API calls and automation steps.
- **Always include a confidence score output.** The confidence score is the human override signal — low-confidence outputs should surface a flag for human review rather than routing automatically.
- **Add error handling awareness.** Automation AI steps can fail (API timeout, empty input, malformed source). Design a fallback: an `AI Run Status` field updated at the start (`Processing`) and end (`Complete` / `Failed`) so failures are visible.

---

### AI Credit Budget and Model Cost

AI credits are pooled monthly across all users in a workspace (Free/Team) or organization (Business/Enterprise). Every AI action — fields, automations, agents — draws from this shared pool. Credit cost per action scales with input volume, model power, and output volume.

**Plan allocations:**
- Free: 500 credits/user/month (Editor+). Cannot purchase more — must upgrade.
- Team: 10,000 credits/user/month. Credit packs available for overages.
- Business / Enterprise Scale: Contact Sales for allocation and overage pricing.

Credits expire monthly — no rollover. This makes credit budget a design constraint, not just a billing concern.

**Design implications:**
- **Default to "Low cost" tagged models for bulk AI operations.** Categorization, summarization, sentiment analysis, and tagging across large tables should use low-cost models unless accuracy testing proves they can't handle the task. Reserve higher-powered models for multi-step reasoning, internet search, and complex tool-calling.
- **Gate AI field auto-run on large tables.** Auto-run AI fields can exhaust credits mid-run, leaving some records unprocessed with no error. Confirm credit headroom before enabling auto-run, and design automation triggers to be as selective as possible.
- **Low-powered models cannot handle complex tool-calling.** Using a low-cost model with Field Agents that use internet search or multi-step tool calls causes errors ("Unknown error while using tools with the agent"). These tasks require higher-powered models.
- **Prompt language matters for lower-tier models.** Use direct imperative instructions rather than conditional phrasing when using low-cost models — they handle "Classify this as X, Y, or Z" better than "If the content seems to be about X, then consider..."
- **Internet access multiplies cost.** When internet access is enabled on a Field Agent, the text pulled from the web is also charged as credits on top of the base prompt cost. Flag this during scoping.
- **Estimate and communicate credit burn during discovery.** For each AI feature, estimate volume × model tier and flag high-consumption scenarios (document analysis at 500–1,500 credits per large doc, internet search agents) as explicit budget line items for the client.

**Word limits by model tier:**
- Lower-powered models: ~12,000 words (query + response combined)
- Higher-powered models: ~90,000 words (query + response combined)
- 64,000 character prompt limit applies regardless of model
- Responses exceeding the model's word limit are silently truncated — not errored

**Admin model restrictions (Enterprise):**
- Enterprise admins can restrict which AI platforms/providers are available org-wide.
- Omni requires OpenAI and/or Anthropic (Amazon Bedrock) to be enabled — it will not function if only Gemini, Meta, IBM, or Amazon Titan/Nova are allowed.
- Confirm enabled providers with the client admin before designing any AI features.

---

### State Machine Design (Status Fields)

- Design Status fields as explicit state machines with defined transitions. Document which transitions are human-driven vs. system-driven.
- Not all transitions should be manually editable. Use automation-enforced transitions for system-driven states (e.g., "AI Processing" should only be set by the automation, not a user).
- Automation triggers should watch for a **specific state transition** (Status changes TO "Pending Review"), not a general field-change watch. This prevents spurious triggers.

---

### Human-in-the-Loop Gates

- For high-stakes AI decisions (legal hold designation, escalation to external parties, irreversible actions), insert a human confirmation step rather than routing fully automatically.
- Pattern: AI sets a "Recommended Action" field → human confirms or overrides → a separate trigger fires on confirmation to execute the routing.
- This is not a performance concern — it is a **defensibility concern**. The AI's judgment should inform the decision, not make it unilaterally for high-stakes outcomes.

---

### Audit Trail Fields

For any AI-processing workflow, always include:

- `AI Processed At` — timestamp of when the AI step ran. (Created Time is insufficient — records may be created before AI processing begins.)
- `Reference Version Used` — linked record to the specific version of the reference data the AI used. Answers "what rules governed this decision?" months later.
- `AI Recommended [Field]` — separate from the human-editable `[Field]` so the AI's original recommendation is preserved even if a human overrides it.

---

### Script Action Escape Hatches

Script actions (`Run a script`) bypass the automation token picker entirely by accessing field values through the scripting API. This makes them the escape hatch when the standard automation builder can't provide the data path you need.

**When to reach for a Script action:**
- **Multi-collaborator field expansion** — token picker shows "No valid nested options." Script reads the array via `getCellValue()` and iterates programmatically.
- **Linked record field expansion** — same token picker limitation. Script queries the linked table directly via `selectRecordsAsync()`.
- **Find Records by Record ID** — not possible in the conditions UI. Script finds by ID natively.
- **Complex conditional logic** — when nested conditionals would exceed 3-4 levels of depth, a single Script can replace the entire branch tree with readable `if/else` logic.
- **Batch operations exceeding Find Records' 1,000 limit** — Script can paginate through all records.
- **Multiple table queries in one step** — Script can query 2-3 tables and correlate results, replacing a chain of Find Records + Conditional + Find Records steps.

**Script action constraints:**
- 30-second execution timeout
- `input.config()` requires explicit variable mapping via "+ Add property" in the UI — names are case-sensitive
- `selectRecordsAsync()` with a `fields` parameter can silently fail if a field name doesn't match exactly — omit `fields` for reliability when querying source tables
- Uncaught errors fail silently — always wrap in try/catch
- No `output.set()` means no downstream tokens — if the script needs to pass data forward, declare output variables explicitly

**Design principle:** Prefer the standard automation builder (Find Records, Conditionals, Repeating Groups) when the token picker provides the data you need. Reach for Script actions when the token picker hits a wall. This keeps automations maintainable for non-developers while giving you an escape hatch for platform limitations.

---

## Naming Conventions

### AI-Generated Fields
Prefix with `AI ` (e.g., `AI Risk Verdict`, `AI Confidence Score`, `AI Executive Summary`). Signals to users that the field is system-generated and should not be manually edited. Human-editable counterparts should be clearly differentiated (e.g., `Risk Verdict [Confirmed]`).

### Automation-Written Cache Fields
Suffix with `[Cache]` or `[Cached]` to signal the field is system-maintained and should not be manually edited (e.g., `Vendor Name [Cache]`, `Policy Version [Cached]`).

### Status Fields (State Machines)
Use unambiguous present-state language, not action language:
- ✅ `Pending Review`, `In Processing`, `Complete`, `Failed`
- ❌ `Submit`, `Process`, `Click to Complete`

Include a transitional state for automation-driven transitions (e.g., `Processing...`) so agents can see that work is in progress.

### Hub / Reference Tables
Name hub tables as pluralized nouns describing the reference entity (e.g., `Airports`, `Vendors`, `Policy Library`, `Configurations`). This signals that these are lookup targets, not operational tables, and makes fan-out risk more recognizable during design review.
