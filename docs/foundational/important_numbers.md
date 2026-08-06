# Important Numbers & Cold Hard Facts

A quick-reference list of the key numbers and facts in this project — no
explanations of *how* things work here (see `glossary.md`,
`algorithm_overview.md`, and `segmentation_process.md` for that). This
doc is just the numbers and facts themselves, for fast lookup.

---

## Final chosen parameter values (segmentation.py)

| Parameter | Final value | What it controls |
|---|---|---|
| `smooth_days` | 12 | Size of the NSD smoothing window, in days |
| `trend_days` | 12 | How far back "now vs. then" comparisons look, in days |
| `flat_threshold_frac` | 0.08 | Rate-of-change cutoff (fraction of year's max rate) |
| Wintering NSD cutoff | 0.85 × max NSD | Distance-from-home cutoff for detecting wintering |
| `max_south_days` | 110 | Hard safety cap on southbound run length, in days |

---

## Paper's published migration numbers (Egevang et al. 2010, Table 1)

| Phase | Average duration | Range |
|---|---|---|
| Southbound migration | 93 days | 69–103 days |
| Northbound migration | 40 days | 36–46 days |

- These are **population averages across 10 Greenland birds**, pooled
  into a single row. There is no per-bird breakdown in the source table.
- Northbound average distance: **24,270 km** (range 20,070–27,790 km),
  at an average of **520 km/day**.
- No specific southbound average distance figure was found in the
  sources checked so far — only a qualitative statement that southbound
  "involved greater distances" than northbound.

---

## Paper's published seasonal windows (Figure 1 caption)

| Phase | Months |
|---|---|
| Southbound (autumn/postbreeding) migration | August–November |
| Wintering | December–March |
| Northbound (spring/return) migration | April–May |

---

## Where the tracked birds actually come from

- **10 birds from Greenland, 1 bird from Iceland.** (11 total in the
  original study; this project uses the 9 Greenland birds with usable
  data — see below.)
- **Not Svalbard.** Svalbard belongs to a different, unrelated tracking
  study — see `common_q_and_a.md`.
- Breeding colonies are in the high Arctic — this is the basis for
  treating each bird's first GPS fix as "home" / north. See
  `segmentation_process.md` for how this inference works and its
  limitations.

---

## This project's 9 birds

`ARTE_370`, `ARTE_371`, `ARTE_373`, `ARTE_376`, `ARTE_390`, `ARTE_395`,
`ARTE_406`, `ARTE_408`, `ARTE_410`

- **ARTE_395** has no usable northbound data (tracking record ends in
  Nov 2007) — expected, not a bug.
- **ARTE_370** never reached the paper's southbound minimum (69 days) at
  any tested parameter value — open issue, see `known_limitations.md`.

---

## Original authors' own stopover-detection rule (not currently used
## in this codebase — see `known_limitations.md`)

Latitudinal movement **<0.8°** over a **0.5-day period**, smoothed over
**3 days**, counts as a stopover.

---

## Sampling rate

Approximately **2 GPS fixes per day** (`GPS_SAMPLING_INTERVAL_HOURS = 12`
in `params.py`).

---

## Ocean gyre facts (see `north_vs_south.md` for full explanation)

- Two Atlantic gyres are relevant: the **North Atlantic Gyre** (clockwise)
  and the **South Atlantic Gyre** (counter-clockwise).
- Southbound birds take **one of two coastal routes**: West African coast
  or Brazilian coast.
- Northbound birds follow a **single, more direct, sigmoidal (S-shaped)
  open-ocean path** through the central Atlantic — not a coastal route.
- It is **southbound**, not northbound, that hugs coastlines. (This is
  worth remembering — the intuitive-sounding version of this fact is
  easy to get backwards.)