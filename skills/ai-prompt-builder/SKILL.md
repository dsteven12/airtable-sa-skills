---
name: ai-prompt-builder
description: "Generate production-ready AI prompts for Airtable AI features — both Automation AI actions (Generate Text, Generate Structured Data, Generate Images) and Field Agents (Deep Match, Build Prototype, Generate Image, Research Companies, Analyze Attachment, Find Image from Web, custom agents). Use when writing prompts for any Airtable AI action or agent, converting task descriptions into prompt content, or optimizing existing prompts. MANDATORY TRIGGERS: AI prompt, write the prompt, generate prompt, prompt for this step, AI action prompt, structured data prompt, field agent prompt, deep match prompt, build prototype prompt, generate image prompt, agent instructions, prompt engineering for Airtable. ALWAYS invoke when an automation spec includes AI actions, a field agent needs instructions, or the user needs actual prompt content. Also invoke proactively when automation-architect produces a spec with AI steps or when configuring field agents on a new base."
---

# AI Prompt Builder

Generate production-ready prompts for Airtable AI features. Covers two prompt surfaces:

1. **Automation AI actions** — Generate Text, Generate Structured Data, Generate Images. XML-structured prompts with output schemas, pasted into the automation builder.
2. **Field Agents** — Deep Match, Build Prototype, Generate Image, Research Companies, Analyze Attachment, Find Image from Web, and custom agents. Plain-text instructions configured in the field settings UI.

## Prerequisites

Before generating prompts, read:
- **`automation-architect/references/ai-prompt-patterns.md`** — canonical rules for structured output schema design, prompt engineering patterns, and prompt size estimation.
- **`automation-architect/references/platform-reference.md`** — AI action constraints (64K char limit, 4-level nesting max, structured vs. free-text output).
- **`airtable-design-principles/SKILL.md`** — AI Step Design patterns (automation AI vs. Omni AI, confidence scores, error handling, audit trail fields).

## When to Use This Skill

Use when:
- An automation spec includes a Generate Text, Generate Structured Data, or Generate Images action and the user needs the prompt content
- A Field Agent needs instructions (Deep Match, Build Prototype, Generate Image, custom agents, etc.)
- A task description needs to be translated into an automation-ready AI prompt or agent instruction
- An existing prompt needs to be restructured or optimized
- The user asks "write the prompt for this step," "what should the agent instructions look like," or "optimize the Deep Match prompt"

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

### Model Catalog & Selection

For the full model catalog, performance notes, selection matrix, credit cost guidance, and caution flags, read **`references/model-catalog.md`**. Key quick-reference points:

- **Claude 4.5 Sonnet** is the current best choice for automations where output drives downstream conditionals (strongest enum adherence and instruction-following).
- **Claude 4.5 Haiku** and **GPT-4o mini** / **GPT-4.1 mini** are the go-to low-cost options for bulk categorization and summarization.
- **Internet-enabled agents and complex tool-calling prompts require standard-tier models** — low-cost models cause tool-calling errors.
- Always confirm provider availability with Enterprise admins before designing AI features (Omni requires OpenAI and/or Anthropic).

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

## Field Agent Prompts

For the complete Field Agent prompt guide — templates, agent type reference, prompt patterns, model selection, and validation checklist — read **`references/field-agent-guide.md`**.

Key points to keep in mind:
- Field Agents use **plain-text instructions** (not XML), configured in the field settings UI
- Character limit is ~2-4K chars (much shorter than automation AI's 64K)
- Use **@FieldName** for all field references — both source and match table fields
- Deep Match prompts should use the dual field listing structure and include negative instructions to prevent false positive matches
- Internet-enabled agents require standard-tier models — low-cost models cause tool-calling errors

---

## Generate Images (Automation AI Action)

Generate Images is an AI Labs automation action that produces images from text prompts. Available in the automation builder alongside Generate Text and Generate Structured Data.

### Prompt Format

Generate Images uses a **plain-text prompt** (not XML). The prompt describes what to generate. Unlike Generate Text/Structured Data, there is no output schema — the output is an image attachment.

```
[Subject description — what appears in the image]
[Style direction — artistic style, color palette, mood]
[Composition — layout, framing, perspective]
[Exclusion rules — what to avoid]
```

### Key Constraints

- **Cannot render text reliably.** Brand names, captions, taglines, and fine print come out garbled. Always instruct: "Do NOT include any text, words, titles, captions, logos, or brand names in the image."
- **Content safety filters.** Images with photorealistic human faces/bodies may trigger content policy flags. Product-only, abstract, or scenic compositions are safer. For beauty/skincare domains, expect ~30-50% flag rate.
- **Token references work.** You can inject field values into the prompt: `Create a hero image for {{Trigger: Product Name}} featuring {{Trigger: Product Description}}`.
- **Position as inspiration tier.** AI-generated images are useful for mood boards, creative direction, and placeholder assets — not production-ready marketing materials.

### Generate Images Prompt Pattern

```
Create a [style] image of [subject].

Composition: [layout description — centered product shot, lifestyle scene, flat lay, etc.]
Color palette: [specific colors or mood — warm earth tones, bright pastels, brand blue #2D7FF9]
Mood: [aesthetic direction — minimalist, luxurious, energetic, clinical]
Lighting: [natural daylight, studio, golden hour, dramatic shadows]

DO NOT include any text, words, titles, captions, logos, or brand names in the image.
DO NOT include human faces. Focus on [product/abstract/scene].
```

### Model Selection for Generate Images

Generate Images uses image generation models (e.g., DALL-E, Imagen), not the text model catalog. The model picker may offer fewer choices. Credit cost scales with image resolution and complexity.

---

## Relationship to Other Skills

- **`automation-architect`** — produces the automation spec with AI step placeholders. This skill fills those placeholders with actual prompts. Read the automation spec first to understand trigger tokens, step numbering, and downstream conditionals.
- **`airtable-design-advisor`** — decides whether to use automation AI vs. Omni AI fields. By the time this skill is invoked, that decision is made.
- **`airtable-design-principles`** — provides AI Step Design patterns (confidence scores, audit trail fields, error handling). This skill operationalizes those patterns into concrete prompt content.
