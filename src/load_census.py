"""Load ABS Census 2021 dwelling counts for WA postal areas."""

from pathlib import Path

import pandas as pd

G36_FILE = (
    Path(__file__).resolve().parents[1]
    / "data/raw/abs/census_gcp_poa_wa/2021 Census GCP Postal Areas for WA/2021Census_G36_WA_POA.csv"
)


def load_houses() -> pd.DataFrame:
    """Occupied houses per postal area: separate plus semi-detached, row and townhouses.

    These are the dwellings with their own roof, so they are the realistic base for
    rooftop solar. Flats and apartments are left out.
    """
    df = pd.read_csv(G36_FILE)
    return pd.DataFrame({
        # The Census writes postal areas as "POA6000".
        "postcode": df["POA_CODE_2021"].str.removeprefix("POA"),
        "houses": df["OPDs_Separate_house_Dwellings"] + df["OPDs_SD_r_t_h_th_Tot_Dwgs"],
    })


if __name__ == "__main__":
    houses = load_houses()
    print(houses.head())
    print(f"{len(houses)} WA postal areas, {houses['houses'].sum():,} houses")
