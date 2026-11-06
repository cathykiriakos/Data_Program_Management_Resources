# Facilitator Notes: Agentic AI Standards Workshop

These notes are for the person running the room. The audience is small teams of one to ten people at social sector organizations, mixed technical comfort, often with one person who already uses an AI tool and nobody who has written a charter. The participant materials are the one-page checklist (`Agentic_AI_Standards/workshop/CHECKLIST_ONE_PAGE.md`) and the exercise (`Agentic_AI_Standards/workshop/EXERCISE_BUILD_AN_AGENT_CHARTER.md`). The worked example is in `Agentic_AI_Standards/examples/donor_acknowledgment_agent/`.

## Timing

### 90 minute format

| Minutes | Segment | Notes |
|---|---|---|
| 0 to 10 | Why charters, why not trust them | Say it plainly: a charter is a prompt, and only a control outside the model holds. Use section 3 of `Agentic_AI_Standards/01_Agentic_Best_Practices.md` |
| 10 to 20 | Walk the worked example | Read the example charter aloud, section by section. Point at each "Enforced by" line |
| 20 to 80 | Exercise, steps 1 to 7 | 70 minutes as written. Cut step 7 to 5 minutes if the room runs late |
| 80 to 90 | Checklist and close | Hand out the one-page checklist. Each person names one no they will fix this month |

In 90 minutes, skip the assessor agent charter. Participants name a second reviewer role and set the assessor to null, which the T3 rule allows. They still do the swap in step 6 as a human assessor.

### Half-day format (about 3.5 hours with a break)

| Minutes | Segment |
|---|---|
| 0 to 15 | Opening and the risk picture, using the landscape facts confirmed that morning |
| 15 to 40 | Walk the worked example and the assessor run (`Agentic_AI_Standards/examples/donor_acknowledgment_agent/assessor_run.md`) |
| 40 to 125 | Exercise, with the assessor charter built from the boundary assessor template and the linter run on both |
| 125 to 140 | Break |
| 140 to 170 | Pairs rotate and assess a second charter. Add a sample the author tries to make fail |
| 170 to 190 | Consent and equity discussion, using prompts below |
| 190 to 210 | Checklist, "ten things teams usually miss", and one commitment each |

## Room setup

- Tables of two or three so the swap in step 6 is quick. Pairs sit side by side.
- Each person has a laptop with a text editor. At least one in each pair has Python 3 and PyYAML working. Test this the day before: run `python tools/agent_lint.py Agentic_AI_Standards/examples` on a loaner machine. It should print "agent_lint: clean".
- Printed one-page checklists and printed copies of the lean path section of the exercise for anyone without Python.
- A shared folder or a printed set of the worked example files. A projector for walking through the charter.
- Do not ask people to use real client or donor data. Check the folder for real names before anyone shares a screen.

## Common failure modes

- **People pick an agent that sends.** A "follow-up email agent" is the most common idea. Redirect to a draft-only version. The worked example does exactly that.
- **The charter reads like a policy statement.** No "Enforced by" lines, or lines such as "the model will not". Ask what stops it when the model does not comply.
- **Skipping the mirror.** The linter fails because the charter and row disagree on a write tool, a data class, or a gate. This is the lesson, not a mistake to hurry past.
- **Tier shopping.** Participants pick T4 so there is less to fill in. Ask what data it touches and take the highest tier any answer gives, unless the recorded draft-only exception applies.
- **Choosing a forbidden data class.** Immigration status, health, safety-sensitive, or children's data. Name the default exclusion in AGT-DAT-01 and AGT-CON-02, and ask them to pick another idea.
- **The assessor is treated as a gate.** Say it out loud: the assessor is a triage aid, and a person approves anything that leaves the organization.
- **Fluent samples pass.** Peers say yes because the sample sounds good. Ask them for the one observable claim in it that they could not verify.
- **Python problems eat the clock.** Move that person to the lean path at once. Do not debug an install in the room.
- **Real details leak in.** Stop the screen share and ask them to replace names with roles.

## Discussion prompts

1. Which of your current tools, with an AI feature, already has write access you did not choose?
2. What would you do if the agent in your charter told you to stop and then did not?
3. Who in your organization could be harmed if this agent gets it wrong, and who would hear about it?
4. If a client objected to AI processing of their record, how would you take them out of the export without changing the service they receive?
5. What would your board or funder want to see about this agent next quarter, and is it in the registry row?
6. Who is the second reviewer, and what do they stop doing to find the time?
7. The worked example needed an exception to land at T3 for donor data. Would your organization accept that, or classify donor contact as personal data and take T2?
8. If the pinned model were retired in 30 days, who would find out, and who would run the saved test cases?

## Morning-of list: check before relying

