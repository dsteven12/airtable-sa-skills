---
name: review
description: "Generate a structured review of work done over a given time period by sweeping connected sources (Slack, Gmail, Google Calendar, Airtable, Obsidian vault) and producing a markdown note in the Work Brain vault. Supports daily, weekly, monthly, quarterly, and yearly cadences. Use when the user asks to look back at or summarize work — phrases like 'daily review', 'weekly review', 'what did I do today', 'what did I accomplish', 'recap my week', 'summarize my day', 'EOD review'. Do NOT use for ending the current session — that is session-wrapup."
---

# Review Skill

Generate structured reviews of the user's work at five cadences (daily → yearly), pulling from all connected sources and writing to the Obsidian vault at `06 - Reviews/`.

## Cadence Detection

Determine the cadence from the user's request or scheduled task parameters:

| Trigger | Cadence | Time Range | Output Path |
|---------|---------|------------|-------------|
| "daily review", "what did I do today", "EOD review" | daily | Today | `06 - Reviews/daily/YYYY-MM-DD.md` |
| "weekly review", "summarize my week" | weekly | Current week (Mon–Sun) | `06 - Reviews/weekly/YYYY-WNN.md` |
| "monthly review", "monthly recap" | monthly | Current month | `06 - Reviews/monthly/YYYY-MM.md` |
| "quarterly review", "Q1/Q2/Q3/Q4 review" | quarterly | Current quarter | `06 - Reviews/quarterly/YYYY-QN.md` |
| "yearly review", "annual review", "performance review" | yearly | Current year | `06 - Reviews/yearly/YYYY.md` |

If ambiguous, default to **daily**. If the user specifies a past period (e.g., "review last week"), adjust the date range accordingly.

## Source Sweep Protocol

For each review, gather data from all available sources within the time range. The sources and what to extract from each:

### 1. Google Calendar (via gcal MCP)
- List all events in the date range
- Extract: meeting titles, attendees, duration
- Focus on: customer meetings, internal syncs, architecture reviews, demos

### 2. Slack (via slack MCP)
- Search messages sent by the user in the date range
- Search channels the user is active in for threads they participated in
- Extract: channels active in, key threads, messages sent
- Focus on: customer-facing channels, technical discussions, deliverable handoffs

### 3. Gmail (via gmail MCP)
- Search sent emails in the date range
- Search received emails that were replied to
- Extract: threads, recipients, subjects
- Focus on: customer communication, deliverable attachments, scheduling

### 4. Airtable (via airtable MCP)
- Check recently modified bases (use list_bases and look at modification dates if available)
- Note which bases were worked on
- Focus on: bases built or modified, fields/tables created

### 5. Obsidian Vault
- Read the daily note(s) from `03 - Daily/` for the date range
- Read `05 - Cowork/_context.md` for active project context
- Read any project notes from `01 - Projects/` that were referenced
- Read any decision records from `04 - Decisions/` in the date range
- For weekly+ cadences: read existing lower-level review notes from `06 - Reviews/`

### Source Sweep Execution

Run source sweeps in parallel where possible — launch calendar, Slack, Gmail, and Airtable queries concurrently via subagents or parallel tool calls. The vault reads can happen inline since they're fast.

**If a source is unavailable** (MCP not connected, auth expired, etc.), skip it gracefully and note it was skipped in the review. Never block the entire review because one source failed.

**Rate limiting**: For Slack searches, limit to 3-5 targeted searches rather than exhaustive sweeps. Use `slack_search_public_and_private` with date filters. For Gmail, use date-scoped search queries.

## Status Accuracy Rule

**Never assume a thread or task is finalized based on activity alone.** This is the most important accuracy principle for daily reviews.

A message sent, a Slack thread contributed to, or a document drafted does not mean the work is complete. Before categorizing anything as a deliverable or completed outcome, ask: is this actually done, or still in flight?

Use this framework for every item captured:
- **Deliverable (✅ Complete)**: The thing was created and handed off with no action needed from the user. A doc was sent and accepted. A channel was created and is live. A meeting was scheduled and confirmed.
- **In Progress (⏳ Pending)**: Work was done but something is still outstanding — waiting on a response, a decision by someone else, customer confirmation, or further refinement. Include specifically what's being waited on.
- **Context / Contribution**: The user participated in a discussion or provided input, but the output isn't theirs to own (e.g., contributed estimates to someone else's scoping process, weighed in on a thread, attended a meeting).

Common traps to avoid:
- A Slack message with information ≠ delivered. If the other party hasn't confirmed or acted, it's still in flight.
- A rough estimate shared in a channel ≠ a finalized scope. Note it as preliminary if the thread is still active.
- An email sent ≠ an issue resolved. If you're waiting on a reply, it's pending.

Daily review structure should reflect this with separate sections:
- **Deliverables** — truly completed, handed off items
- **In Progress** — active threads with clear pending state and who owns next action
- **Impact & Outcomes** — only claim impact that has actually occurred, not projected or anticipated

## Aggregation Rules

