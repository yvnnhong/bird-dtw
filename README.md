# Bird DTW

Dynamic Time Warping for analyzing migratory bird flight paths.

## What is this?

Compare individual bird migration routes against template paths using Dynamic Time Warping (DTW). Useful for studying behavioral patterns in species like arctic terns and bar-tailed godwits.

## Installation

```bash
pip install git+https://github.com/yvnnhong/bird-dtw.git
```

## Quick Start

```python
from bird_dtw import DTW

# Define paths as (latitude, longitude) tuples
individual_path = [(0, 1), (2, 2), (3, 3)]
template_path = [(0, 0), (1, 1), (2, 2)]

# Create DTW instance with window size
dtw = DTW(individual_path, template_path, window=2)
distance, dp_matrix = dtw.dynamic_time_warping()

print(f"DTW Distance: {distance}")

# Get the optimal alignment path
path = dtw.backtrack()
print(f"Alignment path: {path}")
```

## How It Works

This library uses the Sakoe-Chiba band constraint to efficiently align bird migration paths. The window parameter controls how much temporal flexibility is allowed.

See [DTW Walkthrough](./docs/dtw_walkthrough.md) for a detailed explanation with an example.

## Testing

```bash
python tests/test_dtw.py
```

## Contributing

Contributions welcome! Feel free to add species-specific implementations or improvements.

## License

MIT