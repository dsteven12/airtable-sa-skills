---
name: executive-brief
description: "Generate a structured executive leadership brief (.docx) designed as a decision document, not an analytical narrative. MANDATORY TRIGGERS: executive brief, leadership brief, decision brief, decision document, executive summary doc, brief for leadership, escalation brief, leadership decision, options paper, recommendation paper, brief for VP, brief for exec, write up the situation for leadership. ALWAYS invoke this skill when the user needs to present a situation with options to senior leadership for a decision — even if they just say 'write this up for my VP' or 'I need to present this to leadership.' Also invoke when the user has a draft leadership doc that reads too analytical or narrative and needs to be restructured as a decision document. Do NOT invoke for technical design docs, training guides, or internal team documentation — those have their own skills."
---

# Executive Leadership Brief

Generate a structured executive leadership brief as a .docx file. This skill encodes editorial patterns for documents that help senior leaders make decisions quickly — typically in under 5 minutes of reading.

## The Three Tests

Before writing a single section, answer these three questions. They determine whether the document moves people or just informs them.

1. **Does the reader know enough to evaluate a recommendation right now?** If yes, lead with the recommendation. If no, give them three sentences of context first: what is true, why it is a problem, and what you are asking them to do. Then stop. Three sentences is a frame. Four is a document.

2. **Is every section answering the question the exec is actually holding?** In a technical situation, that question is almost never "what happened" or "how does this work." It is "what do I need to decide, what are my options, and what happens after I choose." Structure sections around those questions, not around the chronology of how you discovered the problem.

3. **Does the close name a specific decision, a specific owner, and a specific timeline?** An exec doc that ends without those three things has informed but not moved. The close is where alignment either solidifies or dissolves.

## The Core Distinction: Decision Document vs. Analytical Narrative

Leadership briefs fail when they read as analytical narratives — documents that walk the reader through a journey of discovery, building understanding section by section. They succeed when they read as decision documents — documents that present the choice upfront, provide just enough supporting evidence, and close with a clear action.

**Analytical narrative** (what to avoid): "Here's what happened → here's what we found → here's what it means → here's what we could do → here's our recommendation."

**Decision document** (what to produce): "Here's the decision you need to make → here's what each option looks like → here's the evidence that informs it → here are the next steps with owners."

The reader should know what they're being asked to decide within 90 words. Everything after that supports the decision — it doesn't build toward it.

## Document Architecture

### The SCR Opening

Every brief opens with a Situation-Complication-Resolution table. Three rows, one sentence each. This is the load-bearing frame of the entire document — the RESOLUTION row determines the document's structure.

| Row | Purpose | Example |
|-----|---------|---------|
| SITUATION | What is true right now. Context only — no stakes, no ask. | "Acme Corp is approaching go-live on a complex Airtable build serving 177 Account Managers and 2,175 Team Contacts." |
| COMPLICATION | Why the reader can't ignore this. Stakes and urgency. | "Load testing has surfaced performance risk that we cannot resolve without leadership decisions." |
| RESOLUTION | What you need from them. Promises the document's structure. | "There are five decisions for leadership. Two can unblock immediate low-risk work. Three determine the heavier path." |

**Why this works:** The RESOLUTION row isn't decorative — it's structural. If it promises five decisions, the reader expects a five-decision table. If it promises two options, the reader expects a comparison. The SCR frame earns whatever structure follows it. Without that frame, the structure surprises the reader.

**Why narrative openings fail:** A two-paragraph executive summary mixes context, findings, stakes, and options into prose. The reader processes it linearly and holds everything in working memory. An SCR table lets them process three distinct pieces in sequence — what's true, why it matters, what you need — and drop each one before picking up the next.

### Section Structure

After the SCR opening, the document follows this architecture:

```
SCR TABLE               → 3 sentences: context, stakes, ask
DECISION TABLE          → Every decision in a row, immediately after SCR
SUPPORTING SECTIONS     → Evidence, cost/scope tables, option comparisons
ORG / COMMERCIAL        → Implications beyond the technical (if applicable)
NEXT STEPS              → Specific actions, named owners, concrete timing
BACKGROUND (appendix)   → Technical context, design history, root cause detail
```

This is the inverse of how most technical people write. The natural instinct is to build the case, then present the decision. Leadership briefs invert it: present the decision, then support it. Evidence validates choices — it doesn't build toward them.

### Decision Decomposition

One of the most impactful structural moves: decompose a single binary choice into discrete, tiered decisions. In most complex situations, what looks like one decision ("should we do A or B?") actually contains several:

- Who does the work?
- Who pays for it?
- What's the timing?
- Who provides specialized resources?
- What org changes are needed?

Each of these can be decided independently, by different people, on different timelines. A binary frame (Option A vs. Option B) forces all-or-nothing. A decision table lets leadership say yes to decisions 1–2 today and take more time on 3–5.

**Decision table format:**

