---
name: solution-hub
description: "Populate an Airtable Solution Hub base from engagement transcripts, meeting notes, SOWs, or architecture docs. Extracts structured records across 11 areas (Project, People, Timeline, Definitions, PBOs, Risks, Decisions, User Personas, Meetings, Updates, Action Items), reviews with the SA, then writes via MCP. For transcript/meeting-notes inputs, ALWAYS creates BOTH a Meeting record (rich Notes + transcript + Gong link + linked attendees) AND an Update record (status, type, notes) — never skipped. TRIGGERS: solution hub, populate solution hub, extract from transcript, hub population, update the solution hub, log this call, process this transcript, sync to hub. Invoke when the user provides a transcript, notes, SOW, or engagement input and wants extracted data written to a Solution Hub base — even if they just say 'here's the transcript' or 'log this call'. Also for incremental updates of existing Hub records. Do NOT invoke for schema design (airtable-design-advisor) or workflow documents (workflow-doc)."
---

# Solution Hub Population

Extract structured engagement data from transcripts, meeting notes, SOWs, and architecture documents, then write it to an Airtable Solution Hub base via MCP.

## Why This Skill Exists

Solution Hubs are the single source of truth for Airtable SA engagements. They track everything from project scope to user personas across 10 interconnected areas. Populating them manually is tedious and error-prone — you're reading through hour-long transcripts, translating conversational language into structured records, and keeping field formats consistent across dozens of singleSelect options and linked records.

This skill automates the extraction and writing while keeping the SA in the loop. Every extracted record is presented for review before anything touches Airtable.

## Prerequisites

**Required MCP tools** (Airtable connector):
- `list_bases` / `search_bases` — find the Solution Hub base
- `list_tables_for_base` — discover table IDs
- `get_table_schema` — fetch field IDs and singleSelect options
- `list_records_for_table` — scan for existing records (dedup)
- `create_records_for_table` — batch create (up to 10 per call)
- `update_records_for_table` — update existing records

## Mandatory Outputs (Transcript / Meeting-Notes Inputs)

When the input is a call transcript, meeting notes, sync recap, or any time-stamped engagement input, **every run MUST produce both** of the following — this is non-negotiable:

1. **A Meeting record** in the Meetings table with:
   - The Gong/recording link (Call Link – Customer facing)
   - The full transcript pasted into the Call transcript field
   - A custom meeting name following the `Topic 1 | Topic 2 | Topic 3` convention
   - Linked attendees (including the SA — see People extraction rules)
   - Linked Build/Project record
   - **A rich Notes field** that summarizes what was covered, key issues addressed and resolutions, learnings reinforced, and explicit next steps. The Notes field is the human-readable record of the call — do NOT leave it sparse or skip it. Treat it as the deliverable a teammate would read instead of re-watching the call.

