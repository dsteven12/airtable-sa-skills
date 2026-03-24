# Airtable SA Skills

A collection of AI-powered skills for Airtable Solution Architects. These skills run inside [Cowork](https://claude.com) (Anthropic's desktop automation tool) and automate the repetitive parts of SA work — generating deliverables, reviewing architecture, designing automations, and maintaining a structured knowledge base across engagements.

If you're not an SA but work closely with the team (CSMs, PMs, enablement), several of these skills are useful to you too. The [skill inventory](#skill-inventory) section marks which skills are SA-specific and which are broadly applicable.

---

## What This Repo Contains

```
airtable-sa-skills/
├── skills/                  # 26 Cowork skills (the core of the repo)
├── vault-scaffold/          # Obsidian vault template for the Work Brain system
├── claude-md/               # CLAUDE.md configuration template
├── docs/                    # Onboarding guide, architecture docs
└── README.md                # You're here
```

**Skills** are instruction sets that teach Cowork how to do specific tasks. When you ask Cowork to "generate a workflow doc from these call notes," the `workflow-doc` skill provides the structure, brand theming, section templates, and quality standards that turn a vague request into a polished deliverable. Without skills, Cowork produces generic output. With them, it produces SA-grade work.

**The vault scaffold** is an Obsidian folder structure that gives Cowork persistent memory across sessions. Projects, decisions, daily notes, and lessons accumulate over time, so Cowork doesn't start cold every session. It reads what happened last time and picks up where you left off.

**The CLAUDE.md template** is a configuration file that controls when skills fire. Skills have trigger descriptions, but the CLAUDE.md routing table is what makes triggering reliable — it tells Cowork "when the user says X, use skill Y" with enough specificity to avoid misfires.

---

## Quick Start

### Prerequisites

You need three things installed before the skills do anything useful:

1. **Claude Desktop** with Cowork mode enabled
2. **Obsidian** (free, https://obsidian.md) — for the vault / knowledge base
3. **MCP connectors** configured in Claude Desktop:
   - Airtable (required for schema inspection, health checks, and technical design docs)
   - Slack (required for automated reviews)
   - Gmail (required for automated reviews)
   - Google Calendar (required for automated reviews and scheduling)

### Install the Skills

Until the plugin marketplace is live, install skills manually:

1. Clone this repo (or download the ZIP)
2. Copy the contents of `skills/` into your Cowork skills directory
3. Copy `claude-md/CLAUDE.md.template` to your CLAUDE.md and customize the personal sections

For detailed setup, see [docs/ONBOARDING.md](docs/ONBOARDING.md).

### Set Up the Vault

1. Copy the `vault-scaffold/` folder to your preferred location (e.g., `~/Documents/Work Brain`)
2. Open the folder as a vault in Obsidian
3. Edit `05 - Cowork/_preferences.md` with your role, communication style, and tool setup
4. Point Cowork at this folder as your working directory

The vault structure is explained in [How the File System Works](#how-the-file-system-works).

---

## Skill Inventory

### Deliverable Skills — Generate Customer-Facing Documents

These take raw input (call transcripts, meeting notes, base schemas) and produce formatted, branded documents ready for customer delivery.

| Skill | What it produces | Input | Output format |
|-------|-----------------|-------|---------------|
| `workflow-doc` | Technical workflow document with ERD, user stories, workflow diagrams, AI opportunities | Discovery call notes, transcripts, process descriptions | HTML (landscape PDF) |
| `technical-design-doc` | System architecture documentation for a completed Airtable build | Live base via Airtable MCP | HTML (landscape PDF) |
| `training-guide` | End-user training materials with numbered steps and annotated UI descriptions | Video transcripts (VTT/SRT), screen recordings, workflow descriptions | HTML (print-ready) |
| `health-check` | Scalability and risk assessment with severity matrices | Live base via Airtable MCP | .docx |
| `deliverable-qa` | Quality gate — accessibility, print-readiness, content checks | Any HTML deliverable | Pass/fail report |

**Who uses these:** Primarily SAs. CSMs and enablement could use `training-guide` for customer onboarding materials.

### Advisory Skills — Interactive Design and Architecture

These run during active work sessions — when you're designing a schema, reviewing a proposed data model, or debugging an automation. They don't produce standalone documents; they provide expert guidance in conversation.

| Skill | When to use it |
|-------|---------------|
| `airtable-design-advisor` | Reviewing a proposed schema before building. Evaluates linking strategies, field types, scalability risks, computed field density. |
| `automation-architect` | Designing or debugging Airtable automations. Produces structurally correct specs that respect platform constraints (token scoping, Find Records behavior, Repeating Group patterns). |
| `ai-prompt-builder` | Writing prompts for Airtable's AI automation actions (Generate Text, Generate Structured Data). Handles typed field constraints, output schemas, model selection. |
| `customer-scenario-generator` | Creating realistic fictional customer scenarios for demos, workshops, or learning exercises. Produces a company narrative plus an Airtable schema skeleton. |

**Who uses these:** SAs during build and design work. `customer-scenario-generator` is also useful for enablement and sales engineering.

### Custom Extension Development — Build Airtable Extensions

These skills support the full lifecycle of building Airtable Custom Extensions — from scaffolding a new project to building production-quality React UIs.

| Skill | What it does |
|-------|-------------|
| `scaffold-extension` | Scaffolds a new Custom Extension project with git initialized, secrets protected, and context indexing configured. Gets you from zero to a working repo in minutes. |
| `extension-ui` | Builds production-quality Custom Extension UIs with React. Covers component architecture, styling, performance, and accessibility. Includes reference docs for field types, React patterns, shadcn components, and toolkit utilities. |

**Who uses these:** SAs and DCs building Custom Extensions for customer engagements. Also useful for anyone prototyping extension ideas.

### Shared Dependencies — Libraries Read by Other Skills

These aren't invoked directly. They're reference materials that the deliverable and advisory skills read before executing. You don't need to think about them — they just need to be installed.

| Skill | What it provides | Used by |
|-------|-----------------|---------|
| `airtable-design-principles` | Risk heuristics, linking patterns, automation design patterns, naming conventions | design-advisor, automation-architect, health-check, workflow-doc, technical-design-doc |
| `doc-css-framework` | Brand color detection, CSS variables, print-ready component classes | workflow-doc, technical-design-doc, training-guide |
| `base-metadata-extractor` | MCP-based schema extraction plus browser console scripts for automation/interface metadata | technical-design-doc, health-check, training-guide |
| `structured-input` | Input normalization framework — converts any input format into a canonical object | All doc-generating skills |
| `file-input-schema` | XML schema for file-based inputs (uploads, MCP attachments, screenshots) | structured-input |
| `ai-opportunities` | Framework for identifying AI touchpoints in customer workflows | workflow-doc |

### Productivity Skills — Personal Workflow Automation

These require the vault scaffold to work. They manage session context, generate reviews, and maintain the knowledge base.

| Skill | What it does |
|-------|-------------|
| `engagement-orchestrator` | Tracks multi-phase engagements (Align → Design → Build → Deploy → Adopt). Knows which phase you're in, which skills to invoke next, and passes accumulated context forward. |
| `learning-loop` | Two modes: **brief** (session start — sets learning objectives) and **reflect** (session end — extracts discoveries, maps to themes, proposes skill adaptations). |
| `review` | Sweeps Slack, Gmail, Google Calendar, and the vault to generate daily/weekly/monthly/quarterly/yearly work reviews. |
| `session-wrapup` | End-of-session protocol: updates the project log, refreshes the daily note, syncs _context.md, creates decision records. |
| `schedule` | Creates reusable scheduled tasks — automated reviews, recurring reports, reminders. |

**Who uses these:** Anyone using the vault system. The `review` skill is particularly useful for anyone who needs to track what they accomplished across tools.

### Utility Skills — Writing and Development

| Skill | What it does |
|-------|-------------|
| `stop-slop-technical` | Removes AI writing patterns from any prose. Eliminates filler phrases, passive voice, formulaic structures while preserving technical precision. |
| `prompt-strategy-router` | Pre-flight check that selects the optimal prompting strategy before executing non-trivial tasks. Runs automatically. |
| `frontend-design` | Produces high-quality frontend interfaces (React, HTML/CSS) that avoid generic AI aesthetics. |
| `extension-ui` | Builds production-quality Airtable Custom Extension UIs with React and accessibility. |
| `scaffold-extension` | Scaffolds new Airtable Custom Extension projects with git and CI wired in. |
| `skill-creator` | Creates, modifies, evaluates, and optimizes skills. Used to build and maintain the skills in this repo. |

---

## How the File System Works

The vault is an Obsidian-based knowledge base that gives Cowork persistent memory. Without it, every session starts from zero. With it, Cowork reads `_context.md` at the start of each session and knows what you've been working on, what decisions were made, and what's next.

### Folder Structure

```
Work Brain/
├── 00 - Inbox/              Quick capture — unsorted notes, will be triaged later
├── 01 - Projects/           One note per project with running session logs
├── 02 - Clients/            One note per client relationship
├── 03 - Daily/              Daily index notes (auto-generated links to what was worked on)
│   └── action-items/        Dated action item snapshots
├── 04 - Decisions/          Standalone decision records — atomic and linkable
├── 05 - Cowork/             AI working memory
│   ├── _context.md          SESSION BOOTSTRAP — Cowork reads this first, every session
│   ├── _preferences.md      Your patterns, style, naming conventions
│   ├── drafts/              Work-in-progress documents
│   └── reports/             Automated reports
├── 06 - Reviews/            Automated review outputs
│   ├── daily/               Weekday reviews at 5:30 PM
│   ├── weekly/              Friday reviews at 5:00 PM
│   ├── monthly/             1st of month reviews
│   ├── quarterly/           Quarterly summaries
│   └── yearly/              Annual summaries
├── 07 - Artifacts/          Customer deliverables, organized by project
├── Templates/               Obsidian templates for consistent note structure
└── tasks/
    └── lessons.md           Platform lessons — constraints and patterns learned the hard way
```

### How Sessions Work

The system follows a loop: **bootstrap → work → wrapup → review**.

**Session start:** Cowork reads `05 - Cowork/_context.md` and immediately knows your active projects, recent decisions, and pending items. If you reference a specific project, it loads the full session history from `01 - Projects/`.

**During work:** Skills produce deliverables, advisory guidance, and design decisions. Everything is contextual — the workflow-doc skill knows your customer's brand colors, the automation-architect knows which platform constraints to flag, the design-advisor references lessons from prior engagements.

**Session end:** The `session-wrapup` skill runs a 4-step protocol:
1. Appends a session log entry to the project note in `01 - Projects/`
2. Updates today's daily note in `03 - Daily/`
3. Refreshes `05 - Cowork/_context.md` so the next session bootstraps correctly
4. Creates decision records in `04 - Decisions/` if architectural decisions were made

**Automated reviews:** Scheduled tasks sweep Slack, Gmail, Google Calendar, and the vault itself, then generate structured review notes. Daily reviews list deliverables, in-progress items, and key interactions. Weekly and monthly reviews aggregate these into narrative summaries suitable for performance reviews or stakeholder updates.

### Note Conventions

All notes use YAML frontmatter for metadata that Obsidian's Dataview plugin (and Cowork) can query:

```yaml
---
project: "Acme Corp - Inventory Pipeline"
client: "[[Acme Corp]]"
status: in-progress
created: "2026-03-15"
---
```

Cross-references use `[[wikilinks]]` for Obsidian graph connectivity. Session logs use XML blocks (`<session>`, `<decisions>`, `<next_steps>`) with wikilinks inside them, so both the graph and structured parsing work simultaneously.

---

## How Skills Connect to the File System

The skills and the vault aren't independent systems — they feed each other.

When the `workflow-doc` skill generates a deliverable, it lands in `07 - Artifacts/<project>/`. When `session-wrapup` runs, it logs what was produced. When the next session starts, `_context.md` references those artifacts. When the `review` skill runs at end of day, it includes the deliverable in the daily summary.

The `lessons.md` file is where platform constraints accumulate. When the `automation-architect` skill flags a token scoping issue, and you discover a workaround, that gets logged as a lesson. The next time any SA hits the same constraint, the lesson is already loaded in their session context.

The `engagement-orchestrator` skill reads from `01 - Projects/` to determine which phase of the engagement you're in, then recommends which skills to invoke next. It doesn't just track status — it threads context forward, so the training-guide skill knows what was decided in the design phase without you re-explaining it.

---

## Maintenance

### Keeping Skills Current

Airtable's AI features evolve fast. Field Agents, structured data schemas, automation actions — these change quarterly. The skills need to track those changes or they'll give stale guidance.

**What to update and when:**

The `airtable-design-principles` skill is the single most important maintenance target. It's a shared dependency read by 5 other skills. When Airtable ships a new feature that changes architectural guidance (new field types, new automation actions, new risk categories), update this skill first. Everything downstream inherits the change.

The `automation-architect` and `ai-prompt-builder` skills reference specific platform behaviors (which operators Find Records supports, how structured data nesting works, which AI models are available). These need updates when the automation builder UI changes.

The `base-metadata-extractor` uses Airtable's MCP API. If the API adds new endpoints or changes response formats, this skill needs to match.

**How to contribute updates:**

1. Fork this repo
2. Update the skill's SKILL.md (and any reference files in its folder)
3. Update the `last_updated` frontmatter field
4. If the change affects platform constraints, add a lesson to `vault-scaffold/tasks/lessons.md`
5. Submit a PR with a description of what changed and why

### Staleness Detection

If a skill hasn't been updated in 90+ days and Airtable has shipped relevant features in that window, it's probably giving outdated guidance. The `skill-creator` skill includes an eval framework that can test skill outputs against recent engagement artifacts — use it quarterly to catch drift.

---

## Architecture Decisions

### Why Obsidian (not Notion, not Google Docs)?

Obsidian stores everything as local markdown files. Cowork reads and writes files. The match is direct — no API translation layer, no sync delays, no permission issues. The vault is just a folder on your computer that both you and Cowork can access.

Notion and Google Docs would require MCP connectors with rate limits, authentication, and eventual consistency issues. The vault approach gives Cowork instant, reliable read/write access to your full knowledge base.

### Why a Routing Table in CLAUDE.md?

Skill descriptions alone produce roughly 50% triggering accuracy. The CLAUDE.md routing table pushes this above 90% by providing explicit disambiguation rules. "Workflow" during interactive design work shouldn't fire the workflow-doc skill. "Wrap up" at end of session should fire session-wrapup, not review. These distinctions require explicit routing rules that live outside the skill descriptions.

### Why XML Blocks Inside Markdown?

Session logs need to be both human-readable in Obsidian and machine-parseable by Cowork. XML blocks (`<session>`, `<decisions>`, `<next_steps>`) give Cowork structured access to session data. Wikilinks inside the XML blocks maintain Obsidian's graph connectivity. The format serves both readers without compromising either.

### Why Shared Dependency Skills?

Six skills exist solely as reference material for other skills. This avoids duplicating 200+ lines of CSS, design principles, and extraction logic across 10 deliverable skills. When the brand color algorithm changes, you update `doc-css-framework` once. All downstream skills inherit the change.

---

## Contributing

### Adding a New Skill

1. Create a folder in `skills/` with a kebab-case name
2. Add a `SKILL.md` file with YAML frontmatter:
   ```yaml
   ---
   name: your-skill-name
   description: "When this skill should trigger. Be specific — include trigger phrases, use cases, and what it outputs."
   ---
   ```
3. Write the skill instructions in the body of SKILL.md
4. Add the skill to the routing table in `claude-md/CLAUDE.md.template`
5. Add disambiguation rules if the skill's trigger patterns overlap with existing skills
6. Submit a PR

### Updating Lessons

Platform constraints discovered during real engagements should be added to `vault-scaffold/tasks/lessons.md`. Format each lesson as a bold topic sentence followed by the specific constraint and workaround. Include which Airtable feature the lesson applies to so the team can search by feature name.

### Reporting Issues

If a skill produces incorrect output, open an issue with:
- The skill name
- What you asked Cowork to do
- What the skill produced
- What it should have produced
- The Airtable feature version if relevant (e.g., "Structured Data now supports X")

---

## License

Apache 2.0 — See individual skill directories for any additional license terms.
