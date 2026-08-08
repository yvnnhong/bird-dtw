# Formulas Used in the Arctic Tern DTW (Dynamic Time Warping) Implementation

**Computing the ideal column value, given some r**: `expected_c = r * (COLS / ROWS)`

**Testing if c in (r, c) lies within the Sakoe-Chiba band**: `abs(c - expected_c) > window`