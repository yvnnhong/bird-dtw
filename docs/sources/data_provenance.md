# Data Provenance

## Source dataset
Arctic tern GPS/geolocator tracking data is fetched live from the
**OBIS-SEAMAP** API by `src/bird_dtw/species/arctic_tern/data.py`.

- **Dataset ID:** `f3316d34-fbbd-4c9a-9c1b-382a1d9877d3`
- **Original source study:** Egevang, C., Stenhouse, I. J., Phillips,
  R. A., Petersen, A., Fox, J. W., & Silk, J. R. D. (2010). *Tracking of
  Arctic terns Sterna paradisaea reveals longest animal migration.*
  Proceedings of the National Academy of Sciences (PNAS).

## Birds included
9 unique birds, identified by `organismID`:
`ARTE_370`, `ARTE_371`, `ARTE_373`, `ARTE_376`, `ARTE_390`, `ARTE_395`,
`ARTE_406`, `ARTE_408`, `ARTE_410`.

All 9 are Greenland-breeding birds. (The original study also tracked one
Iceland-breeding bird, pooled separately in the paper's Table 1; that bird
is not part of this project's 9-bird set.)

## Sampling rate
Approximately 2 GPS fixes per day (`GPS_SAMPLING_INTERVAL_HOURS = 12` in
`params.py`).

## Facts pulled directly from the paper (confirmed by reading the actual
## text, not a secondhand summary)

**Table 1 — migration duration (population averages, Greenland birds
pooled together; no per-bird breakdown exists in the source):**
- Southbound migration: 93 days average, range 69–103 days
- Northbound migration: 40 days average, range 36–46 days

**Figure 1 caption — seasonal windows:**
- Autumn/postbreeding migration (southbound): August–November
- Winter range (wintering): December–March
- Spring/return migration (northbound): April–May

**Methods section — the original authors' own stopover-detection rule:**
latitudinal movement <0.8° over a 0.5-day period, smoothed over 3 days,
counts as a stopover. (Not currently implemented in this codebase — see
`known_limitations.md`.)

## Why there is no per-bird "target" number
Table 1 in the source paper pools all Greenland birds into a single row —
there is no separate, individual row for any specific `organismID` like
`ARTE_370`. This means there is no way to obtain a personalized "correct"
day-count for any individual bird from this source. The 69–103 /
36–46-day ranges are used throughout this project as a plausibility check
against the population as a whole, not as an exact per-bird target. See
`methodology.md` for how this shapes our validation approach.