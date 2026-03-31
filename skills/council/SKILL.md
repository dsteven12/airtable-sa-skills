---
name: council
description: "Orchestrate multiple parallel subagents as a deliberative council to analyze problems from independent perspectives and synthesize a recommendation. Use this skill whenever a problem benefits from multi-perspective analysis before committing to a direction — design tradeoffs, architecture decisions, strategy choices, debugging approaches, process design, or any situation where anchoring bias from a single viewpoint could lead to a suboptimal outcome. MANDATORY TRIGGERS: council, multiple perspectives, weigh the tradeoffs, think this through from different angles, devil's advocate, pros and cons, what am I missing, second opinion, stress-test this idea, evaluate options. Also invoke when airtable-design-advisor or automation-architect surfaces a non-obvious tradeoff that warrants deeper exploration, or when the user is stuck between two or more viable approaches."
---

# Council

Orchestrate parallel subagents as independent analysts, each examining a problem through a distinct lens, then synthesize their perspectives into a unified recommendation. The goal is to surface tradeoffs, blind spots, and non-obvious considerations that a single-pass analysis would miss.

This skill is domain-agnostic. It works for Airtable schema design, code architecture, customer engagement strategy, process design, hiring decisions, or any problem with meaningful tradeoffs.

---

## Why This Works

When you ask a single agent to "think about the tradeoffs," it tends to anchor on its first instinct and then rationalize. The council pattern breaks this by giving each perspective its own context window — they literally cannot see each other's reasoning. This produces genuinely independent viewpoints that frequently surface considerations the others missed entirely.

The synthesis step is where the real value lands: not just listing what each perspective said, but identifying where they agree (high-confidence signals), where they conflict (the actual decision points), and what the user should weigh most heavily given their specific context.

---

## How It Works

### Stage 1: Perspective Collection (Parallel)

Spawn 3 subagents simultaneously using the `Agent` tool. Each agent receives:
- The **full problem context** (what the user described, any relevant files or data)
- A **persona assignment** that defines their analytical lens
- Instructions to produce an **independent analysis** without hedging or trying to be balanced — they should advocate strongly from their assigned perspective

Each agent works in isolation. They cannot see each other's output.

### Stage 2: Synthesis

After all agents return, synthesize their perspectives into a single structured recommendation. This is done inline (not as a separate agent) because the synthesizer needs to see all three perspectives simultaneously and weigh them against the user's specific context.

---

## Persona Selection

The skill ships with a default set of three lenses that cover the most common tradeoff dimensions. However, personas should be adapted to fit the problem domain. The user can specify which lenses they want, or the skill selects automatically based on the problem.

### Default Personas (General-Purpose)

These three lenses create productive tension across the dimensions that matter most in technical and strategic decisions:

**1. The Pragmatist**
> "What's the simplest thing that works today and is still maintainable tomorrow?"

Optimizes for: implementation speed, operational simplicity, maintainability, reduced cognitive load for the team. Skeptical of over-engineering. Asks: "Do we actually need this complexity, or are we solving a future problem that may never arrive?"

**2. The Architect**
> "What happens when this needs to scale 10x — in data, users, or complexity?"

Optimizes for: extensibility, structural integrity, separation of concerns, graceful degradation under load. Thinks in systems, not features. Asks: "What assumptions are baked into this design, and which ones will break first?"

**3. The Advocate**
> "How does the person actually using this experience it day-to-day?"

Optimizes for: end-user experience, workflow friction, error recovery, onboarding clarity, adoption likelihood. Prioritizes the human over the system. Asks: "Will the people who live in this every day love it, tolerate it, or work around it?"

### Domain-Specific Persona Sets

When the problem clearly falls into a specific domain, swap in more targeted lenses. Here are common presets — but always feel free to compose custom sets based on what the problem actually needs.

**Airtable Schema Design:**
- **Scale Strategist** — Record volume projections, linking cardinality, rollup/lookup chain depth, API rate limits, sync performance
- **Builder's Advocate** — Automation complexity, formula maintainability, field count per table, cognitive load for the person configuring it
- **End-User Champion** — Interface usability, filter/sort/group behavior, view performance, data entry friction, mobile experience

**Code Architecture:**
- **Reliability Engineer** — Failure modes, error handling, observability, recovery paths, testing surface area
- **Velocity Optimizer** — Developer experience, onboarding speed, iteration cycle time, deploy confidence
- **Security Reviewer** — Attack surface, data exposure, auth boundaries, dependency risk, compliance implications

**Strategy / Process Design:**
- **Execution Realist** — Resource constraints, timeline feasibility, team capability, coordination costs, what could go wrong
- **Opportunity Maximizer** — Upside potential, leverage points, second-order effects, what this enables next
- **Risk Analyst** — Downside scenarios, reversibility, dependencies, what happens if assumptions are wrong

**Customer Engagement:**
- **Technical Advisor** — Platform fit, integration complexity, migration risk, performance implications
- **Relationship Manager** — Stakeholder dynamics, change management, adoption barriers, political considerations
- **Value Architect** — ROI framing, quick wins vs. long-term value, measurable outcomes, expansion opportunities