| DECISION | THE QUESTION | OPTIONS | WHAT HAPPENS NEXT |
|----------|-------------|---------|-------------------|
| 1. [Name] | What specifically is being asked | A) ... B) ... | Immediate action per choice |
| 2. [Name] | ... | ... | ... |

**Decision tiering:** Group decisions by urgency and risk. "Two decisions unblock immediate low-risk work and can be made independently. Three determine the heavier path." This gives leadership permission to move fast on some things while deliberating on others.

**"What Happens Next" column:** This is the column that separates a decision document from an analysis. For each decision, name the immediate consequence of choosing. Not "this would be beneficial" — "Work begins in sandbox immediately once decided." The reader should be able to trace: I choose B → this specific thing happens → this person is responsible.

### Option Comparison Tables

When one of the decisions is a genuine either/or (e.g., timing: before go-live vs. phased rollout), use a comparison table with rows that answer the exec's actual questions:

| Dimension | Option A | Option B |
|-----------|----------|----------|
| Go-live timing | What happens to the timeline | What happens to the timeline |
| Choose this when | Risk/context conditions that favor this option | Risk/context conditions that favor this option |
| Account/customer perception | How the customer and relationship are affected | How the customer and relationship are affected |
| Cutover complexity | What the operational transition looks like | What the operational transition looks like |
| Primary risk | What could go wrong | What could go wrong |

These rows answer "what do I need to decide, what are my options, and what happens after I choose" — not "what are the technical tradeoffs." Save technical tradeoffs for the supporting sections.

### Cost and Effort Visibility

Leadership briefs without numbers force the decision-maker to estimate effort against incomplete data. Always quantify:

- **Per-item estimates:** Break down work into discrete changes with hours and cost per item
- **Totals with ranges:** "$4,200–$8,400 (14–28 hrs at $300/hr)"
- **Pending confirmations:** If estimates are preliminary, say so: "pending the user's confirmation"
- **Risk per item:** Not just aggregate risk — per-change risk assessment

A table format makes costs scannable:

| CHANGE | WHAT IT DOES | EST. HRS | EST. COST | RISK |
|--------|-------------|----------|-----------|------|
| Item 1 | Impact | 4-8 hrs | $1,200-$2,400 | Low |
| TOTAL | | 14-28 hrs | $4,200-$8,400 | |

### Supporting Evidence Sections

Evidence sections (load tests, metrics, user reports) appear AFTER the decision frame. They validate the decisions — they don't build toward them. An executive who scans the SCR and decision table should already know what they're choosing. The evidence sections answer "should I feel confident about this choice?"

Structure findings as boxed callouts with a bold headline and interpretation:

> **Under moderate concurrent use, save times degrade significantly**
>
> When 3–5 users save simultaneously, save times exceeded two minutes. What this means for go-live: coordinators during peak hours could experience meaningful delays. The no-code changes reduce this risk before launch.

**Hedging discipline:** Consolidate all caveats into a single honest statement in the evidence section. One well-placed caveat is more credible than five scattered qualifications. State it, then deliver the takeaway without re-qualifying.

**Decision boundaries:** When evidence establishes a threshold, frame it as a decision criterion: "The decision boundary is 3–10 seconds." This makes later references (phase gates, success criteria) feel like intentional callbacks, not repetition.

### Org / Commercial Implications

Technical situations almost always have organizational dimensions. A brief that treats the problem as purely technical is strategically incomplete. If the situation reveals process gaps, pre-sales misalignment, or relationship dynamics, surface them in a dedicated section:

> **A Shared Blind Spot: What We Need to Change**
>
> [What the situation revealed about process/org gaps]
> [Specific asks for leadership — concrete, actionable]
> [Timeline for follow-up: "Joint debrief within 30 days"]

This signals to leadership: "We're not just solving the immediate problem — we're preventing the next one."

### Next Steps

A table with specific actions, named owners, and concrete timing. Every row must have all three.

| ACTION | OWNER | TIMING |
|--------|-------|--------|
| Confirm estimates | the user | Before leadership decisions |
| Investigate blocker | SA lead | Immediately |
| Leadership makes decisions 1–5 | PS and Services leadership | This week |
| If Option A: scope timeline | SA lead + Delivery partner | Within 5 days of decision |

**Timing specificity:** "This week" not "once direction is confirmed." "Within 5 days of decision" not "after alignment." "Within 30 days" not "in the coming weeks." Vague timing produces vague accountability.

**Named owners:** "Alice will..." not "the team will..." Not roles or streams — people. This enables executives to verify alignment and follow up.

**Conditional actions:** If actions depend on which option is chosen, prefix them: "If Option A: ..." / "If Option B: ..." This shows leadership you've thought through both paths.

### Background Appendix

Technical context — schema complexity, design rationale, root cause detail — lives in an appendix at the end, not front-loaded before the decisions.

The reader doesn't need to understand the system architecture to choose. They need to trust that YOU understand it. The appendix provides that trust: "Here's full context if you want to verify our analysis, but you don't need this to decide."

