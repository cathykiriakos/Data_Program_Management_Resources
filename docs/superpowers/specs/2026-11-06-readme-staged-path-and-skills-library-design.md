# Design: Staged README and a Starter Skills Library

Date: 2026-11-06. Author: Claude, with Cathy Kiriakos. Status: draft for approval.
Deadline: the "AI for Social Sector" workshop on Thursday 2026-11-12.

## Intent and why

The library was written for a large enterprise data program. The partners it now needs to serve are small nonprofits with no data program, where one person owns "the data stuff" next to other duties. For that reader the current README is a wall: it opens with a Snowflake and Collibra stack diagram and an audit vocabulary they do not use.

The idea Cathy wants every partner to take away is that AI is only as good as the data beneath it. A clean, consistent data repository is the foundation of any successful AI work, and it is what keeps results repeatable as pipelines grow. The README should say this first and let it organize everything else.

Two additions follow from that. First, a staged path (crawl, walk, run) so a partner can see which concepts are required now and which can wait. Second, a small skills library the team can keep iterating on, plus a short list of vetted outside plugins and skill libraries, so partners have working tools on day one.

## Audience

Primary: the one person at a small nonprofit who owns the data, usually without a data background, who has been told AI is coming. Secondary: the executive director or board member who needs to know what to ask that person for. Tertiary: partners at larger organizations, who can skip to the walk and run material and the existing enterprise standards.

## Goals

1. A reader can say within five minutes what this library is for, whether it is for them, and what to do first.
2. Each stage of crawl, walk, and run has a short list of must-haves, a list of what can wait, and a plain "ready for the next stage when..." test.
3. The crawl stage is usable by one person in a week with a spreadsheet and no tooling.
4. A starter skills library of nine skills, each installable by a non-engineer in three steps, with a "when to use it" line.
5. A vetted links page for outside plugins and skill libraries, with the evidence for each entry.
6. The workshop can end with a quick live walkthrough of installing and running two or three of the skills.

## Non-goals

- Rewriting the existing enterprise standards. They stay as the "later" material and are linked from the stages.
- Building software beyond the skill files and, where a skill needs it, one small checking script.
- Covering every possible nonprofit use case. Nine skills, not ninety.

## Anti-goals

- A README that reads as enterprise governance with a friendly paragraph added on top.
- Treating AI as step one for a team with no data program.
- Links to tools nobody has checked. An unverified entry labeled unverified is acceptable. An unlabeled one is a failure.
- Anything from a private vault, private partner context, or personal voice and brand skills ending up in a public repo.

## The staged path

Crawl: make the data consistent. Labels are identical everywhere. A state is written one way, with no leading or trailing spaces. Affiliate and partner names follow a convention that is easy to read and still works when the list grows from 10 to 200. A peer double-checks the work instead of a formal audit function. Strategy gets pressure-tested with the board-of-advisors and devils-advocate skills before it is presented, because small blind spots compound over time.

