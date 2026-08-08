# Finding: Northbound Routes Are More Similar Across Birds Than Southbound

## The question we were testing

**Hypothesis:** northbound migration routes should be more similar to
each other across different birds (tighter/lower DTW distance) than
southbound routes are, since there's no "correct" template to compare
against — just birds compared against each other.

**Why we expected this (biological reasoning):** northbound is a more
direct, wind-driven open-ocean path — birds funnel through similar
routes. Southbound has genuine route-choice variability (West Africa
coast vs. Brazil coast) plus stopover variability, so southbound routes
should differ more from each other.

## What we did

1. **Segmented every bird once.** For all 9 usable birds, ran
   `segment_track()` (from `segmentation.py`) to split each bird's raw
   yearly GPS track into southbound / wintering / northbound legs.
2. **Built a pairwise DTW comparison.** For every unique pair of birds
   (36 pairs total, from `itertools.combinations`), ran the `DTW` class
   (`dtw.py`) on their southbound legs, and separately on their
   northbound legs. ARTE_395 was skipped for northbound pairs — it has
   no northbound data (tracking record ends Nov 2007).
3. **Computed two versions of the average distance:**
   - **Raw total DTW distance**, averaged across all southbound pairs vs.
     all northbound pairs.
   - **Per-step average distance** (`distance / max(len(path_a),
     len(path_b))`), to control for the fact that southbound legs are
     naturally longer than northbound legs (93 days vs. 40 days, per the
     source paper) — a longer path accumulates more total DTW cost
     regardless of how similar the routes actually are. Per-step
     normalizes this out.

## What we found

| Metric | Southbound | Northbound | Northbound tighter? |
|---|---|---|---|
| Average raw DTW distance | 381,173.03 | 103,476.41 | Yes |
| Average per-step distance (km) | 3,074.60 | 1,163.01 | Yes |

Northbound stayed roughly **2.6x tighter** than southbound even after
controlling for path length. This means the result isn't just an
artifact of southbound legs being longer — it reflects a genuine
difference in how similar the routes are, shape-for-shape.

## Which functions/files did this work

- `segmentation.py` → `segment_track()`: split each bird's track into
  legs.
- `dtw.py` → `DTW` class, specifically `dynamic_time_warping()`: computed
  the alignment cost between each pair of tracks, using `_in_band()` (the
  Sakoe-Chiba window) and `_get_haversine_km()` (real sphere distance) as
  the local cost function.
- Pairwise loop (`test_pairwise_dtw.py`, repo root): looped over all 9
  birds, all 36 pairs, both legs, and computed the averages above.

## What this supports

This is evidence in favor of the hypothesis: northbound migration is
more constrained/similar across individual birds, while southbound
shows more genuine route variability. This lines up with the reasoning
in `docs/north_vs_south.md` about gyres and wind patterns shaping
northbound into a narrower, more converged path.

## What this does NOT prove (be careful not to overclaim)

- This is 9 birds, one season, one dataset (Egevang et al. 2010,
  Greenland/Iceland colony). It's a real, measured result for this
  dataset — not a generalized claim about all Arctic terns everywhere.
- The southbound legs in this dataset are also longer in raw day-count,
  which could allow more opportunity for route divergence to accumulate,
  even after per-step normalization. Worth keeping in mind as a caveat,
  not a flaw — normalization controls for path *length* in the DTW
  math, but doesn't fully separate "more days" from "more chances to
  diverge" biologically.
- No statistical significance test (e.g. t-test) has been run yet on
  whether the southbound vs. northbound difference is significant beyond
  chance — this is currently a descriptive comparison of averages, not a
  hypothesis test in the statistical sense.

## Possible next steps (not started yet)

- Visualize the spread, not just the average (e.g. box plot of all 36
  southbound distances vs. 36 northbound distances) to see if this is a
  consistent pattern or driven by a few outlier pairs.
- Run a statistical test on the two distributions if a stronger claim is
  wanted later.