# DTW WALKTHROUGH - COMPLETE AND CORRECT

**NOTE:** A IS UP AND DOWN (rows). TEMPLATE IS LEFT TO RIGHT (COLS)

## Given:
- Individual path (A): [(0,1), (2,2), (3,3)]
- Template path (B): [(0,0), (1,1), (2,2)]
- Window (W): 2

---

## STEP 1: INITIALIZE DP GRID

Create 3x3 grid, all inf except dp[0][0]:

```
dp[0][0] = euclidean_distance((0,1), (0,0)) + 0
         = sqrt((0-0)^2 + (1-0)^2)
         = sqrt(0 + 1)
         = sqrt(1)
         = 1.0
```

|          | B0(0,0) | B1(1,1) | B2(2,2) |
|----------|---------|---------|---------|
| A0(0,1)  | 1.0     | inf     | inf     |
| A1(2,2)  | inf     | inf     | inf     |
| A2(3,3)  | inf     | inf     | inf     |

---

## STEP 2: FILL FIRST ROW (row 0)

**Formula:** `dp[0][c] = euclidean_distance(A0, Bc) + dp[0][c-1]`

**Constraint:** only fill if c <= window (c <= 2)

### dp[0][1]:
```
- local_cost = sqrt((0-1)^2 + (1-1)^2) = sqrt(1 + 0) = sqrt(1) = 1.0
- previous = dp[0][0] = 1.0
- dp[0][1] = 1.0 + 1.0 = 2.0
```

### dp[0][2]:
```
- local_cost = sqrt((0-2)^2 + (1-2)^2) = sqrt(4 + 1) = sqrt(5) = 2.236
- previous = dp[0][1] = 2.0
- dp[0][2] = 2.236 + 2.0 = 4.236
```

|          | B0(0,0) | B1(1,1) | B2(2,2) |
|----------|---------|---------|---------|
| A0(0,1)  | 1.0     | 2.0     | 4.236   |
| A1(2,2)  | inf     | inf     | inf     |
| A2(3,3)  | inf     | inf     | inf     |

---

## STEP 3: FILL FIRST COLUMN (col 0)

**Formula:** `dp[r][0] = euclidean_distance(Ar, B0) + dp[r-1][0]`

**Constraint:** only fill if r <= window (r <= 2)

### dp[1][0]:
```
- Check: is 1 <= 2? YES
- local_cost = sqrt((2-0)^2 + (2-0)^2) = sqrt(4 + 4) = sqrt(8) = 2.828
- previous = dp[0][0] = 1.0
- dp[1][0] = 2.828 + 1.0 = 3.828
```

### dp[2][0]:
```
- Check: is 2 <= 2? YES
- local_cost = sqrt((3-0)^2 + (3-0)^2) = sqrt(9 + 9) = sqrt(18) = 4.243
- previous = dp[1][0] = 3.828
- dp[2][0] = 4.243 + 3.828 = 8.071
```

|          | B0(0,0) | B1(1,1) | B2(2,2) |
|----------|---------|---------|---------|
| A0(0,1)  | 1.0     | 2.0     | 4.236   |
| A1(2,2)  | 3.828   | inf     | inf     |
| A2(3,3)  | 8.071   | inf     | inf     |

---

## STEP 4: FILL INTERIOR CELLS

**Formula:** `dp[r][c] = euclidean_distance(Ar, Bc) + min(dp[r-1][c], dp[r][c-1], dp[r-1][c-1])`

**Constraint:** only fill if |r - c| <= window

---

### dp[1][1]:
```
- Check band: |1 - 1| = 0 <= 2? YES
- local_cost = sqrt((2-1)^2 + (2-1)^2) = sqrt(1 + 1) = sqrt(2) = 1.414
- neighbors:
    * dp[0][1] (up) = 2.0
    * dp[1][0] (left) = 3.828
    * dp[0][0] (diagonal) = 1.0
- min_neighbor = min(2.0, 3.828, 1.0) = 1.0
- dp[1][1] = 1.414 + 1.0 = 2.414
```

---

### dp[1][2]:
```
- Check band: |1 - 2| = 1 <= 2? YES
- local_cost = sqrt((2-2)^2 + (2-2)^2) = sqrt(0 + 0) = sqrt(0) = 0.0
- neighbors:
    * dp[0][2] (up) = 4.236
    * dp[1][1] (left) = 2.414
    * dp[0][1] (diagonal) = 2.0
- min_neighbor = min(4.236, 2.414, 2.0) = 2.0
- dp[1][2] = 0.0 + 2.0 = 2.0
```

|          | B0(0,0) | B1(1,1) | B2(2,2) |
|----------|---------|---------|---------|
| A0(0,1)  | 1.0     | 2.0     | 4.236   |
| A1(2,2)  | 3.828   | 2.414   | 2.0     |
| A2(3,3)  | 8.071   | inf     | inf     |

---

### dp[2][1]:
```
- Check band: |2 - 1| = 1 <= 2? YES
- local_cost = sqrt((3-1)^2 + (3-1)^2) = sqrt(4 + 4) = sqrt(8) = 2.828
- neighbors:
    * dp[1][1] (up) = 2.414
    * dp[2][0] (left) = 8.071
    * dp[1][0] (diagonal) = 3.828
- min_neighbor = min(2.414, 8.071, 3.828) = 2.414
- dp[2][1] = 2.828 + 2.414 = 5.242
```

---

### dp[2][2]:
```
- Check band: |2 - 2| = 0 <= 2? YES
- local_cost = sqrt((3-2)^2 + (3-2)^2) = sqrt(1 + 1) = sqrt(2) = 1.414
- neighbors:
    * dp[1][2] (up) = 2.0
    * dp[2][1] (left) = 5.242
    * dp[1][1] (diagonal) = 2.414
- min_neighbor = min(2.0, 5.242, 2.414) = 2.0
- dp[2][2] = 1.414 + 2.0 = 3.414
```

---

## FINAL DP GRID

|          | B0(0,0) | B1(1,1) | B2(2,2) |
|----------|---------|---------|---------|
| A0(0,1)  | 1.0     | 2.0     | 4.236   |
| A1(2,2)  | 3.828   | 2.414   | 2.0     |
| A2(3,3)  | 8.071   | 5.242   | 3.414   |

---

## RESULT

**Total DTW Distance = dp[2][2] = 3.414**

This represents the minimum cumulative cost to align the individual path to the template path, respecting the Sakoe-Chiba band constraint (window=2).