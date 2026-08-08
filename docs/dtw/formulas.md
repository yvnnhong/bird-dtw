# Formulas Used in the Arctic Tern DTW (Dynamic Time Warping) Implementation

**Computing the ideal column value, given some r**: `expected_c = r * (COLS / ROWS)`

**Testing if c in (r, c) lies within the Sakoe-Chiba band**: `abs(c - expected_c) > window`

## Haversine Formula

Calculates great-circle distance between two lat/lon points on a sphere (Earth), in km.

a = sin²(Δlat/2) + cos(lat1) * cos(lat2) * sin²(Δlon/2)
c = 2 * atan2(√a, √(1-a))
distance = R * c

Where:
- Δlat = lat2 - lat1 (radians)
- Δlon = lon2 - lon1 (radians)
- R = Earth's radius = 6371 km
- lat1, lon1, lat2, lon2 must be converted from degrees to radians first