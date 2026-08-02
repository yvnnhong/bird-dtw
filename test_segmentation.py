from bird_dtw.species.arctic_tern.data import fetch_data, load_tracks
from bird_dtw.species.arctic_tern.segmentation import segment_track

import bird_dtw.species.arctic_tern.segmentation as seg_module
print("Loading segmentation.py from:", seg_module.__file__)

raw = fetch_data()
tracks = load_tracks(raw)

for bird_id, track in tracks.items():
    phases = segment_track(track, smooth_days=12, trend_days=12, flat_threshold_frac=0.08)
    south = phases["southbound"]
    north = phases["northbound"]
    south_len = (south["timestamp"].max() - south["timestamp"].min()).days if len(south) else 0
    north_len = (north["timestamp"].max() - north["timestamp"].min()).days if len(north) else 0
    print(f"{bird_id} -> southbound: {south_len} days, northbound: {north_len} days")

print("\n--- raw data check ---")
for bird_id, track in tracks.items():
    n_fixes = len(track)
    start = track["timestamp"].min()
    end = track["timestamp"].max()
    total_days = (end - start).days
    print(f"{bird_id}: {n_fixes} fixes, {start} to {end} ({total_days} days total)")


print("\n--- detailed check: ARTE_373 and ARTE_410 ---")
for bird_id in ["ARTE_373", "ARTE_410"]:
    track = tracks[bird_id]
    phases = segment_track(track, smooth_days=12, trend_days=12, flat_threshold_frac=0.08)
    south = phases["southbound"]
    winter = phases["wintering"]
    north = phases["northbound"]
    print(f"\n{bird_id}:")
    print(f"  southbound: {south['timestamp'].min()} to {south['timestamp'].max()}" if len(south) else "  southbound: EMPTY")
    print(f"  wintering:  {winter['timestamp'].min()} to {winter['timestamp'].max()}" if len(winter) else "  wintering: EMPTY")
    print(f"  northbound: {north['timestamp'].min()} to {north['timestamp'].max()}" if len(north) else "  northbound: EMPTY")