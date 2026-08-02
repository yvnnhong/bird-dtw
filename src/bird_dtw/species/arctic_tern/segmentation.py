# src/bird_dtw/species/arctic_tern/segmentation.py
"""
Segment a single Arctic tern's yearly track into southbound migration,
wintering, and northbound migration phases using Net Squared Displacement (NSD).

Geolocator fixes are noisy (~2 fixes/day, GPS_SAMPLING_INTERVAL_HOURS in
params.py), so day-to-day NSD change is dominated by noise rather than true
trend. This module smooths heavily and looks for the longest contiguous
rising/falling runs, rather than classifying each fix independently.
"""
from __future__ import annotations
import numpy as np
import pandas as pd


def haversine_km(lat1, lon1, lat2, lon2) -> float:
    """Great-circle distance in km between two lat/lon points."""
    R = 6371
    lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = np.sin(dlat / 2) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2) ** 2
    return R * 2 * np.arcsin(np.sqrt(a))


def compute_nsd(track: pd.DataFrame, home_lat: float, home_lon: float) -> pd.Series:
    """Net Squared Displacement (km^2) for each fix, relative to a home point."""
    distances = haversine_km(home_lat, home_lon, track["lat"], track["lon"])
    return distances ** 2


def _longest_run(mask: pd.Series, max_gap: int = 0) -> tuple[int, int] | None:
    """
    Return (start_idx, end_idx) of the longest run of True values in mask,
    allowing gaps of up to `max_gap` consecutive False values to be bridged
    (e.g. a stopover pausing an otherwise-continuous migration leg).
    """
    best = None
    run_start = None
    gap = 0
    for i, val in enumerate(mask):
        if val:
            if run_start is None:
                run_start = i
            gap = 0
        else:
            if run_start is not None:
                gap += 1
                if gap > max_gap:
                    end = i - gap
                    if best is None or (end - run_start) > (best[1] - best[0]):
                        best = (run_start, end)
                    run_start = None
                    gap = 0
    if run_start is not None:
        end = len(mask) - 1 - gap
        if best is None or (end - run_start) > (best[1] - best[0]):
            best = (run_start, end)
    return best


def segment_track(
    track: pd.DataFrame,
    smooth_days: float = 7.0,
    trend_days: float = 7.0,
) -> dict[str, pd.DataFrame]:
    """
    Split a track into southbound, wintering, and northbound phases.

    Parameters
    ----------
    track : pd.DataFrame
        Columns [lat, lon, timestamp], chronologically sorted.
    smooth_days : float
        Smoothing window, in approximate days (converted to fix-count
        using ~2 fixes/day). Larger = less sensitive to geolocator noise.
    trend_days : float
        How many days apart to compare when computing rate of change
        (instead of fix-to-fix, which is too noisy at 12h sampling).

    Returns
    -------
    dict[str, pd.DataFrame]
        Keys: "southbound", "wintering", "northbound" -- each a
        chronologically sorted sub-DataFrame of the original track.
    """
    home_lat, home_lon = track.iloc[0][["lat", "lon"]]
    nsd = compute_nsd(track, home_lat, home_lon)

    fixes_per_day = 2  # matches GPS_SAMPLING_INTERVAL_HOURS = 12 in params.py
    smooth_window = max(3, int(smooth_days * fixes_per_day))
    trend_lag = max(1, int(trend_days * fixes_per_day))
    stopover_gap_fixes = int(30 * fixes_per_day)  # generous bound on north_atlantic stopover, params.py

    nsd_smooth = nsd.rolling(window=smooth_window, center=True, min_periods=1).mean()
    rate = nsd_smooth.diff(trend_lag) / trend_days  # km^2 per day, averaged over ~a week

    rising = rate > 0
    falling = rate < 0

    south_run = _longest_run(rising, max_gap=stopover_gap_fixes)
    north_run = _longest_run(falling, max_gap=stopover_gap_fixes)

    phase = pd.Series("wintering", index=track.index)
    if south_run:
        phase.iloc[south_run[0]:south_run[1] + 1] = "southbound"
    if north_run:
        phase.iloc[north_run[0]:north_run[1] + 1] = "northbound"

    return {
        name: track.loc[phase == name].reset_index(drop=True)
        for name in ["southbound", "wintering", "northbound"]
    }