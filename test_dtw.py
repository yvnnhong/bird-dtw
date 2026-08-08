from bird_dtw.species.arctic_tern.data import fetch_data, load_tracks
from bird_dtw.species.arctic_tern.segmentation.segmentation import segment_track
from bird_dtw.dtw import DTW
from bird_dtw.species.arctic_tern.params import WINDOW_SIZE

raw = fetch_data()
tracks = load_tracks(raw)

bird_a_id = "ARTE_371"
bird_b_id = "ARTE_373"

phases_a = segment_track(tracks[bird_a_id], smooth_days=12, trend_days=12, flat_threshold_frac=0.08)
phases_b = segment_track(tracks[bird_b_id], smooth_days=12, trend_days=12, flat_threshold_frac=0.08)

south_a = phases_a["southbound"]
south_b = phases_b["southbound"]

# DTW class expects list[tuple[float, float]], not a DataFrame
"""
Why zip(south_a["lat"], south_a["lon"]): the DTW class expects list[tuple[float, float]]. 
segment_track() returns a DataFrame. zip pairs up the lat column and lon column row-by-row 
into tuples — that converts DataFrame → the exact list-of-tuples shape DTW needs.
"""
path_a = list(zip(south_a["lat"], south_a["lon"]))
path_b = list(zip(south_b["lat"], south_b["lon"]))

print(f"{bird_a_id} southbound: {len(path_a)} fixes")
print(f"{bird_b_id} southbound: {len(path_b)} fixes")

dtw = DTW(path_a, path_b, WINDOW_SIZE)
distance, matrix = dtw.dynamic_time_warping()

dtw_same = DTW(path_a, path_a, WINDOW_SIZE)
dist2, mat2 = dtw_same.dynamic_time_warping()

print(f"\nDTW distance: {distance}")
print(f"\nDTW distane of path A against itself: {dist2}")

avg_per_step = distance / max(len(path_a), len(path_b))
print(f"\nAverage per-step distance: {avg_per_step:.2f} km")