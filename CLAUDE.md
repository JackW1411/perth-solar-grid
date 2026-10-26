# Perth Solar Grid

## Project
Geospatial pipeline mapping battery opportunity and detecting rooftop solar in the Perth metro area (SWIS).

## Owner and working style
- Jack writes the code himself to learn. Explain, review and suggest; do not dump large finished files unless asked.
- Python first. QGIS only for sanity checks and final map polish.
- Keep the repo clean and readable. It will be public and linked from LinkedIn. Avoid vibe-coded sprawl.

## Read order at session start
1. CLAUDE.md (this file)
2. docs/DECISIONS.md
3. docs/SCOPE.md (current stage only)
4. docs/GOTCHAS.md

## Rules
- Never claim solar causes household price rises. Network charges are the only supported link, and attribution is unproven.
- Every data source gets an entry in docs/DATA_SOURCES.md with URL, licence, date accessed and known limits.
- Record every real decision in docs/DECISIONS.md the moment it is made.
- Run the auditor (docs/AUDITOR.md) at the end of each working session.
- No secrets, API keys or raw large data files in git.

## Structure
- `data/raw`: untouched downloads (gitignored)
- `data/processed`: pipeline outputs (gitignored)
- `src`: pipeline code
- `notebooks`: exploration only
- `docs`: scope, decisions, gotchas, data sources, auditor

## Gotchas
See docs/GOTCHAS.md. Add to it whenever something wastes more than 15 minutes.
