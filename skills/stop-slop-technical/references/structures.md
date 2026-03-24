# Structures to Avoid

## Binary Contrasts

These create false drama. State the point directly.

| Pattern | Problem |
|---------|---------|
| "Not because X. Because Y." | Telegraphed reversal |
| "[X] isn't the problem. [Y] is." | Formulaic reframe |
| "The answer isn't X. It's Y." | Predictable pivot |
| "It feels like X. It's actually Y." | Setup/reveal cliche |
| "The question isn't X. It's Y." | Rhetorical misdirection |
| "Not X. But Y." | Mechanical contrast |
| "stops being X and starts being Y" | False transformation arc |
| "doesn't mean X, but actually Y" | Negation-then-assertion crutch |
| "not just X but also Y" | Additive hedge |

**Instead:** State Y directly. Drop the negation.

## Negative Listing

Listing what something is *not* before revealing what it *is*.

| Pattern | Problem |
|---------|---------|
| "Not a X... Not a Y... A Z." | Dramatic buildup through negation |
| "It wasn't X. It wasn't Y. It was Z." | Same structure, past tense |

**Instead:** State Z directly. The reader doesn't need the runway.

## Dramatic Fragmentation

Sentence fragments for emphasis. Manufactured profundity.

| Pattern | Problem |
|---------|---------|
| "[Noun]. That's it. That's the [thing]." | Performative simplicity |
| "X. And Y. And Z." | Staccato drama |
| "This unlocks something. [Word]." | Artificial revelation |

**Instead:** Complete sentences. Trust content over presentation.

## Rhetorical Setups

Announcing insight rather than delivering it.

| Pattern | Problem |
|---------|---------|
| "What if [reframe]?" | Socratic posturing |
| "Here's what I mean:" | Redundant preview |
| "Think about it:" | Condescending prompt |
| "And that's okay." | Unnecessary permission |

**Instead:** Make the point. Let readers draw conclusions.

## False Agency

Giving inanimate things human verbs when a person is the real actor. Complaints don't "become" fixes. Bets don't "live or die." Someone does the work.

| Pattern | Problem |
|---------|---------|
| "a complaint becomes a fix" | Someone fixed it. |
| "a bet lives or dies in days" | Someone kills the project or ships it. |
| "the decision emerges" | Someone decides. |
| "the culture shifts" | People change behavior. |
| "the conversation moves toward" | Someone steers. |

Software performing its designed function is not false agency — it's accurate description. "The automation sends a Slack notification," "the rollup field aggregates values," "the webhook fires on record creation" — these describe real system behavior. The test: is the inanimate thing literally executing code? Valid subject. Is it a metaphor hiding a human actor? Name the person.

## Narrator-from-a-Distance

Floating above the scene instead of putting the reader in it.

| Pattern | Problem |
|---------|---------|
| "Nobody designed this." | Disembodied observation |
| "This happens because..." | Lecturer voice |
| "This is why..." | Same |
| "People tend to..." | Armchair sociologist |

Put the reader in the room when you're writing to persuade, explain, or recommend. When documenting architecture or system behavior from an operator's perspective, third-person system descriptions are the natural voice — "The base uses a hub-and-spoke linking pattern with Projects as the central table" is clear and accurate.

## Passive Voice

Every sentence needs a subject doing something. Passive voice hides the actor.

| Pattern | Fix |
|---------|-----|
| "X was created" | Name who or what created it |
| "It is believed that" | Name who believes it |
| "A notification is sent" | Name what sends it — the automation, the script, the webhook |
| "The decision was reached" | Name who decided |

The fix is always the same: find the actor and put them first. Sometimes the actor is a person. Sometimes it's software. Both work as subjects.

## Sentence Starters

| Pattern | Fix |
|---------|-----|
| Paragraphs starting with "So" | Start with content |
| Sentences starting with "Look," | Remove |
| Rhetorical Wh- openers ("What does this mean?") | Restructure — make the point |

"When [condition]..." and "Where [scope]..." are standard scoping constructs that set technical boundaries precisely. "When a record enters the Approved view, the automation triggers" is clear. "Where this breaks down is tables exceeding 100k records" scopes a limitation. These are precise, not filler.

## Rhythm Patterns

| Pattern | Fix |
|---------|-----|
| Three-item lists in persuasive prose | Two items or one when the third adds nothing |
| Questions answered immediately | Let questions breathe or cut them |
| Every paragraph ends punchily | Vary endings |
| Staccato fragmentation | Don't stack short punchy sentences |
| "Not always. Not perfectly." | Hedging disguised as reassurance |

Enumerations of real things — system states, automation steps, field types, API parameters — include every item that exists. The count is a fact, not a style choice.

## Em Dash Usage

Em dashes serve one purpose in this skill: holding an inline technical clarification next to the thing it modifies when a separate sentence would lose that proximity.

Good: "The Status field — a single-select with four options — drives the automation trigger."
Bad: "This changes everything — and I mean everything."

If the em dash is doing the work of a comma or period, use a comma or period. If it's holding a parenthetical technical detail in place, it earns its spot.

## Word Patterns

| Pattern | Problem |
|---------|---------|
| Lazy extremes (every, always, never, everyone) | False authority. Use specifics. |
| Filler adverbs (really, just, literally, genuinely) | Empty emphasis. See phrases.md. |
| Technical adverbs (automatically, conditionally, asynchronously) | These carry meaning — keep them. See phrases.md. |
