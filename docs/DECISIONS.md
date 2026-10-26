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
| D8 | Stage 4 (rooftop detection) on hold | No free high-resolution imagery of Perth: Landgate Perth Metro is paid, Nearmap needs university or AURIN access, Sentinel-2 (10 m) is too coarse for panels. Revisit if an imagery source turns up | 2026-10-26 | Active |
| D9 | Use Western Power NCMT and iNOM data in the battery score | Best available network signal. NCMT gives substation catchments, iNOM gives the metro sites where Western Power is paying for evening peak support. Raw files stay out of git | 2026-10-26 | Active |
| D10 | Stage 0: GO for Stages 1 to 3 | CER solar and battery postcode data, ABS boundaries (CC BY 4.0) and Western Power network data are all obtainable. Stage 4 handled by D8 | 2026-10-26 | Active |
| D11 | Stage 1 anchor is AEMO's minimum demand forecast (319 MW in 2025-26 to 193 MW in 2028-29, against a 300 MW threshold), not a wasted GWh figure | AEMO publishes no SWIS curtailed rooftop solar volume, and NEM figures must not be used for WA. The forecast is sourced and conservative. Batteries already absorb midday surplus, so the story is where the next batteries add most value. See STAGE1_WASTE.md | 2026-10-26 | Active |
| D12 | Perth metro = ABS 2021 postal areas whose interior point falls inside Greater Perth (GCCSA 5GPER) | Postal areas do not nest inside GCCSAs, so a point-in-polygon test gives a clean, repeatable cut. Gives 128 postal areas | 2026-10-26 | Active |
