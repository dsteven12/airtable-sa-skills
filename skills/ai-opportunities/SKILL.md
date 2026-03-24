---
name: ai-opportunities
description: "Shared reference for generating the AI Opportunities section in workflow documents. Read by workflow-doc (and potentially technical-design-doc) before rendering the AI-focused section. Provides: the dual-layer framework (business impact + technical context pipeline), AI touchpoint identification protocol, context engineering analysis structure, opportunity card format, and risk/iteration budget heuristics."
---

# AI Opportunities — Reference Skill

Reference framework for generating Section 7 (AI Opportunities) in workflow documents. This skill defines **what to extract, how to analyze it, and how to present it** — the consuming skill (workflow-doc) handles rendering and CSS.

**Consuming skills:** `workflow-doc` reads this file after Step 2 extraction to generate the AI Opportunities section. Future consumers may include `technical-design-doc` (post-build documentation of what was implemented vs. proposed).

---

## When to Generate This Section

Generate the AI Opportunities section when **any** of the following are true:

1. The workflow description includes steps that involve classification, extraction, summarization, evaluation, or transformation of unstructured or semi-structured data
2. The customer describes manual processes that are repetitive and rule-based but require reading/interpreting text
3. The input mentions AI, automation, or intelligent processing
4. The Airtable solution includes long text, rich text, or attachment fields that could serve as AI input

**Always generate this section.** Airtable SAs are mandated to identify AI opportunities in every workflow document, even if the recommendation is "no AI touchpoints identified for this workflow." In that case, include a brief section explaining why (e.g., "All workflows in this solution are structural data management — no unstructured content processing or classification tasks identified").

---

## Core Principle: Context Engineering > Prompt Engineering

The AI Opportunities section is grounded in context engineering — the upstream work of mapping what data each AI step needs, where it lives, and how it gets there. Prompt engineering is the downstream subset: writing the actual instructions once the context pipeline is mapped.

**The framework:**

```
AI Workflow Design = Context Engineering + Prompt Engineering + Output Engineering
```

For each AI touchpoint, the analysis follows this pipeline:

1. **What does this step need to know?** → Context requirements
2. **Where does that data live?** → Source mapping (tables, fields, external APIs)
3. **How does it get to the AI?** → Context routing (field tokens, lookups, prior step output, preprocessing)
4. **Is the data in the right shape?** → Context preparation (cleanup, normalization, semantic tagging)
5. **What does the AI do with it?** → Prompt engineering (role, techniques, instructions)
6. **Where does the output land?** → Output engineering (typed field constraints, format matching)

Steps 1-4 determine iteration budget. Steps 5-6 are where most people start — and where most iteration waste occurs.

---

## Step 1: Identify AI Touchpoints

Scan the extracted workflows (from workflow-doc Steps 2-3) for AI-eligible steps. Classify each touchpoint by **delivery mechanism**:

### Mechanism Types

| Mechanism | What It Is | Context Source | Trigger | Best For |
|-----------|-----------|---------------|---------|----------|
| **Automation AI Action** | Generate Text or Generate Structured Data step within an automation | Token picker: trigger record fields + prior step outputs | Record event, schedule, or button | Multi-step pipelines, extraction into linked records, complex processing chains |
| **AI Field** | AI-powered field on a table that auto-computes | Referenced fields on the same record + lookups | Automatic on field change | Single-record classification, enrichment, summarization. Recalculates when data changes. |
| **Field Agent** | AI agent that can reason across records and access external tools | Multi-record queries, external APIs, file contents | Manual trigger or button | Cross-record analysis, external data integration, multi-step reasoning with tool use |

### Identification Heuristics

Look for these patterns in the workflow description:

**Automation AI Action candidates:**
- "When [record event], automatically [classify/extract/summarize/evaluate]..."
- Any pipeline where AI output feeds into record creation or field updates
- Multi-step processing where each step builds on the prior

**AI Field candidates:**
- "Each [record] should automatically show/indicate/flag [computed value]..."
- Classification or labeling that should stay current when data changes
- Simple enrichment: sentiment, category, summary, priority inference

