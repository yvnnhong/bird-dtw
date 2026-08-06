# Glossary of terms in segmentation.py

**NSD (Net Squared Displacement)**
NSD means the squared straight-line distance from home, at one point in
time. In plain terms, that's like asking "as the crow flies, how far
(squared) is the bird from its nest right now" — squaring makes big
distances stand out more clearly than small ones.

**Haversine distance**
Haversine means the real-world distance between two lat/lon points on a
sphere, not a flat map. In plain terms, that's like measuring distance on
a globe instead of a flat piece of paper — lat/lon degrees aren't equally
spaced in real km, so this fixes that.

**smooth_days (smoothing window)**
Smoothing means averaging NSD values over a time window to remove noise.
In plain terms, that's like squinting at a shaky line on a graph until it
turns into a calm, readable curve.
**Final value used: `smooth_days=12`**

**trend_days (trend lag)**
Trend lag means comparing "now" to "X days ago" to see if the bird is
moving away or coming back. In plain terms, that's like checking "am I
further from home than I was two weeks ago" to guess direction of travel.
**Final value used: `trend_days=12`**

**rate (rate of change)**
Rate means how fast the smoothed NSD is rising or falling. In plain
terms, that's like the bird's "speed away from home," not its literal
flying speed.

**flat_threshold_frac**
This means a cutoff, as a fraction of the year's biggest rate-of-change,
used to decide "is this actually movement, or just noise." In plain
terms, that's like saying "ignore any wiggle smaller than 8% of the
biggest wiggle all year — that's just static, not real travel."
**Final value used: `flat_threshold_frac=0.08`** (tested against 0.07,
0.06, and 0.05 — results were largely insensitive to this parameter
across that range; 0.08 was kept as the original, most stable value. See
`parameter_tuning.md` for the full comparison.)

**rising_threshold / rising / falling**
These mean "the rate cleared the flat_threshold cutoff, in the positive
or negative direction." In plain terms, that's like saying "the bird is
only counted as truly migrating if it's moving fast enough to not be
confused with resting-noise."

**near_max_nsd (wintering cutoff)**
This means "the bird is currently at least X% as far from home as it
ever gets all year." In plain terms, that's like saying "the bird is
basically at its farthest point — call this a wintering candidate,"
instead of guessing wintering from speed.
**Final value used: `0.85 * max_nsd`** (tested against 0.65, 0.7, 0.75,
0.8, and 0.9 — 0.85 gave the best overall balance across all 9 birds,
trading a small overshoot on one bird's northbound leg for the highest
count of birds landing inside the paper's plausible day-range. See
`parameter_tuning.md` for the full comparison and reasoning.)

**stopover_gap_fixes / max_gap**
This means the size of a gap in "moving" data that we're still willing to
bridge over (like a stopover). In plain terms, that's like saying "if the
bird pauses for a rest stop mid-migration, don't count that pause as the
migration being over."

**max_total_gap**
This means capping the SUM of all bridged gaps in one run, not just each
individual gap. In plain terms, that's like saying "you can bridge over
one rest stop, but not five small pauses that add up to a fake extra-long
migration."

**max_south_days (safety cap)**
This means a hard ceiling on how many days southbound is allowed to be,
no matter what. In plain terms, that's like a seatbelt — it stops things
from going wildly wrong even if some other part of the logic misbehaves.
**Final value used: `max_south_days=110`**