---
name: prompt-strategy-router
description: "Automatic pre-flight check that selects the optimal prompting strategy before executing any non-trivial task. Trigger BY DEFAULT on any task beyond a simple factual answer or one-step action — including research, analysis, planning, debugging, document creation, code architecture, problem-solving, comparisons, evaluations, multi-step workflows, building features, writing content, or designing systems. Do NOT wait for keywords like 'think through' or 'analyze' — if the task has any complexity, route it here first. Only skip for: simple factual questions, quick file reads, single terminal commands, or casual conversation. Mandatory first step in every non-trivial workflow: classify, select strategy, reformulate, execute. All strategies grounded in peer-reviewed research."
---

# Prompt Strategy Router

A routing skill that classifies incoming tasks, selects the optimal prompting strategy (or combination), and presents a reformulated prompt for user approval before execution. Every strategy recommendation in this skill is grounded in published research with measured improvements — not theoretical claims.

This skill operates as a **pre-execution layer** — it doesn't produce the final output itself. Instead, it ensures the right cognitive approach is applied before work begins.

---

## How It Works

1. **Classify** the user's task across multiple dimensions
2. **Select** the best-fit strategy (or strategy combination) from the evidence-backed catalog
3. **Reformulate** the user's original prompt using the selected strategy's structure
4. **Present** the recommendation to the user for approval or adjustment
5. **Execute** (or hand off to a downstream skill) once approved

---

## Critical Context: Reasoning Models & Exemplar Quality

Two cross-cutting findings from recent meta-analyses (2024-2025) affect how this skill routes:

### Reasoning models respond differently

Models with built-in reasoning (o1, o1-mini, Claude with extended thinking) internalize many prompting strategies. Research from Wharton Generative AI Labs (2025) and ICML 2025 shows that explicit CoT scaffolding provides negligible benefit and can even hurt performance with these models. Simpler, direct prompts often outperform elaborately structured ones. When routing for a reasoning model, prefer strategies that add *information* (Generated Knowledge, ReAct) or *structure* (Self-Refine) over strategies that add *reasoning scaffolding* (CoT, ToT).

### Exemplar quality matters more than technique choice

The Prompt Report (Schulhoff et al., 2024-2025; 32 researchers, 1,500+ papers analyzed) found that exemplar factors — order, diversity, quantity, quality, and format of examples — have a larger effect on output quality than the choice of prompting technique itself. When reformulating prompts, invest in providing high-quality, diverse examples relevant to the task rather than relying solely on strategy scaffolding.

---

## Step 1: Task Classification

Before selecting a strategy, classify the incoming task across these dimensions:

| Dimension | Options | Signal |
|-----------|---------|--------|
| **Primary mode** | Reasoning, Generation, Research, Decision, Transformation | What is the user fundamentally trying to do? |
| **Correctness sensitivity** | High (math, logic, debugging), Medium (analysis, planning), Low (creative, brainstorming) | How much does getting the intermediate steps right matter? |
| **Structure importance** | High (documents, presentations, multi-section output), Medium (code, analysis), Low (conversation, Q&A) | Does the output need deliberate structural organization? |
| **Ambiguity level** | High (open-ended, underspecified), Medium (clear goal but multiple paths), Low (well-defined with constraints) | How much interpretation is required? |
| **Depth required** | Deep (exhaustive analysis, edge cases), Moderate (thorough but bounded), Surface (quick answer, overview) | How far should exploration go? |
| **Speed sensitivity** | High (time-boxed, rapid iteration, batch work), Medium (normal turnaround), Low (quality trumps all, take your time) | Is faster output at equal quality valuable here? |

Build a mental profile from these dimensions — it drives strategy selection.

### The Cardinal Rule: Quality Is the Hard Constraint

**Quality is never traded for speed.** When selecting strategies or combinations:

1. **First, optimize for output quality.** Select the strategy (or combination) that produces the highest-quality result for the task profile.
2. **Then, if two strategies produce comparable quality, prefer the faster one.** Speed is a tiebreaker, not a goal.
3. **Never recommend a combination that introduces quality degradation risk** unless the combination itself includes a quality gate that fully mitigates the risk (e.g., SoT is only recommended alongside Self-Refine, which catches the 40% degradation cases).

