# Vetted Links
## Outside plugins and skill libraries, with the evidence for each

**Document Owner:** Data Program Management Lead
**Classification:** Internal, Program Reference
**Version:** 1.0 | **Last Updated:** 2026-11
**Review Cycle:** Quarterly, plus a check before each workshop

> **Purpose:** A short list of outside skill and plugin libraries a small nonprofit can look at, each with what was checked and when. Popularity alone does not qualify an entry. Each one has a named maintainer, a license statement, a recent update, and a primary page that was opened. Anything not fully checked says so.

---

## How entries were checked

On 2026-11-06 each repository's GitHub page, license, star count, and latest commit or release were read. Stars show interest, not safety. Confidence labels are confirmed (primary page opened and facts matched), secondary only (seen in a listing but not read in full), and unverified. Page text was read through a summarizer, so re-open a page before quoting it.

## Start here: Anthropic's own libraries

| Library | What it offers a nonprofit | Maintainer | License | Last update | Stars | Confidence |
|---|---|---|---|---|---|---|
| `https://github.com/anthropics/skills` | Skills for Word, PDF, PowerPoint, and Excel files, plus document co-authoring, internal communications, and a skill for writing new skills | Anthropic | Mixed. Many skills are Apache 2.0. The Word, PDF, PowerPoint, and Excel skills are source-available and not open source. No single license covers the repository | 2026-10-28 | 188.1k | confirmed |
| `https://github.com/anthropics/knowledge-work-plugins` | Plugins for data work (validate data, explore data, statistics, charts), marketing, and productivity. A small-business folder has grant, report, and proposal writing skills | Anthropic | Apache-2.0 | 2026-11-06 | 35.0k | confirmed |
| `https://github.com/anthropics/claude-plugins-official` | The official plugin marketplace. Third-party plugins listed there are not written by Anthropic | Anthropic | Apache-2.0 repository, with each plugin carrying its own license | 2026-11-06 | 46.3k | confirmed |

Notes. Some plugins connect to outside services such as email and customer databases, so check what a plugin connects to before installing. The small-business folder was seen in the repository listing and not in the README. The official marketplace README warns: "Make sure you trust a plugin before installing, updating, or using it."

## Other libraries worth a look

| Library | Fit | Maintainer | License | Last update | Stars | Confidence |
|---|---|---|---|---|---|---|
| `https://github.com/K-Dense-AI/scientific-agent-skills` | Research skills including literature synthesis and grant writing. Aimed at scientists and uses many Python packages, so only some of it fits a small team | K-Dense Inc | MIT | 2026-11-02 | 56.3k | confirmed |
| `https://github.com/VoltAgent/awesome-agent-skills` | A directory of skills from many authors. Use it to discover, then read each skill yourself | VoltAgent | MIT | 2026-11-05 | 36.9k | secondary only |

## Browse with care

These are curated lists that point to many authors' work. Anything you find through them is unreviewed.

| Library | Caution | Maintainer | License | Last update | Stars | Confidence |
|---|---|---|---|---|---|---|
| `https://github.com/ComposioHQ/awesome-claude-skills` | Its app-connection skills need an account with the vendor, send data through the vendor's service, and do not document a security model. One entry controls your logged-in browser | Composio (a company) | Apache-2.0 for the repository, and individual skills may differ | 2026-07-24 | 78.9k | confirmed |
| `https://github.com/travisvn/awesome-claude-skills` | The last update was six months ago. Its own warnings are worth reading: skills can run arbitrary code, and you should install only from trusted sources | A community maintainer | Not stated on the page | 2026-04-28 | 15.7k | confirmed for the facts shown, license unverified |

## Safety note for installing any outside skill

1. Install only from Anthropic's repositories or from people and organizations you can name.
2. Open `SKILL.md` and any scripts folder before installing. Do not install if you see network calls, requests for passwords or keys, or instructions to send files somewhere else.
3. Skills and plugins can change after you install them. Recheck after updates and prefer a pinned version.
4. Try a new skill on a copy of non-sensitive data first.
5. Keep donor, client, and case files away from a skill until someone with IT or security responsibility has reviewed it.

## What this list does not cover

It does not rate quality of output, and it does not cover software-development libraries, which are less relevant to a team without engineers. It leaves out libraries that could not be opened. To propose an addition, send a link, and check it against the criteria above before it goes in.

---

*Maintained by: Data Program Management | Last reviewed: 2026-11*
