# Why `max_total_gap` Matters

The paper's day-counts **do** include rest days. The 93-day southbound
average includes the birds' real North Atlantic stopover (about 25 days
resting), because the paper measures "date left colony" to "date arrived
at wintering grounds" — the whole trip, rest included, not just flying
time.

So why does `max_total_gap` matter, concretely?

Because **some rest-day-ignoring is correct and expected** — that's the
whole reason `max_gap` exists in the first place: to let the code
correctly include a bird's one real ~25-day rest stop, matching what the
paper counts. The problem is: without a *limit* on how much ignoring is
allowed, the code doesn't know when to stop, and it can start ignoring
rest days that don't belong to the same trip at all — accidentally
gluing southbound onto part of wintering.

**This isn't hypothetical — it actually happened in this project.**
Before `max_total_gap` existed, two specific birds (ARTE_373 and
ARTE_410) came out with southbound trips of **144–176 days** — nearly
double the paper's maximum of 103. The code had ignored so many rest
days that it accidentally swallowed part of wintering into the
"southbound" count. That made the segmentation useless — you can't
compare "southbound routes" between birds if one bird's southbound
number is secretly half wintering.

`max_total_gap` is what stops that specific failure from happening
again.