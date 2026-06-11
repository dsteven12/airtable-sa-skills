---
name: post-mortem-doc
description: "Generate a branded, decision-first engagement post-mortem / read-out as a .docx for Services leadership — diagnoses what happened on an at-risk or completed delivery, answers the retrospective questions leadership is asking, and lands a consolidated forward plan. TRIGGERS: post-mortem, read-out, retro doc, root-cause write-up, RCA, lessons-learned doc, delivery review for leadership, at-risk engagement read-out, partner co-delivery post-mortem, 'write this up for leadership', 'document what went wrong'. ALWAYS invoke when the user wants a leadership-facing account of a delivery that slipped, escalated, or just finished — even if they only say 'turn this into a read-out' or 'write up the CSI situation.' Pulls from connected sources (Slack, Gong, Gmail, Airtable) plus provided inputs. Do NOT use for pre-build workflow docs, completed-base docs, end-user guides, or a pure decision/options paper with no retrospective (executive-brief)."
---

# Engagement Post-Mortem / Read-Out

Produces a leadership-facing `.docx` that explains a delivery that went sideways (or just finished), answers the specific questions leadership is holding, and closes with a forward plan. The audience is internal — a manager, Services/PS leadership, an account team. It reads as the SA's own analysis, owns what we missed without defensiveness, and is built to be skimmed in five minutes.

This is a **decision/diagnosis document, not an analytical narrative.** The reader should know the situation and the recommendation within the first screen, then find evidence that supports it — not be walked through a journey of discovery.

## Order of operations (do not skip)

1. **Gather the facts first.** A post-mortem is only as good as its sourcing. Before writing anything, pull what you can from connected sources and from whatever the user provided.
2. **Confirm the frame.** Identify the customer, the partner (if any), the audience, the status, and — most important — *the specific questions leadership is asking*. Those questions become the situational sections.
3. **Only then build the doc** using `scripts/postmortem_docx.py`.

Writing the document before the facts are in produces confident-sounding filler. Resist it.

## Step 1 — Gather inputs

Use connected sources when available, plus anything the user pasted or uploaded:

- **Slack** — the engagement channel and escalation threads. Read escalation threads *in full*; the six-point complaint, the partner's response, and the "who said what" live here.
- **Gong** — discovery, check-in, and escalation calls. Direct quotes from these are the strongest evidence in the doc.
- **Gmail** — customer-facing commitments, change-order/scope emails, sign-off language.
- **Airtable / Solution Hub** — record counts, hours, roster, timeline of record.
- **Provided files** — transcripts, notes, SOWs, prior read-outs, screenshots.

Capture: status and dates; the headline issues; who's who (customer / partner / internal); the timeline of decisions; record/hour/scope numbers; and direct quotes with attribution.

**Sourcing discipline.** This is an internal doc, so a short "Sources & confidence" note at the end naming Gong/Slack is appropriate and builds trust. But the **body must read as the SA's own analysis** — never "the transcript says" or "according to the recording" in the narrative. Put the citation in parentheses at the point of evidence (e.g., *"(Gong, May 28 — Furth: '…')"*) or in the appendix, not as the voice of the prose. Mark partner-reported or unconfirmed figures as such.

## Step 2 — Architecture

A fixed core spine, plus situational sections driven by the actual questions leadership asked. Not every engagement needs every section — include a section only if it carries weight.

### Core spine (almost always)

```
TITLE BLOCK        title · subtitle (pillars, "·"-separated) · meta (status · date · partner · audience)
WHERE THINGS STAND status key-value table: Status / Where it stands now / Top risks / In motion
EXECUTIVE SUMMARY  ownership-first; the honest read; recovery path; the structural lesson
[SITUATIONAL]      the numbered answer-sections — one per question leadership asked (see below)
WHAT IT'S COSTING  commercial reality: over-scope, informal slips, no priced mechanism
[STRUCTURAL]       the deeper lesson, if there is one (e.g., "The Co-Delivery Problem")
PLAN FOR FUTURE …  the consolidated forward commitments, as a table, by lifecycle stage
APPENDIX TIMELINE  numbered decision/event table with a "timeline impact" column
ROSTER & SOURCES   who's who; sources & confidence note
```

