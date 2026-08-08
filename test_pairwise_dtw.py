from itertools import combinations
from bird_dtw.species.arctic_tern.data import fetch_data, load_tracks
from bird_dtw.species.arctic_tern.segmentation.segmentation import segment_track
from bird_dtw.dtw import DTW
from bird_dtw.species.arctic_tern.params import WINDOW_SIZE

"""
key trick: segment each bird once, store it, then just loop through pairs.
"""

BIRD_IDS = ["ARTE_370", "ARTE_371", "ARTE_373", "ARTE_376", "ARTE_390",
            "ARTE_395", "ARTE_406", "ARTE_408", "ARTE_410"]

# Step 1: segment every bird ONCE, store the legs
raw = fetch_data()
tracks = load_tracks(raw)

legs = {}  # legs[bird_id] = {"southbound": [...], "northbound": [...]}
for bird_id in BIRD_IDS:
    phases = segment_track(tracks[bird_id], smooth_days=12, trend_days=12, flat_threshold_frac=0.08)
    south = list(zip(phases["southbound"]["lat"], phases["southbound"]["lon"]))
    north = list(zip(phases["northbound"]["lat"], phases["northbound"]["lon"]))
    legs[bird_id] = {"southbound": south, "northbound": north}

# Step 2: run DTW on every pair, for each leg
def pairwise_distances(leg_name: str) -> dict:
    results = {}
    for bird_a, bird_b in combinations(BIRD_IDS, 2):
        path_a = legs[bird_a][leg_name]
        path_b = legs[bird_b][leg_name]
        if len(path_a) == 0 or len(path_b) == 0:
            continue  # skip birds missing this leg (e.g. ARTE_395 northbound)
        dtw = DTW(path_a, path_b, WINDOW_SIZE)
        distance, _ = dtw.dynamic_time_warping()
        results[(bird_a, bird_b)] = distance
    return results

south_distances = pairwise_distances("southbound")
north_distances = pairwise_distances("northbound")

# Step 3: compare averages (the actual hypothesis test)
avg_south = sum(south_distances.values()) / len(south_distances)
avg_north = sum(north_distances.values()) / len(north_distances)

print(f"Average southbound DTW distance: {avg_south:.2f}")
print(f"Average northbound DTW distance: {avg_north:.2f}")
print(f"Northbound tighter? {avg_north < avg_south}")

def pairwise_avg_per_step(leg_name: str) -> dict:
    results = {}
    for bird_a, bird_b in combinations(BIRD_IDS, 2):
        path_a = legs[bird_a][leg_name]
        path_b = legs[bird_b][leg_name]
        if len(path_a) == 0 or len(path_b) == 0:
            continue
        dtw = DTW(path_a, path_b, WINDOW_SIZE)
        distance, _ = dtw.dynamic_time_warping()
        results[(bird_a, bird_b)] = distance / max(len(path_a), len(path_b))
    return results

south_per_step = pairwise_avg_per_step("southbound")
north_per_step = pairwise_avg_per_step("northbound")

avg_south_step = sum(south_per_step.values()) / len(south_per_step)
avg_north_step = sum(north_per_step.values()) / len(north_per_step)

print(f"Avg per-step southbound: {avg_south_step:.2f} km")
print(f"Avg per-step northbound: {avg_north_step:.2f} km")
print(f"Northbound tighter per-step? {avg_north_step < avg_south_step}")