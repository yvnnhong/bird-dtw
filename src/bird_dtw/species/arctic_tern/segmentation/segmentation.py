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
                  within: tuple[int, int] | None = None,
                  max_total_gap: int | None = None) -> tuple[int, int] | None:
    """
    Return (start_idx, end_idx) of the longest run of True values in mask,
    bridging individual gaps up to `max_gap` fixes long. `max_total_gap`
    caps the SUM of all bridged gaps in a single run (defaults to max_gap,
    i.e. only one stopover-length gap total is allowed per run).
    """
    if max_total_gap is None:
        max_total_gap = max_gap
    lo, hi = within if within is not None else (0, len(mask) - 1)
    best = None
    run_start = None
    gap = 0
    total_gap = 0
    for i in range(lo, hi + 1):
        val = mask.iloc[i]
        if val:
            if run_start is None:
                run_start = i
                total_gap = 0
            gap = 0
        else:
            if run_start is not None:
                gap += 1
                total_gap += 1
                if gap > max_gap or total_gap > max_total_gap:
                    end = i - gap
                    if best is None or (end - run_start) > (best[1] - best[0]):
                        best = (run_start, end)
                    run_start = None
                    gap = 0
                    total_gap = 0
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
    max_nsd = nsd_smooth.max()
    near_max_nsd = nsd_smooth > (0.85 * max_nsd)  # "far from home" = candidate wintering
    #^old was 0.7
    min_days_before_winter = 50
    min_start_idx = int(min_days_before_winter * fixes_per_day)
    winter_run = _longest_run(near_max_nsd, max_gap=stopover_gap_fixes, within=(min_start_idx, len(nsd_smooth) - 1))
    print(f"DEBUG: winter_run indices = {winter_run}")
    
    rising_threshold = flat_threshold_frac * max_abs_rate
    rising = rate > rising_threshold
    falling = rate < -rising_threshold

    if winter_run:
        before = (0, winter_run[0] - 1) if winter_run[0] > 0 else None
        after = (winter_run[1] + 1, len(rate) - 1) if winter_run[1] < len(rate) - 1 else None
    else:
        before = (0, len(rate) - 1)
        after = (0, len(rate) - 1)

    max_south_days = 110
    max_south_fixes = int(max_south_days * fixes_per_day)
    south_run = _longest_run(rising, max_gap=stopover_gap_fixes, within=before) if before else None
    print(f"DEBUG: south_run before cap = {south_run}, max_south_fixes={max_south_fixes}")
    if south_run and (south_run[1] - south_run[0]) > max_south_fixes:
        south_run = (south_run[0], south_run[0] + max_south_fixes)
    print(f"DEBUG: south_run after cap = {south_run}")
    if south_run:
        real_start = track["timestamp"].iloc[south_run[0]]
        real_end = track["timestamp"].iloc[south_run[1]]
        print(f"DEBUG: south_run spans real dates {real_start} to {real_end}, index count={south_run[1]-south_run[0]}")
    south_run_nobridge = _longest_run(rising, max_gap=0, within=before) if before else None
    print(f"DEBUG: south_run with NO bridging = {south_run_nobridge}")
    if south_run_nobridge:
        nb_start = track["timestamp"].iloc[south_run_nobridge[0]]
        nb_end = track["timestamp"].iloc[south_run_nobridge[1]]
        print(f"DEBUG: no-bridge south_run spans real dates {nb_start} to {nb_end}")
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