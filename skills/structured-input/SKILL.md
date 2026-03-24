---
name: structured-input
description: "Shared input normalization framework for all doc-generating and analysis skills. Dependency read by consuming skills (workflow-doc, technical-design-doc, health-check, training-guide, etc.) before they process user input. Provides: a base XML input schema, a normalization protocol that converts any input into a canonical object, an extension pattern for domain-specific fields, and file/folder input normalization via file-input-schema. Reference when building new doc-generating skills that accept client context, transcripts, or file attachments as input."
---

# Structured Input Framework

Shared input parsing, normalization, and extension protocol for all Airtable documentation and analysis skills. This file is **read by other skills before they process input** — it is not invoked directly.

**Consuming skills:** `workflow-doc`, `technical-design-doc`, `health-check`, `training-guide`, and any future skill that accepts client context and raw content as input should read this file before parsing user input.

**Dependency:** This skill imports `file-input-schema` for file and folder input normalization. When file-based inputs are detected during Step 0, the file schema's normalization protocol (confidence-tiered prompting, mechanical extraction, contextual inference) runs as a sub-step. Read `file-input-schema/SKILL.md` for the full file schema, field definitions, and prompting rules.

---

## Why This Exists

Claude reads XML natively and reliably — it's the same format used throughout Claude's own tool and prompt infrastructure. By defining a consistent XML schema for skill inputs, we get two benefits: (1) users who know the client name, brand colors, or stakeholders can pass them explicitly and skip guesswork, and (2) Claude has a canonical internal object to work from regardless of whether the input was structured or freeform. This eliminates re-parsing, reduces ambiguity, and makes downstream extraction steps more predictable.

---

## 1. Base XML Schema

Every consuming skill shares these base fields. All fields except `<content>` are optional — users include what they have.

```xml
<input>
  <client>Company or customer name</client>
  <solution>Short solution name (e.g. "Engagement Hub")</solution>
  <brand_color primary="#1E4380" accent="#B09A61" />
  <stakeholders>comma-separated roles (e.g. "ops, finance, team lead")</stakeholders>
  <content><![CDATA[
    Paste transcript, meeting notes, workflow description, or other raw input here.
  ]]></content>

  <!-- File inputs (schema defined in file-input-schema) -->
  <files>
    <file>
      <path>/mnt/uploads/screenshot.png</path>
      <intent>reference</intent>
      <domain>airtable_interface</domain>
    </file>
    <folder>
      <path>/mnt/Work Brain/01 - Projects</path>
      <purpose>project_archive</purpose>
    </folder>
  </files>
</input>
```

**Field behavior when present:**

| Field | When provided | When absent |
|-------|--------------|-------------|
| `<client>` | Skip client-name inference; go straight to brand color verification | Infer from content (look for company names, email domains, meeting titles) |
| `<solution>` | Use as document title / solution label | Infer from content or generate from scope |
| `<brand_color>` | Skip web search entirely; apply hex values directly | Trigger brand color detection algorithm (web search → Airtable fallback) |
| `<stakeholders>` | Use as exact actor/role list in user stories, workflows, personas | Infer roles from content context |
| `<content>` | Main body to extract from | Use conversation context or uploaded files as content source |
| `<files>` | Skip file detection; use declared file/folder entries directly | Scan for file signals (uploads, paths, MCP attachments) per `file-input-schema` protocol |

---

## 2. Extending the Schema

Consuming skills add their own domain-specific fields **inside the same `<input>` wrapper**. The outer tag name can match the skill name for clarity, but the base fields remain the same.

### Extension pattern

```xml
<workflow-doc>
  <!-- Base fields (from structured-input) -->
  <client>Zillow</client>
  <solution>Studio Z Planning</solution>
  <brand_color primary="#0041D9" accent="#F2A619" />
  <stakeholders>Program Manager, Operations Director</stakeholders>
  <content><![CDATA[...]]></content>

  <!-- No additional fields needed for workflow-doc -->
</workflow-doc>
```

