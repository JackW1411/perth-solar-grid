# Decisions

Superseded decisions stay in the table. Never edit a reason to hide a reversal; add a new decision and mark the old one `Superseded by Dn (date)`.

| ID | Decision | Reason | Date | Status |
|----|----------|--------|------|--------|
| D1 | Build as a Python pipeline, not a manual QGIS project | Repeatable, rerunnable, better portfolio signal | 2026-10-26 | Active |
| D2 | Battery map and rooftop detection live in one project, staged | Detection feeds the battery map | 2026-10-26 | Active |
| D3 | Do not claim solar drives household prices | Evidence only supports network charge link, attribution unproven | 2026-10-26 | Active |
| D4 | Problem framed as midday waste then evening fossil dispatch | Strongest, best-supported framing | 2026-10-26 | Active |
| D5 | Scoping pack Part 1 stays out of the repo | Contains unverified figures (export-limit rules); a public repo with wrong facts is worse than an empty one. Facts enter the repo only once sourced in DATA_SOURCES.md | 2026-10-26 | Active |
| D6 | Repo lives outside OneDrive (`C:\Users\jackw\Code\perth-solar-grid`) | OneDrive sync fights large raster files in data/raw and can lock files mid-write | 2026-10-26 | Active |
| D7 | Work on short-lived branches, merge to main by pull request | Public repo: main stays clean and every change has a reviewable history | 2026-10-26 | Active |