Several facts in this workshop come from `Agentic_AI_Standards/LANDSCAPE_SNAPSHOT.md`, which was read on 2026-11-04 and is dated for the workshop on 2026-11-12. On the morning of the workshop, confirm each item below against its primary source (the URLs and access dates are in `Agentic_AI_Standards/SOURCES.md`). If anything has changed, tell the room, and change your slides, not your standards. The standards do not repeat dated facts. Do not teach any claim from a secondary only or unverified row as settled.

Short shelf life, confirm first:

- [ ] Model retirement dates: Claude Sonnet 4.5 and OpenAI Agent Builder on 30 Nov 2026, Gemini 2.5 on 1 Dec 2026, GPT-5 snapshots on 11 Dec 2026. Section 4 and "Things easy to miss" row 1 of the snapshot
- [ ] AIUC-1: the latest release (15 Oct 2026) and the next (15 Jan 2027). Its release page and its changelog disagree on counts and one control number, so quote neither count
- [ ] MCP: current revision is 2026-07-28. Check that no newer revision has been published
- [ ] Colorado: SB26-189 duties from 1 Jan 2027, attorney general rules due the same date
- [ ] EU dates: Digital Omnibus changes to the high-risk dates and the 2 Dec 2026 dates
- [ ] Anthropic API version 2026-10-21 and the removed sampling parameters, if anyone brings old code

Rows with date or version claims graded secondary only or unverified. Say "reported" for these or leave them out:

| Snapshot row | Grade | What not to claim |
|---|---|---|
| EU AI Act, Digital Omnibus | secondary only | Official Journal date 24 Jul 2026 and entry into force 27 Jul 2026 appear only in search summaries. Confirm on the Official Journal first |
| Five Eyes joint guidance | date confirmed, categories secondary only, recommendation count unverified | The number and text of recommendations |
| OWASP Top 10 for Agentic Applications | date confirmed, names secondary only | Any entry beyond ASI01, ASI06, and ASI10 |
| ISO/IEC 42001 | unverified | Any detail beyond "certifiable AI management system" |
| OpenAI Preparedness Framework, Google DeepMind Frontier Safety Framework | unverified | Version numbers and dates |
| CSA MAESTRO and autonomy levels | unverified | Any detail |
| Auth0 for AI Agents and Auth for MCP | unverified | General availability dates |
| Microsoft Entra Agent ID | month confirmed (April 2026), price unverified | A day or a price |
| MCP 2026-07-28 release | confirmed, one date unverified | The 18 Jun 2026 stable date for the Enterprise Managed Authorization extension |
| NIST agent work | confirmed, SP 800-53 overlays unverified | Any statement that overlays exist |
| Meta Llama licences | secondary only | Terms for any specific generation |
| FERPA and AI | secondary only | Any claim that the Department has published AI guidance |
| HIPAA business associate points | unverified | Any statement of regulatory text or dates |
| Consent standards for vulnerable populations, small organization cost data | unverified | Treat AGT-CON-01 and AGT-CON-02 as this library's position, not a cited external standard |
| Liability insurer AI exclusions | unverified | Say "reported" and tell people to ask their broker |
| Colorado litigation and nonprofit coverage | unverified | Any statement about lawsuits or nonprofit scope |

Then confirm the room itself: run the linter on the examples folder with the date pinned (`python tools/agent_lint.py Agentic_AI_Standards/examples --today 2026-11-04`, the same pin the workflow uses so the examples do not expire), check that the worked example still passes after any edits since 2026-11-04 (its `review_date` values are in 2027), and make sure no real names have entered the folder.

## Closing segment: add three skills live (10 minutes)

Run this at the end of either format. It shows attendees how to take the crawl-stage skills home. Most attendees will use the Claude desktop app, with a mix of free and paid accounts, so lead with the app route and have the paste fallback ready for anyone whose menu has no Skills entry. The full steps are in `Skills_Library/INSTALL.md`.

| Minutes | Step |
|---|---|
| 0 to 2 | Show the nine skills in `Skills_Library/README.md` and say which are crawl stage. Make the point that a skill is plain text anyone can read before installing it |
| 2 to 5 | Live install of `data-consistency-check`: zip the folder, then Customize, Skills, plus, Create skill, Upload a skill. Show the folder-inside-the-zip rule and what an upload error looks like |
| 5 to 8 | Run it on the fictional sample list you prepared. Show that it reports and changes nothing |
| 8 to 10 | Run `board-of-advisors` on a one-paragraph strategy from the room. For attendees without skills, show Route C: paste the file's text as the first message |

Before the room fills, check the following the morning of:

- [ ] Your own account can upload a skill, and code execution is on
- [ ] The three skill folders are already zipped on the projector machine and on a shared drive, with the folder at the root of each zip
- [ ] The fictional sample spreadsheet has stray spaces, mixed state formats, and three near-duplicate names, and contains no real names
- [ ] You re-opened the three pages in the Sources list of `Skills_Library/INSTALL.md` and the menu labels still match
- [ ] Attendees were told in advance not to bring client or donor data to the demo
