# Field Agent Prompts

Field Agents are AI-powered fields configured in the Airtable UI (right-click a field → Configure). They use **plain-text instructions** — not XML. The prompt surface is different from automation AI actions, but the quality principles (role framing, negative instructions, specificity) apply identically.

## Key Differences from Automation AI Prompts

| Dimension | Automation AI | Field Agent |
|-----------|--------------|-------------|
| Prompt format | XML-structured (`<role>`, `<context>`, etc.) | Plain text |
| Input reference | `{{Trigger: Field}}` tokens | @FieldName references in prompt text. For Deep Match: @ marks field insertion points for BOTH source and match table fields. |
| Output schema | Defined in Structured Data UI (key/type/description) | Determined by field type (linked record, image, text, etc.) |
| Character limit | 64K chars | Field Agent instruction limit (~2-4K chars — shorter) |
| Configuration | In automation builder | In field settings UI |
| Trigger | Event-driven (record created/updated/matched) | Always-on (auto-generate) or manual trigger |

## Field Agent Instruction Template

Field Agent instructions should follow this structure. Keep it concise — every word costs characters.

**General Field Agent template** (non-Deep Match agents):

```
[Role statement — one sentence, name a real professional]

[Task statement — what to do with the source fields]

[Matching/generation criteria — numbered or bulleted, specific]

[Negative instructions — what NOT to do, what to avoid]
```

**Deep Match template** (use this for all Deep Match agents):

The @ symbol marks a field insertion point in the Airtable UI. Use @FieldName for ALL field references — both "This table" (source) and "Match table" (target) fields. This makes every field reference visible and swappable for anyone reusing the prompt.

```
[Role statement — one sentence, name a real professional]

[Task statement — what to match and why]

About this [record type] — read from these fields:
- @SourceField1: [what this field contains]
- @SourceField2: [what this field contains]

About each [match record type] — compare against these fields:
- @MatchField1: [what this field contains]
- @MatchField2: [what this field contains]

Matching rules:
- [Rule referencing both sides: the record's @SourceField vs the match's @MatchField]
- [Additional semantic matching criteria]

Do not match [negative instruction referencing specific @fields].
```

**Why @ on both sides:** The @ is the field insertion marker in the Airtable UI. Using it for match table fields (not just source fields) means anyone copy-pasting the prompt can immediately see which tokens are field references and swap them for their own field names. Without @, match table field names blend into the prose and are easy to miss.

**Total target: 800-1500 characters for Deep Match** (longer than other agents because the dual field listing adds structure). Other agents: 600-1200 characters. Don't over-specify what the model already knows — specify what's unique to THIS use case.

## Agent Type Reference

Each Field Agent type has a fixed output format and specific instruction needs:

**Deep Match** (output: linked records)
- Produces editable linked record fields — users can manually override AI matches
- Instructions should define: what "match" means semantically, matching criteria hierarchy, and exclusion rules
- **Two field selection panels in the UI:**
  - **"This table" fields** — source fields the agent reads about the current record (the record being matched FROM)
  - **"Match table" fields** — fields on the target table the agent reads about potential match candidates
  - By default the agent reviews all fields on the match table; narrowing the selection improves precision and reduces noise
  - Use @FieldName in prompt instructions for BOTH source and match table fields — this marks every field as a visible, swappable insertion point
- When specifying a Deep Match prompt, always document BOTH field sets: "This table" fields AND "Match table" fields
- Critical pattern: negative instructions prevent false positive matches (superficial keyword overlap)
- "Allow linking to multiple records" toggle controls cardinality — turn OFF for 1:1 matching
- "Limit record selection to a view" can scope matches (e.g., only Active requisitions) — the view MUST belong to the match table, not the source table
- Self-referential Deep Match (same table on both sides) is valid for deduplication or similarity detection — select the same fields in both panels

**Build Prototype** (output: web prototype attachment)
- Generates interactive HTML/CSS/React prototypes from spec data
- Instructions should define: visual style, layout expectations, what to render from source fields
- Zero credit cost (AI Labs) — good for iteration
- Cannot consume attachment fields as source inputs — use text fields only
- Multicultural/multilingual context in source fields causes per-market fragmentation — keep source fields to English content

**Generate Image** (output: image attachment, AI Labs)
- Generates images from text descriptions
- Instructions should define: style direction, composition, what to include/exclude
- Cannot render text reliably — instruct "DO NOT include text, words, logos, or captions in the image"
- Product-only or abstract compositions pass content safety filters more reliably than images with human subjects
- For beauty/skincare/fashion domains: expect ~30-50% content policy flag rate when human subjects are rendered

**Research Companies** (output: long text)
- Generates market research from company/product context
- Instructions should scope research to the specific record's domain — without per-record context, output is generic
- Include Product link or Product Name lookup + Content Type as source fields for specificity
- Web Search tool is available but increases credit cost