**What belongs in Background:**
- System scale (tables, fields, link density)
- Design decisions and why they were made
- Root cause specifics (e.g., "3 fields referenced in 673 places across 376 screens")
- How the cumulative complexity developed

**What does NOT belong in Background:**
- Evidence that informs the decision (that's the evidence section)
- Cost or effort estimates (that's the decision frame)
- Next actions (that's the close)

## Anti-Repetition Architecture

### The Ownership Rule

Every concept gets explained ONCE in its owning section. Other sections can reference it without re-explaining.

| Concept | Owned By | Can Reference From |
|---------|----------|-------------------|
| Business context / scale | SCR SITUATION row | Decision table (brief context) |
| Stakes / urgency | SCR COMPLICATION row | Evidence (as interpretation) |
| What you need from them | SCR RESOLUTION row | Next Steps (as actions) |
| Root cause / technical detail | Background appendix | Evidence (as brief context for findings) |
| Cost / effort estimates | Cost table | Decision table ("What Happens Next") |
| Decision boundaries / thresholds | Evidence section | Decision phases (as gates) |
| Support capacity / hours | Option descriptions | Cost table (as "committed capacity") |
| Accountability / owners | Next Steps table | Decision table ("What Happens Next") |

### How Repetition Happens

Repetition in leadership docs is almost always structural:

1. **A section does two jobs.** If a section explains both the root cause AND previews solutions, it forces solution sections to re-explain the root cause. Fix: complete the diagnosis in one place (Background), keep solutions execution-only.

2. **Work stream sections re-explain the "why."** Stream descriptions should be execution-focused: what gets changed, scope, timeline, cost, result. NOT "The reason we need this is..." If the reader reaches the stream details, they've already absorbed the decision frame.

3. **The opening tries to be both summary AND preview.** An SCR opening states context, stakes, and ask. It does NOT preview solution details, support capacity, or timeline specifics.

4. **Decision tables restate logistics.** A comparison table helps the reader choose based on risk, timeline, and perception tradeoffs. It should NOT include operational logistics (effort estimation steps, support hour breakdowns).

### The Reference Structure

When a concept must appear in multiple sections:

1. **First mention (owning section):** Full explanation with specifics and numbers
2. **Second mention (referencing section):** Use the concept without restating the numbers
3. **Third mention:** There shouldn't be one. If a concept appears three times, the structure needs fixing.

## Format Philosophy

Leadership briefs should be ~90% tables and structured elements, ~10% prose. Every piece of information that can live in a table row should.

- **Tables** for: decisions, comparisons, costs, next steps, findings
- **Boxed callouts** for: key findings with interpretation, specific asks
- **Prose** for: interpretation of evidence, option descriptions where comparison tables aren't sufficient
- **Background appendix** for: technical narrative that provides context but doesn't serve the decision

A table row is scannable in 2 seconds. A paragraph requires 90 seconds of focus. For a 5-minute read, that math matters.

## Document Generation

This skill produces .docx files using the `docx-custom` skill's infrastructure. Read the `docx-custom` SKILL.md for the generation approach (docx-js via Node).

### Formatting Standards

- **Font:** Arial, 12pt body, 18pt H1, 14pt H2
- **Spacing:** 240 twips after body paragraphs, 360 line spacing
- **Tables:** Airtable brand blue (#2D7FF9) header cells with white text, light gray (#F2F2F2) label cells for key-value tables
- **Header:** "[Customer] — Executive Leadership Brief" (right-aligned, italic, gray)
- **Footer:** Page numbers (centered, gray)
- **SCR table:** Gray background (#F2F2F2) for label column, no header row — the labels ARE the structure

### Validation

After generating, validate using:
```bash
python mnt/.claude/skills/docx-custom/scripts/office/validate.py <output.docx>
```

## Pre-Flight Checklist

Before delivering the document, verify:

- [ ] Can a reader state what they're deciding after reading only the SCR table?
- [ ] Does the RESOLUTION row promise the document's structure accurately?
- [ ] Are decisions decomposed into discrete, independently-decidable items?
- [ ] Does every decision row include Question, Options, AND What Happens Next?
- [ ] Are decisions tiered (immediate/low-risk vs. heavier)?
- [ ] Do evidence sections appear AFTER the decision frame?
- [ ] Is technical context appendixed, not front-loaded?
- [ ] Are cost/effort estimates specific (hours, dollars, per-item)?
- [ ] Does the Next Steps table name specific people, actions, and timing?
- [ ] Is timing concrete ("this week", "within 5 days") not vague ("once confirmed")?
- [ ] Are org/commercial implications surfaced (not just technical)?
- [ ] Does every concept have exactly ONE owning section?
- [ ] Is the document ~90% tables/structured elements, ~10% prose?
- [ ] Would a senior reviewer approve this? (Decision document, not analytical narrative.)
