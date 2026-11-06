# Getting Started
## Domain README: The Crawl Stage

**Domain Owner:** Data Program Management Lead
**Platform:** A spreadsheet is enough
**Version:** 1.0 | **Last Updated:** 2026-11
**Classification:** Internal, Program Reference
**Review Cycle:** Annual

> **Purpose:** This folder is for the person who owns "the data stuff" at a small organization with no data program. It holds the first three things to do: make your data consistent, give your affiliates and partners names that scale, and have a peer check your work. Nothing here needs a data platform, and nothing here needs AI. It is the foundation that AI results depend on.

---

## Why this comes first

An AI tool reads your data the way a new colleague would, only faster and without asking questions. If "IL", "Illinois", and "Illinois " (with a trailing space) all appear in the state column, the tool treats them as three different places. The report it produces will look confident and be wrong. Fixing the labels first costs a few hours. Fixing a decision made on bad labels costs far more.

## Document index

| # | Document | Version | Status | Primary audience |
|---|---|---|---|---|
| 01 | `01_Make_Your_Data_Consistent.md` | 1.0 | Active | The one person who owns the data |
| 02 | `02_Naming_Conventions_That_Scale.md` | 1.0 | Active | Anyone who creates or edits lists of partners, affiliates, or programs |
| 03 | `03_Peer_Check_One_Page.md` | 1.0 | Active | The data owner and one trusted peer |

## Quick navigation

| You need to... | Start here |
|---|---|
| Clean a spreadsheet this week | `01_Make_Your_Data_Consistent.md` |
| Decide how to write state names, dates, and phone numbers once | `01_Make_Your_Data_Consistent.md`, section 2 |
| Name affiliates and partners so the list can grow | `02_Naming_Conventions_That_Scale.md` |
| Get a second pair of eyes without a formal audit | `03_Peer_Check_One_Page.md` |
| Have AI scan your file for these problems | `Skills_Library/data-consistency-check/SKILL.md` |
| Pressure-test a strategy before you present it | `Skills_Library/board-of-advisors/SKILL.md` and `Skills_Library/devils-advocate/SKILL.md` |

## Ready for the next stage when

These are proposals. Adjust them to your organization.

- Every list you report from (partners, sites, programs, donors) has one master copy.
- A new column or name added this month follows the written rules without anyone asking how.
- A peer has checked your last three changes.
- You can say, for your most important report, where each number comes from.

When those are true, move to the walk stage: `Data_Quality_Standards/` for quality rules, and the lean track in `Agentic_AI_Standards/02_Agentic_Program_Establishment.md` for a first low-risk agent. The stages are described in the top-level `README.md`.

## Cross-domain dependencies

| Related document | Relationship |
|---|---|
| `Skills_Library/` | Skills that run these checks for you |
| `03_data_governance_standards.md` | The enterprise version of the naming and ownership rules, for the run stage |
| `AGENTIC_README.md` | Where agents come in, after the foundation exists |

---

*Maintained by: Data Program Management | Last reviewed: 2026-11*
