---
name: researching-with-confidence
description: Researches a topic from multiple angles, rates each finding High, Medium, or Low confidence, and names gaps and contradictions. Use to verify a claim or get a sourced, confidence-rated brief.
---

# Researching with Confidence

**When to use this skill.** Deep research skill that investigates a topic from multiple angles, assigns confidence scores to each finding, and surfaces gaps and contradictions. Use this skill whenever the user wants to research a topic, verify a claim, do a deep dive, fact-check something, or get a thorough multi-source breakdown. Triggers on: "research [topic]", "deep dive into", "verify this claim", "how confident are we about", "what do we actually know about", "poke holes in this research", "what's the evidence for", "synthesize this for me", "give me a confident take on". Works with web search when available AND with content the user pastes in. Use this skill even when the user just says "look into X" or "can you find out about Y", any multi-source research task benefits from it.

The goal of this skill is to produce research you can actually act on. Lots of AI research outputs look thorough
but hide the seams, they blend high-confidence facts with speculative claims without telling you which is which.
This skill fixes that. Every major finding gets a confidence rating, every gap gets named, and contradictions get
surfaced rather than smoothed over.

## What counts as a research request

This skill applies when the user wants to know something non-trivial, a topic where sources might disagree,
where the picture is incomplete, or where a claim needs verification before someone acts on it. That includes:
- Landscape research (tools, vendors, models, market trends)
- Factual claims that need verification
- Academic or institutional topics
- Strategic or business questions where the evidence matters
- Any content the user pastes in and wants critically assessed

## How to approach the research

### Step 1: Frame the inquiry

Before diving in, identify:
- The core question (restate it clearly so the user can confirm you're on track)
- What "good enough" confidence looks like for this topic
- Whether the user has pasted source material or you're going out to find it

If the question is ambiguous, make your best interpretation explicit rather than asking. You can always refine
after showing your work.

### Step 2: Research from multiple angles

Good research doesn't just find one answer, it triangulates. For each topic, pursue at least 2 of these angles:
- **Primary sources**: official docs, papers, announcements, data
- **Secondary analysis**: expert commentary, reviews, benchmarks
- **Skeptical framing**: what critics say, known failure modes, counterevidence
- **Recency check**: is this information current? When was it last verified?

Use web search when available. If the user has pasted in content, treat that as one source and cross-reference
against what you already know or can find.

Don't just summarize the first thing you find. If sources conflict, that conflict is valuable information.

### Step 3: Assign confidence scores

For each significant finding or claim, assign one of three confidence levels:

**High confidence**, Multiple independent sources agree, or the claim comes from a primary source with no
credible contradictions. You'd stake a recommendation on this.

**Medium confidence**, Some support exists but the picture is incomplete, sources partially disagree, or
the information may be dated. Worth acting on with caveats.

**Low confidence**, Thin sourcing, speculation, conflicting claims, or significant gaps. Useful as a
signal to investigate further, not as a basis for decisions.

The confidence rating is about evidence quality, not about how certain you feel. If you're not sure, rate lower
and say why.

### Step 4: Surface gaps and contradictions

This is the part most research skips. Be explicit about:
- What you couldn't find or verify
- Where sources disagreed and why
- What would change the confidence level (e.g., "if X is confirmed, this goes from medium to high")
- What the user should follow up on if this decision matters

## Output format

Structure the output as follows. Use this as a template, adjust section depth based on how complex the topic is.

---

## Research: [Topic]

**Core question**: [Restate what you investigated]
**Research approach**: [Brief note on sources used, web search, user-provided content, prior knowledge]

---

### Key Findings

**[Finding 1]**
Confidence: [High / Medium / Low]
[2-4 sentences explaining the finding and why you rated it this way. Cite sources inline where possible.]

**[Finding 2]**
Confidence: [High / Medium / Low]
[Explanation]

[Continue for all significant findings]

---

### Contradictions and Disagreements

[If sources conflicted on anything significant, describe the disagreement plainly. Don't pick a winner unless
the evidence clearly favors one side.]

---

### Gaps and Unknowns

[List what you couldn't determine, what's outdated, or what's missing from the picture. Be specific, "this
area is unclear" is less useful than "no independent benchmarks exist for this claim as of [date]."]

---

### Confidence Summary

| Finding | Confidence | Key caveat |
|---|---|---|
| [Finding 1 short label] | High | [one-line caveat] |
| [Finding 2 short label] | Medium | [one-line caveat] |
| [Finding 3 short label] | Low | [one-line caveat] |

---

### Recommended next steps

[1-3 concrete things the user should do if this research matters for a decision. Optional, include only
when the topic warrants it.]

---

## Tone and style notes

Write like a thoughtful colleague, not a search engine. The user is smart, they don't need hedges on every
sentence, just honest confidence ratings where it counts. Be direct about what you found and what you didn't.
Avoid vague qualifiers like "it seems" or "it appears", either you found evidence or you didn't.

Keep the report skimmable. Use the structure above so the user can land on the confidence summary fast if
they're in a hurry and read the details if they want depth.
