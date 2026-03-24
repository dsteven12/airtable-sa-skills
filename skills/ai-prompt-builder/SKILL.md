---
name: ai-prompt-builder
description: "Generate production-ready AI prompts for Airtable automation actions (Generate Text, Generate Structured Data). Use when designing AI steps for automations, writing prompts for Airtable AI actions, or converting task descriptions into automation-ready prompts with XML structure, flat output schemas, and model recommendations. MANDATORY TRIGGERS: AI prompt, write the prompt, generate prompt, prompt for this step, AI action prompt, structured data prompt, prompt engineering for Airtable. ALWAYS invoke when an automation spec includes AI actions and the user needs the actual prompt content — not just the step description. Also invoke proactively when the automation-architect skill produces a spec with AI steps and the next logical step is writing the prompts."
---

# AI Prompt Builder

Generate production-ready prompts for Airtable automation AI actions. Takes a task description, field context, and downstream requirements, and produces an XML-structured prompt with a flat output schema, model recommendation, and field mapping — ready to paste into the Airtable automation builder.

## Prerequisites

Before generating prompts, read:
- **`automation-architect/references/ai-prompt-patterns.md`** — canonical rules for structured output schema design, prompt engineering patterns, and prompt size estimation.
- **`automation-architect/references/platform-reference.md`** — AI action constraints (64K char limit, 4-level nesting max, structured vs. free-text output).
- **`airtable-design-principles/SKILL.md`** — AI Step Design patterns (automation AI vs. Omni AI, confidence scores, error handling, audit trail fields).

## When to Use This Skill

Use when:
- An automation spec includes a Generate Text or Generate Structured Data action and the user needs the prompt content
- A task description needs to be translated into an automation-ready AI prompt
- An existing prompt needs to be restructured for the Airtable builder (XML format, flat schema)
- The user asks "write the prompt for this step" or "what should the AI prompt look like"

