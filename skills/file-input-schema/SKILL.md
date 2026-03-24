---
name: file-input-schema
description: "Shared XML schema and normalization protocol for file-based inputs — uploads, Work Brain files, MCP attachments (Slack, Gmail, Airtable), screenshots, and folder trees. Dependency imported by structured-input during its normalization pass. Defines: file metadata fields, folder tree representation, source provenance tracking, a confidence-tiered prompting protocol for inference vs. flagging vs. asking, and cost-of-wrong-guess thresholds per field."
---

# File Input Schema

Shared schema, normalization rules, and prompting protocol for all file-based inputs. This file is **imported by `structured-input`** during its normalization pass — it is never invoked directly and consuming skills never need to read it.

**Why this exists:** When files arrive as input — uploads, vault references, MCP attachments, screenshots, folder paths — Claude makes implicit guesses about context, intent, and project association. Without a formal schema, those guesses are ad-hoc, inconsistent, and invisible. Wrong guesses compound silently into bad output. This schema forces structured extraction, makes assumptions explicit, and defines when to ask the user instead of guessing.

---

## 1. File Entry Schema

Every file-based input — regardless of source — normalizes into this XML structure. All fields except `path` are optional; the normalization protocol (Section 4) handles inference and prompting for missing fields.

```xml
<file>
  <path>/mnt/uploads/screenshot-2026-03-18.png</path>
  <type>png</type>
  <mime>image/png</mime>
  <size_bytes>245000</size_bytes>
  <modified>2026-03-18T14:32:00Z</modified>
  <source>upload</source>
  <source_context>
    <channel />
    <thread />
    <sender />
    <message />
  </source_context>
  <intent>reference</intent>
  <project>Acme Engagement Hub</project>
  <domain>airtable_interface</domain>
  <description>Screenshot of the Kanban view in the Projects table</description>
</file>
```

### Field Definitions

| Field | What it captures | Example values |
|-------|-----------------|----------------|
| `path` | Absolute file path or MCP resource URI | `/mnt/uploads/data.csv`, `/mnt/Work Brain/01 - Projects/Acme.md` |
| `type` | File extension (lowercase, no dot) | `png`, `csv`, `docx`, `md`, `pdf` |
| `mime` | MIME type when detectable | `image/png`, `text/csv`, `application/pdf` |
| `size_bytes` | File size in bytes | `245000` |
| `modified` | Last modified timestamp (ISO 8601) | `2026-03-18T14:32:00Z` |
| `source` | Where the file originated | `upload`, `work_brain`, `slack`, `gmail`, `airtable`, `local` |
| `source_context` | Provenance metadata from MCP sources | Channel name, thread URL, sender, surrounding message text |
| `intent` | What role this file plays in the current task | `input_to_transform`, `reference`, `output_to_modify`, `evidence`, `template` |
| `project` | Which project or engagement this belongs to | Project name, engagement name, or `null` |
| `domain` | Content domain classification | `airtable_interface`, `error_log`, `data_export`, `document`, `screenshot`, `schema_export`, `transcript`, `design_artifact` |
| `description` | Brief natural-language summary of file contents | Free text |

### Intent Values

| Value | Meaning | Example |
|-------|---------|---------|
| `input_to_transform` | Raw material to be processed into something else | A transcript to become a workflow doc |
| `reference` | Context to inform the work, not directly transformed | A brand guide to pull colors from |
| `output_to_modify` | An existing deliverable to edit or update | A .docx the user wants revised |
| `evidence` | Proof or documentation of a state/issue | A screenshot showing a bug |
| `template` | A structural pattern to follow | A slide deck template to populate |

---

## 2. Folder Tree Schema

When the input is a directory — a vault folder, a project directory, a set of nested files — normalize into this structure. The schema is recursive: each entry can itself contain children.

