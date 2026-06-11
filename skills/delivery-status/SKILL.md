---
name: delivery-status
description: "Turn raw engagement signal (meeting outcomes, blockers, what changed this week) into two artifacts: a concise weekly project status update (RAG status, summary, key accomplishments, upcoming, risks and issues) and a standalone risk flag that leads with the risk, ties it to the launch date or scope, tags the owner who can act, states the specific ask, and proposes the mitigation. For at-risk or in-flight customer engagements. MANDATORY TRIGGERS: weekly project update, status update, project status, RAG status, flag a risk, flag the account, risk flag, escalate a risk, draft the channel update, update leadership on the project, at-risk update, mitigation plan, what do we tell the sponsor. ALWAYS invoke when producing a recurring engagement status update or surfacing a delivery risk to leadership. Defers to written-voice for voice; owns structure, RAG logic, and the risk scaffold. Do NOT use for decision papers (executive-brief), retrospectives (post-mortem-doc), or personal reviews (review)."
---

# Delivery Status

A leader should know, in one read, three things: is the account healthy, what is at risk, and what is being asked of them. This skill produces the two artifacts that deliver that — the recurring weekly project update and the standalone risk flag — for an in-flight or at-risk customer engagement.

The bar is decision velocity. The reader is a sponsor or delivery lead skimming fast between meetings. If they have to hunt through a recap to find the risk, the update failed, even if every fact in it is correct.

You are writing as the program manager — accountable for the engagement's health across work that others own (a solution architect's design, a build partner's delivery). The status integrates their signal; it does not require you to have done the work yourself. Your job is to make health, risk, and the ask legible, and to route each risk to whoever can actually move it — including the SA and the partner, not just the customer.

## The thing this skill is built to prevent

The common failure is the comprehensive recap: a long, well-organized log where the risk is one accurate bullet buried among logistics, and there is no status marker telling the reader how worried to be. Coverage is high; legibility is low. This skill inverts that — health and risk lead, detail follows, every risk carries a named owner and a proposed move.

## Relationship to written-voice

This skill owns **structure**: what sections exist, how RAG status is decided, and the scaffold every risk follows. `written-voice` owns **voice**: how each sentence reads — decision-first, name the consequence not the category, kill AI cadence, attribute recommendations.

Run both. Build the artifact with this skill, then pass every sentence through written-voice's three tests (show-me, substitution, whiteboard) and its cadence test. If they ever conflict, written-voice wins on phrasing and this skill wins on what goes where.

## When this fires

- Drafting a recurring (weekly/bi-weekly) status update for a customer or services engagement
- Surfacing a delivery risk to internal leadership or to a sponsor
- Someone asks "what's the status," "what do we tell the sponsor," "flag this," or "are we still on track"
- A meeting or gate just produced an outcome that changes the project's health

Do **not** use this for a one-off decision/options paper (`executive-brief`), a post-delivery retrospective (`post-mortem-doc`), a base/system audit (`health-check`), or a summary of your own work for the vault (`review`).

---

## Artifact 1 — The weekly project update

Same five sections, same order, every week. Sameness is the feature: the reader knows where to look, and consecutive updates diff cleanly.

```
Status: 🟡 At risk — [the one sentence that explains the color]

### Summary
[3–5 sentences. What advanced, which gate or decision is pending, and the
current risk posture. The risk posture is stated here, not saved for the end.]

### Key Accomplishments (this week)
- [Concrete, completed things. A reader should be able to verify each one happened.]
- [Name the artifact, the decision, or the session — not "made progress on X."]

### Upcoming Activities
- [Next step] — [date], [owner if not the team]
- [Gate or decision the project is waiting on, and by when]

### Risks & Issues
- [Risk]: [consequence tied to date/scope]. [Owner/ask]. [Proposed mitigation.]
```

Two rules that separate this from a status log:

**The status line is never naked.** "🟡 At risk" alone tells the reader nothing. "🟡 At risk — design sign-off slipped today, which puts the Aug 4 launch in jeopardy unless we reset the gate criteria this week" tells them everything. The color and its reason travel together, in sentence one.

**Accomplishments are evidence, not activity.** "Held the design workshop" is activity. "Resolved Element/Asset workflows and confirmed DAM as source of truth in the design workshop" is evidence. If you could not point at the output, it is not an accomplishment yet.

### RAG logic

Pick the color by what is true about the **date and scope**, not by how the week felt.

- **🟢 On track** — No material threat to the committed date or scope. Open questions exist but none of them, if unresolved, moves the date.
- **🟡 At risk** — The date is still achievable, but only with deliberate action that is not yet guaranteed: a decision someone owes you, a scope trade-off, an accelerated turnaround. State the action in the status line. This is the honest color for most live engagements with a firm deadline.
- **🔴 Off track** — The committed date or scope is no longer achievable without a reset (re-baselined timeline, descoped MVP, added resources). Use it when that reset is the actual ask.

The discipline: 🟡 must always name the action that keeps it from going 🔴. A 🟡 with no stated action is really a 🟢 in disguise or a 🔴 you are avoiding.

---

## Artifact 2 — The risk flag

