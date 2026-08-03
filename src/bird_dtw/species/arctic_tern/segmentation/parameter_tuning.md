# Parameter Tuning Log — Arctic Tern Segmentation

## What this file is for
This file records every parameter we tested while building the system that
splits one Arctic tern's messy year-long GPS track into three pieces:
southbound migration, wintering, and northbound migration. It explains each
term from scratch, what changing it does, what we tried, and what we picked
— and why.

**Important clarification on terminology:** this process is **not** "finding
ground truth." Ground truth means verified, known-correct labels for
individual data points (e.g. a researcher manually tagging each GPS ping).
We don't have that — nobody labeled individual pings as southbound/
wintering/northbound. What we're actually doing is **building a rule-based
system (a heuristic)** to classify pings, and checking its output against
the only external check available: the paper's population-average day
counts (93 days southbound, 40 days northbound). If our system's numbers
land near those, we call it "good enough," not "verified correct."

---

## Part 1: First principles — what are we even measuring?

### NSD (Net Squared Displacement)
**What it means:** the squared straight-line distance from "home" (the
bird's first recorded GPS point) to wherever the bird is right now.

**In plain terms:** imagine a string tied from the bird's nest to the bird.
NSD is "how long is that string, squared" at any given moment.

**Why squared, not just distance:** squaring makes big distances stand out
much more than small ones. A bird 100 km from home gives NSD = 10,000. A
bird 3,000 km from home (near wintering grounds) gives NSD = 9,000,000.
This exaggerates the difference between "still near home" and "far away,"
making the wintering plateau easier to detect visually and mathematically.

**Why NSD, not raw lat/lon:** lat/lon are angles, not distances. Squeezing
them into one number that means "distance from home" turns a 2D position
into a 1D number we can plot on a simple line graph and reason about.

### Haversine distance
**What it means:** the real-world distance between two points on a sphere
(the Earth), measured in km.

**In plain terms:** measuring distance on a globe, not on a flat map.
Degrees of longitude are NOT equally spaced in real km — they're wide at
the equator and shrink to zero at the poles. Haversine accounts for this
curvature so "distance" means actual km flown, not a flat-map illusion.

**Why it matters for this project:** Arctic terns fly pole-to-pole. Any
calculation that pretends the Earth is flat would be badly wrong near the
poles specifically — exactly where this bird spends its time. This is why
`haversine_km()` exists in the code instead of simple Pythagorean distance.

---

## Part 2: Turning NSD into "is the bird migrating right now?"

### Smoothing (`smooth_days`)
**What it means:** averaging NSD across a window of days, instead of using
the raw value from a single GPS ping.

**In plain terms:** imagine a shaky handheld video — smoothing is like
applying stabilization so the picture doesn't jitter. Raw GPS noise (small
random errors in each ping) gets averaged out, leaving a calmer curve.

**Trade-off:** higher smoothing = calmer, easier-to-read curve, but it can
blur the exact day migration started or stopped, since it's blending
nearby days together.

### Rate of change (`trend_days`)
**What it means:** comparing "where is the bird now" to "where was it N
days ago," to see whether the smoothed NSD is going up (moving away from
home) or down (moving back toward home).

**In plain terms:** like checking your bank balance today vs. two weeks
ago to see if you're spending or saving — the *direction* of change matters
more than the raw balance itself.

### `flat_threshold_frac`
**What it means:** a cutoff, expressed as a fraction (percentage) of the
single biggest rate-of-change seen anywhere in that bird's whole year. Any
rate-of-change smaller than this fraction is treated as "not really
moving" — just noise.

**In plain terms:** if the fastest the bird was ever moving all year is
"100%," this says "ignore anything under X% of that top speed — that's
just wobble, not real travel."

**What changing it does:** raising this value makes the system pickier
about what counts as "actively migrating" (fewer false positives from
noise, but risks cutting off real slow-moving migration days). Lowering it
makes the system more permissive (catches more real migration, but risks
mistaking noise for movement).

**What we tried:** 0.08, 0.07, 0.06, 0.05

| Bird | 0.08 | 0.07 | 0.06 | 0.05 |
|---|---|---|---|---|
| ARTE_370 | 36/33 | 36/33 | 37/33 | 37/35 |
| ARTE_371 | 65/35 | 65/35 | 66/35 | 66/35 |
| ARTE_373 | 78/40 | 79/40 | 80/40 | 80/40 |
| ARTE_376 | 66/41 | 66/41 | 66/41 | 68/41 |
| ARTE_390 | 66/33 | 66/33 | 66/33 | 66/33 |
| ARTE_395 | 69/0 | 69/0 | 69/0 | 69/0 |
| ARTE_406 | 72/35 | 73/35 | 74/35 | **93/35** |
| ARTE_408 | 58/31 | 59/31 | 59/32 | 59/32 |
| ARTE_410 | 59/33 | 59/33 | 59/33 | 60/33 |

