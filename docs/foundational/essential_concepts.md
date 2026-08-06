# Essential Concepts — Read This First

This is not a numbers reference (see `important_numbers.md` for that).
This is a short list of **behavioral facts about how the code actually
works** that change how you should read every other doc in this project.
These are the things that, if missed, make the other docs confusing or
misleading.

---

## 1. Only ONE final run is kept per phase — always

`_longest_run()` (the function that finds southbound, wintering, and
northbound) can encounter **multiple separate candidate stretches** while
scanning through a bird's year — stretches broken apart by gaps too big
to bridge. It tracks all of them as it scans, but at the very end, it
keeps **only the single longest one** and throws the rest away.

This applies identically to `south_run`, `winter_run`, and `north_run` —
none of them is ever a combination of multiple stretches. Each is exactly
one winning run, per phase, per bird. See `chaining_and_bridging.md` for
the full mechanics of this.

## 2. Bridging and the total-gap cap apply the same way to all three
## phases

Southbound, wintering, and northbound are all found using the same
underlying logic, called three separate times, with the same `max_gap`
value each time. Nothing behaves differently for any one phase — there's
no special-case logic for southbound vs. wintering vs. northbound in how
gaps get bridged.

## 3. `max_total_gap` is currently NOT set to a different value than
## `max_gap`, anywhere in this codebase

Even though `_longest_run()` supports a separate `max_total_gap`
parameter, none of the three calls in `segment_track()` actually pass a
distinct value for it. This means it silently defaults to being **equal
to** `max_gap` everywhere it's currently used — the two parameters exist
as separate concepts in the code, but aren't currently being used with
different values in practice.

## 4. This is a heuristic system, not ground truth

Nothing in this segmentation output is independently verified,
point-by-point, against a known-correct answer. It's a rule-based best
estimate, checked only in aggregate against the paper's population-level
day-count ranges. See `methodology.md` for the full distinction.

## 5. "Starts in the north" is an inference, not a labeled fact

Nowhere does the data or the paper explicitly say "this GPS point is the
start of migration." The code assumes the bird's very first recorded GPS
fix is "home" (in the Arctic), based on how the tracking devices were
deployed — at breeding colonies, before migration began. This has not
been independently verified per bird in the code (e.g. no check that the
first fix actually has a high latitude). See `segmentation_process.md`.

## 6. The paper-comparison validation is manual, not automated

Comparing each bird's day-counts against the paper's 69–103 / 36–46 day
ranges is something a person does by reading printed output — there is
no `validate()` function or automated pass/fail check anywhere in this
codebase today.

## 7. The birds are from Greenland and Iceland — not Svalbard

10 Greenland birds, 1 Iceland bird, per Egevang et al. 2010. Svalbard
belongs to a different, unrelated tracking study. See
`data_provenance.md`.

## 8. It is southbound, not northbound, that hugs coastlines

Southbound birds follow one of two coastal routes (West Africa or
Brazil). Northbound follows a more direct, open-ocean path. This is easy
to get backwards intuitively. See `north_vs_south.md`.

## 9. Units matter and are easy to mix up

- NSD is in **km²** (a squared distance), not km, not degrees.
- `rate` is in **km² per day**.
- `max_gap` / `max_total_gap` count **rows (GPS fixes)**, not days, hours,
  or any distance — day-equivalents are only computed once, before being
  passed in, via `fixes_per_day`.
- `smooth_days` gets converted into a row-count window internally; it is
  not itself the number of rows averaged. See `nsd_and_smoothing.md`.

## 10. Wintering  
The wintering stretch follows the same run-selection rules as the south and the north stretches except it has that rule about being more than 85%. 