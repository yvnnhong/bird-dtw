# Scaling Walkthrough
In our DTW algorithm, we need scaling to cover the many cases where ROWS != COLS. 
We are using DTW because unlike the Euclidean distance, DTW does not require the
two sequences to have the exact same number of data points. 

Here is a concrete example to demonstrate how scaling works. 
Let's say that ROWS, COLS = len(grid), len(grid[0]) = 3, 5.
Assume we are working in a zero-indexed system. 

        col0  col1  col2  col3  col4
      +------+------+------+------+------+
row0  |      |      |      |      |      |
      +------+------+------+------+------+
row1  |      |      |      |      |      |
      +------+------+------+------+------+
row2  |      |      |      |      |      |
      +------+------+------+------+------+