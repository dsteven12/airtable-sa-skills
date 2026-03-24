# SA Cowork Onboarding Guide

This guide walks you through setting up the full SA toolkit: skills, vault, automated reviews, and the CLAUDE.md configuration. Budget about 60 minutes for initial setup, then 30 minutes for your first guided session.

---

## Step 1: Install Prerequisites (10 minutes)

### Claude Desktop with Cowork

Download Claude Desktop from https://claude.com if you don't have it. Cowork mode should be available under your Airtable team account.

### Obsidian

Download from https://obsidian.md (free for personal use). This is where the vault lives — it's just a folder of markdown files with a nice UI on top.

### MCP Connectors

In Claude Desktop, go to Settings → Connectors and enable:

- **Airtable** — Required. The `health-check`, `technical-design-doc`, and `base-metadata-extractor` skills use it to inspect live base schemas. Without it, those skills can't access your bases.
- **Slack** — Required for `review` skill. The daily/weekly review sweeps your Slack activity.
- **Gmail** — Required for `review` skill. Includes email activity in reviews.
- **Google Calendar** — Required for `review` and `schedule` skills. Reviews include meetings; schedule creates calendar-aware tasks.
- **Figma** — Optional. Used by `frontend-design` and `extension-ui` skills if you work with design files.

Each connector will prompt you to authenticate. Follow the OAuth flow for each one.

---

## Step 2: Set Up the Vault (15 minutes)

### Create the Vault Folder

Copy the `vault-scaffold/` folder from this repo to your preferred location. Most people use `~/Documents/Work Brain`:

```
cp -r vault-scaffold ~/Documents/Work\ Brain
```

### Open in Obsidian

1. Open Obsidian
2. Click "Open folder as vault"
3. Select your `Work Brain` folder
4. Obsidian will index the files and show the folder structure in the left sidebar

### Customize Your Preferences

Open `05 - Cowork/_preferences.md` and fill in:

- **Role & Context** — Your title and what you do (e.g., "Solution Architect, focused on enterprise manufacturing clients")
- **Communication Style** — How you prefer Cowork to interact (direct, exploratory, etc.)
- **Tools & Environment** — Confirm which MCP connectors you have active

The `_context.md` file starts blank — Cowork will populate it as you work. After your first session-wrapup, it'll contain your active projects and session history.

### Install Obsidian Plugins (Optional but Recommended)

These make the vault more useful for manual browsing:

- **Dataview** — Query your notes like a database (filter projects by status, list recent decisions)
- **Templates** — Use the templates in `Templates/` when creating new project notes, daily notes, etc.
- **Calendar** — Visual calendar view linked to your daily notes

---

## Step 3: Install the Skills (10 minutes)

### Option A: From the Plugin Marketplace (when available)

Once the "Airtable SA" plugin is published to the marketplace:
1. In Claude Desktop, go to Customize → Plugins
2. Search for "Airtable SA"
3. Install the plugin

### Option B: Manual Installation (current method)

1. In Claude Desktop, go to Customize → Skills
2. For each skill folder in `skills/`, install the `.skill` file if available, or copy the folder into your Cowork skills directory
3. The skills directory location varies — check Cowork's settings for the exact path

### Verify Installation

Start a Cowork session and ask: "What skills do you have available?" Cowork should list all installed skills. If any are missing, check that the SKILL.md file has valid YAML frontmatter (the `---` delimiters are mandatory).

---

## Step 4: Install the CLAUDE.md Configuration (10 minutes)

The CLAUDE.md file is what makes skills fire reliably. Without it, Cowork guesses when to use each skill based on the description alone — roughly 50% accuracy. With the routing table, accuracy jumps above 90%.

1. Copy `claude-md/CLAUDE.md.template` to your CLAUDE.md location
2. Customize the personal sections (marked with `[CUSTOMIZE]` comments)
3. Leave the skill routing table, disambiguation rules, and document generation standards as-is

The template has comments explaining each section. The critical sections are:

