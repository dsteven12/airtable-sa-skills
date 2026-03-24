# Additional Strategies (Tier 2 & Tier 3)

This document contains the full details on Tier 2 and Tier 3 strategies, which have solid or situational evidence but are most effective in specific contexts. For the quick reference version, see the main SKILL.md.

---

## Tier 2: Solid Evidence (Use When Profile Matches)

These strategies have strong evidence in specific contexts but either show modest gains or are effective only in particular task types.

---

### Chain of Thought (CoT)
**Evidence: Strong but Conditional (2025 updates)** | Wei et al., 2022 (Google); ICML 2025 poster; Wharton GenAI Labs 2025

**What it does:** Sequential, step-by-step reasoning where each step builds on the previous one. The foundational prompting strategy — the one everything else builds on.

**Best for:** Mathematical and symbolic reasoning where intermediate steps determine correctness. Debugging with clear causal chains. Tasks where showing work genuinely improves the answer.

**Critical 2025 findings — CoT is NOT universally beneficial:**

1. **Hurts 6 task classes** (ICML 2025): CoT *reduces* performance on implicit statistical learning, visual recognition, and exception-pattern classification — tasks where deliberation hurts humans too. o1-preview showed a **36.3% accuracy DROP** with explicit CoT; GPT-4o dropped 23.1%.

2. **Negligible for reasoning models** (Wharton GenAI Labs, 2025): For models with built-in reasoning (o1, o1-mini), explicit CoT scaffolding adds minimal value and may not justify the increased processing time. These models internalize chain-of-thought reasoning.

3. **Diminishing returns with frontier models** (Meincke et al., 2024): Newer, more capable models reason well by default, making explicit CoT prompting less impactful than it was with earlier models.

**When to AVOID (expanded):** Classification tasks. Pattern-exception tasks. Any task where intuitive/statistical pattern recognition matters more than deliberate reasoning. Tasks targeting reasoning models (o1, o1-mini). Generative tasks where structure matters more than reasoning.

**Cost:** Low — single forward pass.

**Reformulation pattern:**
```
Let's work through this step by step.

[Original task]

Walk through your reasoning at each stage before arriving at a conclusion. Show the logic chain explicitly.
```

---

### Tree of Thought (ToT)
**Evidence: Moderate-Strong (validated 2025)** | Yao et al., 2023 (NeurIPS); AGoT 2025 | Game of 24: 4% → 74% (+70 points). AGoT: +46.2% on GPQA with better cost-efficiency.

**What it does:** Explores multiple reasoning paths in parallel, evaluates each, and can backtrack from dead ends. CoT with branching and pruning.

**2025 update:** Adaptive Graph of Thoughts (AGoT, 2025) dynamically decomposes complex queries into subproblems using a graph structure rather than a tree — achieving comparable results to ToT (+46.2% on GPQA) with significantly better cost-efficiency. Consider AGoT framing for tasks where ToT's computational overhead is a concern.

**Best for:** Complex search-intensive problems. Architecture decisions with genuine tradeoffs. Debugging with multiple hypotheses. Design problems with competing constraints — where the first approach isn't necessarily the best one.

**When to avoid:** Well-defined problems with a single clear solution path (just use CoT). Any task where CoT already performs well — ToT's gains are minimal in those cases. Real-time or latency-sensitive work (10-100x computational overhead).

**Cost:** Very High for full ToT — 10-100x compute. AGoT variant is more cost-effective.

**Reformulation pattern:**
```
I want to explore multiple approaches to this before committing to one.

[Original task]

For each viable approach:
1. Describe the approach and its rationale
2. Identify strengths and risks
3. Note what would make this approach fail

Then evaluate across all approaches and recommend the strongest path, explaining why the alternatives were weaker.
```

---

### Generated Knowledge Prompting
**Evidence: Moderate-Strong** | Liu et al., 2022 (ACL) | NumerSense: +6%, CSQA2: +2%, QASC: +3%, zero-shot: +7-10%

**What it does:** Before answering, first surfaces all relevant domain knowledge, then uses it as context. Primes the model's internal knowledge before applying it.

**Best for:** Commonsense reasoning tasks. Domain-specific questions where the model "knows" things but might not surface them spontaneously. Technical best-practice recommendations. Specialized domains like Airtable architecture, API design, data modeling.

**When to avoid:** Tasks where the user already provided all necessary context. Simple factual lookups. Highly specialized niche domains where generated knowledge risks hallucination. When external research (not internal knowledge) is what's actually needed.

**Cost:** Medium — 2 forward passes (knowledge generation + application).

**Reformulation pattern:**
```
Before answering, surface everything relevant you know about this domain.

Topic context: [Extract the domain/topic from the original task]

What are the key principles, common patterns, known pitfalls, and best practices?

Now apply that knowledge to:
[Original task]
```

---

