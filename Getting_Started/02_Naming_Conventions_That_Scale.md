# Naming Conventions That Scale
## Names a new colleague understands, and that still work at 200 entries

**Document Owner:** Data Program Management Lead
**Classification:** Internal, Program Reference
**Version:** 1.0 | **Last Updated:** 2026-11
**Review Cycle:** Annual

> **Purpose:** Give your affiliates, partners, programs, and files names that are easy to read today and keep working as the list grows. All names and data in the examples are fictional.

---

## 1. Why naming is the foundation

Every report, join, and AI question depends on being able to say "these two rows are the same organization." When names vary, that question has no reliable answer. A small list can survive messy names because one person remembers. A list of 200 cannot.

## 2. The five rules

1. **One canonical name per entity, in one place.** Keep a master list. Every other file refers to the canonical name or its ID. Do not retype names.
2. **A stable ID for every entity.** Names change when organizations rebrand or merge. IDs do not. Use a short prefix and a number, such as `AFF-0042`. Never reuse an ID.
3. **Plain, readable display names.** Title Case, no abbreviations unless the abbreviation is the official name, no stray punctuation. A new colleague should read the name and know what it is.
4. **Characters that survive every tool.** No leading or trailing spaces, no double spaces, no slashes, and no commas inside a name if you export to CSV.
5. **Agreed words for common parts.** Decide once how to write "Incorporated", "Foundation", "Center", and "Saint". Then write them that way every time.

## 3. Worked examples (fictional)

| Messy entries | Canonical name | ID |
|---|---|---|
| `Lincoln Park Food Pantry`, `Lincoln Pk Food Pantry Inc.`, `lincoln park food pantry ` | Lincoln Park Food Pantry | AFF-0001 |
| `Westside Youth Ctr`, `West Side Youth Center`, `Westside Youth Center, Inc` | Westside Youth Center | AFF-0002 |
| `St. Anne Housing Alliance`, `Saint Anne Housing Alliance` | Saint Anne Housing Alliance | AFF-0003 |

Notice that the three rows each had two or three spellings, and that the fix was to choose one and record it with an ID. The messy versions are kept in an `also_known_as` column so nobody loses the trail.

## 4. Naming files and folders

Use `YYYY-MM-DD_topic_version`, lowercase, words joined by the _ character, and no spaces. For example, `2026-11-06_affiliate_master_v3.csv`. The date sorts correctly, the topic is searchable, and the version tells you which copy to trust.

## 5. A naming scheme that scales

| Decision | Small and scalable choice | Why |
|---|---|---|
| Hierarchy | Put region or program in its own column, not inside the name | You can filter without parsing text |
| Branches or sites | Parent name plus a separate `site_name` column | The parent stays one entity |
| Mergers | Keep the old ID, add a `replaced_by` column | History stays connected |
| Legal vs display name | Two columns | Funders get the legal name, readers get the display name |

## 6. Keep it alive

Write the rules on one page called "Naming Rules" and keep it beside the master list. Name one person who decides when a new case does not fit. Ask a peer to read any new name before it is added. The `naming-convention-builder` skill (`Skills_Library/naming-convention-builder/SKILL.md`) can propose a convention for your list and check names against it.

---

*Maintained by: Data Program Management | Last reviewed: 2026-11*