If a strategy is faster but has *any* measured quality variance without a mitigation step, it does not qualify as a recommendation — even as a secondary strategy.

---

## Step 2: Strategy Catalog

Each strategy below includes its empirical evidence rating and key benchmark results. Strategies are organized into tiers based on the strength of their measured improvements.

### Evidence Rating Scale

- **Strong** — Multiple peer-reviewed papers, reproducible results, significant measured gains
- **Moderate** — Published research with consistent but modest gains, or strong results in narrow domains
- **Emerging** — Promising results but no canonical paper yet, or highly variable across tasks
- **Negative** — Research shows the approach is statistically ineffective in most cases

---

### Tier 1: Strongest Evidence (Recommend First)

These strategies have the strongest empirical support and should be the default recommendations when their task profiles match.

---

#### Self-Consistency (CoT-SC) with Confidence Weighting
**Evidence: Strong** | Wang et al., 2022; ACL 2025 (CISC) | GSM8K: +17.9% (56.5% → 74.4%), SVAMP: +11%, AQuA: +12.2%

**What it does:** Generates multiple independent reasoning paths for the same problem, then selects the most consistent answer. The original version uses simple majority voting; the updated **CISC variant** (Confidence Improves Self-Consistency, ACL 2025) adds self-assessed confidence scores to each path and uses weighted majority voting — this outperforms standard Self-Consistency in both efficiency and accuracy.

**Best for:** High-stakes decisions where confidence matters. Math and arithmetic problems. Any task where you want to stress-test an answer before committing. Pairs naturally with CoT — run CoT multiple ways and compare.

**When to avoid:** Simple factual questions where one pass suffices. Time-sensitive work where 5-10x compute cost isn't justified. Tasks where the model already performs well (diminishing returns on easy problems).

**2025 caveat:** The Prompt Report (Schulhoff et al., 2024-2025) notes Self-Consistency showed "limited effectiveness in comparison" to other techniques in their meta-analysis. It remains strong for math/arithmetic but may be overrated for general reasoning. Prefer Contrastive for math tasks where it applies.

**Cost:** High — requires multiple forward passes (typically 3-5x single CoT with CISC, vs. 5-10x with original).

**Reformulation pattern:**
```
I want high confidence on this. Give me three independent approaches to answering this question, each reasoning from different starting assumptions or frameworks. For each approach, rate your confidence (low/medium/high) in the conclusion.

[Original task]

After presenting all three approaches with confidence ratings, evaluate where they agree and disagree. Weight more confident reasoning paths more heavily. Synthesize the strongest answer, noting which approach(es) contributed most and where uncertainty remains.
```

---

#### Contrastive Prompting
**Evidence: Strong (validated through 2025)** | arXiv:2403.08211 (2024), Auto-CCoT (2025), LCP at ICLR 2025 | GSM8K: +52.9% (35.9% → 88.8%), zero-shot: 14.3% → 73.2%, AQUA-RAT: +20.9%, LCP: 89%+ win rate

**What it does:** Prompts the model to produce both a correct and an incorrect answer, forcing contrastive reasoning. By explicitly identifying the wrong path, the model more reliably finds the right one. Remarkably simple — a single prompt instruction change.

**2025 validation:** Two follow-up approaches strengthen the case. **Auto-CCoT** (Automatic Contrastive Chain-of-Thought, 2025) dynamically retrieves informative correct-wrong pairs, extending gains beyond the original study. **LCP** (Learning from Contrastive Prompts, ICLR 2025) uses contrastive learning for automated prompt optimization, achieving 89%+ win rates. Negative examples generated from zero-shot outputs proved as effective as human-written ones.

**Best for:** Arithmetic and mathematical reasoning. Any task with objectively correct/incorrect answers. Fixing recurring errors where the model keeps making the same type of mistake. Can be layered on top of other strategies for additional gains.

**When to avoid:** Open-ended or subjective tasks where "correct vs. wrong" doesn't apply. Creative work. Tasks where the model can't reliably distinguish the correct answer from the incorrect one.

**Cost:** Low — single forward pass, just a prompt modification.

**Reformulation pattern:**
```
[Original task]

Let's give both a correct and a wrong answer, then identify which is which and why.

First, produce two candidate answers — one correct and one deliberately incorrect. Explain the reasoning error in the wrong answer and why the correct answer avoids it.
```

