"""Load Clean Energy Regulator (CER) small-scale postcode data for WA."""

from pathlib import Path

import pandas as pd

RAW_DIR = Path(__file__).resolve().parents[1] / "data" / "raw" / "cer"
CAPACITY_FILE = RAW_DIR / "sres-postcode-data-capacity-2011-to-present-and-totals.xlsx"
INSTALLS_FILE = RAW_DIR / "sres-postcode-data-installations-2011-to-present-and-totals.xlsx"

# WA postcodes run 6000 to 6797; anything else is another state or a PO box range.
WA_MIN, WA_MAX = 6000, 6799


def load_total(path: Path, sheet: str, name: str) -> pd.DataFrame:
    """Return one row per WA postcode with the sheet's total column renamed to `name`."""
    # The first three rows are notes, so the header is on the fourth row.
    df = pd.read_excel(path, sheet_name=sheet, header=3)
    postcode_col, total_col = df.columns[0], df.columns[-1]

    df = df[[postcode_col, total_col]].rename(columns={postcode_col: "postcode", total_col: name})
    df = df[df["postcode"].between(WA_MIN, WA_MAX)]
    # pandas reads postcodes as numbers; ABS stores them as 4-character text.
    df["postcode"] = df["postcode"].astype(int).astype(str).str.zfill(4)
    return df


def load_wa_cer() -> pd.DataFrame:
    """Solar and battery totals per WA postcode, joined into one table."""
    parts = [
        load_total(CAPACITY_FILE, "SGU-Solar", "solar_kw"),
        load_total(INSTALLS_FILE, "SGU-Solar", "solar_installs"),
        load_total(CAPACITY_FILE, "SGU-Battery", "battery_kwh"),
        load_total(INSTALLS_FILE, "SGU-Battery", "battery_installs"),
    ]
    df = parts[0]
    for part in parts[1:]:
        df = df.merge(part, on="postcode", how="outer")
    # A postcode missing from the battery sheets has no batteries recorded since July 2025.
    df = df.fillna(0).astype({"solar_installs": int, "battery_installs": int})
    return df.sort_values("postcode").reset_index(drop=True)


if __name__ == "__main__":
    cer = load_wa_cer()
    print(cer.head())
    print(f"{len(cer)} WA postcodes")
    print(cer.drop(columns="postcode").sum().round(0))