**Analyze Attachment** (output: long text)
- Reads attachment content (PDFs, images) and produces structured text analysis
- Only agent type that can read attachment fields — other agents cannot
- Output is content-type-aware (extracts different things from different document types)
- Strong for feeding downstream agents — structured output from Analyze Attachment can be referenced by other agents via @field

**Find Image from Web** (output: image attachment)
- Locked-down configuration: Web Search mandatory, model fixed at GPT-4.1
- Fewer configurable options than other agents
- Role in workflow: reference imagery / mood boards, not production assets

**Custom Agents** (output: varies — long text, single/multiple select, number, percent, currency, image, web prototype, deep match, video)
- Created via "Create Custom Agent" in the field agent menu
- Output field type must match the output format (text agent → Long Text, not Attachment)
- Custom text agents cannot consume attachment fields as source inputs

## Field Agent Prompt Patterns

Apply these patterns from the automation prompt section, adapted for plain text:

**Strong role framing** — same principle, shorter format:
```
You are an executive recruiting analyst at a technology-focused search firm.
```
Not: "You are an AI that matches records."

**Dual field listing (Deep Match only).** Explicitly list both source and match table fields in the prompt body with @FieldName markers. This serves two purposes: (1) it tells the agent exactly what to read on each side, and (2) it makes the prompt copy-paste-ready for anyone adapting it to a different base.
```
About this candidate — read from these fields:
- @Background Summary: the candidate's career arc and accomplishments
- @Key Skills: technical and leadership competencies

About each requisition — compare against these fields:
- @Requirements: what the role demands in terms of skills and experience
- @Ideal Candidate Profile: the qualitative description of who fits
```

**Cross-referencing fields in matching rules.** After listing both sides, reference specific @fields from BOTH sides in the matching criteria and negative instructions. This anchors the agent's logic to concrete field content:
```
Matching rules:
- Prioritize semantic fit between the candidate's accomplishments and the requisition's @Requirements and @Ideal Candidate Profile

Do not match when the candidate's @Current Title vs the req's @Role Level shows a seniority gap of more than one level.
```

**Negative instructions are highest-value for Field Agents.** In matching and generation tasks, preventing false positives or hallucinations is more valuable than improving recall. Always include what NOT to match/generate, referencing specific @fields:
```
Do not match based on superficial keyword overlap alone. Do not match when the candidate's @Current Title vs the req's @Role Level shows a seniority gap of more than one level.
```

**Semantic matching guidance** — for Deep Match specifically, define what "similar" or "relevant" means in domain terms:
```
Similar means: a recruiter working on a role for one of these candidates would also want to consider the others.
```

**Domain-specific exclusion rules** — prevent the agent from applying patterns that don't fit the domain:
```
Do not match intel that would require multiple inferential leaps to connect to the candidate.
```

## Field Agent Model Selection

Field Agents have their own model picker. Same models as automation AI, but different cost/quality tradeoffs:

| Agent Task | Recommended Model | Rationale |
|-----------|------------------|-----------|
| Deep Match (small tables, <50 records) | GPT-4.1 mini | Lightweight semantic comparison. Low cost. |
| Deep Match (large tables, 50+ records) | GPT-4.1, Claude 4.5 Haiku | More records = more comparison complexity. |
| Build Prototype | GPT-4.1 | Code generation quality matters. Zero credit cost (AI Labs) makes model choice less cost-sensitive. |
| Generate Image | Default (provider-specific) | Image generation uses dedicated models (not the text model catalog). Limited model choice. |
| Research Companies (with web search) | GPT-4.1, Claude 4.5 Sonnet | Internet-enabled agents need standard-tier models — low-cost models cause tool-calling errors. |
| Analyze Attachment | GPT-4.1, Claude 4.5 Sonnet | Document comprehension benefits from stronger models. |
| Custom agent (simple categorization) | GPT-4.1 mini, Claude 4.5 Haiku | Same as automation: default to low-cost for simple tasks. |
| Custom agent (nuanced analysis) | Claude 4.5 Sonnet | Same as automation: complex judgment needs stronger models. |

## Field Agent Prompt Validation Checklist

Before delivering a Field Agent prompt, verify:

- [ ] Instructions fit within ~2-4K character limit (test by pasting into the UI)
- [ ] Role statement names a real professional, not "an AI assistant"
- [ ] Source fields referenced with @FieldName in instructions match the "This table" fields selected in the UI
- [ ] For Deep Match: "Match table" fields also referenced with @FieldName in the prompt — not just listed in config
- [ ] For Deep Match: prompt uses the dual field listing structure ("About this [record] — read from these fields" / "About each [match] — compare against these fields")
- [ ] For Deep Match: matching rules and negative instructions cross-reference @fields from BOTH sides
- [ ] For Deep Match: view filter (if used) belongs to the match table, not the source table
- [ ] Negative instructions included (what NOT to match/generate)
- [ ] Matching criteria are semantic, not keyword-dependent (for Deep Match)
- [ ] If the agent uses web search tools, model is standard-tier or above
- [ ] Instructions don't over-specify what the model already knows — focus on what's unique to this use case
