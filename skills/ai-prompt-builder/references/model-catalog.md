# Airtable AI Model Catalog

Reference for model selection in Airtable AI features. Updated March 2026.

## Credit Cost Awareness

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

## Available Models (as of March 2026)

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

## Model Performance Notes (as of March 2026)

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

## Model Selection Matrix

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

## Word Limits by Model Tier

| Model Tier | Combined Query + Response Limit |
|-----------|-------------------------------|
| Lower-powered models | ~12,000 words |
| Higher-powered models | ~90,000 words |

The 64,000 character prompt limit applies regardless of model. Responses that exceed the model's word limit are **truncated, not errored** — the output silently cuts off. Design output schemas to keep expected responses well under the limit.

## Models to Be Cautious With

- **All Meta (Llama) models** — every Llama model is tagged Low cost. Weaker at strict structured output adherence and enum constraints. Fine for bulk summarization, unreliable for automations where the output drives conditionals.
- **Mistral (Ministral 3 variants)** — Low cost but less tested in Airtable's structured data pipeline. Consider for simple tasks only. Mistral Large 3 is stronger but still less proven than OpenAI/Anthropic flagships.
- **IBM (Granite 3 8B)** — Low cost, small model. Summarization only.
- **Amazon (Nova Lite, Nova Micro)** — Low cost. Less proven for nuanced analysis or structured output adherence.
- **Any low-cost model + complex tool-calling prompts** — can cause errors (e.g., "Unknown error while using tools with the agent"). If encountered, switch to a standard-tier model and simplify prompt language to direct imperatives rather than conditional phrasing.

## Design Guidance for Credit-Conscious Builds

1. **Default to low-cost models for bulk operations.** Categorization, summarization, and tagging across large tables should use "Low cost" tagged models unless accuracy testing shows they can't handle the task.
2. **Reserve high-powered models for complexity.** Internet search, multi-step reasoning, and chained tool-calling prompts need them — but flag the credit impact during scoping.
3. **Avoid enabling "Run automatically" on AI fields for large tables** unless credit headroom is confirmed. Design automation triggers to be as selective as possible to reduce unnecessary credit burn.
4. **Estimate credit burn during discovery.** For each AI feature, estimate volume × complexity tier and flag high-consumption scenarios (document analysis, internet search) as budget line items.
5. **For Enterprise clients, confirm enabled providers first.** Omni's dependency on OpenAI/Anthropic is a hard constraint that can break designs if those platforms are org-restricted.

**Customer demo tip:** Run the same content through a step with different models and compare output quality, confidence calibration, and enum adherence. That comparison is transferable knowledge for model selection conversations with customers.
