---
name: "delete-with-context"
description: Before any deletion or overwrite, explains what the thing is, why it is safe to remove, and what would be lost. Use for files, folders, records, and rows dropped in a data clean.
---

# Deleting things: context first, always

Why this matters for a small data team: cleaning data means dropping rows, overwriting files, and clearing columns, usually without a second person watching. This skill makes every removal explain itself first.

The person approving a deletion should understand what they are approving before anything is removed. A bare file path in a permission prompt is not enough information to make a decision with, and they should never have to ask "what specifically are we cleaning up?"

## Before any delete, say these five things

1. **What it is**, in plain language. Not the filename, the thing. "A snapshot I took before running the merge script" beats "output.md.bak".
2. **How it got there.** Did Claude create it, is it a working copy, a backup, an export, or something the user put there.
3. **Why it is safe to remove.** What makes it redundant, stale, or superseded.
4. **What would be lost.** If something is unique to that file, name it. If nothing is, say so plainly, because that is the reassurance the user is looking for.
5. **The case for keeping it.** Give a real alternative so the choice is genuine, not a rubber stamp.

Keep this to a short paragraph or a few lines. It is context, not a report.

## Scope

This covers more than `rm`. Apply it to:

- Deleting or trashing files and folders
- Deleting database or spreadsheet records, or clearing a field across records
- Dropping rows, columns, or sheets during a data clean
- Overwriting a file with content that discards what was there
- Any script or tool call that removes something as a side effect

The last one matters most, because it is the easiest to do without noticing. If a script Claude is about to run deletes or overwrites anything, surface that before running it, not after.

## Batch deletes

Never present a bare list of paths. Group by kind, give counts, and describe each group in one line. "Twelve intermediate CSVs the build script generated, plus three PNG previews, none referenced by the final report" is reviewable. A wall of filenames is not.

## Backups Claude creates

If Claude makes a `.bak` or working copy before a risky operation, say so at the time it happens. When the operation succeeds, name the backup and ask before removing it. Do not quietly clean up after yourself; that is exactly the invisible deletion this rule exists to prevent.

## When permission is denied

Acknowledge it and stop. Do not re-request the same deletion with different wording. Offer alternatives instead: leave it, rename it to mark it stale, or move it somewhere out of the way. A denial is useful information about what the user wants to keep, so treat it that way.

## Default when uncertain

Keep the file, flag it in the summary, and move on. An extra file costs almost nothing. A deleted one they wanted costs real work to reconstruct, and sometimes it cannot be reconstructed at all.