### Custom Personas

If the user specifies their own lenses (e.g., "give me a security perspective, a cost perspective, and a developer experience perspective"), use those directly. Map each user-provided label to a full persona with an optimization target, core questions, and analytical posture using the pattern above.

---

## Execution Protocol

### 1. Parse the Problem

Before spawning agents, clearly identify:
- **The decision or question** — what specifically needs to be resolved?
- **The context** — what constraints, prior decisions, or existing systems are relevant?
- **The stakes** — is this easily reversible or a one-way door?

If any of these are ambiguous, ask the user to clarify before proceeding. A council on a vague question produces vague perspectives.

### 2. Select Personas

Choose the persona set based on the problem domain. If the user specified personas, use those. If the problem spans domains (e.g., an Airtable schema decision with customer-facing implications), compose a hybrid set that covers the most important tension points.

Announce the selected personas to the user before spawning: *"I'm going to run this through three lenses: [Persona 1], [Persona 2], and [Persona 3]. Want to adjust before I kick them off?"*

If the user says to just go, or the conversation flow makes it clear they want speed, skip the confirmation and proceed.

### 3. Spawn Parallel Agents

Launch all agents in a **single message** with multiple `Agent` tool calls so they run concurrently. Each agent's prompt should follow this structure:

```
You are [Persona Name] — an independent analyst on a council evaluating a problem.

Your analytical lens: [Persona description and optimization target]

## The Problem
[Full problem context from the user, including any relevant files, data, or prior conversation]

## Your Task
Analyze this problem exclusively through your lens. Be opinionated — your job is to advocate for the considerations your perspective prioritizes, not to be balanced. Other council members will cover other angles.

Produce:
1. **Assessment** — Your read on the situation from your perspective (2-3 paragraphs)
2. **Key Concerns** — The 2-3 things that matter most from your vantage point
3. **Recommendation** — What you'd push for if your perspective were the only one that mattered
4. **Red Flags** — Anything in the current proposal/direction that makes you uneasy, and why

Be specific and concrete. Reference actual details from the problem context, not generic advice. If you'd want to see data or ask a clarifying question, say so.
```

### 4. Synthesize

**Wait for ALL agents to return before beginning synthesis.** Do not start writing the synthesis after receiving only one or two perspectives — the entire value of the council pattern depends on having the complete set of independent viewpoints before any integration happens. Partial synthesis defeats the purpose.

Once all agents have returned, produce a synthesis that:

**Opens with the consensus** — Where do all three perspectives agree? These are high-confidence signals. If all three lenses point the same direction on something, that's a strong indicator.

**Maps the tension points** — Where do perspectives conflict? For each conflict:
- Name the tradeoff clearly (e.g., "Simplicity vs. Scale Readiness")
- Summarize each side's position in one sentence
- Identify what would tip the decision one way or the other (what context matters here?)

**Surfaces blind spots** — Did any perspective raise something the others missed entirely? These are often the most valuable insights — they're the things a single-pass analysis would have overlooked.

**Delivers a recommendation** — Based on the full picture, what direction makes the most sense given the user's specific context? This isn't a wishy-washy "it depends" — take a position, but show your reasoning and name the tradeoff being accepted.

**Flags the reversibility** — Is this decision easy to change later, or does it lock something in? This affects how much certainty is needed before committing.

### 5. Format

The synthesis should be conversational, not a rigid template. The structure above is a thinking guide, not an output format. Write it the way you'd explain a complex tradeoff to a smart colleague — clear, direct, with enough structure to follow the reasoning but not so much that it feels bureaucratic.

---

## When NOT to Use This Skill

- **The answer is obvious.** If there's a clear best practice or an unambiguous correct answer, a council adds latency without value. Just answer.
- **The user needs speed over depth.** If they're in rapid iteration mode and need a quick directional answer, give them one and offer to council it later if they want more confidence.
- **The problem is purely informational.** "How does X work?" doesn't need three perspectives — it needs a clear explanation.
- **There's only one viable option.** If constraints eliminate all but one path, a council won't surface better options. It might help validate the remaining option, but that's a simpler task.

---

## Integration with Other Skills

The council pattern pairs well with several existing skills:

- **airtable-design-advisor** — When a design review surfaces a tradeoff that isn't clear-cut (e.g., "should we denormalize here or accept the lookup chain?"), invoke council to explore it from multiple angles before recommending.
- **automation-architect** — When an automation design has multiple viable approaches (e.g., script action vs. multi-step native actions), council can evaluate the tradeoffs across maintainability, performance, and user transparency.
- **prompt-strategy-router** — For high-stakes problems, the router might select the council pattern as the optimal prompting strategy (it's essentially a structured variant of Self-Consistency with diverse perspectives instead of diverse reasoning paths).

The council skill does not produce documents or files. It produces a structured analysis in the conversation. If the user wants the analysis captured, they can ask for it to be saved to their vault or included in a project note.