### Situational answer-sections (adaptive)

The middle of the doc answers the questions leadership is actually holding. On one engagement that was three: a retrospective risk assessment, a straight UAT answer, and "what a design-review checkpoint should have looked like and why it didn't happen." On another it might be a go-live go/no-go recommendation, an integration-risk ranking, or a root-cause analysis of a timeline slip. **Make each leadership question its own numbered section.** A retrospective-risk section works well as a table: *what surfaced · when we should have caught it · what would have caught it.*

### The structural section (when the failure is systemic)

If the engagement exposes a pattern bigger than this one account — partner co-delivery dynamics, pre-sales misalignment, a missing organizational gate — give it a named section. This is where you tell leadership "we're not just fixing this one, we're naming the class of problem." For partner-delivered work the recurring themes are: the limits of coaching a partner mid-flight, where accountability actually lives (contracting + gates, not coaching), the start trigger (an AE clearing a partner to begin before delivery is ready), and resourcing continuity (key-person loss on critical-path work like migration).

### The forward plan — centralize it

The single most common structural mistake is scattering the go-forward fixes as a "what I'll do next time" tail on every section. **Pull them into one section** — a table organized by lifecycle stage (contracting → before build → before hours → before UAT → before cutover → throughout). Each prior section then ends on its *diagnosis* and lets the plan own the *commitment*. If a reader asks "so what changes?", they should find one place that answers it completely.

## Step 3 — Editorial rules

These are what separate a read-out that moves leadership from one that reads as AI filler. Apply them on every pass.

**Lead with the decision, own the miss.** The Executive Summary states the situation and the honest read in the first few sentences — what's true, what we missed, what's being done. No throat-clearing, no defensiveness. "I came in after the design was built and billed, so I trusted work instead of reviewing it" lands; "a confluence of factors contributed to suboptimal outcomes" does not. Owning the gap cleanly is more credible than explaining why it wasn't our fault.

**Point at things; don't describe them.** Every judgment sentence should survive "show me." Replace categories with the concrete consequence: not "scope was growing" but "the build lead found two junction tables we didn't scope"; not "performance issues" but "1–2s lag creating a task." Numbers, named things, named people — these can't be swapped for the word "stuff." Abstract noun phrases that can be ("instrumented oversight," "engagement velocity," "the transactional layer") should be rewritten.

**Cut the AI cadence.** These tells make a manager feel the doc was generated rather than written:
- Meta-labels that announce instead of inform — "The honest read:", "Straight answer:", "The common thread:", "Net:". Cut the label; let the sentence carry itself.
- Em-dash dichotomies — "The lesson isn't X — it's Y." Rewrite as a plain statement of Y.
- Decorative tricolons / subtitles like "what happened, what it cost, and the fix." Use a real "·"-separated pillar line instead.
- Strategic mid-paragraph bolding. Bold a phrase only if you'd write it on a whiteboard in a different color.
Read it aloud. If you wouldn't say a sentence to the person at a whiteboard, rewrite it to what you would say.

