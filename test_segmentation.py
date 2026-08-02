from bird_dtw.species.arctic_tern.data import fetch_data, load_tracks
from bird_dtw.species.arctic_tern.segmentation import segment_track

raw = fetch_data()
tracks = load_tracks(raw)
track = tracks['ARTE_370']

for smooth_days, trend_days in [(5, 5), (7, 7), (10, 10), (5, 10), (10, 5)]:
    phases = segment_track(track, smooth_days=smooth_days, trend_days=trend_days)
    south = phases["southbound"]
    north = phases["northbound"]
    south_len = (south["timestamp"].max() - south["timestamp"].min()).days if len(south) else 0
    north_len = (north["timestamp"].max() - north["timestamp"].min()).days if len(north) else 0
    print(f"smooth={smooth_days}, trend={trend_days} -> southbound: {south_len} days, northbound: {north_len} days")