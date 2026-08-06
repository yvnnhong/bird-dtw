# Methodology: What This Segmentation System Actually Is

## Who this is for
Anyone using this library's output for research, analysis, or publication
should read this first. It clarifies exactly what kind of claim our
segmentation output can and cannot support.

## "Ground truth" vs. "a heuristic system" — not interchangeable

**Ground truth** specifically means verified, known-correct labels for
individual data points. For this project, that would mean a researcher
manually reviewing each GPS ping for each bird and tagging it "yes, this
specific ping is southbound migration" (or wintering, or northbound) —
ideally cross-checked against independent evidence (e.g. direct
observation, additional sensors).

**We do not have that, for any bird, for any ping.** No individual GPS
point in this dataset has a verified, human-confirmed phase label.

**What we actually built instead** is a **heuristic, rule-based
classification system**: a set of mathematical rules (smoothing, rate of
change, distance-from-home thresholds — see `glossary.md`) that assigns a
phase label to each GPS ping automatically, based on patterns in the data.

## How we validate a system that has no per-point ground truth

Since we can't check "is this specific ping correctly labeled," we instead
check something weaker but still useful: **does the total number of days
our system assigns to each phase, per bird, roughly match the population
average reported in a peer-reviewed source** (93 days southbound, 40 days
northbound, per Egevang et al. 2010)?

This is a **population-level sanity check**, not a per-point validation.
Passing it tells you "our system's overall output is plausible in
aggregate." It does **not** tell you "every individual GPS ping in the
southbound DataFrame for ARTE_373 is correctly southbound." Some
individual points near phase boundaries could plausibly be mislabeled even
while the total day-count looks right — a system can get the right total
by being wrong in ways that cancel out.

## What this means in practice

- Our segmentation output is a **best estimate**, checked indirectly
  against a published range, not a ground-truth-verified dataset.
- Parameter tuning (see `parameter_tuning.md`) means we chose the
  parameter values that make our system's aggregate output best match the
  paper's range — not the values that are provably, individually correct
  for every bird.
- If you build downstream analysis (e.g. DTW comparisons) on top of this
  segmentation, any claims about "route similarity" inherit this same
  caveat: they are claims about our heuristic's output, not about verified
  ground truth.
- Some birds fit this system better than others. See
  `known_limitations.md` for birds where the fit is weaker (e.g. ARTE_370)
  or structurally incomplete (e.g. ARTE_395's missing northbound data).

## Why this distinction matters for a research-facing library

If this library is used by ornithologists or other researchers, it's
important they understand any conclusions drawn from its segmentation
output are conclusions about "what our rule-based system inferred," not
"what was independently observed and verified." This is a normal and
common situation in movement ecology (individual-level ground truth is
rare and expensive to obtain), but it should be stated plainly rather than
implied.