# Pairwise DTW Comparison Plan

## Why pairwise, not template-based

There's no "correct" template route to compare each bird against — no
ground-truth ideal path exists. So instead: compare every bird's leg
against every other bird's same leg (southbound vs southbound, northbound
vs northbound). Each bird acts as its own point of comparison, not judged
against one artificial "ideal."

## The hypothesis

Northbound distances should be tighter across birds than southbound,
since there's no "correct" template to compare against anyway — just
birds against each other.

**Why this might be true (biological reasoning):** northbound is a
wind-driven, more direct open-ocean path — birds funnel through similar
routes. Southbound has genuine route-choice variability (West Africa
coast vs. Brazil coast) plus stopover variability, so southbound DTW
distances between birds should be larger on average.

## Step: build a pairwise distance matrix

Instead of comparing 1 pair (e.g. ARTE_371 vs ARTE_373), run DTW on
every pair of birds, for southbound and northbound separately.

With 9 birds, that's 36 pairs per leg (9 choose 2 = 36). Store results
in a dict or small DataFrame: `{(bird_a, bird_b): distance}`.

Once both matrices (southbound pairs, northbound pairs) exist, compare
the **average** distance across all southbound pairs vs. the average
across all northbound pairs. That average comparison is the actual test
of the hypothesis above.

**Note:** ARTE_395 has no northbound data (tracking ends Nov 2007). Skip
any pair involving ARTE_395 when building the northbound matrix. It can
still be included in the southbound matrix.

## Is this O(n²)? Yes — and that's expected, not a bug

With 9 birds, computing every unique pair is `n choose 2 = 9*8/2 = 36`
pairs per leg. That's quadratic growth (O(n²)) — doubling the birds
roughly quadruples the pair count. For 9 birds this is trivial (36 DTW
calls total per leg). It only becomes a real problem if the bird count
grows into the hundreds or thousands.

### Optimizations available, if/when this matters later

1. **Only compute the upper triangle.** Distance(A, B) == Distance(B, A)
   for DTW here (nothing direction-dependent in the setup), so only
   compute each pair once, not both (A,B) and (B,A). This alone cuts the
   work in half — already assumed in the "36 pairs" count above.

2. **The band (`_in_band` / Sakoe-Chiba window) already limits the cost
   of each individual DTW call.** Without a band, one DTW call costs
   O(rows × cols). With the band, it's closer to O(rows × window) — much
   cheaper per call, since most of the grid is skipped. This doesn't
   reduce the *number* of pairs, but it makes each pair cheap.

3. **Caching `haversine_km()` results**, if the same lat/lon points ever
   get compared more than once across different pairs (unlikely with
   real GPS data, but worth knowing as an option).

4. **Parallelization.** Each pair's DTW calculation is fully independent
   of every other pair — this is "embarrassingly parallel." If this ever
   needs to scale to more birds, the 36 (or more) DTW calls could run
   concurrently instead of one after another.

**For 9 birds specifically: none of this is necessary yet.** 36 DTW
calls, each already cheap due to the band, will run in well under a
second combined. This section is here so the optimization options are
known and written down, not because they're needed right now.

## Next steps after the matrix is built

1. Compute average southbound distance vs. average northbound distance.
2. Check: is average northbound < average southbound? (Confirms or
   denies the hypothesis.)
3. Consider a simple visualization — e.g. a bar chart or box plot of
   southbound distances vs. northbound distances — to see the spread,
   not just the average.