**One concept, one owning section (anti-repetition).** Repetition is almost always structural — a concept gets re-explained because two sections both try to own it. Fix it by altitude:
- *Evidence* lives in the timeline/appendix (full detail, with citation).
- *Argument* lives in the structural or costing section (why it matters).
- *Commitment* lives in the plan (what we'll do).
The same fact can appear as evidence, argument, and commitment — that's fine, because each is doing a different job. What's not fine is the *same sentence* in two sections, or a full list (e.g., the six escalation points) enumerated twice. Cross-account through-lines (e.g., "same gap on Acme Corp") may recur across sections when each is a different facet — that's the point, not redundancy.

**Numbers are the spine.** Record counts, hours, dates, editor/viewer counts, percentage built — these are what a skim retains. Keep them; flag any that are partner-reported or unconfirmed.

## Step 4 — Build the .docx

Use the bundled generator — it has the house style (Calibri; navy `#1F3864` headers; gray `#6B7280` subtitles; body `#444B54`; shaded-label key-value tables; navy-header data tables; US Letter, 0.8"/0.9" margins, 1.12 line spacing, no header/footer) baked in. Don't hand-roll OOXML or restyle from scratch each time.

```python
import sys
sys.path.insert(0, "scripts")            # or the absolute path to the skill's scripts/
from postmortem_docx import PostMortemDoc

d = PostMortemDoc()
d.title("Acme — Partner Oversight Read-Out")
d.subtitle("Retrospective Risk Assessment · UAT Answer · Design-Review Gap")
d.meta("Interim · current as of June 2, 2026 · delivered through Partner · prepared for Services leadership")

d.h1("Where Things Stand"); d.caption("As of June 2, 2026.")
d.kv_table([
    ("Status", "ESCALATED (red) — open customer escalation at the cutover line"),
    ("Where it stands now", "..."),
    ("Top risks", "..."),
    ("In motion", "..."),
])
d.spacer()

d.h1("Executive Summary")
d.body("Two short paragraphs: the situation and the honest read, then it's-still-landable + the structural lesson.")

d.h1("1. Retrospective Risk Assessment")
d.caption("What was missed, when we should have caught it, and the checkpoint that would have surfaced it.")
d.data_table(
    ["What surfaced", "When we should have caught it", "What would have caught it"],
    [["Performance lag (~1–2s)", "At design, before build", "A design review at the customer's volume"]],
    widths=(2.6, 1.9, 2.9),
)

d.h1("Plan for Future Co-Deliveries")
d.caption("The go-forward commitments, pulled into one place — by lifecycle stage.")
d.data_table(
    ["Gate", "What it is", "When"],
    [["Engage before design locks", "Airtable signs off on the data model before the partner finalizes design.", "Contracting → before build"]],
    widths=(1.85, 3.85, 1.0),
)

d.h1("Appendix — Decision Timeline")
d.body("One-paragraph framing of the engagement, then the numbered table.")
d.data_table(
    ["#", "Decision / Event", "Timeline impact"],
    [["1", "Inserted late onto an already-built partner design. (Gong, Jan 12 — …)", "Trusted existing work when review mattered most."]],
    widths=(0.35, 4.05, 3.0),
)

# Mixed bold runs: pass a list of (text, bold) tuples
d.body([("Sources & confidence — ", True), ("Built from the engagement Slack channel and Gong calls; hours are partner-reported.", False)])

d.save("/Users/<you>/Documents/Work Brain/Acme_Read-Out.docx")
```

Section headers use `h1`; sub-headers within a section use `h2`; gray sub-captions under a header use `caption`. For inline bolding (a bold lead-in then normal text), pass `body` a list of `(text, bold)` tuples.

## Step 5 — Deliver

Save the `.docx` into the user's Work Brain folder, then present it with `present_files`. Keep the closing message short — name the headline change, don't re-narrate the document.

## Pre-flight checklist

- [ ] Can the reader state the situation and the recommendation after the Executive Summary alone?
- [ ] Does each leadership question have its own section, answered straight (including the uncomfortable ones)?
- [ ] Is the forward plan in ONE consolidated section, not scattered as per-section tails?
- [ ] Are the cadence tells gone (meta-labels, em-dash dichotomies, decorative tricolons, mid-paragraph bolding)?
- [ ] Does every concept have one owning section, with cross-references at different altitudes (evidence / argument / commitment)?
- [ ] Does the body read as the SA's own analysis, with sources cited at the evidence point or in the appendix — never as "the transcript says"?
- [ ] Are partner-reported / unconfirmed numbers flagged?
