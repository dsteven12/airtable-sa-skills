---
name: airtable-design-advisor
description: "Pre-build Airtable architecture advisor that reviews proposed data models, linking strategies, and automation designs before anything is built. MANDATORY TRIGGERS: design review, schema review, linking strategy, will this scale, high cardinality, architecture decision, design patterns, how should I structure this. ALWAYS invoke this skill when a proposed Airtable schema or automation pattern is being discussed and there are design tradeoffs to evaluate, even if the user doesn't explicitly say 'design review.'"
---

# Airtable Design Advisor

An interactive pre-build design reviewer that evaluates proposed Airtable architectures against platform behaviors, scalability patterns, and known anti-patterns. This skill is meant to be used conversationally — it produces a structured advisory, not a document.

The goal is to catch design problems before they are built in. A schema decision that takes 30 seconds to change during design can take days to migrate in production.

---

## Prerequisites

**Before producing any advisory**, read:
- **`airtable-design-principles/SKILL.md`** — the canonical risk heuristics, linking strategy framework, automation design patterns, AI design patterns, and naming conventions. All advisory content is drawn from this reference. Do not generate risk flags, linking recommendations, or automation guidance from memory — load and apply the principles file.
- **`automation-architect/SKILL.md`** and **`automation-architect/references/platform-reference.md`** — when the advisory includes automation architecture (Section 4), read these for the complete trigger/action reference, structural constraints (Terminal Block Rule), and the structured spec output format. If the user asks to see automation specs during a design review, output them using the automation-architect format.

---

## When to Use This Skill

Use this skill whenever:
- A proposed data model is being described or refined (tables, fields, relationships)
- A linking strategy decision needs to be made (Linked Record vs. Collaborator, display-only links, hub records)
- An automation architecture is being designed (trigger choices, branch logic, AI steps)
- Scale considerations are relevant (concurrent users, record volume, hub record cardinality)
- A design choice involves an Airtable-specific pattern (horizontal vs. vertical scaling, AI fields vs. automation AI actions)

Do **not** use this skill to generate documents (use `workflow-doc` or `technical-design-doc`) or to assess a live base post-build (use `health-check`).

---

## Input

Accept architecture input in any form:
- Conversational description ("I'm thinking about having a Contracts table linked to a Policy Library...")
- Draft field lists (table names + field names in any format)
- An existing base ID to inspect via MCP (`list_tables_for_base`, `get_table_schema`)
- Mixed — some tables described, some inspectable via MCP

If the user provides a base ID or table name that can be inspected via the Airtable MCP connector, inspect it. Otherwise, work from what was described.

---

## Advisory Structure

Produce the advisory as a structured conversational response with these sections. Only include sections where there is something meaningful to say — don't pad.

### 1. Design Strengths
Briefly acknowledge what is well-designed. This grounds the review and is not filler — good patterns deserve positive reinforcement so they are repeated.

### 2. Risk Flags
Apply the **Risk Heuristics** from `airtable-design-principles/SKILL.md` to the proposed design. Use the **design-time thresholds** (ratio-based, cardinality patterns) — not the inspection thresholds, which apply to live bases.

For each identified risk:
- Name the risk
- Rate severity: **Critical** / **High** / **Medium** / **Low**
- Describe what happens at scale or under load (be concrete — cite approximate thresholds from the principles)
- Propose a mitigation that fits the current design

Only flag risks that are actually evidenced by the design. Do not generate generic warnings.

### 3. Linking Strategy Recommendations
Evaluate every linked record relationship and recommend the appropriate strategy using the **Linking Strategy Framework** in `airtable-design-principles/SKILL.md`. Name the pattern (1–5) and explain why it fits.

**When recommending Pattern 3 (Hybrid):** Also specify the sync automation variant. Hybrid links require an automation to keep the Collaborator field and Linked Record field in sync — without it, they drift silently. The variant depends on the collaborator field type:

- **Single collaborator** → Find Records → Repeating Group → Update Record (3-step, no code). This is the default recommendation. See the Collaborator Sync pattern in `automation-architect/SKILL.md`.
- **Multi-collaborator** → Script action (token picker can't expand multi-collaborator fields). Only recommend when the use case genuinely requires multiple assignees per record — the Script adds maintenance complexity.
- **Sync direction matters.** The standard direction is Collaborator → Linked Record (collaborator is the source of truth, linked record follows for reporting). If the user needs bidirectional sync (e.g., reassignment via a People interface that updates the collaborator), flag this as added complexity requiring a second automation.

### 4. Automation Architecture Recommendations
If automations are described, evaluate for queue saturation, implicit chains, double-trigger risks, and error handling gaps using the **Automation Design Patterns** in `airtable-design-principles/SKILL.md`. For structural validation (Terminal Block Rule compliance, nesting depth, token scope), apply the constraints from `automation-architect/references/platform-reference.md`. If the user wants to see full automation specs, output them using the **automation-architect output format** (structured tree with numbered action IDs, Y/N branch encoding, token references, and Gotchas section).

### 5. AI-Specific Design Patterns
If AI fields or automation AI steps are involved, apply the **AI Step Design** patterns from `airtable-design-principles/SKILL.md`.

### 6. Clarifying Questions for Scale
Ask 2–4 targeted questions about usage patterns, record volumes, and concurrent users that would change the design recommendations. Only ask questions whose answers would materially change the advice.

---

## Output Checklist

Before delivering the advisory, verify:
- [ ] `airtable-design-principles/SKILL.md` was read before generating any advisory content
- [ ] Only flagged risks evidenced by the proposed design — no generic padding
- [ ] Design-time thresholds used (not inspection thresholds)
- [ ] Every linked record relationship has a recommended strategy (Pattern 1–5) from the principles
- [ ] Every Pattern 3 (Hybrid) recommendation includes the sync automation variant (single vs. multi-collaborator) and sync direction
- [ ] Automation risks evaluated (queue saturation, implicit chains, double-trigger, error handling, Terminal Block Rule)
- [ ] If automation specs were requested: `automation-architect/SKILL.md` was read and output format applied
- [ ] AI-specific patterns applied if AI steps or fields are involved
- [ ] Clarifying questions are targeted — only questions whose answers would change the recommendations
- [ ] Design strengths acknowledged — not just risks
- [ ] Severity ratings applied to each risk (Critical / High / Medium / Low)
