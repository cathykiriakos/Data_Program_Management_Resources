# Installing a Skill
## Three steps in the Claude app, with a fallback for free accounts

**Document Owner:** Data Program Management Lead
**Classification:** Internal, Program Reference
**Version:** 1.0 | **Last Updated:** 2026-11
**Review Cycle:** Quarterly, plus a check before each workshop

> **Purpose:** Add a skill from this library to Claude so it applies automatically. Steps were checked against Anthropic's help pages on 2026-11-06. Menu names change, so if a label differs, look for the nearest match and check the pages linked at the bottom.

---

## Which route do you have?

| Your account | What to do |
|---|---|
| Free, Pro, Max, or Ultra in the Claude desktop app or claude.ai | Route A. Anthropic's page lists skills as available on these plans. |
| Team or Enterprise (including a discounted nonprofit Team plan) | Route A, but an organization owner may need to switch skills on first. See "Team and Enterprise" below. |
| Claude Code (a developer tool) | Route B. |
| Skills are missing or switched off, and you cannot change it | Route C. It works anywhere. |

The nonprofit plan point comes from Anthropic's help pages through a search result and was not opened directly. Treat it as unverified until you check your own plan.

## Route A: the Claude desktop app or claude.ai

**Step 1. Make a zip of the skill folder.** Each skill here is a folder, such as `data-consistency-check`, containing `SKILL.md`. Zip the folder itself, so that when the zip opens you see the folder, and inside it `SKILL.md`. Do not zip only the files. The folder name must match the skill's `name`. On Windows, right-click the folder and choose Compress to ZIP file. On a Mac, right-click and choose Compress.

**Step 2. Upload it.** In Claude, open Customize, then Skills. Select the plus sign, then Create skill, then Upload a skill, and choose the zip.

**Step 3. Turn it on and test it.** Make sure the skill is enabled in Customize, then Skills. Start a new chat and ask for the job in plain words, such as "Run a data consistency check on this spreadsheet." Claude should say it is using the skill. If it does not, ask for it by name.

**One setting to check.** Skills need code execution switched on. On a personal account, look under Settings, then Capabilities, for "Code execution and file creation" (newer versions may say "Create and edit files").

### Team and Enterprise

An organization owner turns on the feature in Organization settings, under Plugins and skills, on the Policy tab: "Cloud code execution and file creation" and "Skills". Owners can also provision a skill for everyone, and a skill can be shared with specific colleagues. If you cannot upload, ask your owner to check these settings.

## Route B: Claude Code

Copy the skill folder, with no zip, into `C:\Users\<your name>\.claude\skills\` on Windows or `~/.claude/skills/` on Mac and Linux, so the file sits at `.claude/skills/<skill-name>/SKILL.md`. To share it with a team, put it in `.claude/skills/` inside the project instead. A new skills folder may need `/reload-skills`. Anthropic's own skills can be added with `/plugin marketplace add anthropics/skills`.

## Route C: no skills feature, free account, or a locked-down computer

You lose nothing in the workshop with this route.

1. Open the skill's `SKILL.md` and copy all of it.
2. Start a new chat. Paste it as your first message and add: "Use these instructions for this conversation."
3. Paste or attach your material (remove personal details first) and ask for the job.

Do this each time, or keep the text in a project's custom instructions if your plan has Projects.

## Before you trust a skill

Skills are instructions, and some can run code. Anthropic's guidance for its marketplace says to trust a plugin before installing it. For this library: read the `SKILL.md` first, check there are no scripts you did not expect, and try it on a copy of non-sensitive data. Never use a skill on donor, client, or case files until someone has reviewed it. For outside skills, follow the safety note in `VETTED_LINKS.md`.

## If it fails

| Problem | Likely cause |
|---|---|
| Upload error | The zip holds loose files instead of the skill folder, the folder name does not match the skill name, or `SKILL.md` is missing |
| Skill uploads but never runs | It is not enabled, code execution is off, or the request does not match the description. Ask for it by name |
| Skills menu missing | Your organization has not enabled skills. Ask an owner, or use Route C |

## Sources

Checked 2026-11-06. Confidence: confirmed for the pages opened, as returned by a page summarizer.

- Using skills in Claude: `https://support.claude.com/en/articles/12512180-using-skills-in-claude`
- How to create custom skills: `https://support.claude.com/en/articles/12512198-how-to-create-custom-skills`
- Claude Code skills: `https://code.claude.com/docs/en/skills`

---

*Maintained by: Data Program Management | Last reviewed: 2026-11*