---

#### Step-Back Prompting
**Evidence: Strong** | Zheng et al., 2023 (DeepMind) | Physics: +7%, Chemistry: +11%, TimeQA: +27%, MuSiQue: +7%

**What it does:** Before tackling the specific question, steps back to identify and reason about the underlying principles, frameworks, or abstractions. Grounds the response in fundamentals before applying them.

**Best for:** STEM reasoning and technical troubleshooting. Temporal reasoning (when/sequence questions). Multi-hop reasoning where connecting multiple pieces of knowledge is required. Situations where the user is deep in specifics and needs to zoom out. Domain-heavy questions (physics, chemistry, engineering, data modeling).

**When to avoid:** Tasks already well-abstracted. Simple factual lookups. When the user explicitly wants only a narrow, specific answer without context.

**Cost:** Medium — 2 API calls (abstraction pass + solution pass).

**Reformulation pattern:**
```
Before diving into the specifics, let's ground ourselves.

Step 1 — What are the general principles or frameworks relevant to this domain?
[Identify the abstractions]

Step 2 — Now apply those principles to the specific case:
[Original task]

Start with the foundational reasoning, then narrow to the specific answer.
```

---

#### Self-Refine / Iterative Critique
**Evidence: Strong** | Madaan et al., 2023 (NeurIPS) | +20% average across 7 diverse tasks, code optimization: 22.0 → 28.8

**What it does:** Generates a first draft, then explicitly critiques it against criteria, then revises. Most value comes from the first iteration; diminishing returns after 2-3 passes.

**Best for:** Any deliverable where quality matters — documents, code, presentations, emails. Pairs well with SoT (skeleton first, then draft, then refine). The go-to strategy for polishing output.

**When to avoid:** Time-sensitive tasks where a good-enough first pass is acceptable. Beware that self-feedback can occasionally amplify errors rather than fix them — works best when the model has strong domain knowledge for the task.

**Cost:** Medium-High — 3-5 forward passes for iterative refinement.

**Reformulation pattern:**
```
[Original task]

After producing the initial output, critique it against these criteria:
- Does it fully address the original request?
- Is anything missing, redundant, or unclear?
- Where is the weakest section and why?

Then produce a revised version that addresses every critique point. One revision pass is usually sufficient.
```

---

#### Least-to-Most Decomposition
**Evidence: Strong** | Zhou et al., 2022 | SCAN: 99.7% accuracy with 14 examples (vs. 15,000+ training examples for baseline)

**What it does:** Breaks a complex problem into ordered subproblems, solves each sequentially, and feeds each answer into the next. The key distinction from CoT: the decomposition is explicit and structured upfront, not emergent during reasoning.

**Best for:** Compositional and symbolic problems. Multi-part implementation plans where solving part A unlocks part B. Migration plans, dependency-aware workflows, onboarding sequences. Problems that require generalization beyond shown examples.

**When to avoid:** Problems without clear decomposition. Tasks where components are independent rather than sequential. Situations where parallel exploration (ToT) would be more valuable than sequential building.

**Cost:** Medium — sequential multiple passes, one per subproblem.

**Reformulation pattern:**
```
This is a layered problem. Let's decompose it and solve from the foundation up.

[Original task]

First, identify the subproblems in dependency order (what must be solved before what). Then solve each one sequentially, carrying forward what you learned from each step into the next.
```

---

#### ReAct (Reason + Act)
**Evidence: Strong** | Yao et al., 2022 (ICLR 2023) | ALFWorld: +34%, WebShop: +10% (with external tools)

**What it does:** Interleaves reasoning steps with information-gathering actions. Think, search, reason about findings, search again. The strategy is specifically powerful when tools are available — without tools, it's roughly equivalent to CoT.

**Best for:** Research tasks requiring external information. Fact-finding and investigation. Debugging with logs and error messages. Any task where you need to gather evidence before concluding. Naturally aligns with tool-using workflows in Cowork.

**When to avoid:** Tasks where all information is already in context. Pure reasoning problems. When no external tools or data sources are available (in that case, just use CoT).

**Cost:** Variable — depends on how many tool interactions are needed.

