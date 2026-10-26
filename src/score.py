"""Stage 3: battery opportunity score for Perth postal areas.

score = w_solar * solar + w_gap * battery_gap + w_network * network

Each component is a percentile rank (0 to 1) across scored postal areas, so the
weights are the only judgement call. See D14.
- solar: solar systems per 100 houses (more solar, more midday surplus to store)
- battery_gap: batteries per 100 solar systems, reversed (fewer batteries, bigger gap)
- network: Western Power 2028 forecast remaining substation capacity, reversed
  (less headroom, more value from local storage)
"""

from itertools import product
from pathlib import Path

import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd

from build_baseline import BLUES

ROOT = Path(__file__).resolve().parents[1]
BASELINE_FILE = ROOT / "data/processed/perth_baseline.gpkg"
SAL_FILE = ROOT / "data/raw/abs/SAL_2021_AUST_GDA2020_SHP/SAL_2021_AUST_GDA2020.shp"
WP_DIR = ROOT / "data/raw/western_power"
NCMT_FILE = next(WP_DIR.glob("NCMT_Forecast_Remaining_Capacity_2028*GDA2020*/*.gpkg"))
OUT_DIR = ROOT / "data/processed"

WEIGHTS = {"solar": 1 / 3, "battery_gap": 1 / 3, "network": 1 / 3}
TOP_N = 20

# NCMT remaining capacity bands, lowest headroom first.
BANDS = [
    "Less than 5 MVA", "5 to 10 MVA", "10 to 15 MVA", "15 to 20 MVA",
    "20 to 25 MVA", "25 to 30 MVA", "More than 30 MVA",
]


