# NSD, Smoothing, and Rate — From First Principles

## Why this doc exists
Reading `segmentation.py` doesn't make it obvious what's being squared,
what smoothing physically does to the numbers, or what units anything is
in. This doc answers those questions directly, with a fully worked
example showing the actual arithmetic step by step.

---

## Part 1: What is NSD, exactly?

**NSD = Net Squared Displacement.** It is computed here:

```python
def compute_nsd(track: pd.DataFrame, home_lat: float, home_lon: float) -> pd.Series:
    distances = haversine_km(home_lat, home_lon, track["lat"], track["lon"])
    return distances ** 2
```

**What's being squared:** the real-world distance (in km) between the
bird's current position and "home" (the first GPS fix in that bird's
record). This distance comes from `haversine_km()`, which computes actual
great-circle distance on a sphere — not a flat-map approximation, and not
raw degrees of latitude/longitude.

**Units, step by step:**
- `haversine_km()` output: **km**
- NSD (`distances ** 2`): **km²** (kilometers, squared)

So if a bird is 500 km from home at some point in time, its NSD at that
moment is 500² = **250,000 km²**.

---

## Part 2: What does smoothing actually do to the numbers?

Smoothing is applied here:

```python
nsd_smooth = nsd.rolling(window=smooth_window, center=True, min_periods=1).mean()
```

This is a genuine **rolling average** — a real, literal average computed
over a moving window of nearby points, using pandas' built-in `.rolling()`
function. Nothing manual or approximate about it; this is executed code.

### Worked example: 6 NSD values, window size 3

Say we have 6 raw NSD values in chronological order (units: km²):

```
Position:  1     2     3     4     5     6
Raw NSD:  100   200   150   400   380   420
```

With `window=3` and `center=True`, each position's smoothed value is the
average of **itself, one point before, and one point after** — a
3-point window centered on that position. `min_periods=1` means: if a
full 3-point window isn't available (e.g. at the very start or end),
average whatever points *are* available instead of leaving it blank.

**Step-by-step arithmetic for every position:**

- **Position 1** (no point before it exists): average of itself and the
  next point only:
  `(100 + 200) / 2 = 150`

- **Position 2** (has a full 3-point window: positions 1, 2, 3):
  `(100 + 200 + 150) / 3 = 150`

- **Position 3** (window: positions 2, 3, 4):
  `(200 + 150 + 400) / 3 = 250`

- **Position 4** (window: positions 3, 4, 5):
  `(150 + 400 + 380) / 3 = 310`

- **Position 5** (window: positions 4, 5, 6):
  `(400 + 380 + 420) / 3 = 400`

- **Position 6** (no point after it exists): average of itself and the
  previous point only:
  `(380 + 420) / 2 = 400`

**Result — raw vs. smoothed, side by side:**

```
Position:      1     2     3     4     5     6
Raw NSD:      100   200   150   400   380   420
Smoothed NSD: 150   150   250   310   400   400
```

Notice the smoothed line changes more gradually than the raw line — the
sharp jump from 150→400 (positions 3→4) in the raw data becomes a more
gradual climb (250→310→400) in the smoothed version. That's the entire
point of smoothing: it reduces sharp, possibly-noisy jumps into a calmer
trend. Units remain **km²** throughout — smoothing averages the values,
it does not change what they represent.

### An important detail: `smooth_days` is NOT the same as window size

**First, what is a "row"?** The bird's data (`track`) is a table — one
row per GPS fix, i.e. one row per single recorded moment (one timestamp,
one lat, one lon). Since the tracking device records roughly twice a
day, the table has roughly 2 rows per day, for the whole ~9-10 month
tracking period.

**What does `.rolling(window=...)` actually roll over?** It rolls over
**rows** — i.e. over consecutive GPS fixes, in order — not over calendar
days directly. `pandas` has no built-in concept of "days" here; it only
understands "how many rows to include in each averaging window."

**So how does a *day*-based parameter (`smooth_days`) become a
*row*-based window?** It has to be converted, because `.rolling()` only
accepts a row-count, not a day-count:

```python
fixes_per_day = 2
smooth_window = max(3, int(smooth_days * fixes_per_day))
```

In plain terms: "I want to smooth over about 12 days" becomes "12 days ×
2 fixes recorded per day = 24 rows." So `smooth_days=12` actually
produces **`smooth_window = 24`** — a 24-row window, not a 12-row window.
The parameter name (`smooth_days`) is written in the human-friendly unit
(days), but gets translated internally into the unit `.rolling()` needs
(rows/fixes), using the tracker's sampling rate as the conversion factor.
This translation step is easy to miss just from reading the parameter
name.

**Concretely: how many days before and after does this actually cover?**
Because `center=True` is used, this 24-row window is centered ON the
point being smoothed — meaning the window is split roughly evenly
between rows before it and rows after it: **~12 rows before, ~12 rows
after.** Since there are 2 rows per day, that's **~6 days of data before
the point, and ~6 days of data after the point** — 12 days total, spread
evenly around that point in time.

So, concretely: **`smooth_days=12` means "for every GPS fix, average it
together with roughly everything recorded from 6 days before it, through
6 days after it."** That averaged result becomes the smoothed value for
that specific fix.

---

## Part 3: What is `rate`, and what are its units?

```python
rate = nsd_smooth.diff(trend_lag) / trend_days
```

`.diff(trend_lag)` means: take each smoothed NSD value and subtract the
smoothed NSD value from `trend_lag` rows earlier. This gives "how much
did distance-from-home change, compared to N fixes ago" — still in
**km²** at this point (a difference of two km² values is still km²).

Dividing that difference by `trend_days` converts it into **a rate**:
**km² per day**. This tells you how fast the bird's squared
distance-from-home is changing, per day — positive means moving away
from home (rising), negative means moving back toward home (falling).

**Worked example**, continuing from above, with `trend_lag` = 2 positions
and `trend_days` = 2:

- At position 4, compare to position 2:
  `(310 − 150) / 2 = 80` → rate = **+80 km²/day** (rising)
- At position 6, compare to position 4:
  `(400 − 310) / 2 = 45` → rate = **+45 km²/day** (still rising, but
  slower)

(This toy example only rises throughout, since our 6 sample points were
chosen just to demonstrate the smoothing arithmetic clearly — a real
bird's rate would eventually turn negative during the northbound leg.)

---

## Part 4: Two completely different uses of "rolling" — don't confuse
## these

This project uses the word "rolling" (or the concept of averaging) in
two **unrelated** places. They are easy to mix up, so here they are side
by side:

| | **NSD smoothing (Part 2, above)** | **Paper-comparison validation** |
|---|---|---|
| Is it a real rolling average? | **Yes** — literal `pandas.rolling().mean()` | **No** — not a rolling average at all |
| Where does it happen? | Inside `segment_track()`, in `segmentation.py` | Nowhere in code — done manually |
| What is it applied to? | The NSD signal itself, per GPS fix | Total day-counts printed by `test_segmentation.py` |
| How is it checked? | Automatically, by pandas, every time `segment_track()` runs | By a human, reading printed output and comparing it by eye to the paper's 69–103 / 36–46 day range |

If you ever see "rolling" or "average" mentioned elsewhere in this
project's docs, check which of these two it's referring to — they are
not the same process, and only one of them (NSD smoothing) is actual
running code.