**Field Agent candidates:**
- "Check [external system] before [decision]..."
- "Review all [records matching criteria] and [synthesize/compare/flag]..."
- Any step requiring access beyond the current record's data or external APIs

---

## Step 2: Analyze Context Pipeline Per Touchpoint

For each identified touchpoint, map the context pipeline using this structure:

### Context Requirements Table

| Field | Description |
|-------|------------|
| **Data Field** | The specific data this step needs (field name or external source) |
| **Source** | Where it lives: table name, linked record path, prior step output, or external API |
| **Hops** | Distance from trigger: 0 = direct field, 1 = lookup/linked/prior step, 2 = chained lookup, E = external |
| **Shape** | Data format: raw text, structured JSON, date, enum, array, etc. |
| **Quality Assessment** | Is this data clean, predictable, variable? What could go wrong? |
| **Risk** | Low / Medium / High — based on quality + hops + constraints |

### Hop Count Heuristics

Hop count predicts context complexity and correlates with iteration budget:

- **0 hops** (direct field): Lowest risk. Data is on the trigger record, controlled format.
- **1 hop** (lookup, linked record, prior step output): Medium risk. Data exists but routing must be verified. Prior step outputs are only as good as that step's accuracy.
- **2 hops** (chained lookup): Higher risk. Must exist as actual lookup fields on the table — Airtable AI features can't traverse links at runtime. Verify these fields exist during schema design.
- **External** (API, file, web): Highest risk. Data quality is outside your control. Agent permissions required. Availability is not guaranteed.

### Output Constraints Table

For each output field the AI populates:

| Field | Description |
|-------|------------|
| **Target Field** | The field name being populated |
| **Field Type** | Airtable field type (date, single select, number, long text, etc.) |
| **Constraints** | Format requirements: ISO 8601 for dates, exact enum values for selects, number ranges, etc. |
| **Risk** | Low (free text) / Medium (needs normalization) / High (typed field silently rejects non-conforming output) |

**Critical gotcha:** Typed fields (date, number, single select, multiple selects) silently reject AI output that doesn't conform to their expected format. This is the #1 source of extraction prompt iterations. Always document these constraints explicitly.

---

## Step 3: Estimate Iteration Budget

Use evidence from the AI Workflow Learnings hub (if connected) or these baseline heuristics:

### Iteration Budget by Task Type

| Task Type | Expected Iterations | Evidence Basis |
|-----------|-------------------|----------------|
| Classification / Synthesis | 1-2 | UC1: 4 prompts averaged 2 revisions each. Fixes were platform compliance, not logic. |
| Preprocessing (Generate Text) | 2-3 | UC2: Preprocessor took 3 revisions. Mechanical task but output format needs to match downstream expectations. |
| Extraction into Typed Fields | 3-5 | UC2: Extractor took 4 revisions. Date formats, enum matching, and boundary disambiguation drove most iterations. |
| Single-record Classification (AI Field) | 1-2 | Based on UC1 classification evidence. Bounded categories + clean input = fast convergence. |
| Agent Configuration | 3-5 | Theoretical — iterations here are business logic tuning (thresholds, decision frameworks), not prompt accuracy. |

### Context Complexity Multiplier

When estimating, adjust for context complexity:

- **All 0-hop inputs, free-text output**: Use baseline
- **Mixed 0-1 hop inputs, some typed outputs**: Baseline × 1.0-1.5
- **2+ hop inputs or external data**: Baseline × 1.5-2.0
- **Multiple typed output fields**: Add 1-2 iterations for format constraint debugging

---

## Step 4: Generate the Dual-Layer Section

The AI Opportunities section serves two audiences simultaneously. **The business layer is always visible. The technical layer is available on request.**

### Business Layer (Customer-Facing)

For each AI touchpoint, include:

#### A. The Problem (Required)
What pain point does this address? Frame in terms the customer experiences daily:
- Time spent on manual task
- Inconsistency between team members
- Items getting missed at volume
- Downstream consequences of the current process

**Language:** Use the customer's vocabulary. "Your team spends 15-30 minutes after every meeting..." not "The unstructured text input requires NLP processing."

