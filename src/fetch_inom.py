"""Save a dated snapshot of Western Power's iNOM Network Support Service opportunities.

The iNOM updates daily, so each run writes a new file instead of overwriting.
"""

from datetime import date
from pathlib import Path

import requests

URL = (
    "https://services2.arcgis.com/tBLxde4cxSlNUxsM/arcgis/rest/services/"
    "NSSS_Data_gdb/FeatureServer/0/query"
)
OUT_DIR = Path(__file__).resolve().parents[1] / "data/raw/western_power"


def fetch(out_dir: Path = OUT_DIR) -> Path:
    params = {"where": "1=1", "outFields": "*", "outSR": 7844, "f": "geojson"}
    response = requests.get(URL, params=params, timeout=60)
    response.raise_for_status()
    # ArcGIS reports query errors with HTTP 200 and an "error" key.
    if "error" in response.json():
        raise RuntimeError(response.json()["error"])

    path = out_dir / f"inom_opportunities_{date.today():%Y-%m-%d}.geojson"
    path.write_bytes(response.content)
    return path


if __name__ == "__main__":
    print(f"Saved {fetch()}")
