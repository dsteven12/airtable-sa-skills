---
name: solution-hub
description: "Populate an Airtable Solution Hub base from engagement transcripts, meeting notes, SOWs, or architecture docs. Extracts structured records across 10 areas (Project, People, Timeline, Definitions, PBOs, Risks, Decisions, User Personas, Updates, Action Items), presents for review, then writes via MCP. MANDATORY TRIGGERS: solution hub, populate solution hub, populate the hub, extract from transcript, hub population, fill in the solution hub, update the solution hub, add to solution hub, sync to hub, log this call, process this transcript. ALWAYS invoke when the user provides a transcript, notes, SOW, or engagement input and wants extracted data written to a Solution Hub base — even if they just say 'here's the transcript' or 'log this to the hub'. Also invoke to review or update existing Hub records from new information. Do NOT invoke for schema design (airtable-design-advisor) or workflow documents (workflow-doc)."
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

## Process Overview

The workflow has four phases. Never skip the Review phase — the SA must approve all records before they're written.

```
Discover → Extract → Review → Write
```

### Phase 0: Discover the Base

1. **Identify the base.** The user may provide a base ID, base name, or project name. Use `search_bases` to find it. If ambiguous, ask.
2. **Fetch all table schemas.** Call `list_tables_for_base`, then `get_table_schema` for each of the 10 core tables. Cache the results — you'll need field IDs, singleSelect options, and linked record table IDs throughout.
3. **Scan for existing records.** For each core table, call `list_records_for_table` filtered to the current project. This is your dedup baseline.

The 10 core tables (names may vary slightly across template versions):
- Project
- People
- Timeline (Tasks, Milestones & Meetings)
- Definitions
- Positive Business Outcomes
- Risks & Change Impacts
- Decisions
- User personas
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
3. **All other tables** — use batch creates (up to 10 records per `create_records_for_table` call)

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