Walk (Cathy's phrasing leaves this to me, so this is my proposal): data quality rules, named ownership for each dataset, a glossary of the few terms that matter, a simple data inventory, and the lean-track agent charter for a first low-risk agent.

Run: governed agents with identity, charters and assessors, certification of data products, incident response, and the enterprise standards.

My guess on the mapping, for Cathy to correct: Crawl uses new short documents plus the skills library. Walk draws on `Data_Quality_Standards/`, the lean track in `Agentic_AI_Standards/02_Agentic_Program_Establishment.md`, and the one-page checklist in `Agentic_AI_Standards/workshop/`. Run points at everything else in the library.

## Deliverables

1. A rewritten top of `README.md`: intent, audience, how to use the library as guidance, and the crawl, walk, run path, placed before the existing technology stack and index. The existing index and sections remain below it.
2. `Getting_Started/` (new folder, underscore naming per the repo convention) with three short crawl documents: a "make your data consistent" guide, a naming convention guide with worked examples (states, affiliates, dates), and a one-page peer check. Each follows the repo's header block (owner, classification, version, last updated, review cycle).
3. `Skills_Library/` (new folder) with a README and one folder per skill, each holding a `SKILL.md`. Nine skills:
   - Seeded from Cathy's existing skills, as written: `board-of-advisors`, `devils-advocate`, `researching-with-confidence`.
   - Adapted from Cathy's existing skills with her name and personal references removed: `delete-with-context`, `deliverable-validation`, `dont-sound-like-ai`, `content-research-writer`.
   - Newly written: `data-consistency-check` (scans a spreadsheet for stray whitespace, mixed formats, and near-duplicate names, and reports without changing anything) and `naming-convention-builder` (helps design a scalable naming convention, then checks a list against it).
4. `Skills_Library/INSTALL.md`: how to add a skill to Claude, written for a non-engineer, in three steps, and covering the cases a workshop room will hit (Claude desktop app, Claude Code). The exact steps must be verified against current Anthropic documentation at build time.
5. `Skills_Library/VETTED_LINKS.md`: outside plugins and skill libraries, each with a one-line reason, the date checked, and a confidence label of confirmed, secondary only, or unverified. Anthropic's official document skills (Word, PDF, PowerPoint, Excel) are linked, not copied.
6. A workshop segment: a short addition to `Agentic_AI_Standards/workshop/FACILITATOR_NOTES.md` giving a ten-minute walkthrough that installs and runs two or three skills.
7. Index, lint, and ledger upkeep so the existing linters stay clean: new files named in the README index, `REFRESH_LEDGER.md` updated, and prose rules honored.

## Constraints

- Writing rules for anything authored on Cathy's behalf: no em dashes or en dashes, none of the banned words in her global instructions, prose for explanations and lists for procedures.
- The repository is public. Nothing from `CAAI-Vault`, `Context-Engine`, or her private skills (brand, partner, faculty, council, writing voice) goes in.
- No binaries. Skills are Markdown. A checking script, if used, is plain Python with no dependencies beyond the standard library.
- The skills seeded from Cathy's folder are her own work. Adapted copies keep the substance and change only personal references. She approves the adapted versions.
- `library_lint.py` and `agent_lint.py` must stay clean, with the tests passing. The prose scope in `tools/common.py` may need extending to the new folders so the style rules apply there too.
- Must be ready to review by Tuesday 2026-11-10 to leave time for a dry run before Thursday.

## Decisions made by Cathy

- The audience is a small nonprofit with one data owner and no data program.
- Foundation first: consistency of labels, naming that scales, peer review instead of a second line of defense.
- Use skills such as board-of-advisors and devils-advocate to pressure-test strategy.
- The shortlist of nine skills, including the two new data skills.
- Walk through installing the skills at the end of the workshop.

## Decisions made by Claude (Cathy to check)

- Folder names `Getting_Started/` and `Skills_Library/`, matching the underscore convention.
- What the walk stage contains, and the mapping of existing documents to stages.
- New work goes on a new branch stacked on `feat/agentic-ai-standards-pillar`, because PR #1 already rewrote the README index and a separate branch from `main` would conflict. If PR #1 merges first, the new branch rebases onto `main`.
- Vetting criteria for outside links: an active repository or vendor page, a named maintainer, a license, and a primary source I can fetch. Community popularity alone does not qualify.
- The two new data skills are instruction-only. A small script is added only if a skill cannot check a file reliably without one.

## Facts the builder needs

- Repo: `C:\Users\ckiriakos\source\Data_Program_Management_Resources`, a clone of `github.com/cathykiriakos/Data_Program_Management_Resources`. PR #1 (`feat/agentic-ai-standards-pillar`) is open, mergeable, and CI is green as of 2026-11-06. Build on that branch.
- Skill sources are in `C:\Users\ckiriakos\.claude\skills\synced\<id>\<skill-name>\SKILL.md`. The allowlist is exactly these seven: `board-of-advisors`, `devils-advocate`, `researching-with-confidence`, `delete-with-context`, `deliverable-validation`, `dont-sound-like-ai`, `content-research-writer`. Touch no other skill folder. The first three were read in full and contain no personal references. The other four name Cathy or her tools and need adapting.
- The existing README opens with a technology stack diagram and an index. Both stay.

## More calls made by Claude (Cathy to check)

- The adapted skills are staged as drafts. Cathy approves them at the Tuesday 2026-11-10 review, and the dry run follows.
- The README keeps the stack diagram and index, moved below the new opening, with a pointer saying the enterprise material is for larger organizations and for the walk and run stages.
- `SKILL.md` files keep the format Claude requires (name and description frontmatter) and are exempt from the repo header block. The skill folders are added to the prose-rule scope and exempted from the header check in `tools/library_lint.py`.
- The "ready for the next stage when..." tests are drafted by the builder and marked as proposals for Cathy to adjust. The worked examples use fictional data only.

## Decisions from the review round

- The workshop room will mostly use the Claude desktop app, with a mix of free and paid accounts. INSTALL.md leads with the desktop route and states plainly what a free account can and cannot do. Every skill also gets a paste-the-instructions fallback that works without any skills feature, so a free-plan attendee loses nothing in the workshop.
- Status: approved by Cathy on 2026-11-06 ("Let's build this with that in mind").

## Left to the builder

- Exact wording and layout of each document, within the repo header convention.
- Which outside plugins and skill libraries meet the vetting criteria, found by web search at build time.
- The sample data used in the worked examples, which must be fictional.
- How the skills are tested: at least one run of each skill against a fictional input, with the result checked.