```xml
<technical-design-doc>
  <!-- Base fields -->
  <client>Hilton</client>
  <solution>Guest Experience Hub</solution>
  <brand_color primary="#1E4380" accent="#B09A61" />
  <stakeholders>Front Desk Agent, Operations Manager</stakeholders>
  <content><![CDATA[...]]></content>

  <!-- Skill-specific extensions -->
  <base_id>appXXXXXXXXXXXXXX</base_id>
  <workflow_doc_path>/path/to/approved-workflow.html</workflow_doc_path>
</technical-design-doc>
```

```xml
<health-check>
  <!-- Base fields -->
  <client>Acme Corp</client>
  <content><![CDATA[...]]></content>

  <!-- Skill-specific extensions -->
  <base_id>appXXXXXXXXXXXXXX</base_id>
  <partner_name>Integration Partner Inc.</partner_name>
  <base_status>pre-production</base_status>
  <expected_users>150</expected_users>
  <planned_syncs>Jira, Salesforce</planned_syncs>
</health-check>
```

```xml
<training-guide>
  <!-- Base fields -->
  <client>Zillow</client>
  <solution>Content Production Tracker</solution>
  <stakeholders>Editor, Producer, EP</stakeholders>
  <content><![CDATA[...]]></content>

  <!-- Skill-specific extensions -->
  <personas>Editor, Producer, EP</personas>
  <transcript_type>loom</transcript_type>
</training-guide>
```

### Adding extensions to a new skill

When creating a new doc-generating skill that needs additional input fields:

1. Read this file (`structured-input/SKILL.md`) for the base schema and normalization protocol
2. Define your additional fields in your skill's Input Types section
3. Add them to the normalized object in Step 0 (see Section 3 below)
4. Document the field behavior (when present / when absent) following the same pattern as the base fields table

---

## 3. Normalization Protocol

This is the critical step that every consuming skill runs before any extraction or generation. It converts whatever the user provided — structured XML, freeform transcript, uploaded file, or conversational description — into a single canonical object.

### Step 0: Normalize Input

Parse the input into this canonical object:

```
{
  client:        extracted or inferred company name (or null)
  solution:      extracted or inferred solution name (or null)
  brand_primary: hex color if provided or found, else null
  brand_accent:  hex color if provided or found, else null
  stakeholders:  list of roles if specified, else infer from content
  raw_content:   the full transcript / notes / description
  files:         [ ...file entries with metadata and confidence scores ]
  folders:       [ ...folder entries with children and purpose ]
  extensions:    { ...skill-specific fields }
}
```

The `files` and `folders` arrays are populated by the file-input-schema normalization protocol (Steps 0a–0d in that dependency). See `file-input-schema/SKILL.md` for the full field definitions, confidence tiers, and prompting rules.

### Parsing rules

1. **If the input contains recognizable XML tags** (`<client>`, `<content>`, `<brand_color>`, or a skill-named wrapper tag like `<workflow-doc>`), read field values directly from the tags. Parse `<brand_color>` attributes for `primary` and `accent` hex values. Extract `<content>` body (handle `CDATA` if present). Read any extension fields the consuming skill defines.

2. **If the input is freeform text** (no XML tags detected), extract fields through inference:
   - `client` — look for company names in meeting titles, email signatures, participant lists, or explicit mentions
   - `solution` — look for project names, application names, or scope descriptions
   - `stakeholders` — look for role titles, department names, or named participants with titles
   - `raw_content` — the entire input becomes the content body

3. **If the input is a mix** (e.g., the user provides some XML fields but also pastes raw text outside the tags), merge both sources. Explicit XML fields take precedence over inferred values.

4. **If file-based inputs are detected** (uploaded files, file paths in conversation, MCP attachments, folder references, or explicit `<files>` XML block), run the file-input-schema normalization protocol (Steps 0a–0d). This extracts mechanical metadata, infers contextual fields, applies confidence-tiered prompting, and populates the `files` and `folders` arrays in the canonical object. If `<files>` was provided explicitly in XML, use declared entries directly and skip file detection — but still run inference for any contextual fields not provided (intent, project, domain).

