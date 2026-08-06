# Known Limitations

This doc lists things about the current segmentation system that are
known to be imperfect, incomplete, or unresolved — so future work (by you
or anyone else using this library) doesn't have to rediscover them from
scratch.

## ARTE_395 has no northbound segment — this is expected, not a bug

ARTE_395's raw geolocator record only covers Aug 15 – Nov 22, 2007 (99
total days). The tracking data simply ends before winter or northbound
migration would have occurred. There is no GPS data to segment for this
bird's northbound phase, at any parameter setting. Exclude this bird from
northbound validation checks specifically; its southbound result remains
valid and usable.

## ARTE_370 never reaches the paper's southbound minimum

Across every wintering-cutoff value tested (0.65 through 0.9), ARTE_370's
southbound segment tops out around 35–53 days — never reaching the
paper's stated minimum of 69 days. This bird likely has a genuinely
different NSD (distance-from-home) pattern — for example, a smaller or
later peak distance from home — that a single global threshold, shared
across all 9 birds, cannot fully correct. This remains an open issue. A
per-bird or adaptive threshold (rather than one fixed global value) may
be necessary to resolve it, but this has not yet been attempted.

## No single global threshold satisfies every bird simultaneously

During parameter tuning of the wintering NSD cutoff, we found a genuine
tension: ARTE_370, ARTE_408, and ARTE_410 need a *higher* cutoff to reach
their southbound minimum, while ARTE_373 and ARTE_376 need a *lower*
cutoff to avoid exceeding their northbound maximum. No single value in
the range we tested (0.65–0.9) satisfies both groups at once. The chosen
value (0.85) represents a balance, not a perfect fit for all birds. See
`parameter_tuning.md` for the full numeric comparison.

## Population-average validation, not per-point validation

As detailed in `methodology.md`, our only validation method is comparing
aggregate day-counts per bird against the paper's population-average
range. This cannot catch errors where individual points are mislabeled in
ways that still produce a plausible total day count. Segmentation
boundaries (the exact GPS ping where one phase is judged to end and the
next begins) have not been individually verified against any independent
source.

## flat_threshold_frac is not a strong lever

Testing (0.05–0.08) showed this parameter has very little effect on
results — most birds shifted by 0–2 days total across that entire range.
One bird (ARTE_406) showed a large, likely spurious jump at the lowest
value tested (0.05 → 93 days), which further suggested this parameter was
picking up noise rather than a real signal for that bird specifically.
Future tuning efforts are more likely to matter if focused on the
wintering NSD cutoff or a per-bird approach, rather than this parameter.

## Original authors' stopover-detection method not yet implemented

Egevang et al. 2010's own methodology used a different rule for detecting
stopovers: latitudinal movement <0.8° over a 0.5-day period, smoothed over
3 days. This has not been implemented or compared against our
NSD-based/rate-based approach. This remains a possible future improvement
if further tuning is needed, particularly for birds like ARTE_370 where
the current approach falls short.

## Debug print statements

As of this writing, `segmentation.py` still contains `print("DEBUG: ...")`
statements left in intentionally during development for troubleshooting.
These should be removed (or converted to proper logging) before this code
is considered production-ready or shared more widely.