#### B. How It Works (Required)
Plain-language description of what the AI does. No technical jargon. Describe the experience from the user's perspective:
- What triggers it (they paste notes, a record is created, they click a button)
- What happens (the system reads the content, identifies items, creates tasks)
- What they see (new records appear, fields get populated, a flag shows up)

#### C. Impact (Required)
Quantify where possible. Include four dimensions:

| Dimension | What to Show |
|-----------|-------------|
| **Time Saved** | Per-occurrence estimate (e.g., "15-30 min/meeting") |
| **Consistency** | Same logic applied every time vs. variable human judgment |
| **Accuracy** | If evidence exists: "12/12 correct in testing." If not: expected accuracy range. |
| **Scale** | How effort changes with volume (ideally: zero marginal effort per new item) |

#### D. What It Takes From Your Team (Required)
Honest assessment of effort — from the customer's side, not the SA's:
- What tables/fields need to exist
- Setup time estimate
- Behavior change required (ideally: none)
- Dependencies on other systems (calendar integration, etc.)

**Effort levels:**
- **Low**: Single field or configuration. 30-60 min setup. No behavior change.
- **Medium**: Table structure + AI configuration. 2-3 hours setup. Minimal behavior change.
- **High**: External integrations or multi-step configuration. Half-day to full-day setup. May require permissions or API access.

#### E. Trade-offs & Limitations (Required)
Be honest about what doesn't work or isn't perfect:
- Input quality dependencies
- Edge cases the AI handles poorly
- Output format limitations (e.g., AI fields produce text, not selectable enums)
- Confidence thresholds and what happens with uncertain results

**This section builds trust.** Customers respect honesty about limitations more than overselling.

#### F. Without This (Required)
What happens if they don't implement this opportunity? Frame as cost of inaction:
- Manual process continues
- Risk of missed items increases with volume
- No audit trail or consistency guarantee

This is not a scare tactic — it's decision context. Sometimes "manual is fine at your volume" is the right answer.

#### G. Dependencies (Required)
What must exist before this opportunity can work:
- Required tables and fields
- External integrations
- Other opportunities that must be in place first (e.g., "Requires Opportunity A to populate the Tasks table")

### Technical Layer (SA Reference)

For each touchpoint, include in a collapsible/expandable section:

- **AI Steps**: Step name, action type (Generate Text / Generate Structured Data / AI Field / Field Agent), model recommendation, and purpose
- **Context Pipeline Table**: Data field, source, hops, shape, quality, risk (from Step 2)
- **Output Constraints Table**: Target field, field type, constraints, risk (from Step 2)
- **Iteration Budget**: Expected iterations with reasoning (from Step 3)
- **Evidence**: Reference to Learning Hub records or past engagements if available. If no direct evidence, note the extrapolation basis.

---

## Step 5: Implementation Recommendation

After presenting all opportunities, include a recommendation section:

### Phase Assignment

Group opportunities into phases based on:
- **Phase 1**: Core value, validated patterns, no external dependencies. Start here.
- **Phase 2**: Extensions that add value once Phase 1 is proven. May have external dependencies.
- **Phase 3**: Aspirational. High value but high complexity or unvalidated patterns.

### Recommendation Matrix

For each opportunity, summarize:

| Opportunity | Phase | Effort | Value | Recommendation |
|------------|-------|--------|-------|---------------|
| A — [Name] | Phase 1 | Medium | High | Start here |
| B — [Name] | Phase 1 | Low | Medium | Add alongside A |
| C — [Name] | Phase 2 | High | High | After A is proven |

### Recommendation Narrative

Write 2-3 sentences explaining the sequencing logic in business terms:
- Why start with X (highest volume pain point, validated, no external deps)
- Why Y comes alongside or after (incremental value, low effort)
- Why Z is Phase 2 (highest complexity, depends on trust in the process)

---

## Step 6: Design Decisions

For any non-obvious architectural choices in the AI pipeline, document:

### Decision Format

For each decision:

1. **Question** — framed as something the customer would ask: "Why two AI steps instead of one?"
2. **Business Answer** — plain language explanation of the reasoning
3. **Technical Rationale** — expandable/collapsible SA reference with pattern names, evidence, and alternatives considered

