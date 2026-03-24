---
name: learning-loop
description: "Two-mode skill for kinesthetic learning acceleration. BRIEF mode (session start): reads the project note and sets high-level learning objectives — 'here's what you're going to learn today' — anchored to the target patterns for the current use case. REFLECT mode (session end): extracts granular discoveries from the session, maps them back to the core learning themes, identifies platform constraints and skill gaps, and proposes concrete skill adaptations. MANDATORY TRIGGERS: brief me, what am I learning today, learning objectives, learning briefing, retro, retrospective, what did I learn, lesson extractor, skill adaptations, what did we discover, learning review, reflect on this session. ALWAYS invoke when starting or ending a learning-type engagement session — even if the user just says 'let's start UC2' (brief) or 'what did we learn' (reflect)."
---

# Learning Loop

Two modes, one skill. **Brief** sets the stage at session start. **Reflect** captures what actually happened at session end. Together they form a learn-by-doing feedback loop that accelerates pattern acquisition through deliberate framing and structured extraction.

The insight behind this skill: kinesthetic learners need repetition, but structured repetition compounds faster than raw repetition. Briefing creates intentional focus. Reflection converts experience into transferable knowledge. The gap between "what you expected to learn" and "what you actually learned" is where the deepest insights live.

## Mode Detection

Determine the mode from context:

| Signal | Mode |
|--------|------|
| Session start, "brief me", "what am I learning today", beginning work on a use case | **BRIEF** |
| Session end, "retro", "what did I learn", "reflect", after completing a build or test phase | **REFLECT** |
| Ambiguous — user just says "learning loop" | Ask which mode, or infer from session state (no work done yet → brief; work completed → reflect) |

---

## BRIEF Mode

Run at session start for any learning-type engagement. Sets high-level learning objectives that the reflect phase will measure against.

### Input

Read these sources:

1. **Project note** from `01 - Projects/` — the `<engagement>` block, use case definitions, target patterns, design principles mapped to this UC
2. **Prior session logs** — what was built before, what's already been learned
3. **`tasks/lessons.md`** — existing platform knowledge (so the brief can focus on what's NEW, not what's already captured)
4. **Prior reflect outputs** — if this is UC2+ in a series, read the previous UC's reflection to identify carry-forward themes

### Output: Learning Briefing

Present the briefing conversationally — not as a rigid template, but covering these elements:

**Core Themes** (3-5 high-level learning objectives)
For each theme:
- What the pattern is, in plain language
- Why it matters for customer work (not abstract — ground it in "when would a customer need this")
- What you already know about it from prior builds (if anything)
- What's new or different this time

**Design Principles in Play**
Which architectural principles this build will exercise, and what to watch for. Reference the specific risk heuristics or linking patterns that apply.

**Watch List**
Platform behaviors or edge cases to pay attention to during the build, based on patterns from prior sessions. These are the "I wonder if..." items — hypotheses to test, not just patterns to practice.

**Connection to Prior Builds**
How this session's themes build on what was learned before. For UC2, what from UC1 carries forward? What's the delta — the genuinely new ground?

### Briefing Principles

- Keep it concise. The briefing should take 2-3 minutes to read, not 15. It's a compass heading, not a textbook.
- Frame themes as questions when possible: "Can we get AI to produce consistently structured output that an automation can parse?" is more engaging than "Learn structured extraction."
- Be honest about knowledge gaps. If something hasn't been tried yet, say so — that's where the real learning happens.
- Don't restate the entire use case scenario. The user already knows the customer story. Focus on the learning angle.

---

## REFLECT Mode

Run at session end after a build or test session. Extracts granular learnings and maps them back to the briefing's core themes.

### Input

Read these sources:

1. **The current session's work** — session log entries, decisions made, platform discoveries
2. **The briefing** (if one was produced this session) — the core themes and watch list items
3. **`tasks/lessons.md`** — to check what's already captured and avoid duplication
4. **Existing skills** — when a discovery implies a skill gap, read the relevant skill to confirm the gap exists