```xml
<folder>
  <path>/mnt/Work Brain/01 - Projects</path>
  <purpose>project_archive</purpose>
  <naming_pattern>One markdown note per project, prefixed with client name</naming_pattern>
  <file_count>24</file_count>
  <file_types>md</file_types>
  <depth>1</depth>
  <last_modified>2026-03-17T22:15:00Z</last_modified>
  <staleness_days>1</staleness_days>
  <children>
    <file>
      <path>/mnt/Work Brain/01 - Projects/Acme - Engagement Hub.md</path>
      <type>md</type>
      <intent>reference</intent>
      <project>Acme Engagement Hub</project>
    </file>
    <!-- additional children -->
  </children>
</folder>
```

### Folder Fields

| Field | What it captures |
|-------|-----------------|
| `path` | Absolute directory path |
| `purpose` | Folder role: `project_archive`, `inbox`, `output_dir`, `reference_library`, `daily_notes`, `working_dir`, `template_store` |
| `naming_pattern` | Observed file naming convention (free text) |
| `file_count` | Total files (non-recursive) in this directory |
| `file_types` | Comma-separated list of extensions present |
| `depth` | Maximum nesting depth below this folder |
| `last_modified` | Most recent modification timestamp across all contents |
| `staleness_days` | Days since `last_modified` relative to today |
| `children` | Nested `<file>` or `<folder>` entries (populated only when depth ≤ 3 to avoid context bloat) |

### Children Depth Limit

Populate `<children>` recursively only to a depth of 3. Beyond that, summarize with `file_count` and `file_types` only. This prevents context window bloat when scanning deep directory trees. If a specific file deeper than 3 levels is relevant, pull it into the `<files>` collection as a standalone entry.

---

## 3. Collection Wrapper

When multiple files and/or folders are involved in a single input, wrap them in a `<files>` collection inside the `<input>` tag. This is how the file schema integrates with structured-input's existing base schema.

```xml
<input>
  <!-- Base fields from structured-input -->
  <client>Acme Corp</client>
  <solution>Engagement Hub</solution>
  <brand_color primary="#1E4380" accent="#B09A61" />
  <content><![CDATA[...]]></content>

  <!-- File inputs -->
  <files>
    <file>
      <path>/mnt/uploads/interface-screenshot.png</path>
      <type>png</type>
      <source>upload</source>
      <intent>evidence</intent>
      <domain>airtable_interface</domain>
    </file>
    <folder>
      <path>/mnt/Work Brain/01 - Projects</path>
      <purpose>project_archive</purpose>
      <file_count>24</file_count>
    </folder>
  </files>
</input>
```

This allows a single normalized object to contain both narrative content (`<content>`) and file references (`<files>`), which is the common case — a user pastes a transcript AND attaches screenshots.

---

## 4. Normalization Protocol

This protocol runs as part of structured-input's Step 0. When file-based inputs are detected, the following extraction and inference sequence executes.

### Step 0a: Detect File Inputs

Scan the input for file signals:
- Uploaded files in `/mnt/uploads/`
- File paths referenced in conversation
- MCP attachment references (Slack file shares, Gmail attachments, Airtable attachment field values)
- Directory paths or folder references
- Inline file references in `<content>` blocks

If no file signals are detected, skip the file normalization entirely — structured-input proceeds with narrative-only normalization.

### Step 0b: Extract Mechanical Fields

For each detected file, extract fields that can be determined programmatically with certainty:

| Field | Extraction method | Confidence |
|-------|------------------|------------|
| `path` | Direct from file reference | **Certain** |
| `type` | Parse extension from filename | **Certain** |
| `mime` | Derive from extension or `file` command | **Certain** |
| `size_bytes` | `stat` the file | **Certain** |
| `modified` | `stat` the file | **Certain** |
| `source` | Determine from path prefix: `/mnt/uploads/` → `upload`, `/mnt/Work Brain/` → `work_brain`, MCP tool origin → `slack`/`gmail`/`airtable` | **Certain** |
| `source_context` | For MCP sources: extract channel, thread, sender from the MCP response metadata | **Certain** (when MCP provides it) |