**Reformulation pattern:**
```
This requires research before conclusions. Use a think-act-observe loop:

[Original task]

For each cycle:
1. THINK: What do I need to know next?
2. ACT: Search/fetch/read to find it
3. OBSERVE: What did I learn? Does this change my understanding?

Continue until you have sufficient evidence, then synthesize your findings.
```

---

### Tier 2 & 3 Strategies

For the full details on Tier 2 and Tier 3 strategies, read `references/additional-strategies.md`. Here's the quick reference:

| Strategy | Evidence | Best For |
|----------|----------|----------|
| CoT | Strong but Conditional | Math/symbolic (non-reasoning models only) |
| ToT/AGoT | Moderate-Strong | Complex search, tradeoff evaluation |
| Generated Knowledge | Moderate-Strong | Domain best-practices, commonsense |
| Analogical/Thought Prop. | Moderate | Design patterns, architecture |
| Meta-Prompting | Moderate | Novel/unclear tasks |
| SoT + Self-Refine | Moderate | Speed-critical structured output |

**Excluded:** Role/Persona Prompting (no significant effect in testing)

---

## Step 3: Strategy Selection Logic

Use the task classification profile to select strategies. Prefer Tier 1 strategies when multiple tiers match. Many tasks benefit from **strategy combinations** — a primary strategy with a secondary.

### Selection heuristics (ordered by evidence strength)

| Task Profile | Primary Strategy | Common Combinations |
|-------------|-----------------|-------------------|
| Math / arithmetic / clear right-wrong | **Contrastive** | Contrastive + CoT (non-reasoning models only) |
| High-stakes decision, need confidence | **Self-Consistency (CISC)** | Self-Consistency + Step-Back |
| STEM reasoning, domain-heavy | **Step-Back** | Step-Back + Generated Knowledge |
| Compositional / multi-phase problem | **Least-to-Most** | Least-to-Most + Contrastive per subproblem |
| Research requiring external data | **ReAct** | ReAct + Generated Knowledge |
| Quality-critical deliverable | **Self-Refine** | Self-Refine + Contrastive |
| Complex search / tradeoff evaluation | **ToT** | ToT + Step-Back for grounding |
| Long-form structured document | **Self-Refine** | Self-Refine + outline-first structure |
| Domain best-practices question | **Generated Knowledge** | GK + Step-Back |
| Design pattern / architecture | **Analogical** | Analogical + Generated Knowledge |
| Standard reasoning (non-reasoning model) | **CoT** | CoT + Self-Consistency for higher stakes |
| Classification / pattern recognition | **Direct prompt** | Avoid CoT — it hurts these tasks (ICML 2025) |
| Speed-critical + structured output | **SoT + Self-Refine** (mandatory pair) | Never SoT alone — Self-Refine is the quality gate |
| Novel / unclear task type | **Meta-Prompting** | Meta + whatever it suggests |

### Combination rules