- **Skill Routing Table** — Maps user phrases to skills. Don't edit unless you're adding a new skill.
- **Disambiguation Rules** — Resolves overlapping triggers (e.g., "workflow" during design vs. "workflow doc" as a deliverable request). Don't edit unless you're adding a skill with overlapping triggers.
- **Obsidian Bootstrap Protocol** — Tells Cowork to read `_context.md` first every session and follow the session-end wrapup protocol.

---

## Step 5: Set Up Automated Reviews (10 minutes)

Reviews are the highest-leverage automation in the system. They turn Cowork from a session tool into a persistent work journal.

Start a Cowork session with your Work Brain vault as the working directory and say:

> "Set up my automated review cadences: daily at 5:30 PM weekdays, weekly at 5:00 PM Fridays, monthly on the 1st at 9 AM, quarterly on the 1st of Jan/Apr/Jul/Oct at 9 AM, and yearly on Jan 2nd at 9 AM."

Cowork will use the `schedule` skill to create each task. Each review sweeps your connected sources (Slack, Gmail, Google Calendar, Airtable, vault) and generates a structured note in `06 - Reviews/`.

Daily reviews take about 2 minutes of Cowork's time and produce a note listing your deliverables, in-progress items, key interactions, and decisions for the day. Weekly and monthly reviews aggregate daily reviews into narrative summaries.

---

## Step 6: Run Your First Session (30 minutes)

The best way to learn the system is to use it on a real engagement.

### Warm-Up: Process a Transcript

If you have a recent discovery call transcript or meeting notes:

1. Start a Cowork session with Work Brain as the working directory
2. Paste the transcript and say "Generate a workflow doc from these notes"
3. Watch the `workflow-doc` skill produce a branded HTML document with ERD, user stories, and workflow diagrams
4. Run `deliverable-qa` by saying "QA check this document" before sharing with the customer

### Try the Advisory Skills

Open a base you're currently working on:

1. Say "Review the schema for [base name] — will this scale?"
2. The `airtable-design-advisor` skill will pull the schema via MCP and evaluate linking strategy, computed field density, and automation risk
3. If you're designing automations, say "Design the automations for [workflow]" — the `automation-architect` skill produces structurally correct specs

### End the Session Properly

When you're done:

1. Say "Wrap up the session"
2. The `session-wrapup` skill updates your project log, daily note, and `_context.md`
3. Next session, Cowork will know exactly where you left off

---

## What to Expect in the First Week

**Day 1-2:** You'll spend most of your time in the deliverable skills — workflow-doc, technical-design-doc, health-check. These produce the most visible value immediately.

**Day 3-5:** The advisory skills become more natural. Instead of designing automations from scratch, you'll start saying "Design the automations for this" and iterating on the spec Cowork produces.

**End of Week 1:** Check your `06 - Reviews/daily/` folder. You should have 5 daily reviews. Read through them — they're useful for status updates and weekly reporting.

**Week 2+:** The vault context starts compounding. Cowork references prior session decisions, the engagement-orchestrator tracks which phase you're in, and lessons.md catches platform constraints before they bite you.

---

## Troubleshooting

### Skills not triggering

Check your CLAUDE.md routing table. If a skill isn't firing when you expect, the most common cause is a missing or misworded routing rule. Compare your CLAUDE.md against the template.

### Reviews not generating

Verify that the `schedule` skill created the tasks (ask Cowork "list my scheduled tasks"). Check that Slack, Gmail, and Google Calendar MCP connectors are authenticated — reviews fail silently if a connector's auth has expired.

### Session wrapup not updating the vault

Make sure Cowork's working directory is pointed at your Work Brain vault. If Cowork can't write to the vault folder, the wrapup protocol fails. Check file permissions on the vault directory.

### Skills producing stale Airtable guidance

Check the `last_updated` field in the skill's SKILL.md frontmatter. If it's more than 90 days old, check this repo for updates. Airtable ships AI features frequently — skills need to track those changes.

### "No Airtable bases found" errors

The Airtable MCP connector needs to be authenticated and have access to the workspace containing the base. Re-authenticate in Claude Desktop → Settings → Connectors → Airtable.
