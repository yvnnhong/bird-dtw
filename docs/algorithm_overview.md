# Algorithm Overview: How segment_track() Works, Step by Step

## Purpose of this doc
`glossary.md` explains what each individual term/parameter *means*. This
doc explains the *order* in which `segment_track()` uses them — the
actual sequence of steps, from raw GPS points to three labeled
DataFrames. Read this if you want to understand the flow of logic, not
just the vocabulary.

File: `src/bird_dtw/species/arctic_tern/segmentation.py`

## Step-by-step

**1. Establish "home."**
The bird's very first GPS fix in its record is treated as home (the
Arctic breeding ground). This assumes each bird's raw tracking data
starts near the breeding season, before southbound migration begins —
true for all 9 birds in this dataset.

**2. Compute NSD for every GPS fix.**
Using `haversine_km()` (real sphere-distance, not flat-map distance),
calculate how far each GPS point is from home, then square that distance.
This produces one NSD value per fix, per bird.

**3. Smooth the NSD signal.**
Average NSD values over a rolling window (`smooth_days`) to remove GPS
noise/jitter, producing a calmer curve (`nsd_smooth`).

**4. Compute the rate of change.**
Compare each smoothed NSD value to its value `trend_days` earlier, to get
a rate: is the bird currently moving away from home (positive rate) or
back toward it (negative rate)?

**5. Find the wintering candidate window.**
Rather than using the noisy rate-of-change signal, wintering is detected
using the smoothed NSD *value* itself: any point where the bird is above
a set fraction (`near_max_nsd`, currently 0.85) of its single farthest
distance from home all year is a wintering candidate. The longest
qualifying run of such points (bridging over short gaps up to
`stopover_gap_fixes`, capped by `max_total_gap`) becomes `winter_run`.

A minimum offset (`min_days_before_winter`) prevents the very start of the
year from accidentally being mistaken for wintering, since the bird is
also near home (low NSD) right after tagging, not during a real wintering
plateau.

**Important: only ONE final run is kept per phase.** While scanning
through the data, the run-finding logic can encounter several separate
candidate stretches (broken up by gaps too big to bridge). All of them
are tracked as it goes, but only the single **longest** one is kept as
the final answer — the rest are discarded. This applies identically to
`winter_run`, `south_run`, and `north_run`: each is one single winning
stretch, not a combination of multiple stretches. See
`chaining_and_bridging.md` for a full walkthrough of exactly how this
works.

**6. Split the timeline into "before wintering" and "after wintering."**
Once `winter_run` is found, everything before it becomes the search
window for southbound; everything after becomes the search window for
northbound. If no wintering run is found at all, the whole year is
searched for both (a fallback case).

**7. Find the southbound run.**
Within the "before wintering" window, find the longest run where the
rate of change clears the `rising_threshold` (a `flat_threshold_frac`-
based cutoff) — meaning the bird is moving away from home fast enough to
count as real migration, not noise. Short gaps (stopovers) up to
`stopover_gap_fixes` are bridged.

**8. Apply the safety cap.**
If the resulting southbound run is longer than `max_south_days`, it gets
hard-truncated. This is a safety net against runaway results, not a
routine part of normal operation — see `known_limitations.md` for how
this was originally discovered and fixed.

**9. Find the northbound run.**
Same process as step 7, but within the "after wintering" window, looking
for a *falling* rate of change (moving back toward home).

**10. Assign phase labels and split into three DataFrames.**
Every GPS fix defaults to `"wintering"`. Fixes inside the southbound run
get relabeled `"southbound"`; fixes inside the northbound run get
relabeled `"northbound"`. The full track is then split into three
separate DataFrames — one per phase — and returned.

## What downstream code receives
`segment_track()` returns a dictionary with three keys: `"southbound"`,
`"wintering"`, `"northbound"` — each a DataFrame of just that phase's GPS
points, with a fresh reset index. This is the exact input the DTW step
will consume: comparing one bird's `"southbound"` DataFrame against
another bird's `"southbound"` DataFrame (and separately, northbound
against northbound).