### Daily Review
Raw synthesis from all sources. No prior reviews to aggregate — this is the foundation layer.

Write the review with three core sections (Deliverables, In Progress, Impact & Outcomes) plus Key Interactions, Decisions Made, and Notes:
- **Deliverables**: Only items that are genuinely complete and handed off. Mark with ✅. Include customer/project name.
- **In Progress**: Active threads where work happened today but something is still pending. For each, note what's outstanding and who owns the next action. Mark with ⏳.
- **Impact & Outcomes**: What has actually changed for a customer or stakeholder today. Don't project — if the impact is still pending (e.g., "billing will be unblocked once Matt decides"), say so.
- **Key Interactions**: Meetings attended (from calendar), important threads (from Slack), notable emails. Brief context on each.
- **Decisions Made**: Any technical or strategic decision. Link to `04 - Decisions/` if a record exists.
- **Notes**: Blockers, ideas, follow-ups, anything that doesn't fit above.

### Weekly Review
Read all daily reviews from `06 - Reviews/daily/` for the week. Synthesize up:
- **Deliverables Summary**: Group by customer/project. Don't repeat daily-level detail — summarize.
- **Impact & Outcomes**: Elevate the most significant impacts from the week.
- **Patterns & Themes**: What type of work dominated? Was it build-heavy, meeting-heavy, support-heavy? Any shifts?
- **Key Decisions**: The most consequential decisions from the week.
- **Carry Forward**: What's unfinished? What needs attention next week?

### Monthly Review
Read all weekly reviews for the month. Synthesize up:
- **Deliverables Ledger**: Complete list by customer, with deliverable type and status (delivered, in-progress, blocked).
- **Impact Narrative**: 2-3 paragraphs in first person. This should read like something the user would share with their manager. No bullet-point lists — actual narrative prose.
- **Projects Snapshot**: Status of each active project at month end.
- **Skills & Growth**: New technologies or domains engaged with.
- **Next Month Focus**: Priorities based on carry-forward items and project trajectories.

### Quarterly Review
Read all monthly reviews for the quarter. Synthesize up:
- **Executive Summary**: One paragraph capturing the quarter's defining theme.
- **Deliverables by Customer**: Organized by customer with full deliverable history.
- **Impact & Business Outcomes**: Quantified where possible — number of go-lives, customers served, escalations resolved.
- **Technical Leadership**: Architecture decisions, patterns established, knowledge sharing.
- **Themes & Reflection**: What went well, what was hard, what to improve.
- **Next Quarter Priorities**: Forward-looking goals.

### Yearly Review
Read all quarterly reviews. This is the performance review draft:
- **Year in Summary**: 2-3 paragraphs — the narrative arc of the year. First person, performance-review ready.
- **Deliverables & Achievements**: Complete inventory by quarter, then by customer.
- **Business Impact**: Quantified metrics aggregated from quarterlies.
- **Technical Growth**: Skills developed, technologies adopted, architectural contributions.
- **Leadership & Collaboration**: Mentorship, cross-functional work, process improvements.
- **Challenges & Lessons Learned**: Growth narrative.
- **Looking Ahead**: Goals for next year.

## Writing Standards

### Tone
- First person (the user's voice) for monthly+ cadences
- Factual and evidence-based for daily/weekly
- Never reference "transcripts", "AI-generated", "Slack search results", or source mechanics
- Write as if the user authored this themselves

### Linking
- Use `[[wikilinks]]` to connect to project notes, client notes, and decision records
- Link deliverables to their project: "Delivered [[Acme - Inventory App]] workflow doc"
- Link decisions to `04 - Decisions/` entries when they exist

### Performance Review Optimization
At monthly+ cadences, frame accomplishments using impact language:
- Not: "Built a workflow doc for Acme"
- Instead: "Designed and delivered the technical workflow for [[Acme - Inventory App]], enabling the customer to begin UAT on schedule"

Quantify when possible: number of deliverables, meetings, customers, bases, go-lives.

## Output Protocol

1. Determine cadence and date range
2. Run source sweep (parallel where possible)
3. For weekly+ cadences, read existing lower-level reviews first
4. Generate the review note using the appropriate template from `Templates/Review-{Cadence}.md`
5. Save to `06 - Reviews/{cadence}/{filename}.md`
6. Update today's daily note in `03 - Daily/` with a link to the review
7. Present a summary to the user — don't just say "done", give them the highlights

## Handling Missing Data

If this is a new system and prior reviews don't exist yet for aggregation:
- For weekly: fall back to sweeping all sources directly for the full week (same as daily but wider range)
- For monthly: fall back to source sweep for the full month
- For quarterly/yearly: explain that lower-level reviews are needed first, offer to backfill them

If the vault has no daily notes for a period, rely more heavily on Slack/Gmail/Calendar to reconstruct what happened.

## Scheduled Task Integration

When invoked by a scheduled task, the cadence is passed as part of the prompt. The skill should:
1. Run the full protocol without user interaction
2. Save the review note
3. Return a brief summary of what was captured

The user can then review and edit the note in Obsidian at their convenience.