For folders, also extract: `file_count` (via `ls | wc -l`), `file_types` (via extension scan), `depth` (via `find`), `last_modified` (via `stat` on most recent file).

These fields are never inferred. Proceed silently — no flagging, no prompting.

### Step 0c: Infer Contextual Fields

For fields that require interpretation, apply inference logic and score confidence based on available signals:

#### `intent` — What role does this file play?

**Inference signals (strongest to weakest):**
1. User's explicit statement ("fix this doc" → `output_to_modify`, "here's the transcript" → `input_to_transform`)
2. Active skill context (workflow-doc is running → uploads are likely `input_to_transform`)
3. File type heuristics (`screenshot` + no editing request → `reference` or `evidence`)
4. Conversation position (file uploaded at start of task → likely `input_to_transform`)

**Cost of wrong guess: HIGH.** Misidentifying intent can send the entire processing pipeline in the wrong direction — transforming a reference doc, or treating an editable deliverable as read-only input.

#### `project` — Which project or engagement does this belong to?

**Inference signals:**
1. File path contains a project name (Work Brain path like `01 - Projects/Acme...`)
2. Active conversation context references a specific project
3. User's recent session history (read from `_context.md`)
4. File content mentions a client or project name

**Cost of wrong guess: MEDIUM-HIGH.** Wrong project association means wrong brand colors, wrong stakeholders, wrong context pulled in. Recoverable but wastes a full processing pass.

#### `domain` — What kind of content is this?

**Inference signals:**
1. File type narrows the domain (`.csv` → likely `data_export`, `.md` in vault → `document`)
2. For images: visual inspection (Airtable UI elements → `airtable_interface`, terminal output → `error_log`)
3. For text files: content keywords and structure
4. Filename conventions (`export-...`, `error-...`, `schema-...`)

**Cost of wrong guess: LOW-MEDIUM.** Domain classification affects how content is interpreted but rarely derails the entire output.

#### `description` — What does this file contain?

**Inference signals:**
1. For text files: read first ~50 lines, summarize
2. For images: visual description of contents
3. For binary files: filename + type heuristics
4. Folder: naming patterns + sample filenames

**Cost of wrong guess: LOW.** Description is context enrichment, not a routing decision.

#### `purpose` (folders only) — What is this folder for?

**Inference signals:**
1. Path conventions (Work Brain structure is well-known: `01 - Projects/` → `project_archive`, `00 - Inbox/` → `inbox`, `03 - Daily/` → `daily_notes`)
2. Content analysis (all `.md` files → likely notes/docs, mixed file types → likely `working_dir`)
3. User's explicit framing

**Cost of wrong guess: MEDIUM.** Wrong purpose affects how systematically the folder is scanned and what metadata is extracted from children.

### Step 0d: Apply Confidence-Tiered Prompting

After inference, each contextual field gets a confidence score. The prompting behavior is determined by the **intersection of confidence level and cost-of-wrong-guess:**

```
                        Cost of Wrong Guess
                   LOW          MEDIUM        HIGH
              ┌────────────┬────────────┬────────────┐
  HIGH conf   │  Silent    │  Silent    │  Silent    │
              ├────────────┼────────────┼────────────┤
  MED conf    │  Silent    │  Flag      │  Flag      │
              ├────────────┼────────────┼────────────┤
  LOW conf    │  Flag      │  Ask       │  Ask       │
              └────────────┴────────────┴────────────┘
```

**Silent** — Proceed without mentioning the inference. Use this for high-confidence inferences regardless of cost, and for low-cost fields even at medium confidence.

**Flag** — Proceed with the inference, but state the assumption explicitly in the response so the user can correct it without breaking flow.

> "Treating `interface-screenshot.png` as a reference screenshot of the Acme Engagement Hub — let me know if it belongs to a different project."

**Ask** — Stop and prompt the user with a structured question that names the specific field and offers concrete options when possible.

