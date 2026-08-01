"""
Fetch Arctic tern GPS/geolocator tracking data from OBIS-SEAMAP.

Data source: Egevang et al. (2010), PNAS. See REFERENCES.md for full citation.
License: CC-BY-NC 4.0 -- data is fetched at runtime and NOT redistributed
in this repository. Non-commercial use only.
"""

from __future__ import annotations

import pandas as pd
import requests

OBIS_API_URL = "https://api.obis.org/v3/occurrence"
DATASET_ID = "f3316d34-fbbd-4c9a-9c1b-382a1d9877d3"


def fetch_data(size: int = 5000, timeout: int = 30) -> pd.DataFrame:
    """
    Fetch raw Arctic tern occurrence (GPS/geolocator fix) records from OBIS.

    Parameters
    ----------
    size : int
        Max number of records to request from the API.
    timeout : int
        Request timeout in seconds.

    Returns
    -------
    pd.DataFrame
        Raw occurrence records with columns including decimalLatitude,
        decimalLongitude, eventDate, and an individual/track identifier.
    """
    response = requests.get(
        OBIS_API_URL,
        params={"datasetid": DATASET_ID, "size": size},
        timeout=timeout,
    )
    response.raise_for_status()
    payload = response.json()

    records = payload.get("results", [])
    if not records:
        raise ValueError("No records returned from OBIS API -- check dataset ID or API status.")

    return pd.DataFrame.from_records(records)


def load_tracks(df: pd.DataFrame) -> dict[str, pd.DataFrame]:
    """
    Split raw OBIS occurrence data into per-individual tracks, sorted by time.

    NOTE: inspect df.columns after your first fetch_data() call to confirm
    the exact name of the individual/track ID field for this dataset
    (commonly something like 'occurrenceID', 'organismID', or a custom
    field) -- it is not guaranteed to be identical across OBIS datasets.

    Parameters
    ----------
    df : pd.DataFrame
        Output of fetch_data().

    Returns
    -------
    dict[str, pd.DataFrame]
        Mapping of individual/track ID -> chronologically sorted fixes,
        each with columns [lat, lon, timestamp].
    """
    # TODO: confirm actual column names once you've run fetch_data() once
    id_col = "organismID"  # placeholder -- verify against df.columns
    lat_col = "decimalLatitude"
    lon_col = "decimalLongitude"
    time_col = "eventDate"

    tracks: dict[str, pd.DataFrame] = {}
    for track_id, group in df.groupby(id_col):
        track = (
            group[[lat_col, lon_col, time_col]]
            .rename(columns={lat_col: "lat", lon_col: "lon", time_col: "timestamp"})
            .assign(timestamp=lambda d: pd.to_datetime(d["timestamp"]))
            .sort_values("timestamp")
            .reset_index(drop=True)
        )
        tracks[str(track_id)] = track

    return tracks


if __name__ == "__main__":
    raw = fetch_data()
    print(f"Fetched {len(raw)} records.")
    print("Columns:", list(raw.columns))
    print(raw.head())