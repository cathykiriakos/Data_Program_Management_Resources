---
name: dont-sound-like-ai
description: Edits writing to remove AI cliches and stock patterns so it reads like a person wrote it. Use for grants, appeals, emails, and reports, or when asked to make a draft sound human.
---

# Don't Sound Like AI

Language models converge on the same tics: the same handful of words, the same
sentence shapes, the same throat-clearing openers and hedge-everything
closers. None of it is wrong, exactly, it's just recognizable, and
recognizable reads as fake. This skill is a checklist plus a self-critique
loop: write normally, then scan what you wrote against the lists below,
rewrite anything that got flagged, and repeat until the text is clean.

Treat this as an editing pass, not a constraint you write under from the
first word. Trying to dodge every banned word while composing the first draft
produces stilted, over-careful sentences, worse than the thing you're trying
to avoid. Write naturally first. Then edit.

## Why this matters

Each item below got banned because it's a shortcut: a word that sounds
important without saying anything, a sentence shape that manufactures
profundity, a closer that pads instead of ending. A person writing carefully
reaches for a plain word, says the specific thing, and stops when they're
done. That's the target.

## Step 1: Write the draft

Answer the actual request first. Don't pre-filter every sentence against the
banned list while composing, that's how you end up with mangled, overly
cautious prose. Get the content right, then move to Step 2.

## Step 2: Scan for banned words

Search the draft for these. If found, replace with a plainer, more specific
word, usually something shorter and more ordinary.

**Banned outright:**
delve, crucial, pivotal, tapestry, foundational, robust, seamless, landscape, realm <!-- lint:allow -->

**Also watch for** (same family, same problem, inflated, vague, or
overused to the point of meaninglessness): leverage (as a verb), utilize, <!-- lint:allow -->
game-changer, cutting-edge, unlock, unleash, elevate, holistic, synergy, <!-- lint:allow -->
navigate (as in "navigate this challenge"), journey (as a metaphor for a <!-- lint:allow -->
process), ecosystem (unless literally about biology or software
architecture), multifaceted, nuanced (as a filler compliment), testament to, <!-- lint:allow -->
underscore (as a verb), boasts (as in "the city boasts a museum"). <!-- lint:allow -->

If a plain synonym does the job, use it. "Robust system" → "system that <!-- lint:allow -->
holds up under load." "Delve into the data" → "look at the data" or just <!-- lint:allow -->
look at it and report what you found. "Crucial step" → say why it matters,
or cut the adjective, if it's actually crucial, the sentence around it
should already show that.

## Step 3: Scan for banned phrases

These are stock phrases, recognizable as a unit, not just individual words.

**Throat-clearing openers** (cut them, start with the actual content):
- "Here's the thing"
- "Let's dive in" / "Let's unpack this"

Note: "I wanted to provide a quick update" / "I wanted to reach out" is fine
to use if the user writes that way. Don't flag it.

**Padded or hedgy closers** (cut them, or end on the actual last point):
- "Hope this helps!" / "Hope this helps after careful consideration"
- "Let me know if you have any questions!" tacked on reflexively rather than because there's a real open question
- "In conclusion" / "In summary" (only cut if the piece is short enough that a summary is redundant, long documents can still earn a real closing section)

