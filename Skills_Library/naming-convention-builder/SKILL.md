---
name: naming-convention-builder
description: Designs a naming convention for affiliates, partners, programs, or files that stays readable as the list grows, then checks a list against it. Use for messy or growing name lists.
---

# Naming Convention Builder

A good naming convention is understood by a new colleague without explanation, and it keeps working when 10 names become 200. This skill designs one with the user and then checks real names against it.

## When to use it

- Setting up a list of affiliates, partners, sites, programs, or funders.
- Naming files, folders, tables, or columns before a project grows.
- Cleaning an existing list that grew without rules.

## Step 1: Learn what is being named

Ask what the things are, how many exist now, how many might exist in two years, who types the names, and which tools read them (spreadsheet, CRM, database, AI tool). Ask which names already exist that cannot change, such as legal names or names a funder requires, and whether a legal suffix like Inc is part of the legal name.

## Step 2: Propose the convention

Offer one recommended convention, with the reasoning, and show five worked examples using the user's own kinds of things. A sound default:

- One canonical name per entity, written once, in one place (a "master list"). Every other file points at the canonical name.
- Plain readable words in Title Case for display names. No abbreviations unless the abbreviation is the official name, with one exception: the agreed words in the last bullet.
- A short stable ID for each entity (for example `AFF-0042`), because names change and IDs do not. Never reuse an ID.
- No leading or trailing spaces, no double spaces, and no special characters that break tools (slashes, or commas inside a name when exporting to CSV).
- For files: `YYYY-MM-DD_topic_version`, lowercase, words joined by the _ character, no spaces.
- For states, countries, and dates: choose one form and write it down. Two-letter state codes and ISO dates are good defaults.
- A short list of agreed words for common parts, written one way each: "Center" (never "Ctr"), "Saint" (never "St."), and a rule for legal suffixes such as Inc or LLC (keep them in the legal name column and drop them from the display name).

Explain the tradeoff of each choice in a sentence. If the user prefers something else, adopt theirs and keep it consistent.

## Step 3: Check a list against it

This step checks names only. For other columns such as states, dates, and phones, point the user to the `data-consistency-check` skill. When the user shares names, return a table of each name that breaks the convention, the rule it breaks, and the suggested fix. Group near-duplicates and flag possible matches for a human decision instead of merging them. Report counts first: names checked, names passing, names needing a fix. A name that passes alone but belongs to a near-duplicate group counts as needing a decision.

## Step 4: Write it down

Finish with a one-page "Naming Rules" the team can keep next to the master list: the rules, five examples, and who decides when a new case does not fit. Suggest a peer check: a second person reads any new name before it is added.

## Rules

- Never rename or delete anything in the user's data. Recommend and report.
- Legal and funder-required names stay as given. Put the display convention in a separate column.
- Treat lists of people or clients as sensitive. Work on organization names unless the user says otherwise.

## Free-plan fallback

If skills are unavailable, paste this file's text at the start of a conversation, then paste your list of names and ask: "Build a naming convention for this list and check it."