> "You uploaded `data-export.csv` but I'm not sure what you'd like me to do with it. Should I:
> (a) Transform this into a formatted report
> (b) Use it as reference data for the current analysis
> (c) Something else?"

### Prompting Format Rules

When asking (not flagging), structure the prompt to minimize user effort:
- Name the file specifically (don't say "the uploaded file")
- State what you *do* know ("I can see this is a PNG screenshot of an Airtable interface")
- Ask about the specific field you're missing ("Which project does this belong to?")
- Offer concrete options when the space of answers is bounded (intent has 5 values — offer them)
- Allow freeform when the space is open (project name could be anything)

### Multiple Files: Batch Prompting

When multiple files arrive simultaneously and several have low-confidence fields:
- Group related questions together (don't ask about each file individually if they likely share context)
- Ask "Do all of these belong to the Acme project?" rather than asking per-file
- If files clearly relate to different projects/intents, ask per-group not per-file

---

## 5. Post-Normalization Output

After normalization, the file data merges into structured-input's canonical object:

```
{
  client:        "Acme Corp",
  solution:      "Engagement Hub",
  brand_primary: "#1E4380",
  brand_accent:  "#B09A61",
  stakeholders:  ["ops", "finance"],
  raw_content:   "...transcript text...",
  files: [
    {
      path:           "/mnt/uploads/screenshot.png",
      type:           "png",
      mime:           "image/png",
      size_bytes:     245000,
      modified:       "2026-03-18T14:32:00Z",
      source:         "upload",
      source_context: null,
      intent:         "evidence",
      project:        "Acme Engagement Hub",
      domain:         "airtable_interface",
      description:    "Kanban view of Projects table showing 5 status columns",
      confidence: {
        intent:      "high",
        project:     "medium",
        domain:      "high",
        description: "medium"
      }
    }
  ],
  folders: [
    {
      path:           "/mnt/Work Brain/01 - Projects",
      purpose:        "project_archive",
      naming_pattern: "Client - Solution Name.md",
      file_count:     24,
      file_types:     ["md"],
      depth:          1,
      last_modified:  "2026-03-17T22:15:00Z",
      staleness_days: 1,
      children:       [ ... ]
    }
  ],
  extensions: { ...skill-specific fields }
}
```

The `confidence` sub-object is retained in the canonical object so consuming skills can make their own decisions about how to handle uncertain fields. A skill with high tolerance for ambiguity (like a general summary) can proceed on medium-confidence fields, while a skill with low tolerance (like health-check producing a formal report) can re-prompt.

---

## 6. Consuming Skill Integration

Consuming skills never read this file directly. They get file-awareness through structured-input. However, skills that process files should be aware of the following:

### File-Aware Skill Checklist

- [ ] Does the skill check for `files` and `folders` in the canonical object?
- [ ] Does the skill know which `intent` values are relevant to its work? (e.g., workflow-doc cares about `input_to_transform`, not `template`)
- [ ] Does the skill handle the case where files are present but `<content>` is empty? (file-only input with no narrative)
- [ ] Does the skill handle the case where `<content>` exists but no files are present? (narrative-only input — the existing behavior)
- [ ] Does the skill check confidence scores for fields it depends on, and re-prompt if needed?
- [ ] For image files: does the skill read the image (via Read tool) when it needs visual content, or rely on `description` when text summary suffices?

### Common Patterns

**Screenshot as documentation input:** `domain: airtable_interface` + `intent: evidence` → The consuming skill should read the image to extract UI details (field names, view configuration, record counts) rather than relying on the description alone.

**CSV as data source:** `domain: data_export` + `intent: input_to_transform` → The consuming skill should parse the file programmatically (read + process) rather than treating it as narrative content.

**Vault file as context:** `source: work_brain` + `intent: reference` → The consuming skill should read the file for context enrichment but not transform it.

**Folder scan for project bootstrap:** `purpose: project_archive` → Use `children` to build a project index; don't re-scan the filesystem.
