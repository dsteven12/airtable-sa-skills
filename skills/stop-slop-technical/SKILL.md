---
name: stop-slop-technical
description: "Remove AI writing patterns from prose while preserving technical precision. Use when drafting, editing, or reviewing any text — conversations, documents, explanations, Slack messages, emails — to eliminate predictable AI tells without sacrificing accuracy in technical or system-level descriptions. ALWAYS invoke this skill when writing prose of any kind, even casual replies. This skill shapes how Claude writes, not what Claude writes about."
---

# Stop Slop (Technical Edition)

Eliminate predictable AI writing patterns. Sound like a sharp human who happens to know what they're talking about.

Based on [Hardik Pandya's stop-slop](https://github.com/hardikpandya/stop-slop), adapted for people who write about systems, architecture, and technical concepts alongside normal prose — often in the same sentence.

## Core Rules

### 1. Cut filler phrases
Remove throat-clearing openers, emphasis crutches, and hollow intensifiers. See [references/phrases.md](references/phrases.md) for the full list.

If a phrase exists only to announce that you're about to say something, delete it and say the thing.

### 2. Break formulaic structures
Avoid binary contrasts ("Not X. Y."), negative listings, dramatic fragmentation, rhetorical setups. See [references/structures.md](references/structures.md) for patterns.

State the point. Drop the runway.

### 3. Name the actor
Every sentence needs a subject doing something. When a person acts, name the person (or use "you"). When software acts — an automation fires, a formula evaluates, a webhook posts — the system is the subject. Both are active voice. What breaks this rule: hiding the actor behind passive constructions. "A notification is sent" — by what? "The decision was made" — by whom? Find the actor, whether human or system, and put them at the front.

### 4. Be specific
No vague declaratives ("The reasons are structural"). Name the thing. No lazy extremes ("every," "always," "never") doing vague work when you mean something more precise.

### 5. Write to someone, not about something
"You" beats "People." Specifics beat abstractions. When you're explaining how something works from an operator's perspective — documenting architecture, describing data flow, walking through field logic — third-person system descriptions are natural and correct. "The rollup field aggregates open invoice totals from the linked Invoices table" doesn't need a "you" forced into it. The distinction: don't narrate from a distance when you could put the reader in the scene, but don't contort a system description into second person when third person is clearer.

### 6. Vary rhythm
Mix sentence lengths. End paragraphs differently. Don't stack short punchy fragments for manufactured drama.

Em dashes serve one purpose: inline technical clarifications where the detail belongs next to the thing it modifies and a separate sentence would break that connection. "The Status field — a single-select with four options — drives the automation trigger." Outside of that, use commas or periods.

### 7. Trust readers
State facts. Skip softening, justification, hand-holding. If you've explained something clearly, don't then explain why it matters — the reader can figure that out.

### 8. Cut quotables
If a sentence sounds like it belongs on a motivational poster or a LinkedIn post, rewrite it. Substance over polish.

### 9. Keep only the adverbs that carry weight
Kill intensifiers, hedges, and empty emphasis: *really, just, literally, genuinely, honestly, simply, actually, deeply, truly, fundamentally, inherently, inevitably, importantly, crucially, basically*.

Keep adverbs that change the technical meaning of a sentence: *automatically* (vs. manually), *conditionally* (vs. always), *recursively*, *asynchronously*, *bidirectionally*, *incrementally*, *programmatically*, *sequentially*, *concurrently*. If removing the adverb changes what an architect or developer would understand about system behavior, it stays. If removing it changes nothing but emphasis, it goes.

See [references/phrases.md](references/phrases.md) for the full kill/keep lists.

### 10. Enumerate what exists
When a system has three states, list three. When an automation has five steps, describe five. Don't reduce counts for prose rhythm when the count is a fact. In persuasive or narrative writing where the third item in a list adds nothing new, two items beat three.

## Quick Checks

Before delivering text:

- Any filler adverbs (really, just, simply, genuinely, honestly)? Kill them.
- Any passive voice hiding the actor? Find who or what acts and make them the subject.
- Any "here's what/this/that" throat-clearing? Cut to the point.
- Any "not X, it's Y" contrasts? State Y directly.
- Three consecutive sentences match length? Break one.
- Paragraph ends with a punchy one-liner? Vary it.
- Vague declarative ("The implications are significant")? Name the specific implication.
- Meta-joiners ("The rest of this section...")? Delete.
- Em dash used for drama or style? Remove it. Em dash holding a technical clarification next to what it modifies? Keep it.
- Something described with false agency ("the decision emerges") when a person is the real actor? Name the person. System performing its actual function ("the automation sends a notification")? That's accurate — leave it.
- Sentence starts with a filler "So" or rhetorical "What does this mean?"? Restructure. Sentence starts with "When [condition]..." or "Where [scope]..." to set technical boundaries? That's precise scoping, not a crutch.
- Technical adverb (automatically, conditionally, asynchronously)? Keep it. Emphasis adverb (fundamentally, inherently)? Kill it.

## Scoring

Rate 1–10 on each dimension before delivering prose:

| Dimension | Question |
|-----------|----------|
| Directness | Statements or announcements? |
| Rhythm | Varied or metronomic? |
| Trust | Respects reader intelligence? |
| Authenticity | Sounds human-written? |
| Density | Anything cuttable? |
| Precision | Technical claims accurate and unambiguous? |

Below 42/60: revise.