def add_suburb_names(gdf: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    """Name each postal area after its three largest suburbs (ABS SAL 2021)."""
    sal = gpd.read_file(SAL_FILE)
    sal = sal[sal["STE_CODE21"] == "5"][["SAL_NAME21", "AREASQKM21", "geometry"]]
    sal["SAL_NAME21"] = sal["SAL_NAME21"].str.removesuffix(" (WA)")
    sal["geometry"] = sal.representative_point()

    joined = gpd.sjoin(sal, gdf[["postcode", "geometry"]], predicate="within")
    names = (
        joined.sort_values("AREASQKM21", ascending=False)
        .groupby("postcode")["SAL_NAME21"]
        .agg(lambda s: ", ".join(s.head(3)))
        .rename("suburbs")
    )
    return gdf.merge(names, on="postcode", how="left")


def add_network_headroom(gdf: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    """Attach the NCMT band of the substation catchment covering most of each postal area.

    Catchments leave gaps, so an interior-point match missed some suburbs entirely.
    """
    ncmt = gpd.read_file(NCMT_FILE)[["sub_name", "descrip", "geometry"]]
    # Areas need a projected CRS: MGA2020 zone 50 covers Perth.
    pieces = gpd.overlay(gdf[["postcode", "geometry"]], ncmt, how="intersection").to_crs(7850)
    pieces["overlap_km2"] = pieces.area / 1e6
    joined = pieces.sort_values("overlap_km2", ascending=False).drop_duplicates("postcode")
    joined["headroom_band"] = joined["descrip"].map(BANDS.index)
    cols = joined[["postcode", "sub_name", "descrip", "headroom_band"]]
    return gdf.merge(cols.rename(columns={"descrip": "headroom"}), on="postcode", how="left")


def add_inom_flag(gdf: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    """Flag postal areas that overlap a Western Power Network Support Service opportunity."""
    latest = sorted(WP_DIR.glob("inom_opportunities_*.geojson"))[-1]
    nss = gpd.read_file(latest).dissolve("OPP_ID").reset_index()[["OPP_ID", "ZSS", "geometry"]]
    hits = gpd.sjoin(gdf[["postcode", "geometry"]], nss, predicate="intersects")
    sites = hits.groupby("postcode")["ZSS"].agg(lambda s: ", ".join(sorted(set(s))))
    return gdf.merge(sites.rename("nss_site"), on="postcode", how="left")


def components(gdf: gpd.GeoDataFrame) -> pd.DataFrame:
    """Percentile-ranked components for postal areas that have every input."""
    rated = gdf.dropna(subset=["solar_per_100_houses", "battery_per_100_solar", "headroom_band"])
    return pd.DataFrame({
        "solar": rated["solar_per_100_houses"].rank(pct=True),
        "battery_gap": rated["battery_per_100_solar"].rank(pct=True, ascending=False),
        "network": rated["headroom_band"].rank(pct=True, ascending=False),
    })


def weighted(comp: pd.DataFrame, weights: dict) -> pd.Series:
    return sum(comp[k] * w for k, w in weights.items())


def sensitivity(comp: pd.DataFrame) -> tuple[pd.DataFrame, pd.Series]:
    """Re-score under every weighting in steps of 0.1 (each weight at least 0.1).

    Returns one row per weighting, and the share of weightings that put each
    postal area in the top N.
    """
    base = weighted(comp, WEIGHTS)
    base_top = set(base.nlargest(TOP_N).index)
    rows, top_counts = [], pd.Series(0, index=comp.index)
    steps = [i / 10 for i in range(1, 9)]
    for ws, wg in product(steps, steps):
        wn = round(1 - ws - wg, 1)
        if wn < 0.1:
            continue
        score = weighted(comp, {"solar": ws, "battery_gap": wg, "network": wn})
        top = set(score.nlargest(TOP_N).index)
        top_counts[list(top)] += 1
        rows.append({
            "w_solar": ws, "w_gap": wg, "w_network": wn,
            "top_overlap": len(top & base_top) / TOP_N,
            # Spearman = Pearson on ranks; avoids a scipy dependency.
            "spearman": score.rank().corr(base.rank()),
        })
    runs = pd.DataFrame(rows)
    return runs, (top_counts / len(runs)).rename("top_share")


def plot(gdf: gpd.GeoDataFrame, path: Path) -> None:
    fig, ax = plt.subplots(figsize=(7, 9), facecolor="#fcfcfb")
    gdf.plot(
        column="score", cmap=BLUES, ax=ax, edgecolor="#fcfcfb", linewidth=0.3, legend=True,
        legend_kwds={"shrink": 0.5, "label": "Score (0 to 1)"},
        missing_kwds={"color": "#e4e3df", "label": "Not scored"},
    )
    top = gdf.nsmallest(10, "rank")
    top.boundary.plot(ax=ax, color="#0b0b0b", linewidth=1)
    ax.set_title("Battery opportunity score, Greater Perth\n(top 10 outlined)", loc="left", fontsize=11)
    ax.set_axis_off()
    fig.text(
        0.01, 0.01,
        "Equal weights: solar per house, battery gap, network headroom. "
        "Sources: CER, ABS, Western Power.",
        color="#52514e", fontsize=8,
    )
    fig.savefig(path, dpi=150, bbox_inches="tight")


if __name__ == "__main__":
    gdf = gpd.read_file(BASELINE_FILE)
    gdf = add_network_headroom(add_inom_flag(add_suburb_names(gdf)))

    comp = components(gdf)
    runs, top_share = sensitivity(comp)
    scored = comp.assign(score=weighted(comp, WEIGHTS)).join(top_share)
    scored["rank"] = scored["score"].rank(ascending=False, method="min").astype(int)
    gdf = gdf.join(scored)
    gdf["rank"] = gdf["rank"].astype("Int64")  # unscored rows stay blank, not 1.0-style floats

    gdf.to_file(OUT_DIR / "perth_score.gpkg", layer="postcodes", driver="GPKG")
    cols = ["rank", "postcode", "suburbs", "score", "top_share", "solar", "battery_gap",
            "network", "solar_per_100_houses", "battery_per_100_solar", "headroom", "nss_site"]
    ranking = gdf.dropna(subset=["score"]).sort_values("rank")[cols]
    ranking.to_csv(OUT_DIR / "perth_score_ranking.csv", index=False, float_format="%.3f")
    plot(gdf, OUT_DIR / "perth_score.png")

    pd.set_option("display.width", 200, "display.max_colwidth", 40)
    print(f"{len(ranking)} of {len(gdf)} postal areas scored\n")
    print(ranking.head(TOP_N)[cols[:5] + ["headroom", "nss_site"]].to_string(index=False))
    print(f"\nSensitivity over {len(runs)} weightings:")
    print(runs[["top_overlap", "spearman"]].describe().loc[["min", "50%", "max"]].round(2))
    print("\nNSS site postal areas:")
    print(ranking[ranking["nss_site"].notna()][["rank", "postcode", "suburbs", "nss_site"]].to_string(index=False))