### Extraction Process

Work through the session's activity and extract:

1. **Platform Discoveries**
   Concrete things learned about how Airtable actually behaves (vs. how you'd assume it behaves). These are the most valuable learnings because they prevent future mistakes.
   - What was the assumption?
   - What actually happened?
   - What's the workaround or correct approach?

2. **Pattern Validations**
   Patterns that were exercised and confirmed to work as expected. Brief — just note that they worked and any nuances.

3. **Design Decision Rationale**
   Decisions made during the build and why. These are transferable to customer work — "we chose X over Y because Z" is a reusable reasoning pattern.

4. **Skill Gap Identification**
   Places where existing skills gave incorrect guidance, missed a platform constraint, or lacked a pattern that was needed. For each gap:
   - Which skill is affected
   - What's missing or wrong
   - Proposed fix (specific enough to act on)

5. **Unexpected Learnings**
   Things that weren't on the watch list but emerged during the build. These are often the highest-value discoveries because they reveal unknown unknowns.

### Output: Reflection

Present the reflection in two parts:

**Part 1: Theme Scorecard**
For each core theme from the briefing:
- What was the objective?
- What actually happened?
- Key takeaway (one sentence)
- Confidence level: how well do you understand this pattern now? (exploring → practicing → fluent)

If no briefing was produced this session, skip the scorecard and go straight to Part 2.

**Part 2: Granular Discoveries**
Organized by category (platform discoveries, pattern validations, design decisions, skill gaps, unexpected learnings). Each entry should be:
- Specific enough to be actionable
- Written as a lesson, not a narrative ("Find Records results require Repeating Group for linked record writes" not "we discovered that when we tried to...")
- Tagged with which skill it affects (if any)

**Part 3: Proposed Actions**
Concrete next steps, ordered by priority:
- Lessons to add to `tasks/lessons.md` (with draft text)
- Skill adaptations to queue (with affected skill and proposed change)
- Watch list items to carry forward to the next session
- Open questions to investigate

### Reflection Principles

- Separate discovery from opinion. "Token picker doesn't expand multi-collaborator fields" is a discovery. "Airtable should fix this" is an opinion. Capture the first, skip the second.
- Be ruthless about deduplication. If it's already in `tasks/lessons.md`, don't re-extract it — note that it was validated and move on.
- Prioritize skill gaps over general lessons. A lesson that updates a skill prevents the same mistake for every future invocation. A lesson in `lessons.md` only helps if someone reads it.
- The theme scorecard is the most important part for the user. It connects the granular work back to the learning arc and shows progression across sessions.

---

## Cross-Session Learning Arc

When reflecting on UC2+ in a series, the skill should track the learning arc:

- **UC1 → UC2**: What patterns from UC1 were reused? Did they work the same way or require adaptation? What's genuinely new?
- **UC2 → UC3**: Same questions, but now the baseline includes both prior UCs.

This accumulation is what distinguishes kinesthetic learning from isolated practice. Each build should feel like it's adding to a growing foundation, not starting over.

The reflect output should explicitly call out:
- Patterns that transferred cleanly (building confidence)
- Patterns that needed adaptation (deepening understanding)
- Entirely new ground (expanding capability)

---

## Integration with Other Skills

- **engagement-orchestrator**: The learning-loop Brief aligns with the orchestrator's SCOPE and DESIGN+BUILD phases for learning builds. The orchestrator tracks phase state; the learning-loop adds the learning lens on top.
- **session-wrapup**: The Reflect output feeds into the session wrapup — skill gaps and lessons identified here should be captured in the wrapup's project log and lessons.md updates.
- **review**: Weekly/monthly reviews can reference learning-loop Reflections to build a skills-development narrative.

The learning-loop doesn't replace any of these — it adds a learning-specific layer that those skills don't cover.