### Common Design Decisions to Document

- Single-step vs. multi-step extraction (when to add a preprocessor)
- AI Field vs. automation step for classification (recalculation needs)
- Field Agent vs. automation for external data (API access, complexity trade-off)
- Phase sequencing (why certain opportunities depend on others)
- Model selection (when to specify Claude 3.5 Sonnet vs. Auto/GPT-4o)

---

## Step 7: Clarifying Questions

Add AI-specific clarifying questions to the Clarifying Questions section (Section 6 of the workflow doc). These supplement the standard questions — don't duplicate them.

### AI-Specific Question Categories

**Input Quality & Format:**
- "How structured are the [input type] today? Do team members follow a consistent format?"
- "What's the typical length of [input field]? Are there edge cases (very short, very long, multiple topics)?"

**Accuracy Expectations:**
- "How should the system handle items it's uncertain about? Flag for review, or create with a confidence indicator?"
- "Is 90% accuracy acceptable, or does this need human verification on every item?"

**Volume & Scale:**
- "How many [records/meetings/submissions] per week does this process handle?"
- "Is volume expected to grow? This affects whether AI investment is worth the setup cost."

**External Dependencies (if applicable):**
- "Do your team members maintain their [external system] accurately?"
- "Are there permission or security constraints on accessing [external data]?"

**Decision Boundaries:**
- "Are the [categories/classifications] well-defined, or do they overlap?"
- "Who decides when the categories change? How often do they change?"

---

## Evidence Integration

When the AI Workflow Learnings hub is accessible (via Airtable MCP), pull:

1. **Pattern matches**: Search the Patterns table for patterns matching the identified touchpoint types. Include pattern names, validation status, and iteration history.
2. **Technique evidence**: Search the Techniques table (when available) for techniques used in similar task types. Include usage counts and average confidence.
3. **Gotcha warnings**: Search the Gotchas table for gotchas matching the identified mechanism types and output field types. Surface these in the trade-offs section.
4. **Iteration precedent**: Pull Test Summary data from the Prompts table for similar task types to ground iteration budget estimates in real data.

If the hub is not connected, use the baseline heuristics in Step 3. Note in the evidence fields: "Based on baseline heuristics — no hub connection available."

---

## HTML Rendering Notes

When the consuming skill (workflow-doc) renders this section, use these CSS components from the doc-css-framework:

- **Section container**: Standard `.section-header` + `.section-intro`
- **Pipeline diagram**: Use `.workflow-card` with `.flow-node` elements for the visual pipeline
- **Opportunity cards**: Use `.module-card` pattern with:
  - Business layer in the main card body
  - Technical layer in a collapsible `<details>` element
- **Impact metrics**: Use `.stats-bar` + `.stat-chip` for the impact grid
- **Recommendation matrix**: Use `.detail-grid` pattern
- **Design decisions**: Use `.summary-card` with `<details>` for technical rationale
- **Clarifying questions**: Append to existing `.q-cat` section (don't create a separate section)

The consuming skill handles all actual CSS — this skill only specifies which components to use.

---

## Output Checklist

Before the consuming skill finalizes the AI Opportunities section, verify:

- [ ] Every workflow was scanned for AI-eligible steps
- [ ] Each touchpoint classified by mechanism (Automation / AI Field / Field Agent)
- [ ] Context pipeline mapped per touchpoint (data, source, hops, quality, risk)
- [ ] Output constraints documented for every typed target field
- [ ] Iteration budget estimated per touchpoint with reasoning
- [ ] Business layer uses customer vocabulary, no technical jargon
- [ ] Impact quantified with time saved, consistency, accuracy, scale
- [ ] Trade-offs are honest — limitations stated clearly
- [ ] "Without This" section frames cost of inaction, not scare tactics
- [ ] Implementation recommendation includes phasing with rationale
- [ ] Design decisions framed as customer questions with plain-language answers
- [ ] AI-specific clarifying questions added to Section 6
- [ ] Evidence referenced from hub (or baseline heuristics noted if no hub)
- [ ] No source-revealing language (follows doc-css-framework language rules)
