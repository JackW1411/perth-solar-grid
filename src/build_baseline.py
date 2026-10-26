"""Stage 2: join CER solar and battery totals to Perth postcode boundaries."""

from pathlib import Path

import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

from load_cer import load_wa_cer
from load_census import load_houses

ROOT = Path(__file__).resolve().parents[1]
POA_FILE = ROOT / "data/raw/abs/POA_2021_AUST_GDA2020_SHP/POA_2021_AUST_GDA2020.shp"
GCCSA_FILE = ROOT / "data/raw/abs/GCCSA_2021_AUST_SHP_GDA2020/GCCSA_2021_AUST_GDA2020.shp"
OUT_DIR = ROOT / "data/processed"
MIN_HOUSES = 200

# Single-hue sequential ramp, light (low) to dark (high).
BLUES = LinearSegmentedColormap.from_list(
    "blues", ["#cde2fb", "#86b6ef", "#3987e5", "#1c5cab", "#0d366b"]
)


def perth_postcodes() -> gpd.GeoDataFrame:
    """Postal areas whose interior point falls inside Greater Perth (GCCSA 5GPER).

    Postal areas do not nest inside GCCSAs, so a point-in-polygon test decides
    membership. See decision D12.
    """
    poa = gpd.read_file(POA_FILE)[["POA_CODE21", "AREASQKM21", "geometry"]]
    poa = poa.rename(columns={"POA_CODE21": "postcode", "AREASQKM21": "area_km2"})
    gccsa = gpd.read_file(GCCSA_FILE)
    perth = gccsa.loc[gccsa["GCC_CODE21"] == "5GPER", "geometry"].iloc[0]
    return poa[poa.representative_point().within(perth)].reset_index(drop=True)


def build() -> gpd.GeoDataFrame:
    poa = perth_postcodes()
    cer = load_wa_cer()

    unmatched = sorted(set(poa["postcode"]) - set(cer["postcode"]))
    if unmatched:
        print(f"Perth postal areas with no CER record: {unmatched}")

    gdf = poa.merge(cer, on="postcode", how="left").fillna(
        {"solar_kw": 0, "solar_installs": 0, "battery_kwh": 0, "battery_installs": 0}
    )
    gdf = gdf.merge(load_houses(), on="postcode", how="left")
    gdf["solar_mw"] = gdf["solar_kw"] / 1000
    # Houses are from the 2021 Census and installs run to 2026 and include upgrades,
    # so fast-growing suburbs can exceed 100.
    # Below MIN_HOUSES the postcode is industrial or commercial and a per-house rate
    # is meaningless (see D13).
    gdf["solar_per_100_houses"] = 100 * gdf["solar_installs"] / gdf["houses"].where(
        gdf["houses"] >= MIN_HOUSES
    )
    # Batteries are only recorded from July 2025, so this is a recent-uptake rate,
    # not the share of solar homes that own a battery.
    gdf["battery_per_100_solar"] = 100 * gdf["battery_installs"] / gdf["solar_installs"].where(
        gdf["solar_installs"] > 0
    )
    return gdf


def plot(gdf: gpd.GeoDataFrame, path: Path) -> None:
    fig, axes = plt.subplots(1, 2, figsize=(12, 8), facecolor="#fcfcfb")
    panels = [
        ("solar_per_100_houses", "Solar systems per 100 houses\n(houses from 2021 Census)"),
        ("battery_per_100_solar", "Batteries installed since Jul 2025\nper 100 solar systems"),
    ]
    for ax, (col, title) in zip(axes, panels):
        gdf.plot(
            column=col, cmap=BLUES, ax=ax, edgecolor="#fcfcfb", linewidth=0.3, legend=True,
            legend_kwds={"shrink": 0.6}, missing_kwds={"color": "#e4e3df", "label": "No data"},
        )
        ax.set_title(title, color="#0b0b0b", fontsize=11, loc="left")
        ax.set_axis_off()
    fig.text(
        0.01, 0.01,
        "Source: Clean Energy Regulator postcode data to 30 Sep 2026; ABS Census 2021 and ASGS 2021 postal areas. "
        "Greater Perth only.",
        color="#52514e", fontsize=8,
    )
    fig.savefig(path, dpi=150, bbox_inches="tight")


if __name__ == "__main__":
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    gdf = build()
    gdf.to_file(OUT_DIR / "perth_baseline.gpkg", layer="postcodes", driver="GPKG")
    plot(gdf, OUT_DIR / "perth_baseline.png")
    print(f"{len(gdf)} Greater Perth postal areas")
    print(gdf[["solar_mw", "solar_installs", "battery_kwh", "battery_installs"]].sum().round(1))
    print(gdf[["solar_per_100_houses", "battery_per_100_solar"]].describe().round(1))
    print(gdf.nlargest(5, "solar_per_100_houses")[["postcode", "houses", "solar_installs", "solar_per_100_houses"]])