### Post-normalization contract

Once the canonical object is built:
- It becomes the **single source of truth** for all downstream steps
- Never re-parse the raw input after normalization
- Consuming skills reference `client`, `brand_primary`, `stakeholders`, etc. from this object — not from the original input
- If a field is null, the consuming skill applies its own fallback logic (e.g., web search for brand colors, Airtable defaults, etc.)

---

## 4. Large Input Chunking Protocol

When the user provides input that exceeds comfortable processing in a single pass — long transcripts (30+ minutes), multi-page specs, large datasets, or multiple source documents — use sequential chunking instead of attempting to process everything at once.

### Why this matters

A wall of text with no markers produces shallower extraction than the same content fed in labeled sections. The normalization protocol (Section 3) assumes it receives manageable input. This section handles the case where it doesn't.

### Protocol

**Step 1: Establish structure before content.**

Before processing any content, identify or create a structural map: table of contents, section headers, speaker turns, or logical break points. Confirm the structure with the user if it's ambiguous.

```
"I see this transcript has 7 agenda items across 45 minutes. I'll process each agenda item separately,
then synthesize across all of them. Here's the structure I'm seeing: [list]. Does this match?"
```

**Step 2: Feed sections sequentially with extraction checkpoints.**

Process each section through normalization independently. After each section, surface what was extracted — key claims, stakeholders mentioned, decisions made, action items — before moving to the next. This creates a correction opportunity between sections.

```
Section 1 processed. Extracted: 2 stakeholder roles (Ops Director, IT Lead), 1 decision (migrate Q3),
3 constraints (no API budget, must integrate with SAP, 500-user scale). Moving to Section 2.
```

**Step 3: Cross-section synthesis after all sections are processed.**

Only after every section has been individually processed, run a synthesis pass that looks across all extracted data for: contradictions between sections, themes that span multiple sections, dependencies or sequencing, and gaps where expected information is missing.

### When to chunk vs. when to process whole

| Signal | Action |
|--------|--------|
| Input fits comfortably in a single message | Process whole — no chunking needed |
| Input is >3000 words of dense content | Chunk by logical sections |
| Input has clear structural markers (headers, timestamps, agenda items) | Chunk along those markers |
| Input is a single unstructured narrative with no break points | Ask the user for structure, or chunk by ~1000-word segments with overlap |
| Multiple source documents | One document per chunk, then cross-document synthesis |

### Integration with normalization

Chunking happens *before* Step 0 normalization. Each chunk produces a partial canonical object. After all chunks are processed, merge the partial objects:

- `client`, `solution`, `brand_*` — use the first non-null value found (these are typically stated once)
- `stakeholders` — union across all chunks, deduplicate
- `raw_content` — concatenate in order (preserve sequence)
- `files` — union across all chunks
- `extensions` — merge, with later chunks overriding earlier ones for same-key conflicts

The merged object then becomes the single source of truth per the post-normalization contract.

---

## 5. Consuming Skill Integration Checklist

When a skill references this framework, verify:

- [ ] `structured-input/SKILL.md` was read before input parsing began
- [ ] Step 0 normalization ran and produced a canonical object
- [ ] XML fields were read directly when present (not re-inferred)
- [ ] Freeform input was handled gracefully when no XML tags were detected
- [ ] Brand color web search was skipped when `<brand_color>` was provided
- [ ] Stakeholder roles from XML were used as actors/personas in the output
- [ ] Skill-specific extension fields were parsed if present
- [ ] File inputs were detected and normalized per file-input-schema protocol (if any files/folders present)
- [ ] Confidence scores were retained for contextual file fields (intent, project, domain)
- [ ] Ambiguous file fields triggered appropriate prompting (flag or ask) per cost-of-wrong-guess matrix
- [ ] The canonical object was the sole source of truth for all downstream steps
