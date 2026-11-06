---
name: board-of-advisors
description: Simulates a board of expert advisors reviewing a proposal, decision, or strategy, each from a distinct lens. Use to anticipate stakeholder reactions or pressure-test a plan before presenting it.
---

# Board of Advisors

**When to use this skill.** Simulates a board of diverse expert advisors reviewing a proposal, decision, strategy, or plan, each from their own distinct perspective and expertise. Use this skill whenever the user wants multi-perspective feedback, wants to anticipate how different stakeholders will react, or needs to pressure-test an idea across multiple lenses. Triggers on: "what would my board say", "360 review", "different perspectives on this", "how would [type of expert] see this", "stakeholder reactions", "what would a [VC / engineer / lawyer / CFO / skeptic] think", "run this by the board", "advisory review", "pressure test with multiple views", or any request for structured multi-stakeholder feedback. Also use when the user shares a proposal and asks "am I thinking about this the right way", a board review often surfaces what they are missing.

This skill gives you the benefit of diverse expert perspectives without needing
a room full of people. It simulates a small advisory board reviewing your idea,
each advisor bringing a distinct lens, expertise, and set of concerns.

The value is not in any single advisor's view, it is in seeing your idea through
multiple fundamentally different frameworks at once. The CEO and the engineer and
the skeptical operator all notice different things.

## How to assemble the board

The composition of the board should match the nature of the proposal. The default
board covers four perspectives that apply broadly:

**Default board:**
- **The Strategist**, Thinks about positioning, long-term implications, and
  opportunity cost. Asks whether this is the right move, not just whether it can
  be executed.
- **The Operator**, Thinks about execution, resourcing, dependencies, and what
  makes real-world implementation hard. Asks whether this can actually be done.
- **The Skeptic**, Questions the assumptions, challenges the optimistic framing,
  and asks what the downside looks like when things do not go as planned.
- **The User / Customer / Stakeholder**, Thinks about the experience of the
  people most affected by this decision. Asks whether it actually serves them.

**Customize when relevant.** If the topic clearly warrants a specific expert lens
(legal, financial, technical, political, ethical), substitute or add that advisor.
Make the selection explicit so the user knows who is at the table.

Examples of specialized advisors:
- The CFO (financial sustainability, unit economics, risk)
- The Engineer (technical feasibility, debt, complexity)
- The Lawyer (legal exposure, compliance, precedent)
- The Academic (evidence base, rigor, what the research says)
- The Devil's Advocate (assigned to find the strongest case against)

## How to run the review

### Step 1: Understand the proposal

Read the user's input carefully. Identify what is being reviewed and what kind of
feedback is most useful, validation, risk identification, stakeholder mapping,
or all of the above.

If the proposal is unclear, state your interpretation before proceeding.

### Step 2: Run each advisor

For each advisor, stay in their perspective. Think about what genuinely matters
to them, what their instinct would be, and what they would catch that others might
miss. A good advisor review should feel like different people in the room, not like
the same voice wearing different hats.

Each advisor should:
- State their overall reaction (supportive, concerned, skeptical, enthusiastic, etc.)
- Raise 1-3 specific points from their perspective
- Ask one sharp question they would want answered before endorsing this

### Step 3: Synthesize across the board

After the individual advisor views, step back and synthesize:
- Where is there alignment across perspectives? (strong signal)
- Where is there disagreement? (worth examining why)
- What does the full picture suggest about the biggest risk and the biggest opportunity?

### Step 4: Surface the key question

End with one question, the most important question the user should answer
before moving forward. Often the advisors will converge on a common gap even if
they approach it differently.

## Output format

---

## Board Review: [Topic]

**Proposal as understood**: [One sentence]

---

### [Advisor Name]: [Their Role/Lens]

**Reaction**: [Supportive / Cautiously supportive / Concerned / Skeptical]

[2-4 sentences from their perspective. Stay in voice, an operator does not
sound like a strategist.]

**Key question**: "[One sharp question they would ask]"

---

[Repeat for each advisor]

---

### Board Synthesis

**Where there is alignment**: [What multiple advisors agree on, positive or negative]

**Where there is tension**: [Where advisors see it differently and why that matters]

**The biggest risk on the table**: [One sentence]

**The biggest opportunity on the table**: [One sentence]

---

### The question you need to answer

[One question, the most important thing to resolve before moving forward]

---

## Tone notes

Each advisor should have a distinct voice. Do not have them all say variations of
the same thing with different labels. A strategist who just echoes the operator
adds no value.

Be honest about where advisors would genuinely push back. If the proposal has a
real weakness, the relevant advisor should name it directly, not soften it.

The synthesis should be genuinely integrative, not just a summary of what each
person said, but an observation about what the full picture means.
