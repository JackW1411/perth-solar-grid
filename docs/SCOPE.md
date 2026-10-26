# Scope

**Current stage: Stage 0**

Each stage ends with a go or no-go decision logged in DECISIONS.md.

## Stages

### Stage 0: Feasibility and data audit
Confirm what is actually public. Check Clean Energy Regulator postcode solar installation data, WA battery rebate uptake data, Western Power network and zone substation locations, ABS postcode or SA2 boundaries, and imagery options.
Output: a data source table and a go or no-go. If constraint data is not public, the map falls back to a proxy of solar density and battery gap.

### Stage 1: Quantify the waste
Find a defensible number for curtailed or wasted midday solar from AEMO and WA market operator sources. This anchors the whole story.
Output: one sourced figure and a note on method.

### Stage 2: Baseline solar and battery layers
Ingest installation counts and capacity by postcode, join to boundaries, add battery uptake.
Output: a clean joined dataset and a first choropleth, sanity checked in QGIS.

### Stage 3: Battery opportunity score
Define a transparent score from solar density, battery gap and network constraint or proxy. Keep the formula simple and documented.
Output: ranked suburbs and a sensitivity check on the weights.

### Stage 4: Rooftop detection prototype
Pick imagery and a method, either a pretrained model or a small custom one, on a small test area. Measure accuracy against registered installations.
Output: a precision and recall figure and a go or no-go on scaling.

### Stage 5: Integrate detection into the score
Use detected solar to fill gaps or flag mismatches against registered data.
Output: updated score and a comparison of before and after.

### Stage 6: Presentation
A web map or notebook, a clean README, and a short write-up with an honest limitations section.
Output: public repo and a LinkedIn-ready summary.

## Risks to watch
- Network constraint data may not be public, which weakens the battery score.
- Imagery licensing or resolution may block detection.
- Scope creep from running two layers at once. Stage 4 is the first place to cut if time is tight.
- Overclaiming on prices. See decision D3.

## Done
_Nothing yet._
