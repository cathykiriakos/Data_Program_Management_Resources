---
name: data-consistency-check
description: Checks a spreadsheet or CSV for stray spaces, mixed formats, and near-duplicate names, and reports findings without changing the file. Use before data feeds a report or an AI tool.
---

# Data Consistency Check

AI and reporting are only as good as the data under them. The first job is making the same thing look the same everywhere. This skill finds where it does not. It reports and recommends. It never edits the original.

## When to use it

- Before a dataset feeds a report, a dashboard, or an AI tool.
- When two lists should match and do not (donors, affiliates, partners, programs, sites).
- As the first pass of the guide in `Getting_Started/01_Make_Your_Data_Consistent.md`.

## What to check, column by column

Work through each column and report counts and examples.

1. **Stray whitespace.** Leading or trailing spaces, double spaces inside a value, tabs, and non-breaking spaces.
2. **Capitalization.** The same value written in different cases ("chicago", "Chicago", "CHICAGO").
3. **Format families.** Name the format the team should standardize on (the recommended default below, or the dominant format if the user has already chosen one) and list every value that differs. States should be one form (either "IL" or "Illinois", not both). Dates should be one form (ISO `2026-11-06` is the recommended default). Phone numbers should follow one pattern (`312-555-0142` is the recommended default, since no pattern dominates in most files). Zip codes should be five digits as text, so watch for lost leading zeros.
4. **Near-duplicates.** Names that differ only by punctuation, spacing, case, an abbreviation, or a small typo ("Lincoln Park Food Pantry", "Lincoln Park Food Pantry Inc.", "Lincoln Pk Food Pantry"). Group them and show each group.
5. **Blank and placeholder values.** Empty cells, "N/A", "none", "TBD", "-", and zero used to mean unknown.
6. **Mixed types and impossible values.** Numbers stored as text, text inside a numeric column, dates far in the future or before the organization existed (compare against today's date), and negative counts.
7. **Duplicate rows.** Fully identical rows, and rows that share an identifier but disagree.

## How to report

Start with one line saying how many rows and columns were checked and how many cells have an issue (count each affected cell once, and list issue types in the table). Then a table:

| Column | Issue | Count | Examples | Suggested standard |
|---|---|---|---|---|

Then list the three fixes that would clear the most affected cells, in order, breaking ties by which is quickest to do. Do not fix anything. Offer to write a cleaned copy to a new file, with the original untouched, and before removing any row, explain what the row is and what would be lost, as the `delete-with-context` skill describes.

## Rules

- Never change, overwrite, or delete the user's file. Work on a copy if a cleaned version is requested.
- Treat the data as sensitive. If it holds personal information about individuals (names, home contact details, case details), work from column samples and counts, and avoid repeating individual records in the summary. Organization contact details are lower risk, but still keep them out of the summary.
- When two values might be the same entity or might not, list them as "possible match, needs a human decision". Do not merge them.
- If the file is too large to read fully, say what was sampled and how.

## Free-plan fallback

If skills are unavailable, paste this file's text into the start of a conversation, attach or paste a sample of the table (a few hundred rows, with personal details removed), and ask: "Run the data consistency check on this."