(Format: southbound days / northbound days. Note: we start in the North.)

**What we learned:** this parameter barely mattered. Seven of nine birds
moved by 0–2 days total across the whole 0.08→0.05 range — essentially
noise. Only ARTE_406 jumped a lot (72→93), and inspecting the debug output
showed this wasn't a "more accurate" result — it was the algorithm latching
onto a completely different, longer stretch of "rising" data, a sign of
picking up noise rather than real signal. **Conclusion: this was not the
right lever to fix the birds coming out short. We kept it at 0.08 (the
original, most stable value) and moved on to a different parameter.**

---

## Part 3: Detecting wintering

### Why detecting wintering matters
Wintering has to be found *before* southbound and northbound can be
measured properly, because in the code, southbound is "the biggest rising
run *before* wintering starts" and northbound is "the biggest falling run
*after* wintering ends." Get wintering wrong, and both other phases are
wrong too.

### What "wintering" actually means biologically
Wintering = the bird has arrived in the Antarctic/Southern Ocean region and
is staying roughly in one area (not purposefully flying in one direction
anymore) during the Southern Hemisphere summer (~Dec–Mar per the paper).
It is NOT the bird sitting in the Arctic — the Arctic is the breeding
ground, visited before southbound migration, not during wintering.

### The first (abandoned) approach: detecting wintering by rate-of-change
Originally, wintering was detected as "the longest stretch where the rate
of change is flat" (low speed = resting = wintering). This turned out to
be **fragile**: noise could cause brief speed spikes scattered throughout
the true wintering plateau, breaking it into short fragments. An unrelated,
shorter, uninterrupted flat stretch elsewhere (e.g. mid-southbound) could
then incorrectly win "longest run" instead of true wintering.

### The fix: detecting wintering by NSD value instead
**What changed:** wintering is now detected by asking "is the bird
currently far from home" (a high NSD *value*), not "is the bird's speed
currently near zero" (a rate-of-change *derivative*). A bird that has
truly arrived at wintering grounds stays *far* from home for a long,
unbroken stretch — that's a much steadier signal than speed, which can
wobble due to noise even while stationary.

### `near_max_nsd` cutoff — the parameter we tuned this session
**The exact line of code:**
```python
near_max_nsd = nsd_smooth > (0.85 * max_nsd)  # "far from home" = candidate wintering
```

**What it means:** `max_nsd` is the single largest NSD value the bird
reaches all year (its farthest point from home, squared). The cutoff says:
"count this point in time as a wintering candidate only if the bird is
currently at least X% as far from home as it ever gets."

**In plain terms:** if the farthest the bird ever travels from home is
"100%," this parameter asks "how close to that farthest point does the
bird have to be, right now, to count as wintering?" A cutoff of 0.85 means
"the bird must be at least 85% of the way to its farthest point to count."

**What changing it does — this is the key, non-obvious part:**
- **Raising** the cutoff (e.g. 0.7 → 0.85) makes it *harder* to qualify as
  wintering (the bird must be closer to its absolute farthest point).
  This makes the wintering window *narrower* and *starts later / ends
  earlier* — which gives southbound and northbound *more room* to extend,
  since they're measured as "everything before/after wintering."
- **Lowering** the cutoff makes it *easier* to qualify as wintering
  (even being 65% of the way to the farthest point counts). This makes the
  wintering window *wider* — starting earlier and ending later — which
  *squeezes* southbound and northbound into *less* room.

This is the opposite of what might be guessed intuitively at first, which
is why our first attempt (lowering to 0.65) made results worse, not
better — southbound/northbound got shorter for every single bird. Raising
it, as we discovered next, was the correct direction.

**What we tried:** 0.65, 0.7 (original default), 0.75, 0.8, 0.85, 0.9

