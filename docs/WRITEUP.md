# Where should Perth's next home batteries go?

## The problem

Rooftop solar in the SWIS has doubled since 2020, to 3.2 GW across about 600,000 systems. On mild, sunny days it pushes midday grid demand towards the 300 MW floor AEMO needs for secure operation. AEMO forecasts minimum demand falling from 319 MW in 2025-26 to 193 MW by 2028-29 and 50 MW by 2035-36 (2026 WEM ESOO). Below the floor, the surplus has to be stored or switched off.

Batteries are already absorbing a lot of it. Grid batteries now charge at over 1 GW at midday, evening battery discharge passed 1 GW in December 2025, and gas generation fell 16% year on year in Q4 2025. Household batteries took off from July 2025 under the federal and WA rebates. So the question is not whether solar is being wasted today. It is where the next batteries add the most.

## What I built

A Python pipeline that scores 116 Greater Perth postcodes on three things:

1. **Solar per house**: more rooftop solar means more midday surplus to store.
2. **Battery gap**: fewer batteries per solar system means more room to add them.
3. **Network headroom**: less forecast spare capacity at the local substation means local storage is worth more.

Each is a percentile rank, averaged with equal weights. Data comes from the Clean Energy Regulator, the ABS and Western Power.

## What it found

- **The opportunity is on the urban fringe.** The top of the list is the outer growth corridors: Serpentine-Jarrahdale, Pinjarra, the Mandurah coast and Rockingham to the south, and Alkimos, Clarkson and Joondalup to the north. They combine high solar per house, low recent battery uptake and substations with less than 5 MVA of forecast spare capacity.
- **Inner Perth is the reverse.** Solar per house is lower and recent battery uptake is higher.
- **The ranking holds up.** Across 36 different weightings, the median top-20 overlap with the equal-weight list is 80%, and five postcodes stay in the top 20 under every weighting.
- **It partly matches Western Power's own view.** Western Power publishes the feeders and substations where it pays for evening peak support. Its outer sites (Byford, Gosnells, Rockingham) land at ranks 1 to 18. Its inner single-feeder sites (Morley, Hadfields, Arkana, North Beach) rank 53 to 103. A postcode-level score finds substation-scale opportunity but cannot see one constrained feeder.

## Limitations

- **Network data is coarse.** Western Power's capacity forecast comes in seven bands, and the whole top 20 sits in the lowest one. It does not say whether the figure is spare demand or spare generation capacity.
- **Battery data starts in July 2025.** The battery gap measures recent uptake, not total ownership.
- **Houses are from the 2021 Census.** New estates built since then show inflated solar per house, and CER install counts include upgrades.
- **Weights are a choice.** Equal weights are a starting point, not a finding. The sensitivity check shows how much they matter.
- **No wasted-energy figure.** AEMO does not publish a figure for curtailed rooftop solar in the SWIS, so this project does not quote one.
- **Not about household prices.** Nothing here shows that solar raises household electricity bills.
- **Rooftop detection was dropped.** Detecting panels from imagery was planned, but there is no free high-resolution imagery of Perth.

## LinkedIn summary

> Perth has 3.2 GW of rooftop solar, and AEMO forecasts midday grid demand falling below its 300 MW security floor by 2028-29. Batteries are the fix, so I built a Python pipeline to find where the next ones would help most.
>
> Scoring 116 Greater Perth postcodes on solar per house, battery uptake and substation headroom points to the outer growth corridors: Serpentine-Jarrahdale, Mandurah, Rockingham, and Alkimos to Joondalup. The ranking holds across 36 different weightings, and it lines up with the outer sites where Western Power already pays for network support.
>
> Interactive map, code and an honest limitations section: https://github.com/JackW1411/perth-solar-grid
