from bird_dtw.species.arctic_tern.data import fetch_data, load_tracks

df = fetch_data()
tracks = load_tracks(df)

print(f"Loaded {len(tracks)} tracks")
for track_id, track_df in tracks.items():
    print(f"{track_id}: {len(track_df)} fixes, "
          f"from {track_df['timestamp'].min()} to {track_df['timestamp'].max()}")
    print(track_df.head(2))
    print()