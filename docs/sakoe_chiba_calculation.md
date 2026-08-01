# Sakoe-Chiba Band Constraint - Explanation & Examples

## What is the Band Constraint?

The Sakoe-Chiba band constraint limits which cells in the DP grid can be filled during DTW calculation. It ensures that the individual path and template path stay roughly in sync during alignment.

Note: every (lat, lon) point represents a GPS ping for a single bird's location at a given time on a given date, so this method relies on a predictable frequency of bird GPS pings. 

**Constraint Formula:** `|r - c| <= window`

Where:
- **r** = row index = **individual path (A)**
- **c** = column index = **template path (B)**
- **window** = the band width (how far apart the indices can be)

---

## Understanding the Formula

The expression `|r - c|` measures **how far out of sync** the two sequences are at any given cell:

- If `|r - c|` is small → the two sequences are progressing at similar rates
- If `|r - c|` is large → one sequence has moved ahead of the other by a lot
- The `window` parameter sets the maximum allowed "drift" between sequences

If `|r - c| > window`, that cell is **outside the band** and should **not be filled** (leave it as `inf`).

---

## Example: Window = 2

Given:
- Individual path (A): 3 points → rows 0, 1, 2
- Template path (B): 3 points → columns 0, 1, 2
- Window: 2

### Which cells get filled?

Check each cell against the constraint `|r - c| <= 2`:

| Cell | r | c | \|r - c\| | <= 2? | Fill? |
|------|---|---|-----------|-------|-------|
| dp[0][0] | 0 | 0 | 0 | YES | YES |
| dp[0][1] | 0 | 1 | 1 | YES | YES |
| dp[0][2] | 0 | 2 | 2 | YES | YES |
| dp[0][3] | 0 | 3 | 3 | NO | NO |
| dp[1][0] | 1 | 0 | 1 | YES | YES |
| dp[1][1] | 1 | 1 | 0 | YES | YES |
| dp[1][2] | 1 | 2 | 1 | YES | YES |
| dp[1][3] | 1 | 3 | 2 | YES | YES |
| dp[2][0] | 2 | 0 | 2 | YES | YES |
| dp[2][1] | 2 | 1 | 1 | YES | YES |
| dp[2][2] | 2 | 2 | 0 | YES | YES |
| dp[2][3] | 2 | 3 | 1 | YES | YES |
| dp[3][0] | 3 | 0 | 3 | NO | NO |
| dp[3][1] | 3 | 1 | 2 | YES | YES |
| dp[3][2] | 3 | 2 | 1 | YES | YES |
| dp[3][3] | 3 | 3 | 0 | YES | YES |

### Visual Band Pattern

With window = 2, the filled cells form a diagonal band around the main diagonal:

```
    c0  c1  c2  c3
r0  X   X   X   -
r1  X   X   X   X
r2  X   X   X   X
r3  -   X   X   X
```

(X = filled, - = not filled)

Notice how cells become inaccessible when r and c drift too far apart.

---

## Why This Matters

1. **Prevents bad alignments**: Forces sequences to stay reasonably aligned (not comparing point 0 of A with point 100 of B)
2. **Improves computational efficiency**: Skips irrelevant cells, reducing computation time
3. **Improves results**: In practice, good DTW alignments don't stray far from the diagonal anyway

---

## Real Example from DTW Walkthrough

From the given walkthrough with window = 2:

### Checking dp[1][2]:
```
r = 1 (individual path index)
c = 2 (template path index)
|1 - 2| = |-1| = 1
1 <= 2? YES 
-> This cell gets filled
```

### If we had dp[0][3] (hypothetically):
```
r = 0 (individual path index)
c = 3 (template path index)
|0 - 3| = |-3| = 3
3 <= 2? NO 
-> This cell stays as inf (not filled)
```

---

## Key Takeaway

Always remember:
- **r** moves down (individual sequence progresses)
- **c** moves right (template sequence progresses)
- The band constraint `|r - c| <= window` prevents them from drifting too far apart during alignment