### Analogical Prompting / Thought Propagation
**Evidence: Moderate (strengthened 2024)** | Yasunaga et al., 2023; Yu et al., 2024 (Thought Propagation) | Analogical: +4% consistent. Thought Propagation: +12% shortest-path reasoning, +13% creative writing, +15% LLM-agent planning.

**What it does:** Auto-generates relevant analogous examples from other domains, then maps the solution pattern onto the current problem. The newer **Thought Propagation** variant (2024) takes this further — it explores analogous problems, solves them, and propagates solutions back to the original problem through an explicit analogy chain.

**Best for:** Design patterns and architecture decisions. Schema design, workflow architecture, system integration patterns. "I've seen something like this before" situations. Thought Propagation is stronger for complex planning and creative tasks where the analogy mapping itself generates novel insight.

**When to avoid:** Truly novel problems with no useful analogies. Cases where surface-level similarity is misleading (the analogy looks right but the underlying dynamics are different).

**Cost:** Medium — 2-3 forward passes (exemplar generation + solving + propagation).

**Reformulation pattern:**
```
This problem likely has analogues in other domains or past solutions.

[Original task]

First, identify 2-3 analogous problems or patterns from other contexts. For the closest analogy, describe how it was solved and map that solution back to the current problem. Note where the analogy breaks down and adjustments are needed.
```

---

## Tier 3: Situational (Use With Awareness of Limitations)

---

### Meta-Prompting
**Evidence: Moderate (strengthened 2025)** | Multiple sources 2024-2025; TextGrad in Nature 2025 | Game of 24: +60% accuracy, Python puzzles: +15%, Sonnet writing: +18%, reasoning suite: 0.772 macro-accuracy vs. 0.64-0.73 static selection

**What it does:** Asks the model to design the optimal prompt for the task before executing it. The model becomes its own prompt engineer. The approach is being validated by frameworks like DSPy (automated prompt compilation) and TextGrad (published in Nature 2025), which treat prompt optimization as a differentiable process.

**Best for:** Novel or ambiguous tasks where no established strategy clearly fits. Fallback when classification is uncertain. Can also be used as a "second opinion" — let the model suggest an approach and compare it to your own selection. Increasingly seen as a paradigm shift: the model optimizes its own approach rather than following a prescribed strategy.

**When to avoid:** Well-understood tasks where a Tier 1 or Tier 2 strategy already works. Simple, clear requests. Results can be variable.

**Cost:** Medium — 2 forward passes (prompt design + execution).

**Reformulation pattern:**
```
Before executing this task, first design the ideal prompt for it.

Task: [Original task]

What information would you need? What structure would produce the best output? What constraints or criteria matter? Write the prompt you wish you'd received, then follow it.
```

---

### Skeleton of Thought (SoT) — Always Paired with Self-Refine
**Evidence: Moderate (efficiency with mandatory quality gate)** | Ning et al., 2023 (ICLR 2024) | 2-2.39x speed improvement across 8 of 12 models. Quality: equal or better in ~60% of cases, degraded in ~40%.

**What it does:** Produces a high-level outline first, then expands each section independently. Designed for parallelized generation — the skeleton enables concurrent expansion of multiple sections.

**Important context:** SoT alone has a 40% quality degradation rate — this violates the cardinal rule. SoT is therefore **never recommended as a standalone strategy.** It is only available as an accelerator paired with Self-Refine, which serves as the quality gate. The SoT pass generates structure and content quickly; the Self-Refine pass catches and corrects any degradation. Together they deliver speed gains while preserving quality parity.

**Best for:** Long-form structured content where speed matters AND a Self-Refine pass will follow: batch document generation, rapid iteration cycles, first-draft generation. The outline-first pattern also prevents front-loading (disproportionate detail in early sections).

**When to avoid:** Any situation where a Self-Refine pass cannot or will not follow. Short-form content where the skeleton overhead exceeds the speed benefit. SoT without Self-Refine is never recommended.

**Cost:** Medium — skeleton pass + expansion passes + mandatory refine pass. Net faster than Self-Refine alone due to the structured skeleton reducing refine scope.

**Reformulation pattern:**
```
Before writing anything, produce an outline with section headers and 1-sentence descriptions of what each section will cover.

[Original task]

Once the skeleton is confirmed, expand each section to full detail, maintaining proportional depth across all sections.

After completing the draft, critique it against these criteria:
- Does each section deliver on the outline's promise?
- Is anything thin, redundant, or structurally imbalanced?
- Where is the weakest section?

Revise to address every critique point.
```

---

## Excluded Strategies (Statistically Insignificant)

The following strategies were evaluated and excluded from the routing catalog due to insufficient or negative empirical evidence:

- **Role/Persona Prompting** — 162 personas tested across 6 models showed no statistically significant effect on output quality (arXiv:2311.10054, arXiv:2402.10811). Larger models were *less* responsive. The only positive result was a niche Jekyll & Hyde ensemble (+9.98%) requiring careful manual design — not practical for automated routing.
