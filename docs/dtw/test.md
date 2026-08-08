# Scaling Walkthrough
In our DTW algorithm, we need scaling to cover the many cases where ROWS != COLS. 
We are using DTW because unlike the Euclidean distance, DTW does not require the
two sequences to have the exact same number of data points. 

Here is a concrete example to demonstrate how scaling works. 
Let's say that ROWS, COLS = len(grid), len(grid[0]) = 3, 5.
Assume we are working in a zero-indexed system. 

|     | 0 | 1 | 2 | 3 | 4 |
|-----|---|---|---|---|---|
| 0   |   |   |   |   |   |
| 1   |   |   |   |   |   |
| 2   |   |   |   |   |   |

Our example: given a zero-indexed 3x5 grid, if we're at row 1, then we can use the following formula to figure out what the appropriate c value is at r=1: 

expected_c = r * (COLS / ROWS)

Then, we use the following formula to see if it lies within the Sakoe-Chiba band: 
abs(c - expected_c) > window

Anything strictly greater than window is marked as an unusable cell in our path.

The result that we get is: 
expected_c = r * (COLS / ROWS)
expected_c = 1 * (5/3) = 1.67

Next, we perform the band check. Since we are going from top row to bottom row, left to right, c is the loop variable that ranges over 0,1,2,3,4 (each column in row r=1). In other words: c is not one fixed value. For this example, expected_c=1.67 stays fixed, and c gets checked against it separately at c=0, c=1, c=2, c=3, c=4.

Here are the results of each of these c-values. (keep in mind that we set r=1). Let's say that window=2 for simplicity: 

`for c=0: abs(0-1.67) = 1.67 (qualifies)` -> this corresponds to the point (1, 0) which is a valid option in our path 

`for c=1: abs(1-1.67) = 1.67 (qualifies)` -> this corresponds to the point (1, 1) which is a valid option in our path 

`for c=2: abs(2-1.67) = 0.33 (qualifies)` -> this corresponds to the point (1, 2) which is a valid option in our path 

`for c=3: abs(3-1.67) = 1.33 (qualifies)` -> this corresponds to the point (1, 3) which is a valid option in our path 

`for c=4: abs()`

[finish this later]

Note that the window is symmetric (+/- in either direction), but the abs() essentially renders it as positive.

The general idea: The goal: For each cell (r, c) in the grid, we need to decide: is this cell "close enough to the diagonal" to bother calculating? Or is it too far off, so we skip it?

