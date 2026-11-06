# Make Your Data Consistent
## A one-week guide for a team of one

**Document Owner:** Data Program Management Lead
**Classification:** Internal, Program Reference
**Version:** 1.0 | **Last Updated:** 2026-11
**Review Cycle:** Annual

> **Purpose:** Get your most important spreadsheet to the point where the same thing is written the same way everywhere. This is the single most useful step before reporting, dashboards, or AI.

---

## 1. Pick one spreadsheet

Choose the file you report from most often: the list of partners, sites, programs, or donors. Make a copy and work on the copy. Keep the original untouched until you are done and a peer has looked.

You will need about two hours per day for a week. Do one section a day.

## 2. Decide each format once

Write these decisions on one page called "Data Rules". Everyone who edits the file follows it.

| Field | Pick one form | Example |
|---|---|---|
| State | Two-letter code, or full name, never both | `IL` |
| Dates | Year, month, day, with dashes | `2026-11-06` |
| Phone | One pattern | `312-555-0142` |
| Zip code | Five digits stored as text so leading zeros survive | `02134` |
| Yes or no | Two values only | `Yes`, `No` |
| Names of people | Given name, then family name, in separate columns | `Maria`, `Alvarez` |
| Empty values | Leave the cell blank. Do not write N/A, none, TBD, or a dash | (blank) |

## 3. The five-day pass

**Day 1: Spaces.** Remove leading and trailing spaces and double spaces inside values. In Excel or Google Sheets, a helper column with `=TRIM(A2)` does this. Copy the results back as values only.

**Day 2: Capitalization and spelling.** Filter each column and read the unique values. Pick one spelling for each real thing and replace the others. "chicago", "Chicago", and "CHICAGO" become `Chicago`.

**Day 3: Formats.** Apply the decisions from section 2. Convert states, dates, phones, and zip codes. Check that dates are real dates and not text that looks like dates.

**Day 4: Duplicates.** Sort by the name column. Look for the same entity written two ways ("Lincoln Park Food Pantry" and "Lincoln Pk Food Pantry Inc."). Pick the canonical name. Do not delete either row yet. Add a column called `canonical_name` and fill it in. Merge only after a peer agrees.

**Day 5: Blanks and outliers.** Replace placeholders with blanks. Look for impossible values: a date in 2062, a negative count, a zip code with four digits.

## 4. Keep a change log

Add a second sheet called "Changes". For each fix, write the date, the column, what changed, how many rows, and who checked it. This is your audit trail, and it is also how you remember what you did in six months.

## 5. Before you delete anything

Write down what it is, why it is safe to remove, and what would be lost. Keep a copy of the original file in a folder labeled "before cleaning". An extra file costs almost nothing. A row you needed costs real work to rebuild.

## 6. Have AI scan it

After your own pass, ask Claude to scan the file with the `data-consistency-check` skill (`Skills_Library/data-consistency-check/SKILL.md`). It reports what it finds and changes nothing. If your file includes personal information about people, remove those columns first or work from a sample.

## 7. You are done when

- Every column passes the Data Rules page.
- The `canonical_name` column is filled in and a peer has checked it.
- The Changes sheet is up to date.
- A peer has completed `03_Peer_Check_One_Page.md`.

---

*Maintained by: Data Program Management | Last reviewed: 2026-11*
