# Solution Hub Schema Patterns

Per-table extraction rules, field mappings, and heuristics. Read this before extracting records.

These patterns were discovered during real population sessions and encode the schema nuances that differ from what you'd guess from field names alone.

---

## Table of Contents

1. [Project](#project)
2. [People](#people)
3. [Timeline](#timeline)
4. [Definitions](#definitions)
5. [Positive Business Outcomes](#positive-business-outcomes)
6. [Risks & Change Impacts](#risks--change-impacts)
7. [Decisions](#decisions)
8. [User Personas](#user-personas)
9. [Updates](#updates)
10. [Action Items](#action-items)

---

## Project

**Operation**: Always UPDATE the existing single project record — never create a new one.

**Key fields to populate:**
- `Problem Statement` (richText) — The pain the customer is trying to solve. Frame as a narrative: current state → impact → urgency.
- `Why Change Now` (richText) — The forcing function. What makes this quarter different from last quarter?
- `Why Airtable` (richText) — Why Airtable over alternatives. Platform-specific advantages.
- `Vision Statement` (richText) — The aspirational end state in the customer's words.
- `Measure of Success (KPIs)` (richText) — Bulleted list of measurable outcomes.
- `Current Phase` (singleSelect) — Options: Align, Design, Build, Deploy, Adopt
- `Build Package` (singleSelect) — Options: Standard, Scaled, Custom, Retainer
- `Target Kick-off`, `Target Go Live`, `Target Completion` (date fields)
- Hours fields (number) — Total Hours Purchased, Hours Used, etc.

**Extraction heuristic**: Problem Statement and Why Change Now often come from early scoping calls where the customer describes their current pain. Vision Statement emerges from kickoff discussions about the desired future. KPIs may be explicit ("we want to reduce turnaround by 50%") or implicit (translate business goals into measurable terms).

---

## People

**Operation**: CREATE new records; UPDATE if person already exists (dedup by name).

**Key fields:**
- `Name` (singleLineText) — Full name
- `Title` (singleLineText) — Job title
- `Email` (email) — If mentioned
- `Team` (singleSelect) — "Airtable" or "Client" (or other options per base)
- `Engagement Role` (singleLineText) — Their role on this specific project (e.g., "Executive Sponsor", "Primary Contact", "SA")
- Link to Project (multipleRecordLinks)

**Extraction heuristic**: In transcripts, people introduce themselves or are introduced. Look for patterns like "I'm [Name], I handle [role]" or "[Name] from [team] who manages [area]". In SOWs, look for the stakeholder/contact section.

**Don't forget the Airtable team**: The SA running this session and the CSM assigned to the project are People too. If you're extracting from a kickoff transcript where 6 people attended, you need 6 People records — including the SA and CSM. This is the most commonly missed extraction.

**Dedup**: Always scan existing People records before creating. Match by name (case-insensitive, trim whitespace). If a person exists but their role has changed, update the role field.

---

## Timeline

**Operation**: CREATE new records. UPDATE existing milestones/phases if dates have shifted.

**Key fields:**
- `Name` (singleLineText) — Phase or milestone name (e.g., "Design Phase", "Go-Live", "Code Freeze")
- `Activity Type` (singleSelect) — "Task" for phases (have duration), "Milestone" for point-in-time events
- `Start Date` (date) — Phases get start dates; milestones do NOT
- `End Date` (date) — Both phases and milestones get end dates
- `Phase` (singleSelect) — Align, Design, Build, Deploy, Adopt
- `Status` (singleSelect) — Not Started, In Progress, Complete, At Risk, Blocked
- Link to Project (multipleRecordLinks)
- `Owner` (multipleRecordLinks to People) — If an owner was mentioned

**Phase vs. Milestone distinction**:
- **Phase** = Activity Type "Task", has Start Date AND End Date. Examples: "Align Phase", "Design Phase", "Build Phase", "Deploy Phase", "Adopt Phase"
- **Milestone** = End Date ONLY (no Start Date). Examples: "Go-Live", "Code Freeze", "UAT Start", "Sign-off Deadline"

**Timeline calculation heuristics**:
- Code Freeze should be ~2 weeks before Go-Live (not 1 week)
- Design and Build should be separate phase records, not combined
- If only a Go-Live date is given, work backwards: Build ends at Code Freeze (Go-Live minus 2 weeks), Design ends where Build starts, etc.
- Meeting cadence records (e.g., "Weekly Syncs") can be timeline entries too

---

## Definitions

**Operation**: CREATE. Dedup by term name.

**Key fields:**
- `Name` (singleLineText) — The term being defined
- `Definition` (richText) — What it means in this project's context
- Link to Project (multipleRecordLinks) — via "Related to" or similar field

**What to extract:**
- **Legacy/external systems** (e.g., "BrewTrack", "PartTracker", "Salesforce", "HyperDB") — define what the system is, what data it holds, and how it connects to the project. Even well-known systems like Salesforce get a Definition because the entry captures what Salesforce means *in this project's context* (which objects, which integration pattern, which data flows).
- **Architecture patterns** (e.g., "EMA", "Development Base", "Schema Holder") — define the pattern and why it was chosen
- **Data concepts** (e.g., "Merch Hierarchy", "Item Master", "Shot List", "BOM") — define the domain meaning
- **Modeling decisions** (e.g., "Option A") — define what the option means
- **Process/workflow terms** (e.g., "Seasonal Brew Calendar", "QC Checkpoint", "Compliance Checklist") — define what the process is and who owns it

**Extraction heuristic**: Be aggressive. If a term is mentioned more than once and would be confusing to a new team member joining the project, it's a Definition. Err on the side of creating more Definitions — they're cheap records and extremely valuable for context. A scoping call for a brewery project might yield 6-8 Definitions; a SOW for a financial services project might yield 5-7.

---

## Positive Business Outcomes

**Operation**: CREATE.

**Key fields:**
- `Name` (singleLineText) — Short outcome label
- `Description` (richText) — Detailed explanation of the business impact
- Link to Project (multipleRecordLinks)
- `Timeline` (multipleRecordLinks to Timeline) — When this outcome is expected
- `Quantified Benefit` (singleLineText) — If a number was mentioned ("save 20 hours/week")

**Extraction heuristic**: PBOs come from the "why" conversations. When a client says "right now it takes us 3 days to do X" or "we lose track of Y," that's a PBO waiting to be framed positively: "Reduce X turnaround from 3 days to same-day" or "Single source of truth for Y."

Frame as measurable business outcomes, not technical deliverables. "Build a dashboard" is not a PBO. "Real-time visibility into production status, eliminating daily status email chains" is.

---

## Risks & Change Impacts

**Operation**: CREATE.

**Key fields:**
- `Name` (singleLineText) — Short risk or change label
- `Type` (singleSelect) — "Risk" or "Change Impact"
- `Category` (singleSelect) — Technical, User Adoption & Training, Resource, Project Management
- `Description` (richText) — Full description
- `Current State` (richText) — How things work today
- `Future State` (richText) — How things will work after the change
- `Implications` (richText) — What could go wrong (risks) or what changes for users (change impacts)
- `Mitigation Plan` (richText) — How to address it
- `Magnitude/Complexity` (singleSelect) — "1", "2", or "3" (string values, not integers)
- `Probability/Impact` (singleSelect) — Low, Medium, High
- `Status` (singleSelect) — Proposed, Active, Resolved
- Link to Project (multipleRecordLinks)

**Risk vs. Change Impact distinction:**
- **Risk** = uncertain event that might happen. "HyperDB API may have rate limits we haven't tested." Category skews Technical or Project Management.
- **Change Impact** = known change that WILL happen. "Users will switch from spreadsheets to Airtable for photo scheduling." Category skews User Adoption & Training.

**Extraction heuristic**: Risks surface as concerns, unknowns, and "what if" statements. Change Impacts surface as descriptions of workflow changes: "currently they do X, in the new system they'll do Y."

---

## Decisions

**Operation**: CREATE. Decisions evolve across calls — don't dedup, capture the journey.

**Key fields:**
- `Name` (singleLineText) — Short decision label
- `Decision Context` (richText) — Background: what prompted this decision
- `Proposed Decision` (richText) — What was suggested (may differ from final)
- `Final Decision` (richText) — What was agreed upon
- `Status` (singleSelect) — "Proposed Decision" or "Final Decision Accepted"
- `Notes` (richText) — Context: when discussed, who pushed for what, rationale
- `Is this a Sign-off Decision?` (checkbox) — Yes for decisions requiring formal client approval
- `Is this related to a Design Principle/Best Practice?` (checkbox) — Yes for architecture-relevant decisions
- `Are there exceptions?` (checkbox)
- Link to Project (multipleRecordLinks)

**Extraction heuristic**: Decisions emerge when someone says "let's go with X" or "we decided to..." or when two options are discussed and one is chosen. A decision from an early call may be "Proposed" and get elevated to "Final Decision Accepted" in a later call — create separate records for each stage.

---

## User Personas

**Operation**: CREATE.

**Key fields:**
- `Role (As a...)` (singleLineText) — The persona's role title (e.g., "Photo Coordinator", "Brand Director")
- `Description` (richText) — What this persona does in the context of the project
- `I want to (Acceptance Criteria)` (richText) — Bulleted list of what this persona needs from the system
- `Persona Type` (singleSelect) — Usually "End User"
- `Interface Permission Level` (singleSelect) — Read Only, Comment Only, Editor, Creator
- `Base Permission Level` (singleSelect) — Creator, Editor, Viewer/Comment, None
- `Work Pattern` (multipleSelects) — Intake & submit, Review & triage, Monitor & analyze, Optimize & schedule, Update & entry, Store & search
- Link to Project (multipleRecordLinks)

**Permission heuristics:**
- For EMA (Enterprise Managed App) projects, Base Permission Level is typically "None" — users interact through interfaces only
- Interface Permission Level depends on the persona's role: data entry roles get "Editor" or "Creator", oversight roles get "Read Only" or "Comment Only"
- Work Patterns should reflect actual workflows: someone who submits requests gets "Intake & submit", someone who approves them gets "Review & triage"

**Extraction heuristic**: Personas emerge from discussions about "who uses this" and "what do they need to do." In transcripts, look for role descriptions, permission discussions, and workflow walkthroughs that reveal distinct user types.

---

## Updates

**Operation**: CREATE. Unlikely to duplicate (date-stamped).

**Key fields:**
- `Name` — Often auto-generated by formula. May not need to be set; check schema.
- `Status` (singleSelect) — Options use emoji: "🟢 On track", "🟡 At risk", "🔴 Off track"
- `Update type` (singleSelect) — "Project Update" or "Email"
- `Notes` (richText) — Detailed update content
- `Update` (multilineText) — Brief summary
- `Created Date` (date) — The date of the update (not the same as Airtable's auto-created timestamp)
- Link to Project (multipleRecordLinks)

**Extraction heuristic**: Create one update record per significant event: kickoff completion, major milestone reached, status change, blocker encountered. Sync calls where "everything is on track" may not warrant a new record unless there's something notable to capture.

---

## Action Items

**Operation**: CREATE. Dedup by description similarity for follow-up updates.

**Key fields:**
- `Name` (singleLineText) — Brief action item description
- `Type` (singleSelect) — "Question for Airtable", "Action item for Airtable", "Question for Client", "Action item for Client"
- `Priority` (singleSelect) — Urgent, Higher, Medium, Low, Optional
- `Status` (singleSelect) — New, In progress, Pending Airtable, Pending Client, Solved, Stuck
- `Notes` (richText) — Why this matters, not just what needs to happen
- `Due` (date) — Realistic date based on project timeline
- `Assigned to` (multipleRecordLinks to People) — Who owns this
- `Created By` (multipleRecordLinks to People) — Who raised it
- Link to Project (multipleRecordLinks)

**Type heuristic:**
- "Question for Airtable" — SA needs to research or answer something internally
- "Action item for Airtable" — SA has a deliverable to produce
- "Question for Client" — Need information from the customer
- "Action item for Client" — Customer has a task (e.g., "share CSV exports", "set up access")

**Status heuristic:**
- Items that block the SA pending client input → "Pending Client"
- Items the SA needs to do → "New" or "In progress"
- Items discussed and resolved in the same call → "Solved"

**Notes should explain WHY**, not just WHAT. "Need HyperDB API documentation" is weak. "Need HyperDB API docs to validate rate limits before designing the sync automation — if rate limits are too low, we'll need a queuing layer" is strong.
