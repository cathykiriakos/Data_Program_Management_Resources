---
name: "deliverable-validation"
description: Runs a pre-delivery check on reports, decks, spreadsheets, and documents. Checks that counts match, totals recompute, and dates and names agree. Use before presenting any deliverable as finished.
---

# Deliverable Validation

Most people are poor proofreaders of their own work, so these checks replace
proofreading. Run them before calling any deliverable done. Do not ask
whether to run them, and do not skip them because a change seemed small. Most
of the errors below were introduced by small edits and reorders, not by
first drafts.

**Verify by running code, not by reading.** Eyeballing a deck is what lets a
headline claim "eight moves" above a five-row table. Parse the artifact and
assert. For HTML, load it in jsdom and query the DOM; for xlsx, read the cells;
for docx, extract the text. If the deliverable has a runtime (a deck with
navigation, a dashboard with filters), execute it, don't just inspect markup.

Report findings as a short table of what was checked and what failed. If
everything passes, say so in one line and name the specific checks that ran.

## 1. Counts stated in prose must match reality

Any number in a heading, sentence, or label that describes the size of
something visible has to match what is actually there.

- "Eight priority moves" over a table with five rows.
- "Five items awaiting sign-off" over a six-row table after one was added.
- "Four hours, five modules" when the agenda has six.
- "Three interns" in a heading with two cards.

Extract every number-word and digit from headings and captions, count the
corresponding rows, bullets, or cards, and compare. Watch for the case where
the count *was* right and a later edit added an item without touching the
heading. Numbers that are dates, years, times, or currency are not counts , 
exclude them so they don't produce false flags.

## 2. Recompute every derived figure from its inputs

Never carry a percentage, ratio, average, or total forward on trust.

- Engagement rates shown as 0.07% when engagements ÷ impressions is 7.4% , 
  four of five rows were wrong by one or two decimal places.
- Totals that no longer sum after a row was added (27 + 21 + 12 labelled 60).
- Growth percentages that don't follow from the first and last values.

If a table shows the inputs and the derived value, compute the derived value
and assert equality. If the inputs aren't shown, say in a footnote how the
figure was derived and where it came from.

## 3. Chart geometry must be honest and internally consistent

- Bar widths proportional to their values, on one consistent scale.
- Two charts in the same deliverable must not use different scaling rules
  (one normalised to its max, another to an arbitrary denominator).
- Colour used for emphasis must point at the row being discussed.
- Conditional formatting (status pills, RAG colours) must match the corrected
  value, not the value it had before a fix.

## 4. Hunt cross-section contradictions

The same fact stated twice in different places is where drift shows up. Grep
for each key figure and phrase across the whole artifact, not per section.

- "7 gap dimensions" on one slide, "eight priority gaps" on another.
- "2026 to 2028" in a headline, "2026 to 2029" in a body list.
- A person marked "declined" in a table and "attending virtually" in a card.
- A venue described as "held as default, being reconsidered" in one place and
  "locked" in another.

Where two numbers legitimately differ because they count different things,
say so on the slide. An unexplained discrepancy reads as an error even when
it isn't.

## 5. Find duplicated content

Identical or near-identical blocks across sections mean either a copy-paste
that was never localised, or two sections doing the same job. Compare card and
paragraph text across sections and flag close matches. Then decide which
section owns the point and cut it from the other.

## 6. Check dates and tense against today

- Relative words that go stale: "today," "this week," "yesterday," "next month."
- Absolute dates that have passed since drafting, still written in future
  tense ("a work review around Aug 11" presented on Aug 12).
- Day-of-week and date pairs that don't agree with each other or with the
  calendar.
- Deadlines that have already expired.

Get the real current date from the environment and compare.

## 7. After any reorder or renumber, re-verify the whole chain

Reordering is the highest-risk edit. Every one of these broke at least once:

- Section numbers in headings, kickers, and labels.
- Cross-references in body text and speaker notes ("as shown in Module 2").
- Transition lines that assume what came immediately before ("Florence just
  showed us…" when Florence now comes later).
- Comment markers and anchors used by scripts, especially if they differ in
  case from the visible text (`MODULE 3` vs `Module 3`), a case-sensitive
  rename will silently miss them and mis-scope a later cut.
- Whether the sequence is monotonic and no section number is skipped or repeated.

Assert the section sequence is non-decreasing and that visible numbering,
cross-references, and any structural comments all agree.

## 8. Re-read live data at the end, don't trust the draft

When figures come from a connected system, query it again before delivery. In
one pass a roadmap count moved from 60 to 62 because two records were added
after the first draft. Cite the source and the read date next to any figure
pulled from a system, so the next person knows how to re-check it.

Flag records that are known problems rather than real work (duplicates,
items already marked out of scope) instead of letting them inflate a count.

## 9. Names, spellings, and titles

Check each proper noun spells the same way everywhere, and flag the conflict
rather than silently picking one. Example: "Maria Alvarez" in one place,
"Marie Alvarez" in the source note. Same for organisation names, program names, and
job titles.

## 10. Accessibility and render integrity

For anything that renders:

- Every slide, page, or view actually renders and contains real content , 
  no blanks, no unrendered template placeholders (`${...}`), no "undefined".
- Navigation works and clamps at both ends; keyboard paths work.
- Speaker notes or alt text present wherever the format expects them.
- Decorative graphics are `aria-hidden`; meaningful ones carry a label.
  Repeating a background motif three times per divider with no label makes a
  screen reader announce three unnamed graphics.
- Small text meets contrast requirements, check the actual token used, not
  the palette's intent.

## 11. Claims that outrun their evidence

Flag statements the underlying data doesn't support, and soften or caveat them:

- A conclusion drawn from a very small sample presented as a general rule
  (a 35.7% response rate off 446 recipients is not a general rule).
- A favourable read on incomplete evidence (declaring an internship model
  proven before the final reports and hours are in).
- Unsourced figures. Every number should have a named source system, and
  anything unconfirmed should be marked as such before it goes in front of
  a senior audience.

## Final step

Re-run the full pass after making fixes. Fixes introduce their own errors , 
a corrected count changes a total, a corrected rate changes a pill colour, a
reorder breaks a transition. One clean pass end to end, not a clean diff.

