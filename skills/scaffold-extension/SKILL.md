---
name: scaffold-extension
description: "Scaffold a new Airtable Custom Extension project with git initialized, secrets protected, and GitNexus context indexing wired into Claude Code. Use ONLY when the user explicitly requests creating a new extension project — phrases like 'scaffold an extension', 'new extension project', 'spin up a new repo'. Do NOT trigger on general mentions of extensions, building features, or UI work — those are handled by extension-ui."
---

# Scaffold Extension Project

This skill walks through creating a new Airtable Custom Extension project with the full dev environment in place: git initialized with the Airtable identity, secrets protected via `.gitignore`, environment variable template, and GitNexus indexing so Claude Code has full codebase context.

## What's assumed to already be set up

- `~/work/` directory with `~/work/.templates/` (`.gitignore` and `.env.example`)
- `~/work/new-extension.sh` scaffolding script (executable)
- GitNexus globally configured (`npx gitnexus setup` run once)
- GitHub CLI (`gh`) authenticated

If any of these are missing, check the setup guide at:
`~/Documents/Work Brain/05 - Cowork/git-setup/SETUP-GUIDE.md`

## Step 1: Get the project name

If the user hasn't provided a project name, ask for one. Suggest this naming convention:

`<customer>-<description>-ext`

Examples: `acme-inventory-ext`, `usaf-calendar-ext`, `hmart-dashboard-ext`

Keep it lowercase with hyphens. Avoid spaces or underscores.

## Step 2: Run the scaffolding script

```bash
~/work/new-extension.sh <project-name>
```

This handles:
- Creating `~/work/<project-name>/`
- Initializing git (your Airtable email kicks in automatically via the conditional gitconfig)
- Copying `.gitignore` (secrets excluded) and `.env.example` from `~/work/.templates/`
- Creating the initial commit
- Running `npx gitnexus analyze` to index the codebase

If the script isn't found, run the steps manually:

```bash
mkdir -p ~/work/<project-name>
cd ~/work/<project-name>
git init
cp ~/work/.templates/.gitignore .gitignore
cp ~/work/.templates/.env.example .env.example
cp ~/work/.templates/.env.example .env
git add .gitignore .env.example
git commit -m "Initial commit: project scaffold"
npx gitnexus analyze
```

## Step 3: Create a private GitHub repo

Ask the user if they want to push to GitHub. Default: yes.

```bash
cd ~/work/<project-name>
gh repo create <project-name> --private --source=. --remote=origin --push
```

## Step 4: Verify everything is wired up

Run a quick sanity check:

```bash
cd ~/work/<project-name>
echo "Git identity:" && git config user.email
echo "Git status:" && git status
```

Expected:
- `git config user.email` → your Airtable corporate email
- `git status` → clean working tree

## Step 5: Next steps to share with the user

After scaffolding, remind them:

1. Add their `AIRTABLE_PAT` and any other secrets to `.env` (never committed)
2. The `.env.example` documents what vars are needed — keep it updated as vars are added
3. GitNexus will auto-reindex after commits via the PostToolUse hook — no manual re-runs needed
4. To push future changes: `git add -A && git commit -m "message" && git push`

## Troubleshooting

| Problem | Fix |
|---|---|
| `new-extension.sh: command not found` | Run `chmod +x ~/work/new-extension.sh` then try again |
| GitNexus analyze fails | OK to continue — run `npx gitnexus analyze` manually later from the project dir |
| GitHub push fails | Run `gh auth status` to check auth, `ssh -T git@github.com` to check SSH |
| Wrong email on commits | Verify `~/work/.gitconfig` exists and has the Airtable email |