**Bandwagon appeals** (cut or replace with a specific, checkable claim):
- "Many people agree that..."
- "It's widely accepted that..."
- "Studies show..." (unless you're naming the actual study)
These manufacture consensus instead of citing it. If you can name who agrees
and why, do that instead. If you can't, the sentence is probably filler , 
cut it.

## Step 4: Scan for banned sentence patterns

These are shapes, not words, the same construction shows up in fresh
vocabulary every time, so word-matching won't catch them. Read each sentence
and ask if it fits one of these molds:

**Negative parallelism**, "It's not X, it's Y."
> "This isn't a budget, it's a statement of intent."
> "It's not a bug, it's a feature."

This construction manufactures depth by pretending to correct a
misconception nobody had. If the sentence would still make sense with just
"it's Y," the "it's not X" half is doing nothing but sounding profound. Cut
it, or replace the whole thing with the actual claim: "This budget commits
funding to three priorities before anything else."

**The grand pronouncement**, a short, declarative sentence positioned to
sound like a revelation, usually right after a list or a transition. If you
can imagine it echoing in a movie trailer voice, it's this pattern.
> "This isn't just a redesign. It's a rethinking of what the product stands for."

Replace it with the specific thing you actually mean. What does "rethinking
what the product stands for" cash out to? Say that instead.

**The quiet-verb personification**, giving an abstract or inanimate subject
a soft, deliberate-sounding verb to imply competence or restraint.
> "The new caching layer quietly handles the heavy lifting."
> "Underneath, a lightweight scheduler quietly orchestrates the workflow."

"Quietly," "seamlessly," and "effortlessly" paired with a technical subject
are the tell. Say what it actually does and skip the personality: "The
caching layer handles repeated reads so the database doesn't have to."

**Rule-of-three padding**, reflexively listing three adjectives or clauses
where one specific one would do ("fast, flexible, and future-proof").
If the three items are near-synonyms, keep the best one and cut the rest.

## Step 4b: No em dashes

Never use ", " (or " - " standing in for one) to splice two clauses
together. It's one of the most recognizable AI tics because the model reaches
for it as a default connector regardless of what relationship the two
clauses actually have. Every time you're tempted to use one, figure out the
real relationship between the two halves and pick accordingly:

- Related, standalone thoughts → split into two sentences.
- One clause adds a quick aside or clarification → comma.
- Two independent clauses that are closely linked in meaning → semicolon.
- One clause explains or justifies the other → "because," "so," or a colon.

> AI-ish: "The migration finished early, the team had prepped the pipeline for weeks."
> Fixed: "The migration finished early because the team had prepped the pipeline for weeks."

This applies even inside lists and asides, not just full sentences.

## Step 5: Cut adverb abuse

Scan for -ly adverbs propping up a weak verb: "significantly improves,"
"dramatically reduces," "carefully considers," "actively works to." Usually
the fix is a stronger, more specific verb, or a number. "Significantly
improves load time" → "cuts load time from 4s to 1.2s" (if you have the
number) or "cuts load time" (if you don't and shouldn't invent one).

Not every adverb is guilty, "rarely," "barely," "only" often carry real
information. The test is whether the adverb is doing the verb's job for it.
If removing it leaves the sentence just as true, cut it.

## Step 6: Oversimplify like a person would

AI writing tends to qualify everything, "it's worth noting that,"
"generally speaking," "in many cases", because hedging feels safe. People
writing casually just say the thing, even when it's not perfectly precise,
and let context carry the rest. Where a hedge isn't protecting against a
real, likely misreading, cut it and say the plain version. A little bit of
imprecision reads as more honest than total, defensive coverage.

## Step 7: Self-critique and fix until clean

Before finishing, reread the draft once specifically hunting for anything
from Steps 2 to 5. This is a distinct pass, not something to trust yourself to
have caught while writing. For each hit:

1. Quote the flagged line.
2. Name which rule it breaks.
3. Rewrite it.

Repeat this pass until a fresh read turns up nothing. Two passes is typical;
if a third pass still finds something, do it, don't stop at "close enough."

If the user asked to see your edits (not just the final text), show this as
a short table or list: flagged line → issue → fix. Otherwise, just deliver
the clean final text, the self-critique is working scaffolding, not
something to narrate unprompted.

## Quick reference

| Category | Examples |
|---|---|
| Banned words | delve, crucial, pivotal, tapestry, foundational, robust, seamless, landscape, realm | <!-- lint:allow -->
| Banned openers | "here's the thing," "let's dive in" ("I wanted to provide a quick update" is fine) |
| Banned closers | "hope this helps," reflexive "let me know if you have questions" |
| Bandwagon | "many people agree," "studies show" (unnamed) |
| Negative parallelism | "it's not X, it's Y" |
| Grand pronouncement | short trailer-voice sentence after a transition |
| Quiet-verb personification | "X quietly handles/orchestrates/powers Y" |
| Adverb abuse | "-ly + weak verb" instead of a strong verb or number |
| Em dashes | ", " splicing two clauses; use a comma, semicolon, "because/so," or a new sentence instead |
