# Auditor

Run this at the end of every session and before any commit to main.

## Purpose
Keep documentation truthful and lean. Decisions stay current, stale files get flagged for deletion.

## Steps
1. Read docs/DECISIONS.md. For each Active decision, check it still matches the code and scope. Mark any contradicted or superseded decision as Superseded, with the new decision ID and date.
2. Read docs/SCOPE.md. Tick completed tasks, move finished stages to Done, and confirm the current stage is accurate.
3. Read docs/GOTCHAS.md. Remove entries that no longer apply. Merge duplicates.
4. Read docs/DATA_SOURCES.md. Flag any source with a missing licence, missing access date, or a dead link.
5. List every briefing, scratch note or planning file older than the current stage or no longer referenced. Propose them for deletion in a list. Do not delete without Jack approving.
6. Check CLAUDE.md read order still points to files that exist.
7. Output a short report: decisions changed, files proposed for deletion, open questions.

## Rules
- Never silently delete. Always propose.
- Never edit a decision's reasoning to hide a reversal. Supersede it instead.
