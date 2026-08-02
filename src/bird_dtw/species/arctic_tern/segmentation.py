# src/bird_dtw/species/arctic_tern/segmentation.py
"""
Segment a single Arctic tern's yearly track into southbound migration,
wintering, and northbound migration phases using Net Squared Displacement (NSD).
"""
from __future__ import annotations
import numpy as np
import pandas as pd


def haversine_km(lat1, lon1, lat2, lon2) -> float:
    R = 6371
    lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = np.sin(dlat / 2) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2) ** 2
    return R * 2 * np.arcsin(np.sqrt(a))


def compute_nsd(track: pd.DataFrame, home_lat: float, home_lon: float) -> pd.Series:
    distances = haversine_km(home_lat, home_lon, track["lat"], track["lon"])
    return distances ** 2


def _longest_run(mask: pd.Series, max_gap: int = 0,
                  within: tuple[int, int] | None = None) -> tuple[int, int] | None:
    lo, hi = within if within is not None else (0, len(mask) - 1)
    best = None
    run_start = None
    gap = 0
    for i in range(lo, hi + 1):
        val = mask.iloc[i]
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
        end = hi - gap
        if best is None or (end - run_start) > (best[1] - best[0]):
            best = (run_start, end)
    return best


def segment_track(
    track: pd.DataFrame,
    smooth_days: float = 7.0,
    trend_days: float = 7.0,
    flat_threshold_frac: float = 0.15,
) -> dict[str, pd.DataFrame]:
    home_lat, home_lon = track.iloc[0][["lat", "lon"]]
    nsd = compute_nsd(track, home_lat, home_lon)

    fixes_per_day = 2
    smooth_window = max(3, int(smooth_days * fixes_per_day))
    trend_lag = max(1, int(trend_days * fixes_per_day))
    stopover_gap_fixes = int(30 * fixes_per_day)

    nsd_smooth = nsd.rolling(window=smooth_window, center=True, min_periods=1).mean()
    rate = nsd_smooth.diff(trend_lag) / trend_days

    max_abs_rate = rate.abs().max()
    flat = rate.abs() < (flat_threshold_frac * max_abs_rate)
    winter_run = _longest_run(flat, max_gap=stopover_gap_fixes)

    rising = rate > 0
    falling = rate < 0

    if winter_run:
        before = (0, winter_run[0] - 1) if winter_run[0] > 0 else None
        after = (winter_run[1] + 1, len(rate) - 1) if winter_run[1] < len(rate) - 1 else None
    else:
        before = (0, len(rate) - 1)
        after = (0, len(rate) - 1)

    south_run = _longest_run(rising, max_gap=stopover_gap_fixes, within=before) if before else None
    north_run = _longest_run(falling, max_gap=stopover_gap_fixes, within=after) if after else None

    phase = pd.Series("wintering", index=track.index)
    if south_run:
        phase.iloc[south_run[0]:south_run[1] + 1] = "southbound"
    if north_run:
        phase.iloc[north_run[0]:north_run[1] + 1] = "northbound"

    return {
        name: track.loc[phase == name].reset_index(drop=True)
        for name in ["southbound", "wintering", "northbound"]
    }