A standalone message between updates, when something threatens the account and a leader needs to act before the next scheduled update. It leads with the risk and ends with what you need.

```
Flagging [N] risk(s) ahead of [forum / date]:

• **[Risk name].** [The fact — what happened or is true.] [The consequence,
  tied to the date or scope.] [@owner who can act] [The specific ask.]
  [The proposed mitigation / where it gets resolved.]

• **[Next risk]** … same shape.

Goal for [forum]: [the decision or alignment you want out of it.]
[If you need internal backing to make the case, say so and tag who.]
```

### The risk scaffold (the reusable core)

Every risk — in an update or a flag — follows the same four beats. This is the single most copyable thing in this skill.

1. **Fact.** What is true, stated plainly. "The customer submitted design feedback today and is withholding sign-off pending our replies, due EOD Wednesday."
2. **Consequence, anchored to date or scope.** Not "timeline pressure" — "we've absorbed the buffer we were afforded, so missing design alignment today puts the Aug 4 launch at significant risk." The reader must see what breaks.
3. **Owner + ask.** Tag the one person who can move it and say exactly what you need. "@sponsor — we need top-down alignment on MVP scope and confirmation that someone on the customer side is empowered to make trade-off calls."
4. **Mitigation.** The move you are proposing, and the forum where it happens. "Proposing a focused interface-education session to reset expectations; I have a hold out for us to sync internally first."

A risk missing beat 2 reads as noise. A risk missing beats 3 and 4 makes the problem the reader's to solve. All four, every time.

### Worked example (real shape)

> Flagging a few risks ahead of Wednesday's exec meeting:
>
> • **Timeline & scope.** The customer is withholding design sign-off pending replies due Wednesday. We've absorbed the timeline buffer we were afforded, so failure to align on design now puts the Aug 4 launch at significant risk. @sponsor @delivery-lead — we need to reset their understanding of what the design gate is for, and prepare them to make scope trade-offs to land a V1 MVP on time.
> • **Design methodology.** They're treating sign-off as requiring fully-built UX across every capability. The mitigation is to reset the expectation that design aligns the entity model, workflow logic, and integration behavior — UX is built and refined during Build. I may need support making this case.
> • **Platform knowledge.** Several of their questions (concurrent editing, filter persistence) treat platform constraints as design failures. Proposing a focused interface-education session to reorient expectations; @product-voice I'll want you there.
>
> Goal for Wednesday: align on sign-off criteria and surface the scope/timeline risk.

Notice what it does not do: no preamble, no "I wanted to reach out," no apology for the length. The risk is the first word.

---

## Internal diagnosis vs. customer-ready draft

The strongest move in this style is running two registers at once: be blunt internally about the real problem, and in the same message hand over a polished artifact the leader can use without editing.

- **Internal register:** name the real dynamic, including the uncomfortable part. "We're seeing a gap between surfacing decisions and having the authority structure to resolve them." "The misalignment on delivery expectations is strong — I may need support."
- **Customer-ready register:** a send-ready draft, in the customer's language, that the sponsor can forward as-is. Give it as a quote block so the boundary is obvious, and say "feel free to adapt."

When you produce a customer-ready draft, apply the document-output language rules: never reference transcripts, recordings, or "notes" as the source; state observations as facts; make it read as if the sponsor authored it.

## Processing raw signal into the artifact

Given meeting outcomes, a thread, or a brain-dump, sort every input into one of four buckets before writing:

- **Accomplishment** — done, with a verifiable output → Key Accomplishments
- **Next step / dependency** — not yet done, has a date or owner → Upcoming
- **Threat to date or scope** → Risks & Issues, run through the four-beat scaffold
- **Logistics / noise** (scheduling, attendee lists, swag) → leave it out of the leadership update; it belongs in working threads, not the status

Then set RAG by the threats bucket: any unmitigated threat to the date is at least 🟡.

## Workflow

1. **Confirm the artifact.** Weekly update, or a one-off risk flag? If ambiguous, ask once.
2. **Sort the raw signal** into the four buckets above. Drop the logistics.
3. **Set RAG** from the threats bucket, and write the one-sentence reason.
4. **Build the structure** — the five sections (update) or the flag template.
5. **Run every risk through the four-beat scaffold.** Fact, consequence, owner+ask, mitigation. Reject any risk missing beat 2.
6. **Pass it through written-voice.** Three sentence tests on every line; cadence test on the whole draft. Lead with the news.
7. **If there's a customer-ready draft,** quote-block it, strip source language, mark it adaptable.
8. **Stop.** Show the artifact and stop. Don't append "let me know if you'd like changes."

## Anti-patterns

- **Naked status.** A color with no reason, or no status marker at all.
- **Buried risk.** The thing the reader most needs to know sitting in the middle of a recap.
- **Activity as accomplishment.** "Worked on," "made progress on," "had discussions about." Name the output or move it to Upcoming.
- **Orphan risk.** A risk with no owner and no proposed move — you've handed the reader a problem instead of a recommendation.
- **Logistics in the leadership update.** Scheduling, phone numbers, lunch. Keep the status about health, risk, and action.
- **The everything-recap.** Comprehensive and unreadable. Coverage is not the goal; one-read legibility is.
