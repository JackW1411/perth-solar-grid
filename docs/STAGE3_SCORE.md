# Stage 3: Battery opportunity score

Code: `src/score.py`. Outputs (gitignored): `data/processed/perth_score.gpkg`, `perth_score_ranking.csv`, `perth_score.png`.

## Formula

```
score = 1/3 solar + 1/3 battery_gap + 1/3 network
```

Each component is a percentile rank (0 to 1) across the 116 scored postal areas, so they share a scale and the weights are the only judgement call (D14).

| Component | Input | Direction |
|---|---|---|
| solar | Solar systems per 100 houses (CER, 2021 Census) | More solar ranks higher |
| battery_gap | Batteries installed since Jul 2025 per 100 solar systems (CER) | Fewer batteries ranks higher |
| network | Western Power NCMT 2028 forecast remaining capacity band of the substation catchment covering most of the postal area | Less headroom ranks higher |

12 of 128 Greater Perth postal areas are not scored: they have fewer than 200 houses (D13).

## Top 10 (equal weights)

| Rank | Postcode | Suburbs | In top 20 under all weightings |
|---|---|---|---|
| 1 | 6125 | Serpentine, Mardella, Hopeland | 100% |
| 2 | 6208 | Fairbridge, Meelon, Nirimba | 100% |
| 3 | 6124 | Jarrahdale | 100% |
| 4 | 6211 | Clifton, Bouvard, Herron | 100% |
| 5 | 6210 | Halls Head, Greenfields, Mandurah | 94% |
| 6 | 6172 | Port Kennedy | 100% |
| 7 | 6214 | West Coolup, Coolup, Birchmont | 94% |
| 8 | 6077 | Jandabup, Gnangara | 86% |
| 8 | 6169 | Warnbro, Waikiki, Safety Bay | 78% |
| 10 | 6121 | Oakford, Oldbury | 83% |

The pattern: outer growth corridors in the south (Peel, Rockingham, Serpentine-Jarrahdale) and north (Alkimos, Clarkson), with high solar per house, low recent battery uptake and substations in the lowest headroom band.

## Sensitivity

The score was rerun under all 36 weightings in steps of 0.1 with every weight at least 0.1.

- Top 20 overlap with the equal-weight top 20: median 80%, worst 50%.
- Spearman rank correlation with the equal-weight ranking: median 0.90, worst 0.70.
- 5 postal areas stay in the top 20 under every weighting.

The worst cases are weightings where one component takes 0.8.

## Validation against Western Power's own sites

The iNOM lists the feeders and substations where Western Power is paying for network support in the evening peak. It is not a score input, so it serves as an independent check.

- Sites in outer growth areas rank high: Byford substation (postal areas ranked 1, 3, 10), Gosnells (11) and Rockingham (18).
- Single-feeder sites in the inner and middle suburbs rank low: Morley, Hadfields, Arkana and North Beach (53 to 103).

Reading: the score finds substation-scale opportunity where solar, battery gap and network stress line up. It cannot see a single constrained feeder inside an otherwise unremarkable postal area, and the inner sites are evening load problems in areas with less solar per house.

## Limitations

- The network band is coarse: 7 classes, and 43 of 106 catchments sit in the lowest band. The whole top 20 is in that band. Western Power does not say whether the band is load or generation headroom.
- Battery data starts in July 2025, so the gap measures recent uptake, not ownership.
- Houses are from the 2021 Census, so fast-growing estates have inflated solar per house.
- Equal weights are a choice, not a finding. The sensitivity check shows how much it matters.
