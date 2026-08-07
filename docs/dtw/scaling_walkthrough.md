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


