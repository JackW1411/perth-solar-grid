"""Stage 6: export the score as a single-file Leaflet web map in docs/map/."""

import json
import shutil
from pathlib import Path

import geopandas as gpd

ROOT = Path(__file__).resolve().parents[1]
SCORE_FILE = ROOT / "data/processed/perth_score.gpkg"
TEMPLATE = Path(__file__).with_name("web_map_template.html")
OUT_FILE = ROOT / "docs/map/index.html"
PREVIEW_SRC = ROOT / "data/processed/perth_score.png"

FIELDS = ["postcode", "suburbs", "rank", "score", "solar_per_100_houses",
          "battery_per_100_solar", "headroom", "nss_site"]
SIMPLIFY_M = 40  # boundary detail in metres; keeps the page small


def export() -> Path:
    gdf = gpd.read_file(SCORE_FILE)[FIELDS + ["geometry"]]
    # Simplify in metres (MGA2020 zone 50), then return to lon/lat for Leaflet.
    gdf["geometry"] = gdf.to_crs(7850).simplify(SIMPLIFY_M).to_crs(4326)
    gdf["score"] = gdf["score"].round(3)
    gdf[["solar_per_100_houses", "battery_per_100_solar"]] = gdf[
        ["solar_per_100_houses", "battery_per_100_solar"]].round(1)

    geojson = gdf.to_json(drop_id=True, na="null")
    geojson = json.dumps(json.loads(geojson), separators=(",", ":"))
    # Five quantile bins, matching the five colours in the template.
    bins = gdf["score"].quantile([0.2, 0.4, 0.6, 0.8, 1.0]).round(3).tolist()

    html = (TEMPLATE.read_text(encoding="utf-8")
            .replace("__DATA__", geojson)
            .replace("__BINS__", json.dumps(bins))
            .replace("__N__", str(int(gdf["rank"].notna().sum()))))
    OUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    OUT_FILE.write_text(html, encoding="utf-8")
    # Static image for the README, which cannot embed the interactive map.
    shutil.copy(PREVIEW_SRC, OUT_FILE.with_name("preview.png"))
    return OUT_FILE


if __name__ == "__main__":
    path = export()
    print(f"Wrote {path} ({path.stat().st_size / 1024:.0f} KB)")
