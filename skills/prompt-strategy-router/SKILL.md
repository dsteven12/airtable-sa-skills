---
name: prompt-strategy-router
description: "On-demand strategy advisor that recommends evidence-backed prompting approaches when the user explicitly asks for help choosing an approach. TRIGGER PHRASES: which prompting strategy should I use, think this through strategically, what's the best approach for this, help me choose a reasoning strategy, recommend a prompting technique. NEVER trigger on: debugging, troubleshooting, fixing errors, building features, code review, research, file operations, document creation, automation design, or any task where the action is already clear. NEVER trigger mid-task — only at the start when the user asks for approach guidance. This skill is a reference catalog and advisor only — it does not dispatch to other skills, gate execution, or create approval checkpoints."
---

# Prompt Strategy Router

An on-demand reference catalog of research-backed prompting strategies. Recommends an approach when asked, then gets out of the way. All strategies grounded in peer-reviewed research.

## Operating Model

**This skill is a reference book, not a gatekeeper.** It works like looking up a technique in a handbook before starting work — you consult it once, pick an approach, and execute. It never inserts itself into the execution flow, never pauses for approval, and never dispatches to other skills.

### What This Skill Does
- Recommends a strategy from the research-backed catalog when the user asks
- Explains why that strategy fits the task (with evidence)
- Shows the reformulation pattern so the user can see how to structure the work

