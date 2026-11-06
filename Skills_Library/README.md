# Skills Library
## A starter set of AI skills for small nonprofit teams

**Document Owner:** Data Program Management Lead
**Classification:** Internal, Program Reference
**Version:** 1.0 | **Last Updated:** 2026-11
**Review Cycle:** Quarterly, plus a check before each workshop

> **Purpose:** A skill is a short set of written instructions that teaches Claude to do one job the same careful way every time. This folder holds nine skills chosen for small nonprofit teams, a three-step install guide, and a short list of outside libraries that have been checked. The library is meant to grow: add a skill when your team keeps repeating the same careful steps.

---

## The nine skills

Each skill is a folder with one file, `SKILL.md`. Read it before you install it. They are plain text.

| Skill | Use it when | Stage |
|---|---|---|
| `data-consistency-check` | A spreadsheet should be clean before you report from it or give it to AI. It reports problems and changes nothing. | Crawl |
| `naming-convention-builder` | You are naming affiliates, partners, programs, or files, or you have a messy list of names. | Crawl |
| `board-of-advisors` | You are about to present a strategy and want it reviewed from several expert points of view. | Crawl |
| `devils-advocate` | You want honest pushback on a plan: hidden assumptions, blind spots, realistic failure modes. | Crawl |
| `delete-with-context` | Anything is about to be deleted or overwritten. It explains what would be lost first. | Crawl |
| `researching-with-confidence` | You need a researched answer where every finding carries a confidence rating and gaps are named. | Walk |
| `deliverable-validation` | A report, deck, or spreadsheet is about to go out. It checks that counts, totals, dates, and names agree. | Walk |
| `content-research-writer` | You are drafting a grant narrative, report, or appeal that needs sources. | Walk |
| `dont-sound-like-ai` | Draft text needs an editing pass so it reads like a person wrote it. | Walk |

The stages match the crawl, walk, and run path in the top-level `README.md`. The first five are worth adopting in your first month.

## How to start

1. Read `INSTALL.md` and add two skills: `data-consistency-check` and `board-of-advisors`.
2. Run `data-consistency-check` on your most important list.
3. Before your next strategy conversation, run `board-of-advisors` and `devils-advocate` on your draft.

## Adding your own skill

When your team repeats the same careful steps, write them down as a skill. Keep it to one job. Copy the format of any skill here: a `SKILL.md` file that starts with a `name` and a `description` (200 characters at most, so it uploads to the Claude app), followed by plain instructions. Test it on fictional data. Have a peer read it. Then add it to this folder with a row in the table above.

Skills in this folder follow three rules: no real names or data inside them, no instructions to send files anywhere, and no scripts unless a reviewer has read every line.

## Provenance

`board-of-advisors`, `devils-advocate`, `researching-with-confidence`, `delete-with-context`, and `deliverable-validation` come from the program lead's own working set, with personal references removed and dashes replaced. `dont-sound-like-ai` is adapted from the same set. `content-research-writer`, `data-consistency-check`, and `naming-convention-builder` were written for this library. Descriptions were shortened to fit the 200-character limit of the Claude app, and the original trigger phrases for three skills moved into the body.

## Related

| Document | Relationship |
|---|---|
| `INSTALL.md` | How to add a skill to Claude, by plan type |
| `VETTED_LINKS.md` | Outside plugins and skill libraries, with the evidence for each |
| `Getting_Started/GS_README.md` | The crawl stage these skills support |

---

*Maintained by: Data Program Management | Last reviewed: 2026-11*
