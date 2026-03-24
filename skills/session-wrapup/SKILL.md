---
name: session-wrapup
description: "Automate the end-of-session protocol for the current Cowork session — updates the project log, refreshes the daily note, syncs _context.md, and creates decision records. Adapts output by session type: engagement, learning, or ad hoc. Use ONLY when the user signals they are done working in this session — phrases like 'wrap up the session', 'save context', 'done for now', 'let's stop here', 'close out', 'that's it for today', 'I think we're good'. Do NOT trigger on 'wrap up' used in other contexts like 'wrap up this discussion' or 'let's wrap up the data model'. Do NOT use when the user asks to review past work — that is the review skill."
---

# Session Wrapup

Automate the 4-step end-of-session protocol that keeps the Obsidian vault current and ensures the next session starts warm instead of cold.

Every Cowork session produces context that's valuable to future sessions — decisions made, things built, platform constraints discovered, next steps identified. Without a structured wrapup, this context evaporates when the session ends. This skill captures it systematically so the bootstrap protocol (`_context.md` → daily note → project note) works.

## Session Type Detection

Determine what kind of session this was by reading the conversation history:

| Signal | Session Type | Wrapup Scope |
|--------|-------------|--------------|
| Active engagement (project note has `<engagement>` block) | **Engagement** | Full: project log + engagement block + daily note + _context.md + decisions |
| Learning build work (Learning Lab, UC exercises) | **Learning** | Full: project log + daily note + _context.md + skill gaps |
| Skill creation/editing | **Skill Work** | Medium: project log (if applicable) + daily note + _context.md |
| Ad hoc work, research, casual | **Ad Hoc** | Light: daily note + _context.md |

## Step 1: Scan the Session

Before writing anything, reconstruct what happened this session. Sources:

1. **Conversation history** — the actual work done, decisions discussed, tools used
2. **Files created or modified** — check the workspace and vault for changes
3. **Current project note** (if applicable) — read the last `<session>` block to understand the prior state

Extract:
- **Summary**: What was accomplished (2-4 sentences, factual)
- **Decisions**: Choices made with rationale (not just "we decided X" but "we decided X because Y")
- **Discoveries**: Platform constraints, unexpected behaviors, things that didn't work as expected
- **Next steps**: What should happen in the next session — specific, not vague
- **Skill impacts**: Any skill gaps identified, adaptations needed, or new skill ideas

## Step 2: Update the Project Log

If a project was worked on (any type), append a `<session>` block to the project note in `01 - Projects/`.

### Session Block Format

```xml
<session date="YYYY-MM-DD" seq="N">
<summary>
[2-4 sentences describing what was accomplished. Factual, not promotional.]
</summary>
<decisions>
- [Decision 1 — with rationale]
- [Decision 2 — with rationale]
</decisions>
<next_steps>
- [Specific next action 1]
- [Specific next action 2]
</next_steps>
</session>
```

**Determining the sequence number**: Read the project note and find the highest existing `seq` value. Increment by 1.

**For engagement sessions**, also update the `<engagement>` block:
- Update the current phase's `<context>` with any new decisions, table names, linking strategies, risk flags, or deliverable references accumulated this session
- If a phase was completed, mark it `complete` and advance the next phase to `in-progress`
- Never overwrite existing context — append to it

**For learning sessions**, include a `<skill_adaptations>` block if any skill gaps were identified:

```xml
<skill_adaptations>
1. **skill-name** — Description of what's missing or wrong and proposed fix
</skill_adaptations>
```

### Writing Standards for Session Logs

- Use `[[wikilinks]]` liberally — every project, skill, client, or decision reference should be linked
- Write decisions as "X because Y" — the rationale is more valuable than the decision itself
- Next steps should be specific enough that someone reading them cold knows what to do
- Never reference "transcripts", "conversation history", or "AI-generated" — write as if the user authored this

## Step 3: Update the Daily Note

Read (or create) today's daily note at `03 - Daily/YYYY-MM-DD.md`.

### If the note doesn't exist, create it:

```markdown
---
date: YYYY-MM-DD
tags:
  - daily
---

# YYYY-MM-DD

## Worked On
- [Brief description of what was worked on, with [[project link]]]

## Notes
- [Any notable observations, blockers, or ideas]

## Tomorrow
- [What should happen next]
```

### If the note exists, append to it:

- Add entries to `## Worked On` for what was done this session
- Add any notes to `## Notes`
- Update `## Tomorrow` with current next steps (replace stale items)

## Step 4: Refresh _context.md

Read `05 - Cowork/_context.md` and update:

### Active Projects
- Update the status and one-line summary for any project worked on
- Add new projects if this session started one
- Move completed projects out of Active (or mark as completed)

### Recent Decisions
- Add any significant decisions from this session (architectural, design, or process decisions — not trivial implementation choices)
- Keep the list to ~5-7 most recent. Older decisions are in the project notes and decision records.

### Pending / Next Up
- Update pending items based on what was accomplished and what's next
- Remove items that were completed this session
- Add new items that emerged

### Session History
- Add a new `<session>` block with date, summary, decisions, and next steps
- Keep the last 5 sessions. If there are more than 5, remove the oldest.

## Step 5: Decision Records (When Warranted)

Not every decision needs a standalone record. Create one in `04 - Decisions/` only for decisions that are:
- Architectural (affects system design across multiple components)
- Precedent-setting (establishes a pattern that will be reused)
- Reversible but costly (would be expensive to change later)

### Decision Record Format

```markdown
---
decision: "Short title"
date: YYYY-MM-DD
status: accepted
tags:
  - decision
  - [relevant-domain]
---

# [Decision Title]

## Context
[What prompted this decision — the problem or question]

## Decision
[What was decided]

## Rationale
[Why this option was chosen over alternatives]

## Alternatives Considered
- [Option B — why rejected]
- [Option C — why rejected]

## Consequences
- [What this enables]
- [What this constrains]
- [What to watch for]
```

Link the decision record from the project note using `[[wikilinks]]`.

## Execution Order

The steps above have dependencies:

1. **Scan the session** (always first — needed for everything else)
2. **Update project log** and **daily note** (independent — can happen in parallel)
3. **Refresh _context.md** (depends on project log being written, since it references session state)
4. **Decision records** (independent, but last since it's conditional)

## Handling Edge Cases

**Multiple projects in one session**: Write separate session blocks for each project. The daily note covers all of them.

**No project note exists**: If ad hoc work was done that doesn't belong to a project, skip Step 2. The daily note and _context.md still get updated.

**Session produced no decisions**: Omit the `<decisions>` block from the session log rather than writing empty decisions.

**User asks to wrap up mid-session**: Honor it. Capture what's been done so far and note that the session was paused, not completed.

**Conflicting next steps**: If the session surfaced competing priorities, present them in the next steps and let the user decide ordering — don't pick for them.

## What This Skill Does NOT Do

- **Does not replace the review skill.** Reviews synthesize across time periods and sweep external sources (Slack, Gmail, Calendar). The wrapup is internal — it captures what happened in this Cowork session specifically.
- **Does not invoke other skills.** It writes to the vault directly. If a learning-loop reflection was produced during the session, the wrapup should reference its outputs but doesn't re-run it.
- **Does not push to external systems.** No Slack messages, no emails, no Airtable updates. Vault only.
