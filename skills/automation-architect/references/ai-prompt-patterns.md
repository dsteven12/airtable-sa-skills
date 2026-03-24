# AI Prompt Design Patterns

This section covers prompt design for both Airtable automation AI actions (Generate Text, Generate Structured Data) and Omni AI features (AI fields, AI-powered search, AI-generated content in interfaces). The principles are the same — the delivery mechanism differs.

## Automation AI vs. Omni AI — When to Use Which

| Scenario | Use Automation AI | Use Omni AI Field |
|----------|------------------|-------------------|
| One-time classification or extraction on a trigger event | ✅ | ❌ |
| Results should never change once written | ✅ | ❌ |
| Output feeds downstream conditional logic or routing | ✅ | ❌ |
| Live, always-current summary visible to users | ❌ | ✅ |
| Display-only enrichment (no downstream logic depends on it) | Either | ✅ |
| High-stakes decision requiring audit trail | ✅ | ❌ |

Key difference: Automation AI actions run exactly once when triggered — results are written to fields and become static. Omni AI fields recalculate when dependencies change or when the record is viewed. For any workflow where the AI output drives routing, assignment, or status changes, use automation AI actions instead.

**Credit cost consideration:** Both automation AI actions and Omni AI fields consume credits from the same pooled monthly budget. Automation AI runs once per trigger — predictable cost. Omni AI fields recalculate on dependency changes and record views — cost scales with table size and edit frequency. For high-volume tables, automation AI with selective triggers is almost always more credit-efficient than Omni AI fields with auto-run enabled.

## Structured Output Schema Design

When designing the JSON schema for a Generate Structured Data action, follow these rules:

1. **One schema key = one Airtable field.** Each key in the schema maps directly to a field on the target table. Name the keys to match the field names (e.g., `risk_verdict` → `AI Risk Verdict`).

2. **Use constrained types for routing fields.** If a field drives downstream conditional logic, constrain its values:
   ```json
   "recommended_action": {
     "type": "string",
     "enum": ["Standard Review", "Senior Review", "Legal Hold"]
   }
   ```
   This prevents the AI from returning unexpected values that don't match any conditional branch.

3. **Always include a confidence score.** The confidence score is the human override signal:
   ```json
   "confidence_score": {
     "type": "number",
     "minimum": 0,
     "maximum": 1,
     "description": "How confident the model is in its classification (0.0-1.0)"
   }
   ```

4. **Boolean flags for downstream branching.** If a yes/no determination drives a conditional:
   ```json
   "auto_renewal_detected": {
     "type": "boolean",
     "description": "Whether the contract contains an auto-renewal clause"
   }
   ```

5. **Nullable fields for conditional data.** If a field only has a value in some cases:
   ```json
   "renewal_date": {
     "type": ["string", "null"],
     "description": "ISO date of the renewal deadline, or null if no renewal clause found"
   }
   ```

6. **Keep the schema under 4 levels of nesting.** Airtable's structured data action supports up to 4 levels of array/object nesting. Flatter is better — each key should map to a single Airtable field.

## Prompt Engineering for Airtable AI Actions

**Prompt structure template:**
```
ROLE: You are a [domain expert]. [One sentence about the task.]

CONTEXT:
[Reference data the model needs — e.g., policy text, configuration rules]
{{[2]: First record: Policy Text}}

INPUT:
[The record data to process]
{{Trigger: Contract Full Text}}

INSTRUCTIONS:
1. [Specific instruction]
2. [Specific instruction]
3. [Constraint — e.g., "If no renewal clause is found, set renewal_date to null"]

OUTPUT:
Return a JSON object matching the provided schema. Every field is required.
```

**Prompt rules:**
- Always include the role and context blocks. The model performs better with explicit framing.
- Reference dynamic tokens explicitly — don't rely on implicit context.
- Include negative instructions ("If X is not found, return null") to prevent hallucination.
- Keep total prompt plus all referenced field values under 64,000 characters.
- If contract text is long, consider truncating to the first N characters with a note: "This is a truncated excerpt. Analyze what is provided."
- **When using low-cost models, keep prompt language direct and imperative** — conditional phrasing ("If X then consider Y") can cause tool-calling errors on lower-tier models. Use "Classify as X, Y, or Z" rather than "If the content seems related to X, you might classify it as..."
- **Be aware of word limits:** lower-powered models cap at ~12,000 words (query + response combined); higher-powered models at ~90,000 words. Responses exceeding the limit are silently truncated — not errored. Design schemas so expected output stays well under the limit.

## Prompt Size Estimation

Before designing the AI step, estimate the prompt size:

```
Prompt template text:       ~500 chars (fixed)
Policy text (referenced):   ~2,000–10,000 chars (varies by policy length)
Contract text (referenced): ~5,000–50,000 chars (varies by contract length)
Schema definition:          ~500 chars (fixed)
─────────────────────────────────────
Total:                      ~8,000–61,000 chars
```

If the estimate approaches 64K, consider:
- Splitting into two AI actions (classification + extraction)
- Truncating input text with a character limit
- Summarizing the reference data before passing it to the classification step

## Omni AI Field Design

When designing Omni AI fields (not automation AI actions):

1. **Use for display-only enrichment.** Omni AI fields recalculate — they are not suitable for driving automation logic or status changes.

2. **Reference only stable fields.** If the AI field references a field that changes frequently, it will recalculate frequently. Reference fields that are set once (e.g., contract text, not status).

3. **Keep prompts concise.** Omni AI fields run on view/open — long prompts slow down the interface experience.

4. **Don't duplicate automation AI outputs.** If an automation already classifies a record and writes `AI Risk Verdict`, don't also create an Omni AI field that re-classifies. Use the automation-written field directly.

5. **Good use cases for Omni AI fields:**
   - Executive summary of a long text field (visible in interface cards)
   - Plain-language explanation of a formula result
   - Dynamic label or tag suggestion based on record content
   - Translation of a field to another language

6. **Credit awareness for auto-run fields.** Auto-run AI fields on large tables can exhaust credits mid-run, leaving some records unprocessed with no error surfaced. Confirm credit headroom before enabling auto-run. For tables with 500+ records, prefer automation-triggered AI with selective conditions over blanket auto-run fields.