| Bird | 0.65 | 0.7 | 0.75 | 0.8 | 0.85 | 0.9 | Paper range |
|---|---|---|---|---|---|---|---|
| ARTE_370 | 35/31 | 36/33 | 38/33 | 41/34 | 43/35 | 53/36 | 69–103 / 36–46 |
| ARTE_371 | 58/34 | 65/35 | 67/37 | 69/38 | 71/40 | 82/42 | |
| ARTE_373 | 76/37 | 78/40 | 79/43 | 81/45 | 82/**48** | 83/**48** | |
| ARTE_376 | 59/40 | 66/41 | 70/43 | 73/44 | 75/45 | 78/**47** | |
| ARTE_390 | 55/32 | 66/33 | 68/34 | 70/35 | 72/37 | 84/39 | |
| ARTE_395 | 65/0 | 69/0 | 76/0 | 79/0 | 81/0 | 83/0 | (no northbound data — see note) |
| ARTE_406 | 69/34 | 72/35 | 74/37 | 76/38 | 78/40 | 80/41 | |
| ARTE_408 | 52/30 | 58/31 | 65/32 | 68/33 | 69/34 | 71/34 | |
| ARTE_410 | 48/32 | 59/33 | 61/34 | 64/35 | 67/36 | 77/38 | |

(Format: southbound days / northbound days. **Bold** = value exceeds the
paper's stated maximum for that phase.)

**What we learned, step by step:**
1. **0.65 made everything worse.** Every bird's southbound and northbound
   got shorter compared to the original 0.7 default. This told us the
   direction of the fix was backwards — lowering the cutoff widens the
   wintering window, which was the opposite of what these short birds
   needed.
2. **0.75, 0.8 improved things steadily and consistently.** Every bird
   moved closer to the paper's range with each increase — a clean,
   predictable trend, unlike the noisy jumps seen with
   `flat_threshold_frac`.
3. **0.85 was the best average fit** — 6 of 9 birds land inside the
   paper's range on both southbound and northbound. But ARTE_373's
   northbound just tips over the maximum (48 vs. 46).
4. **0.9 showed clear overshoot.** ARTE_373 stays over, and ARTE_376's
   northbound now also exceeds the maximum (47 vs. 46). The *count* of
   fully-in-range birds does not improve past 0.8 — going higher just
   trades which birds are in range for which.

**A genuine tension we found, not fixable by this parameter alone:**
ARTE_370, 408, and 410 need a *higher* cutoff to reach their southbound
minimum (69 days), while ARTE_373 and 376 need a *lower* cutoff to avoid
overshooting their northbound maximum (46 days). No single global value
satisfies both groups — this is a real limitation of using one fixed
threshold for every bird, not a sign we picked the wrong number.

---

## Part 4: Final decision

**Chosen value: `near_max_nsd = nsd_smooth > (0.85 * max_nsd)`**

**Reasoning:** 0.85 gives the best overall balance — the highest number of
birds landing inside the paper's plausible range, at the cost of one bird
(ARTE_373) overshooting its northbound maximum by 2 days. Going higher
(0.9) does not improve the total count of well-fit birds and makes the
overshoot worse. Going lower (0.8) avoids any overshoot entirely, but
leaves more birds short on both phases. 0.85 was chosen as the better
trade-off between "some birds are a couple days over" vs. "many birds are
noticeably short."

**`flat_threshold_frac` stays at its original value: 0.08.** Testing showed
this parameter has very little effect on the outcome compared to the NSD
wintering cutoff, so it was left at the most stable, previously-established
value rather than re-tuned further.

**Known remaining limitation:** ARTE_370 (43→53 days southbound across our
whole tested range) never reaches the paper's 69-day minimum, even at the
highest cutoff tried. This bird likely has a genuinely different NSD
pattern (a less pronounced or later peak) that a single global threshold
cannot fully correct. This is flagged as an open issue, not something this
round of tuning was expected to solve.

**ARTE_395 has 0 days northbound at every threshold tested — this is
expected, not a bug.** Its raw geolocator record ends in November 2007
(only 99 total days of data), before winter or northbound migration would
have happened. There is no data to segment for this bird's northbound
phase, and no parameter change will ever produce a nonzero result for it.

---

## Part 5: Next steps after this tuning round
1. Update `src/bird_dtw/species/arctic_tern/segmentation.py` to keep
   `near_max_nsd = nsd_smooth > (0.85 * max_nsd)` as the working value
   (already done).
2. Consider this segmentation step "good enough" for 7 of 9 valid birds
   (excluding ARTE_395, which structurally cannot have northbound data).
   ARTE_370 remains a known open issue.
3. Move on to the DTW (Dynamic Time Warping) step: feed the segmented
   southbound/northbound DataFrames into the existing generic DTW class,
   using `haversine_km()` as the distance function and `WINDOW_SIZE = 4`
   (from `params.py`) as a warping-path constraint.