# Why Northbound and Southbound Migrations Are Different

## Who this is for
Anyone using this library who knows GPS/DTW analysis but not necessarily
the biology behind Arctic tern migration — or vice versa. This doc
explains *why* our code treats northbound and southbound as genuinely
different kinds of journeys, not just "the same trip in reverse."

## The basic pattern
Arctic terns fly from their Arctic breeding grounds (visited roughly
May–August) down to wintering grounds near Antarctica, then back again.
Per Egevang et al. 2010 (the source paper for this project's data):

- **Southbound (autumn/postbreeding) migration:** August–November,
  averaging 93 days (range 69–103 days across the study's birds)
- **Wintering:** December–March
- **Northbound (spring/return) migration:** April–May, averaging 40 days
  (range 36–46 days)

Northbound is roughly **half the length** of southbound, despite covering
similar ground. This isn't a coincidence, and it isn't a data quality
issue — it's a real, published biological asymmetry, driven mainly by
ocean wind patterns.

## What a gyre is
**In plain terms:** a gyre is a giant, slow, circular current of wind and
ocean water, hundreds to thousands of km across. Picture stirring a cup of
water — it doesn't just move in a straight line, it circulates in a loop.
Ocean basins have their own permanent versions of this, driven by global
wind patterns and the Earth's rotation.

The Atlantic Ocean has two major gyres relevant to tern migration:
- **North Atlantic Gyre:** circulates clockwise
- **South Atlantic Gyre:** circulates counter-clockwise

## Why northbound is faster
On the northbound (spring) leg, terns can ride prevailing winds along the
gyres' circulation almost like a highway — flying with the wind rather
than against it for large stretches of the journey. This lets them cover
long distances quickly with less relative effort, which is consistent with
the shorter, more front-loaded 36–46 day window observed in the paper.

## Why southbound is slower and more variable
On the southbound (autumn) leg, terns don't have the same continuous
tailwind advantage. In addition, the paper's tracking data shows Greenland
birds taking **two genuinely different coastal route options** heading
south — some travel down the West African coast, others cross toward the
Brazilian coast — rather than one single shared path. More route options,
plus more stopovers (including a well-documented multi-week stopover in
the North Atlantic to refuel), add up to a longer and more individually
variable journey. This is reflected in the wider 69–103 day range compared
to northbound's tighter 36–46 day range.

## Why this matters for this library specifically
This asymmetry is the reasoning behind a testable hypothesis noted in this
project's development history: **northbound tracks should show tighter
(lower) pairwise DTW distances across birds than southbound tracks**,
because northbound converges on a similar wind-driven path while
southbound has genuine route-choice variability baked in. If our DTW
implementation (once built) recovers this known asymmetry from real data,
that's a strong sign the whole pipeline — segmentation and DTW together —
is behaving sensibly, not just producing plausible-looking numbers by
chance.

## A note on scope
This doc summarizes migration biology at a level relevant to using this
library, not a complete oceanographic or ornithological reference. For the
original source data and its exact figures, see `data_provenance.md`.