### What This Skill Never Does
- Triggers automatically (opt-in only, on explicit user request)
- Interrupts or gates work in progress
- Dispatches to downstream skills (CLAUDE.md routing is the single dispatcher)
- Re-invokes itself mid-task (once a strategy is selected, execute it — don't re-classify)
- Asks "want me to proceed?" or creates any approval checkpoint

### Anti-Loop Rules

These rules exist specifically to prevent feedback loops observed in v1:

1. **Single invocation per task.** Once this skill recommends a strategy, it is done. Do not re-invoke to re-classify, re-select, or course-correct. If the approach isn't working, the user decides to pivot — not this skill.
2. **No downstream handoff.** After recommending a strategy, return control to the main conversation. Never invoke another skill from within this skill's execution.
3. **No mid-task triggering.** If you are already debugging, building, or executing — you do NOT invoke this skill, even if you think a different strategy might help. Finish the current approach first.
4. **Trigger phrases are literal, not semantic.** Only fire on the exact trigger phrases listed in the frontmatter, not on semantically similar language like "analyze from multiple angles" or "think about this differently." Those are normal task descriptions, not strategy-selection requests.

---

## When to Invoke

**Only when the user explicitly asks which approach to take.** The three-condition test:

1. The user's message is asking about *how to approach* the task, not asking you to *do* the task
2. The task has genuine approach ambiguity (multiple viable strategies, choice affects quality)
3. No other skill already handles this task type (if automation-architect, airtable-design-advisor, or another skill covers it, use that skill instead — not this one)

### Examples — INVOKE:
- "Which prompting strategy should I use for this analysis?" → Yes
- "Think this through strategically before we start" → Yes
- "I keep getting bad results — what's a better reasoning approach?" → Yes

### Examples — DO NOT INVOKE:
- "Fix this bug" → No (action is clear)
- "Troubleshoot this load test" → No (debugging)
- "Create a workflow doc" → No (workflow-doc skill)
- "Design the automations" → No (automation-architect skill)
- "Analyze this from multiple angles" → No (task instruction, not strategy request)
- "Let's think about this differently" → No (conversational, not a strategy-selection request)
- "Help me debug why this keeps failing" → No (debugging)

---

## How It Works

When invoked, do this once:

1. **Assess the task profile** — What's the primary mode (reasoning, generation, research, decision)? How sensitive is correctness? How ambiguous is the problem?

2. **Recommend a strategy** from the catalog below. State the strategy name, one line on why it fits, and the key evidence stat.

3. **Show the approach pattern** — How should the work be structured using this strategy?

Then stop. Return to the main conversation. The user executes from here.

---

## Strategy Catalog

### Tier 1: Strongest Evidence

**Contrastive Prompting** — Evidence: Strong | GSM8K: +52.9%
Produce both a correct and incorrect answer, identify which is which and why.
Best for: Math/arithmetic, fixing recurring errors, tasks with objectively correct answers.
Cost: Low (single pass).

**Self-Consistency (CISC)** — Evidence: Strong | GSM8K: +17.9%
Generate 3+ independent reasoning paths with confidence ratings, select by weighted majority.
Best for: High-stakes decisions, stress-testing answers.
Cost: High (3-5x compute).

**Step-Back Prompting** — Evidence: Strong | TimeQA: +27%
Identify underlying principles/frameworks first, then apply to the specific case.
Best for: STEM reasoning, domain-heavy technical problems, multi-hop reasoning.
Cost: Medium (2 passes).

**Self-Refine** — Evidence: Strong | +20% avg across 7 tasks
Generate draft → critique against criteria → revise. Most value from first iteration.
Best for: Quality-critical deliverables (docs, code, presentations).
Cost: Medium-High (3-5 passes).

**Least-to-Most Decomposition** — Evidence: Strong | SCAN: 99.7%
Break into ordered subproblems, solve sequentially, feed each answer forward.
Best for: Multi-phase plans, dependency-aware workflows, migration plans.
Cost: Medium (one pass per subproblem).

**ReAct (Reason + Act)** — Evidence: Strong | ALFWorld: +34%
Interleave reasoning with information-gathering. Think → search → reason → search again.
Best for: Research requiring tools/external data, fact-finding, evidence-based debugging.
Cost: Variable (depends on tool interactions).

### Tier 2: Solid Evidence (Specific Contexts)

| Strategy | Best For | Key Stat |
|----------|----------|----------|
| **CoT** | Math/symbolic (non-reasoning models ONLY) | Hurts 6 task classes (ICML 2025) |
| **ToT/AGoT** | Complex search, tradeoff evaluation | +70pts Game of 24 |
| **Generated Knowledge** | Domain best-practices, commonsense | +6-10% |
| **Analogical** | Design patterns, architecture decisions | +12-15% |

### Tier 3: Situational

| Strategy | Best For | Caveat |
|----------|----------|--------|
| **Meta-Prompting** | Novel/unclear tasks | Variable results |
| **SoT + Self-Refine** | Speed-critical structured output | NEVER SoT alone (40% degradation) |

**Excluded:** Role/Persona Prompting (no significant effect — 162 personas, 6 models).

---

## Selection Quick Reference

| "I need to..." | Reach for... |
|----------------|-------------|
| Solve a math problem | Contrastive |
| Get high confidence on a decision | Self-Consistency (CISC) |
| Solve a deep technical/STEM problem | Step-Back + Generated Knowledge |
| Polish a deliverable | Self-Refine |
| Plan a multi-phase migration | Least-to-Most |
| Research with tools | ReAct |
| Choose between architectures | ToT/AGoT |
| Apply domain best practices | Generated Knowledge |
| Recognize a design pattern | Analogical |
| Handle an uncategorizable task | Meta-Prompting |
| Fix a recurring output failure | Contrastive |
| Classify or sort items | Direct prompt — no CoT (CoT hurts these) |

---

## Combination Rules

- Maximum 2 strategies per task (primary + one supporting)
- Primary defines overall structure; supporting modifies a specific phase
- Never combine in a way that risks quality degradation without a quality gate
- SoT is ONLY available paired with Self-Refine

---

## Key Research Context

**Reasoning models internalize strategies.** Models with built-in reasoning (o1, Claude with extended thinking) make explicit CoT scaffolding negligible or harmful. Prefer strategies that add *information* (Generated Knowledge, ReAct) or *structure* (Self-Refine) over strategies that add *reasoning scaffolding* (CoT, ToT).

**Exemplar quality > technique choice.** The Prompt Report (Schulhoff et al., 2024-2025; 1,500+ papers) found that example quality, diversity, and format have a larger effect than technique choice. When applying any strategy, invest in good examples.

---

## References

Full citation tables in `references/research.md`. Tier 2-3 strategy details in `references/additional-strategies.md`. Last evidence review: March 2026.
