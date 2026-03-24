# Research References

Source citations and evidence summaries for all strategies in the prompt-strategy-router. Each strategy entry in the main SKILL.md references these papers inline — this file provides the full citation index for traceability.

**Last evidence review: March 2026**

---

## Meta-Analyses and Systematic Reviews

| Study | Scope | Key Finding |
|-------|-------|-------------|
| The Prompt Report (Schulhoff et al., 2024-2025) | 1,500+ papers, 58 techniques, 32 researchers | Exemplar quality > technique choice; Self-Consistency "limited effectiveness in comparison" |
| Sahoo et al. systematic survey (2024-2025) | Comprehensive technical survey | Validates strategies work but emphasizes model/task dependence |
| ICML 2025 poster (CoT harm) | 6 task classes, 5 models | CoT reduces performance on classification/pattern tasks; o1 drops 36.3% |
| Wharton GenAI Labs (2025) | Reasoning models analysis | Explicit CoT negligible for o1/reasoning models |

---

## Included Strategies

| Strategy | Key Paper(s) | Key Result | 2025 Status |
|----------|-------------|------------|-------------|
| Contrastive | arXiv:2403.08211; Auto-CCoT 2025; LCP at ICLR 2025 | +52.9% GSM8K; LCP 89%+ win rate | Strengthened |
| Self-Consistency (CISC) | Wang et al., 2022; CISC at ACL 2025 | +17.9% GSM8K; confidence-weighted variant superior | Updated |
| Step-Back | Zheng et al., 2023 (DeepMind) | +27% TimeQA | No contradictions found |
| Self-Refine | Madaan et al., 2023 (NeurIPS); ARIES 2025 | +20% avg across 7 tasks | Validated + extended |
| Least-to-Most | Zhou et al., 2022; DISC/RDoLT 2025 | 99.7% SCAN; hierarchical variants improve further | Validated + extended |
| ReAct | Yao et al., 2022 (ICLR 2023); ACL 2025 dialogue study | +34% ALFWorld | Validated; humans prefer ReAct interactions |
| CoT | Wei et al., 2022; ICML 2025; Wharton 2025 | SOTA on math/symbolic | **Conditional** — hurts 6 task classes, negligible for reasoning models |
| ToT / AGoT | Yao et al., 2023 (NeurIPS); AGoT 2025 | +70pts Game of 24; AGoT +46.2% GPQA | Validated + cost-efficient variant |
| Generated Knowledge | Liu et al., 2022 (ACL) | +6-10% commonsense | Confirmed; not highlighted as top-tier in 2025 surveys |
| Analogical / Thought Propagation | Yasunaga et al., 2023; Yu et al., 2024 | +4% (Analogical); +12-15% (Thought Propagation) | Strengthened with Thought Propagation |
| Meta-Prompting | Multiple 2024-2025; TextGrad in Nature 2025 | +60% Game of 24; 0.772 macro-accuracy | Upgraded from Emerging to Moderate |
| SoT | Ning et al., 2023 (ICLR 2024) | 2-2.39x speed; quality parity in 60% of cases | Re-included as efficiency strategy (Tier 3) |

---

## Excluded Strategies (Evidence-Based)

| Strategy | Key Paper | Reason for Exclusion |
|----------|-----------|---------------------|
| Role/Persona | Multiple, 2023-2024 (arXiv:2311.10054) | No statistically significant effect across 162 personas and 6 models |
