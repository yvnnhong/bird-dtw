# Scaling Walkthrough
In our DTW algorithm, we need scaling to cover the many cases where ROWS != COLS. 
We are using DTW because unlike the Euclidean distance, DTW does not require the
two sequences to have the exact same number of data points. 

Here is a concrete example to demonstrate how scaling works. 
Let's say that ROWS, COLS = len(grid), len(grid[0]) = 3, 5.
Assume we are working in a zero-indexed system. 

       0     1     2     3     4
    ┌─────┬─────┬─────┬─────┬─────┐
 0  │     │     │     │     │     │
    ├─────┼─────┼─────┼─────┼─────┤
 1  │     │     │     │     │     │
    ├─────┼─────┼─────┼─────┼─────┤
 2  │     │     │     │     │     │
    └─────┴─────┴─────┴─────┴─────┘