Do **not** use for:
- Omni AI field prompts (these are simpler, shorter — handle inline)
- General prompt engineering outside Airtable context
- Deciding whether to use AI in the first place (that's `airtable-design-advisor` or `automation-architect`)

---

## Input Requirements

To generate a prompt, gather these from the user or the automation spec:

1. **Task description** — what the AI step should accomplish (classify, summarize, extract, synthesize, generate)
2. **Input fields** — which trigger/action tokens feed into the prompt (field names + expected content type)
3. **Upstream context** — outputs from previous AI steps that this step should reference
4. **Output requirements** — what fields the AI should produce, what types they are, whether any drive downstream conditionals
5. **Domain context** — who the "user" of this output is (reviewer, manager, system) and what they need from it

If any of these are missing, ask before generating. A prompt built on assumptions about the output schema will break downstream automations.

---

## Prompt Template

Every Airtable automation AI prompt follows this XML structure. The sections are always in this order. Omit sections that don't apply (e.g., `<context>` if there are no upstream AI outputs or metadata fields), but never reorder them.

```xml
<role>
You are a [domain-specific expert role].
Your task is to [one-sentence task statement].
</role>

<context>
[Metadata from trigger fields and upstream AI step outputs]
<field_name>{{token reference}}</field_name>
<upstream_output>{{Step N: key_name}}</upstream_output>
</context>

<input>
[The primary content being processed]
<field_name>{{Trigger: Field Name}}</field_name>
</input>

<instructions>
[Numbered, specific instructions]
[Enum definitions with exact values when output drives conditionals]
[Scoring rubrics with range definitions]
[Negative instructions to prevent hallucination]
[Confidence score instructions with calibration guidance]
</instructions>

<output_rules>
Return a JSON object with the keys defined in the output schema. All fields are required.
[Constraint reminders — exact enum values, no paraphrasing, etc.]
</output_rules>
```

### Why XML

XML tags give the model unambiguous section boundaries. Compared to markdown headers or plain text blocks, XML reduces cases where the model confuses instructions with input content — particularly when the input itself contains structured text or numbered lists.

---

## Output Schema Format

Airtable's Generate Structured Data UI defines output schemas as flat rows: key name, type dropdown, description. No nested JSON objects. Represent schemas in this format:

```
| Key | Type | Description |
|-----|------|-------------|
| summary | string | A 2-3 sentence summary of the content |
| confidence | number | Confidence in the analysis (1-10) |
| risk_level | string | Exactly one of: Low, Medium, High |
```

### Schema Design Rules

1. **One key = one Airtable field.** Each output key maps directly to a field. Name keys to match the target field names in snake_case (e.g., `risk_verdict` → `AI Risk Verdict`).

2. **Constrain values that drive conditionals.** If a downstream Conditional checks `risk_level = "High"`, the schema must constrain the value to an exact set. Put the allowed values in both the instructions (with definitions) and the description column.

3. **Always include a confidence score.** Every AI step that makes a judgment call (classification, assessment, detection) gets a confidence output. This is the human override signal — downstream logic can route low-confidence results to manual review.

   Confidence scale: 1-10 (integers). Include calibration guidance in the instructions:
   - 8-10: Clear input, high certainty in the output
   - 5-7: Some ambiguity in the input, reasonable certainty
   - 1-4: Input is too short, too ambiguous, or outside the model's expertise

4. **Use number type for scores.** Not string. Downstream conditionals compare numerically.

5. **Use string type for enums.** Include the exact allowed values in the description. The instructions section defines what each value means.

6. **Keep schemas flat.** Airtable supports up to 4 levels of nesting in structured output, but flat schemas are easier to map to fields, easier to debug, and don't require parsing. If you find yourself nesting, ask whether the nested structure should be a separate AI step instead.

---

## Prompt Component Patterns

These are reusable patterns extracted from production AI automation prompts. Mix and match based on the task.

### Pattern: Domain Role + Task Framing

The `<role>` block is not decoration — it primes the model for domain-appropriate vocabulary, judgment calibration, and output style.

**Weak:**
```xml
<role>You are an AI assistant that analyzes content.</role>
```

**Strong:**
```xml
<role>
You are a content quality analyst specializing in B2B and B2C marketing content.
Your task is to identify potential issues in a piece of content before it goes to a human reviewer.
</role>
```

The role should name a real professional who would do this task. "Content quality analyst," "managing editor," "compliance reviewer," "contract analyst" — not "AI assistant" or "helpful analyzer."

### Pattern: Tiered Context Injection

When a prompt consumes outputs from upstream AI steps, wrap each in a named XML tag so the model can distinguish between original content and AI-generated analysis:

```xml
<context>
<content_type>{{Trigger: Content Type}}</content_type>
<ai_summary>{{Step 2: summary}}</ai_summary>
<ai_issues>{{Step 3: issues_text}}</ai_issues>
<ai_quality_score value="{{Step 4: quality_score}}" scale="1-10" />
<ai_confidence score="{{Step 3: issue_confidence}}" scale="1-10" />
</context>
```

Use XML attributes (`value=`, `scale=`, `score=`) for numeric values that need scale context. The model calibrates better when it knows the range.

### Pattern: Enum Definition Block

When an output field drives a downstream Conditional, define every allowed value with a clear boundary:

```xml
<instructions>
1. Risk Level — classify as exactly one of these values:
   Low, Medium, High

   Definitions:
   - High: contains potential legal claims, unverified statistics, competitive
     comparisons, health/safety claims, or content that could damage brand reputation
   - Medium: contains opinion presented as fact, aggressive CTAs, culturally
     sensitive references, or claims that are plausible but unverified
   - Low: standard content with no elevated risk indicators
</instructions>
```

The word "exactly" and the explicit list prevent the model from returning variants like "low risk," "LOW," or "Moderate."

### Pattern: Negative Instructions (Hallucination Prevention)

Tell the model what NOT to do when the risk of fabrication is real:

```xml
<output_rules>
Do not invent issues that don't exist — only flag what is actually evidenced in the content.
</output_rules>
```

```xml
<instructions>
If the body is empty or incoherent, return: "Unable to summarize — content appears incomplete."
</instructions>
```

Negative instructions belong in `<instructions>` (for behavior) or `<output_rules>` (for output constraints). Place the most critical constraint — the one that would break downstream logic if violated — in `<output_rules>` where it's the last thing the model reads before generating.

### Pattern: Conditional Brief Logic

When a synthesis step needs to adapt its output based on upstream values, write the conditions explicitly:

```xml
<instructions>
1. If EITHER confidence score is below 6, open the brief with:
   "AI analysis confidence is low for this piece — please apply extra scrutiny
   to [specific areas where confidence is low]."

2. If risk level is High, flag it prominently in the opening sentence.

3. End with exactly one of these recommendations:
   - "Likely approve with minor edits" (quality 7+, risk Low, no High-severity issues)
   - "Needs careful review" (quality 5-6, or risk Medium, or High-severity issues present)
   - "Significant concerns — consider rejection" (quality below 5, or risk High)
</instructions>
```

The conditions map to specific upstream output values. The model applies them as if/else logic. This replaces what would otherwise be a complex Conditional tree in the automation builder — the AI handles the branching internally.

### Pattern: Content-Type Adaptation

When the same prompt processes different content types, include type-specific instructions:

```xml
<instructions>
2. Tailor the summary style to the content type:
   - Blog Post: focus on thesis and target reader
   - Marketing Email: focus on offer, CTA, and audience segment
   - Social Post: focus on hook and intended engagement
   - Ad Copy: focus on value proposition and target demographic
</instructions>
```

This prevents one-size-fits-all outputs. The content type token comes from the trigger record's metadata field.

---

## Model Recommendations

Available providers in Airtable: OpenAI, Anthropic, Meta, Mistral AI, IBM, Google, Amazon. Enterprise admins can restrict which providers are available org-wide. **Omni requires OpenAI and/or Anthropic (Amazon Bedrock) — it will not function if only Gemini, Meta, IBM, or Amazon Titan/Nova are enabled.** Confirm provider availability with the client's admin before designing AI features.

### Credit Cost Awareness

Every AI action consumes credits from a pooled monthly budget. Credit cost scales with three factors: input data volume, model power, and output data volume. Models tagged **"Low cost"** in the Airtable UI consume fewer credits per action.

**Plan allocations (monthly, pooled across all users):**

| Plan | Credits/User/Month | Overage |
|------|-------------------|---------|
| Free | 500 (Editor+) | Cannot purchase — must upgrade |
| Team | 10,000 | Credit packs available |
| Business | Contact Sales | Credit packs via Sales |
| Enterprise Scale | Contact Sales | Credit packs via Sales |

Credits reset monthly — unused credits expire, no rollover.

**High-consumption scenarios to flag during scoping:**
- Large document processing (50–25,000+ pages): 500–1,500 credits per run
- Very large text inputs (100,000+ words): 2,000–5,000+ credits per run
- Internet-enabled Field Agents: additional credits for web content pulled in
- Auto-run AI fields on large tables: can exhaust credits mid-run, leaving some records unprocessed

### Available Models (as of March 2026)

The full model catalog in Airtable, organized by provider and cost tier. Models tagged **"Low cost"** in the UI consume fewer credits per action. All other models are standard/high cost.

**OpenAI:**

| Model | Cost Tier | Notes |
|-------|-----------|-------|
| GPT-4.1 | Standard | **Default model.** Solid general-purpose baseline. |
| GPT-4.1 mini | Low cost | Good cheap option for simple tasks. |
| GPT-5.2 | Standard | Latest flagship. Strong reasoning. |
| GPT-5.1 | Standard | |
| GPT-5 | Standard | |
| GPT-5 mini | Low cost | Budget-friendly with GPT-5 architecture. |
| GPT-5 nano | Low cost | Smallest GPT-5 variant. Bulk summarization candidate. |
| o3 | Standard | Reasoning model. Slower but stronger on multi-step logic. |
| o4-mini | Standard | Lighter reasoning model. |
| GPT-4o | Standard | Previous-gen flagship. Still reliable for enum adherence. |
| GPT-4o mini | Low cost | Previous-gen budget option. Proven in structured data pipelines. |
| o3-mini | Standard | Previous-gen reasoning model. |

**Anthropic:**

| Model | Cost Tier | Notes |
|-------|-----------|-------|
| Claude 4.5 Sonnet | Standard | Latest Sonnet. Strong instruction-following and structured output. |
| Claude 4 Sonnet | Standard | |
| Claude 3.7 Sonnet | Standard | |
| Claude 3.5 Sonnet | Standard | Well-tested for enum adherence, confidence calibration, and complex prompts. |
| Claude 4.6 Opus | Standard | Highest-capability Anthropic model. Reserve for the most complex analysis. |
| Claude 4.5 Opus | Standard | |
| Claude 4.5 Haiku | Low cost | Fast, cheap Anthropic option. Good for bulk categorization. |
| Claude 3.5 Haiku | Low cost | Previous-gen budget option. |

**Meta:**

| Model | Cost Tier | Notes |
|-------|-----------|-------|
| Llama 3.3 70B | Low cost | Weaker at strict enum constraints. Fine for simple extraction, unreliable for conditional-driving outputs. |
| Llama 4 Maverick 17B | Low cost | |
| Llama 4 Scout 17B | Low cost | |
| Llama 3.1 8B | Low cost | Smallest Llama. Summarization only. |
| Llama 3.3 70B (on IBM) | Low cost | Same model, IBM-hosted. |

**Mistral AI:**

| Model | Cost Tier | Notes |
|-------|-----------|-------|
| Mistral Large 3 | Standard | Strongest Mistral option. Less tested in Airtable's structured data pipeline than OpenAI/Anthropic. |
| Ministral 3 14B | Low cost | |
| Ministral 3 8B | Low cost | |

**Google:**

| Model | Cost Tier | Notes |
|-------|-----------|-------|
| Gemini 3 Flash | Standard | |
| Gemini 3 Pro | Standard | |
| Gemini 2.5 Flash | Standard | |
| Gemini 2.5 Pro | Standard | |
| Gemini 2.5 Flash Lite | Low cost | Budget Google option. |

**IBM:**

| Model | Cost Tier | Notes |
|-------|-----------|-------|
| Granite 3 8B | Low cost | Summarization only. Not proven for nuanced analysis. |

**Amazon:**

| Model | Cost Tier | Notes |
|-------|-----------|-------|
| Nova Pro | Standard | |
| Nova Premier | Standard | |
| Nova Lite | Low cost | |
| Nova Micro | Low cost | Smallest Amazon model. |

### Model Performance Notes (as of March 2026)

These observations are drawn from benchmarks, vendor docs, and field testing. Airtable wraps these models — behavior may differ slightly from direct API access — but the behavioral tendencies carry through. Validate with your own test data before committing to a model for production automations.

**Claude Sonnet (4.5, 4, 3.7, 3.5):**
- Strongest instruction-following among available models for complex, multi-part prompts. Outperforms GPT on structured output tasks requiring nuanced judgment.
- Structured outputs enforce schema compliance at the token generation level — the model cannot produce tokens that violate the schema. Near-100% enum adherence on first attempt.
- Claude 4.5 Sonnet is the current best choice for automations where output drives downstream conditionals.

**Claude Haiku (4.5, 3.5) — Low cost:**
- Claude 4.5 Haiku achieves roughly 90% of Sonnet 4.5's performance at a fraction of the cost and runs faster. Best low-cost option for well-defined classification and extraction where the prompt is clear and the task isn't multi-step.
- Strong candidate for replacing GPT-4o mini / GPT-4.1 mini in bulk operations if enum adherence matters.

**Claude Opus (4.6, 4.5):**
- Highest-capability Anthropic model. Reserve for the most complex analysis — multi-document synthesis, expert-level reasoning, or tasks where Sonnet's quality falls short.
- Overkill for classification and extraction. Credit cost is high.

**GPT-4.1 (Default):**
- Airtable's current default model. Solid general-purpose performance. Good for straightforward structured output tasks.
- For strict enum compliance, test against Claude 4.5 Sonnet — Claude's structured output enforcement is more reliable.

**GPT-5.x (5.2, 5.1, 5):**
- Latest OpenAI flagship generation. Stricter schema adherence than GPT-4o. May reject loosely defined schemas that GPT-4o accepted — a good thing for production reliability.
- Strong reasoning capabilities, competitive with Claude Sonnet for complex prompts.

**GPT-4o:**
- Previous-gen flagship. Still reliable for enum adherence and well-tested in Airtable's structured data pipeline.
- Being superseded by GPT-4.1 and GPT-5.x — still a safe fallback.

**o3 / o4-mini (Reasoning models):**
- Best for multi-step classification requiring expert-level reasoning. The model "thinks" before responding, which improves accuracy on complex decisions.
- o4-mini supports tool use and function calling with 128K context; o3-mini does not support function calling — prefer o4-mini for agent-style tasks.
- Slower than standard models. Use for quality-critical decisions, not bulk operations.
- Not tagged Low cost — credit consumption is standard tier or above.

**Meta (Llama) — all Low cost:**
- Every Llama model in Airtable is tagged Low cost. Weakest at strict structured output adherence and enum constraints among all providers.
- Fine for simple summarization and extraction where exact output values don't drive conditionals. Unreliable when output must match an exact enum set.
- Llama 3.1 8B is the smallest — summarization only. Llama 3.3 70B is the strongest Meta option but still trails OpenAI/Anthropic on structured output.

**Mistral (Large 3, Ministral variants):**
- Mistral Large 3 is standard-tier and competitive for general tasks, but less tested in Airtable's structured data pipeline than OpenAI/Anthropic.
- Ministral 3 variants (14B, 8B) are Low cost — consider for simple tasks only.

**Google (Gemini 3.x, 2.5.x):**
- Gemini 3 Pro and 2.5 Pro are strong general-purpose models. Less field-tested for Airtable structured output than OpenAI/Anthropic.
- Gemini 2.5 Flash Lite is the only Low cost Google option — consider for simple summarization.

**IBM (Granite 3 8B) / Amazon (Nova variants):**
- Granite 3 8B is Low cost and small — summarization only, not suitable for nuanced analysis.
- Nova Pro and Nova Premier are standard-tier but less proven for structured output adherence. Nova Lite and Nova Micro are Low cost.

### Model Selection Matrix

Match the model to the task complexity — but factor in credit cost. The relationship is direct: higher-powered models consume more credits per action.

| Task Complexity | Cost Tier | Recommended Models | Rationale |
|----------------|-----------|-------------------|-----------|
| Summarization, simple extraction | Low cost | GPT-4o mini, GPT-5 mini, Claude 4.5 Haiku, Gemini 2.5 Flash Lite | Straightforward comprehension. Bulk-safe — won't burn through credits on high-volume tables. |
| Simple categorization, sentiment, tagging | Low cost | Claude 4.5 Haiku, GPT-4.1 mini, GPT-5 nano | High-volume field agent work. Default to low-cost unless accuracy suffers. |
| Multi-category classification with enums | Standard | Claude 4.5 Sonnet, GPT-4.1, GPT-4o | Strict adherence to exact enum strings. Test across providers — if one returns inconsistent casing, switch. |
| Nuanced qualitative analysis | Standard | Claude 4.5 Sonnet, Claude 3.5 Sonnet | Multi-part instructions, calibrated confidence, avoiding false positives. Strongest instruction-following for complex prompts. |
| Synthesis across multiple upstream outputs | Standard | Claude 4.5 Sonnet, o3 | Conditional logic across prior outputs (thresholds, severity routing). Reasoning models (o3) also strong here. |
| Internet search / Field Agents with web access | Standard+ | GPT-4.1, Claude 4.5 Sonnet, GPT-5.x, o3 | Low-powered models cause tool-calling errors ("Unknown error while using tools with the agent"). Must use standard-tier or above. |
| Complex tool-calling / multi-step reasoning | Standard+ | o3, Claude 4.6 Opus, GPT-5.2 | Conditional phrasing and chained tool use require stronger models. Simplify prompt language if forced to use a lower tier. |
| Translation / cultural adaptation | Standard | Claude 4.5 Sonnet, GPT-4.1 | Cultural nuance requires more than word substitution. Test with native speakers. |

### Word Limits by Model Tier

| Model Tier | Combined Query + Response Limit |
|-----------|-------------------------------|
| Lower-powered models | ~12,000 words |
| Higher-powered models | ~90,000 words |

The 64,000 character prompt limit applies regardless of model. Responses that exceed the model's word limit are **truncated, not errored** — the output silently cuts off. Design output schemas to keep expected responses well under the limit.

### Models to Be Cautious With

- **All Meta (Llama) models** — every Llama model is tagged Low cost. Weaker at strict structured output adherence and enum constraints. Fine for bulk summarization, unreliable for automations where the output drives conditionals.
- **Mistral (Ministral 3 variants)** — Low cost but less tested in Airtable's structured data pipeline. Consider for simple tasks only. Mistral Large 3 is stronger but still less proven than OpenAI/Anthropic flagships.
- **IBM (Granite 3 8B)** — Low cost, small model. Summarization only.
- **Amazon (Nova Lite, Nova Micro)** — Low cost. Less proven for nuanced analysis or structured output adherence.
- **Any low-cost model + complex tool-calling prompts** — can cause errors (e.g., "Unknown error while using tools with the agent"). If encountered, switch to a standard-tier model and simplify prompt language to direct imperatives rather than conditional phrasing.

### Design Guidance for Credit-Conscious Builds

1. **Default to low-cost models for bulk operations.** Categorization, summarization, and tagging across large tables should use "Low cost" tagged models unless accuracy testing shows they can't handle the task.
2. **Reserve high-powered models for complexity.** Internet search, multi-step reasoning, and chained tool-calling prompts need them — but flag the credit impact during scoping.
3. **Avoid enabling "Run automatically" on AI fields for large tables** unless credit headroom is confirmed. Design automation triggers to be as selective as possible to reduce unnecessary credit burn.
4. **Estimate credit burn during discovery.** For each AI feature, estimate volume × complexity tier and flag high-consumption scenarios (document analysis, internet search) as budget line items.
5. **For Enterprise clients, confirm enabled providers first.** Omni's dependency on OpenAI/Anthropic is a hard constraint that can break designs if those platforms are org-restricted.

**Customer demo tip:** Run the same content through a step with different models and compare output quality, confidence calibration, and enum adherence. That comparison is transferable knowledge for model selection conversations with customers.

---

## Prompt Size Estimation

Before writing the prompt, estimate whether it fits within the 64K character limit:

```
Prompt template text:       ~500-1,500 chars (fixed, scales with instruction complexity)
Context fields (metadata):  ~100-500 chars per field
Primary input field:        variable — this is usually the largest component
Upstream AI outputs:        ~200-1,000 chars per referenced step
Schema definition:          ~200-500 chars (fixed)
```

If the primary input field (contract text, article body, meeting transcript) regularly exceeds 40K characters, consider:
- Splitting into two AI steps (classification on truncated text, extraction on full text)
- Truncating the input with an explicit instruction: "This is a truncated excerpt. Analyze what is provided."
- Summarizing long reference data in a prior step before passing to the classification step

---

## Field Mapping Table

Every prompt output includes a mapping table showing where each output key lands:

```
| Output Key | Writes To (Field) | Field Type | Downstream Use |
|------------|-------------------|------------|----------------|
| summary | AI Summary | Long text | Context for Steps 3, 4, 6 |
| risk_level | AI Risk Level | Single select | Conditional in Step 9 |
| confidence | AI Assessment Confidence | Number | Brief logic in Step 6 |
```

The "Downstream Use" column is the critical addition — it flags which outputs are consumed by later steps or conditionals. If an output key feeds a downstream Conditional, its value MUST be constrained (enum, boolean, or numeric threshold).

---

## Output Format

When producing a prompt, deliver it in this structure:

### 1. Step Header
```
### Step N: GENERATE STRUCTURED DATA — [Task Name]
Model: [Recommended model]
```

### 2. Prompt Block
The full XML prompt wrapped in a code fence, with token references using `{{Trigger: Field}}` or `{{Step N: key}}` syntax.

### 3. Output Schema Table
Flat key/type/description table.

### 4. Field Mapping Table
Output key → target field → field type → downstream use.

### 5. Writes To
Single line listing the Airtable fields this step populates.

### 6. Design Notes
Anything the builder needs to know: why this model was chosen, what to watch for in testing, prompt size estimate, dependencies on upstream steps.

---

## Validation Checklist

Before delivering a prompt, verify:

- [ ] XML structure follows the template order: role → context → input → instructions → output_rules
- [ ] Every token reference (`{{Trigger: Field}}`, `{{Step N: key}}`) points to a real field or a prior step's output key
- [ ] Output schema is flat — no nested objects or arrays (unless the nesting is intentional and within 4 levels)
- [ ] Every output key that drives a downstream Conditional has constrained values (enum list or numeric threshold)
- [ ] Confidence score included on every judgment/classification step
- [ ] Negative instructions present for hallucination-prone outputs (issue detection, claim extraction, risk flagging)
- [ ] Enum values match exactly between the instructions definitions and the schema descriptions
- [ ] Prompt size estimate stays under 64K characters with realistic field content
- [ ] Model recommendation included with rationale
- [ ] Field mapping table shows downstream use for every output key
- [ ] Empty/missing input handling specified (what the model returns when the primary input is blank)

---

## Relationship to Other Skills

- **`automation-architect`** — produces the automation spec with AI step placeholders. This skill fills those placeholders with actual prompts. Read the automation spec first to understand trigger tokens, step numbering, and downstream conditionals.
- **`airtable-design-advisor`** — decides whether to use automation AI vs. Omni AI fields. By the time this skill is invoked, that decision is made.
- **`airtable-design-principles`** — provides AI Step Design patterns (confidence scores, audit trail fields, error handling). This skill operationalizes those patterns into concrete prompt content.