2. **An Update record** in the Updates table with:
   - Status (🟢 / 🟡 / 🔴 — match the prior update's trajectory unless something changed)
   - Update type = "Project Update" (default for sync/working sessions)
   - Created Date matching the meeting date
   - Linked Build/Project record
   - **A rich Notes field** that mirrors the Meeting Notes but condensed for stakeholder/leadership consumption — lead with adoption/sentiment when relevant, then key resolutions, then next steps.

**Why both:** The Meeting record is the working artifact for the project team (full context, transcript, attendees). The Update record is the leadership/exec-facing rollup that flows into status reports and dashboards. Skipping either one breaks downstream consumers — the SA loses traceability and the AE/CSM/leadership lose the status feed.

If a transcript is provided and you only create one of these, you have not completed the task. Always create both before reporting completion.

For non-transcript inputs (SOW, architecture doc, requirements doc), the Meeting record is not required, but an Update record is still encouraged when the input represents a meaningful engagement event.

## Process Overview

The workflow has five phases. Never skip the Review phase — the SA must approve all records before they're written.

```
Discover → Collect Missing Info → Extract → Review → Write
```

### Phase 0.5: Collect Missing Meeting Information

**Before extracting records**, check whether the user has provided everything needed for a complete Meeting record. If any of the following are missing, prompt the user before proceeding:

1. **Call Link (Gong link)** — The URL to the call recording (e.g., Gong, Zoom, or other recording platform). This populates the "Call Link - Customer facing" field on the Meetings table.
2. **Call Transcript** — The full transcript text. If the user provided a transcript inline, use it. If they only provided notes or a summary, ask if they have the raw transcript available. This populates the "Call transcript" field.
3. **Custom Meeting Name** — A short, focused name highlighting the 2-4 key areas emphasized during the call. This drives the auto-generated meeting Name formula. Examples: "Automation Validation & Deep Dive | Interface Consolidation Strategy | Cutover Planning & Re-migration". Ask the user what the main focus areas were, or suggest them based on the transcript content.

**Prompt format:**
> Before I extract records, I want to make sure the Meeting record is complete. Can you provide:
> - **Gong/call recording link** (if available)
> - **Full transcript** (if not already provided)
> - **Key focus areas** for the custom meeting name (or I can suggest based on the transcript)

If the user says they don't have one of these, proceed without it — but always ask first.

### Phase 0: Discover the Base

1. **Identify the base.** The user may provide a base ID, base name, or project name. Use `search_bases` to find it. If ambiguous, ask.
2. **Fetch all table schemas.** Call `list_tables_for_base`, then `get_table_schema` for each of the 10 core tables. Cache the results — you'll need field IDs, singleSelect options, and linked record table IDs throughout.
3. **Scan for existing records.** For each core table, call `list_records_for_table` filtered to the current project. This is your dedup baseline.

The 11 core tables (names may vary slightly across template versions):
- Project (sometimes "Builds")
- People
- Timeline (Tasks, Milestones)
- Definitions
- Positive Business Outcomes
- Risks & Change Impacts
- Decisions
- User personas
- Meetings
- Updates
- Action items

Match tables by name pattern, not hardcoded IDs — each base instance has different IDs.

### Phase 1: Extract Records

Read the user's input (transcript, notes, SOW, etc.) and extract structured records for each relevant area. Not every input will have data for all 10 areas — that's fine. Extract what's there.

**Before reading the detailed extraction rules**, read `references/schema-patterns.md` in this skill's directory. It contains the per-table field mappings, format rules, and extraction heuristics learned from real population sessions.

**General extraction principles:**

- **Transcripts** are conversational — translate discussion into structured fields. A client saying "we really need to get off spreadsheets before Q3" becomes a PBO record, a timeline milestone, and possibly a risk.
- **Meeting notes** are already semi-structured — map bullet points to the right tables.
- **SOWs and docs** contain formal scope, timeline, and deliverable definitions — these map cleanly to Project, Timeline, and PBO records.
- **When the same topic appears in multiple inputs**, most recent wins for the primary field values. Earlier mentions provide context for Notes fields.
- **Extract conservatively.** If you're unsure whether something warrants its own record, flag it in the review phase rather than creating a marginal record.

**People extraction — don't forget the SA:**
Always include the SA (yourself / the Airtable team member running this session) as a People record if they're not already in the base. The SA is a project team member too. Also include the CSM if mentioned. This is easy to overlook because you're focused on the client's team — but the Solution Hub tracks the full project team, not just the customer side.

**Definitions — be aggressive with external systems and domain terms:**
Any named system, tool, platform, data concept, or architecture pattern mentioned in the input should become a Definition record. If a client mentions "BrewTrack" or "PartTracker" or "Salesforce" in the context of the project, that's a Definition — even if it's a well-known system. The Definition captures what the system means *in this project's context* (how it connects, what data it holds, why it matters). Err on the side of creating too many Definitions rather than too few — they're cheap to create and valuable for onboarding new team members.

**Extraction order matters for linked records:**
1. Project (update the single project record)
2. People (need record IDs before assigning Owners elsewhere — include the SA and CSM)
3. Everything else (Timeline, Definitions, PBOs, Risks, Decisions, User Personas, Updates, Action Items)

### Phase 2: Review

Present all extracted records to the user, organized by table. For each record, show:
- The table it belongs to
- All field values (with field names, not IDs)
- Whether it's a CREATE or UPDATE (and if UPDATE, what changed)
- Any flags or uncertainties (e.g., "couldn't determine priority — defaulted to Medium")

**Format for review:**

```
## [Table Name] — [N] records

### [Record Name] (CREATE)
- Field A: value
- Field B: value
- ⚠️ Flag: [uncertainty or question]

### [Existing Record Name] (UPDATE — changed: Field X, Field Y)
- Field X: old value → new value
- Field Y: old value → new value
```

Wait for the user to approve, modify, or reject records. Apply their changes before proceeding.

If the user wants to skip review for a specific table (e.g., "definitions look good, just write them"), that's fine — but always present the full extraction first.

### Phase 3: Write to Airtable

After approval, write records in this order:
1. **Project** — update the existing record
2. **People** — create new people, note their record IDs
3. **Meeting record** — create FIRST among non-people records so its record ID is available for Action Item linking. Required when input is a transcript or meeting notes.
4. **Update record** — required when input is a transcript or meeting notes. Use the Meeting record ID is not needed here, but the Build link is.
5. **All other tables** (Action Items, Timeline, Definitions, PBOs, Risks, Decisions, User Personas) — use batch creates (up to 10 records per `create_records_for_table` call). Action Items should link to the Meeting record created in step 3.

**Completion check before reporting done:** Verify both the Meeting record AND the Update record were created if a transcript or meeting notes were the input. If either is missing, fix it before declaring completion. A summary table of records created per table makes the missing-record case obvious — always include this in the completion report.

**Critical format rules** (the Airtable MCP is strict about these):
- **multipleRecordLinks**: Plain string arrays → `["recXXX"]`, NOT `[{"id": "recXXX"}]`
- **singleSelect**: Plain string → `"Align"`, NOT `{"name": "Align"}`
- **multipleSelects**: Array of plain strings → `["Tag1", "Tag2"]`
- **date fields**: `"YYYY-MM-DD"` format
- **richText**: Accepts markdown formatting
- **Formula/lookup/rollup fields**: Read-only — never include in create/update payloads

**Validate singleSelect values** against the schema before writing. If an extracted value doesn't match any existing option, flag it during review rather than creating a 422 error at write time.

**Link all records to the Project** via the project's multipleRecordLinks field in each table.

After writing, report the results: how many records were created/updated per table, and any errors encountered.

## Handling Incremental Updates

The skill handles both initial population (empty hub) and incremental updates (new transcript for an existing project). The dedup scan in Phase 0 is what makes this work.

**Dedup strategies per table:**
- **People**: Match by name (case-insensitive). Don't create duplicates of existing team members.
- **Timeline**: Match by milestone/phase name within the project. Update dates if they've changed.
- **Definitions**: Match by term name. Update definition text if it's evolved.
- **Decisions**: Don't dedup — decisions evolve. A "Proposed Decision" from call 1 may become a "Final Decision Accepted" in call 2. Create a new record for the final decision and link or note the evolution.
- **Action Items**: Match by description similarity. Update status if the action was discussed again.
- **Everything else**: Create new records unless there's an obvious exact match.

## Input Types and What to Extract

| Input Type | Best For | Example Signals |
|---|---|---|
| Scoping/Discovery transcript | Definitions, Decisions, Risks, PBOs | Domain terms, architecture choices, unknowns |
| Kickoff transcript | People, Timeline, Action Items, Updates | Attendee intros, confirmed dates, next steps |
| Sync/Status call | Updates, Decisions, Action Items, Timeline adjustments | Progress reports, blockers, trade-off resolutions |
| SOW / Proposal | Project, Timeline, PBOs | Formal scope, hours, deliverables, business case |
| Architecture doc | Definitions, Decisions, Risks | System names, design choices, integration risks |
| Requirements doc | User Personas, PBOs, Definitions | User roles, acceptance criteria, domain terms |

## Error Recovery

If a write fails (422, 500, etc.):
1. Report the specific error and which record caused it
2. Most common cause: singleSelect value not in the option list. Fix by checking the schema and using an existing option.
3. Second most common: multipleRecordLinks format wrong. Always use `["recXXX"]` string arrays.
4. Don't retry automatically — let the user decide whether to fix and retry or skip.