- Maximum 3 strategies per combination (primary + up to 2 supporting)
- The primary strategy defines the overall structure; supporting strategies modify specific phases
- When combining, specify which phase each strategy governs (e.g., "SoT for structure, then Self-Refine on the final draft")
- Prefer Tier 1 primaries with Tier 2-3 supports over the reverse
- **Quality constraint:** Never combine strategies in a way that introduces quality degradation risk without a mitigating quality gate in the same combination. If a strategy has known quality variance (e.g., SoT's 40% degradation), a quality-gating strategy (e.g., Self-Refine) must be part of the same combination — not optional
- **Speed as tiebreaker:** When two combinations produce equivalent quality, prefer the faster one. Speed never justifies a combination that risks lower quality

---

## Step 4: Recommendation Presentation

Present the recommendation in this format:

```
**Strategy:** [Primary] (+ [Secondary] if applicable)
**Evidence:** [Key stat — e.g., "+17.9% on GSM8K (Wang et al., 2022)"]
**Why this fits:** [1-2 sentences explaining why this task profile maps to this strategy]

**Reformulated prompt:**

---
[The user's original intent, restructured using the selected strategy's reformulation pattern]
---

Want me to proceed with this approach, or would you prefer a different strategy?
```

The evidence line matters — it reminds both the user and the executing model why this strategy was chosen, grounding the recommendation in data rather than intuition.

### If the user provides XML input

When the input includes a `<prompt-router>` wrapper or `<strategy>` field in structured-input XML, respect the explicit hints:

- `<strategy>` — Use this strategy instead of auto-selecting (but still present the recommendation with evidence for confirmation)
- `<depth>` — Adjusts exploration depth: `surface`, `moderate`, `deep`
- `<constraints>` — Specific things to include or avoid in the approach
- `<combine>` — Explicit secondary strategy to pair with the primary

If the user's explicit strategy choice seems suboptimal for the task based on the evidence, say so — explain what the research suggests and recommend an alternative, but defer to their preference.

---

## Step 5: Execution Handoff

Once the user approves (or adjusts) the strategy:

1. If the task maps to a downstream skill (e.g., `workflow-doc`, `technical-design-doc`), hand off to that skill with the strategy context embedded in the `<strategy>` extension field
2. If the task is general, execute the reformulated prompt directly
3. Preserve the strategy context throughout execution — don't drift back to default behavior mid-task

---

## XML Schema

### Standalone wrapper

For direct use without another consuming skill:

```xml
<prompt-router>
  <task><![CDATA[
    The user's original request or question goes here.
  ]]></task>
  <strategy>contrastive</strategy>                <!-- optional: override auto-selection -->
  <depth>deep</depth>                             <!-- optional: surface | moderate | deep -->
  <constraints>Focus on Airtable-specific patterns</constraints>  <!-- optional -->
  <combine>self-refine</combine>                  <!-- optional: secondary strategy -->
</prompt-router>
```

### Structured-input extension

When used within the structured-input framework (for skills that consume structured-input):

```xml
<workflow-doc>
  <!-- Base structured-input fields -->
  <client>Zillow</client>
  <solution>Studio Z Planning</solution>
  <brand_color primary="#0041D9" accent="#F2A619" />
  <content><![CDATA[...]]></content>

  <!-- Strategy extension fields (from prompt-strategy-router) -->
  <strategy>step-back</strategy>
  <depth>deep</depth>
  <constraints>Emphasize edge cases in user stories</constraints>
</workflow-doc>
```

### Valid strategy values

`chain-of-thought` | `skeleton-of-thought` | `tree-of-thought` | `step-back` | `least-to-most` | `self-consistency` | `self-refine` | `generated-knowledge` | `analogical` | `react` | `contrastive` | `meta-prompting`

---

## Quick Reference: Strategy Selection by Task

| "I need to..." | Reach for... | Evidence |
|----------------|-------------|----------|
| Solve a math or arithmetic problem | Contrastive (+52.9% GSM8K, validated 2025) | Strong |
| Get high confidence on a decision | Self-Consistency CISC (+17.9% GSM8K) | Strong |
| Solve a deep technical/STEM problem | Step-Back + Generated Knowledge (+27% TimeQA) | Strong |
| Polish a deliverable to high quality | Self-Refine (+20% avg across 7 tasks) | Strong |
| Plan a multi-phase migration | Least-to-Most (99.7% SCAN) | Strong |
| Research a topic with tools | ReAct (+34% ALFWorld with tools) | Strong |
| Debug or trace a logic error | CoT (math/symbolic only; avoid for classification) | Conditional |
| Choose between architectures | ToT/AGoT (+70pts Game of 24, +46.2% GPQA) | Moderate-Strong |
| Apply domain best practices | Generated Knowledge (+6-10%) | Moderate-Strong |
| Recognize a design pattern | Analogical / Thought Propagation (+12-15%) | Moderate |
| Write a long structured document | Self-Refine (outline first, then refine) | Strong |
| Handle a task I can't categorize | Meta-Prompting (+60% Game of 24, Nature 2025) | Moderate |
| Fix a recurring output failure | Contrastive | Strong |
| Generate content faster at equal quality | SoT + Self-Refine (mandatory pair; 2-2.39x speed) | Moderate |
| Classify or sort items | **Direct prompt — no CoT** (ICML 2025: CoT hurts) | Strong (negative) |

---

## Research References

Full citation tables for all included and excluded strategies are in `references/research.md` — read it when you need to verify a specific paper, check a 2025 status update, or cite a source. Last evidence review: March 2026.
