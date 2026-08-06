# Common Questions & Answers

A running list of things that were genuinely confusing while building
this project — written down so future-you (or anyone else) doesn't have
to re-figure them out from scratch.

---

**Q: What does `max_total_gap` actually mean? What's a "fake extra-long
migration"?**

Say a bird pauses 3 separate times during otherwise steady southbound
travel — each pause only 5 days long, well under the stopover-length
cap (`max_gap`). `max_gap` alone would let the code bridge over *each*
individual pause, treating the bird as "still migrating" through all
three. But without a *total* cap, the code could chain all three bridged
pauses together into one giant "still migrating" block — even though
15 total days of not-really-moving-with-purpose might represent three
separate, genuine rest events, not one continuous journey. The reported
day-count would still look legitimate (a single unbroken run), but it
would be inflated by summing gaps that shouldn't all count. That's the
"fake extra-long migration" — a plausible-looking number built from
stitched-together pauses. `max_total_gap` caps the sum of bridged gaps in
one run so this can't happen unchecked.

---

**Q: What does "cutoff" mean, in general, and specifically for each
parameter that uses the word?**

**In general:** a cutoff is a line you draw that says "everything on one
side of this line counts as X, everything on the other side doesn't."
It turns a smooth, continuous number (like a distance or a rate) into a
yes/no decision.

**Specifically, for each cutoff used in this project:**
- **`flat_threshold_frac` (a rate-of-change cutoff):** draws the line at
  "X% of the year's fastest rate of change." Below the line = "counts as
  noise, not real movement." Above the line = "counts as actively
  migrating."
- **`near_max_nsd` (a distance cutoff, the wintering threshold):** draws
  the line at "X% of the bird's single farthest distance from home all
  year." Below the line = "not yet at the wintering plateau." Above the
  line = "counts as a wintering candidate."
- **`max_south_days` / `max_south_fixes` (a safety-cap cutoff):** draws a
  hard line at a fixed number of days. Below the line = accepted as-is.
  Above the line = truncated back down, no matter what the underlying
  math said.

In every case here, "cutoff" is doing the same basic job — converting a
continuous, noisy signal into a clean yes/no classification — just
applied to different signals (speed, distance, and duration
respectively).

---

**Q: How was the paper's day-range validation actually done — was it a
rolling average?**

No — it was **not** a rolling average, and it is **not implemented as a
function anywhere in the codebase.** It happened manually: running
`test_segmentation.py` printed each bird's total southbound/northbound
day count to the terminal, and those printed numbers were compared by
eye against the paper's stated range (69–103 days southbound, 36–46 days
northbound). There is currently no `validate()` function, no automated
pass/fail check, and no code file that performs this comparison
programmatically. This is a manual, human-in-the-loop process today —
worth remembering if you ever want to automate it later (e.g. writing a
small script that prints "PASS" or "FAIL — outside paper range" per
bird, per phase).

---

**Q: Isn't it a problem that we didn't implement the original authors'
own stopover-detection method?**

No, and there are two separate things worth untangling here:

1. **No license/citation issue.** A method *described in a paper's text*
   is published scientific knowledge, not code the authors own. Building
   your own implementation of a described method — or choosing a
   different, standard method entirely — and citing the source, is
   completely normal, expected scientific practice.
2. **Not a red flag methodologically, either.** NSD-threshold-based
   migration segmentation (which is what this project does) is itself a
   well-established, widely used approach in movement ecology — it isn't
   an ad-hoc invention. Using a different, standard method than the
   original paper used, while clearly disclosing that choice (see
   `known_limitations.md`), is normal. What *would* be a problem is
   silently claiming to replicate the original authors' exact method
   without disclosing that a different approach was actually used —
   which this project does not do.

---

**Q: Where do the tracked birds actually start? Is it Svalbard?**

**No — Svalbard is not part of this dataset.** This project's birds come
from **Greenland (10 birds) and Iceland (1 bird)** only, per Egevang et
al. 2010 (see `data_provenance.md`). Svalbard is a different Arctic
archipelago (north of Norway) associated with a *different, separate*
tracking study — not this project's data source. If you see Svalbard
mentioned anywhere in searches or secondary sources about Arctic terns,
double-check which study it's actually referring to before assuming it
applies here.

---

**Q: The docs say the code "assumes" migration starts in the north —
isn't that a big thing to just assume? How do we know it's true?**

Fair concern, and worth being precise about. This is an **inference from
how the study was conducted**, not a label present anywhere in the raw
data. Geolocators were physically attached to birds at their breeding
colonies (in Greenland/Iceland, both high-Arctic locations) *before*
southbound migration began. Because of this, the first GPS fix recorded
for each bird should, by construction, be at or near the colony.

This is **not verified point-by-point in the current code** — there's no
check confirming, for example, that each bird's first fix actually has a
high positive latitude. It's a reasonable inference based on experimental
design, but it hasn't been independently double-checked in this codebase.
See `segmentation_process.md` for the full explanation, and consider
adding an automated sanity check (e.g. asserting `home_lat > 60`) as a
future improvement.