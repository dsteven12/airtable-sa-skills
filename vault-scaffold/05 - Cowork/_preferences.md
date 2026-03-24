---
purpose: user-preferences
last_updated:
tags:
  - cowork
  - preferences
---

# Working Preferences

> This file captures patterns, conventions, and recurring instructions so they don't need to be repeated each session. Updated when new preferences are identified.

## Role & Context
- [Your role] at Airtable
- Builds Airtable solutions for enterprise customers
- Creates technical documentation (workflow docs, TDDs, training guides, health checks)

## Communication Style
- [Adjust to your preference — direct vs. exploratory, concise vs. detailed]

## Task Specification Quality
- **Stranger Test:** Before executing a non-trivial task, read the spec back as if a stranger had to start working on it. If they'd need to ask five follow-up questions before they could begin, the spec is too vague. Stop and clarify before building.
- This applies to: skill prompts, automation specs, document generation briefs, customer deliverable scopes, and any multi-step task description

## Technical Preferences
- Airtable-first architecture

## Document Generation
- Brand-aware: always search for customer brand colors first, fall back to Airtable palette
- No references to source material in customer-facing output
- Landscape PDF optimized with proper print CSS

## Naming Conventions
- Skills: kebab-case folder names matching YAML frontmatter `name` field
- Projects: "Client Name - Project Name" format
- Decisions: descriptive sentence format (e.g., "Use linked records over lookups for Acme")
- Artifacts: filed by project subfolder in `07 - Artifacts/`

## Vault Hygiene Rules
- **Vault root** should only contain: numbered folders (00–07), `Templates/`, `Welcome.md`, and `tasks/`
- **Session deliverables** (HTML, JSX, PDF, XLSX, etc.) go to `07 - Artifacts/<project>/` — never left in root
- **Quick capture** goes to `00 - Inbox/` and gets triaged to its permanent home later
- Session-wrapup protocol should flag any new root-level files for relocation

## Tools & Environment
- Obsidian vault: "Work Brain" in ~/Documents
- Review system: automated daily/weekly/monthly/quarterly/yearly reviews via scheduled tasks, outputs to `06 - Reviews/`
- MCP connectors: Airtable, Slack, Gmail, Google Calendar
