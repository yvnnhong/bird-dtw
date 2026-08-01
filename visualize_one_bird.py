"""
Step 1: Just LOOK at one bird's year. No math yet -- pure visual intuition.

This plots ARTE_370's full track, colored from purple (start, August)
to yellow (end, May), so you can literally watch the bird move across
the screen just by looking at the color gradient.
"""
import matplotlib
matplotlib.use("Agg")  # tells matplotlib: just save to a file, don't try to open a window

import matplotlib.pyplot as plt
from bird_dtw.species.arctic_tern.data import fetch_data, load_tracks

df = fetch_data()
tracks = load_tracks(df)

bird_id = "ARTE_370"
track = tracks[bird_id]

fig, ax = plt.subplots(figsize=(10, 8))

# Color each point by how far along in time it is (0 = start, 1 = end)
time_progress = (track["timestamp"] - track["timestamp"].min()) / (
    track["timestamp"].max() - track["timestamp"].min()
)

scatter = ax.scatter(
    track["lon"], track["lat"],
    c=time_progress, cmap="viridis", s=15
)
ax.plot(track["lon"], track["lat"], color="gray", alpha=0.3, linewidth=0.5)

ax.set_xlabel("Longitude")
ax.set_ylabel("Latitude")
ax.set_title(f"{bird_id}'s full year -- purple=August, yellow=May")

cbar = plt.colorbar(scatter, ax=ax)
cbar.set_label("Time progress through the year")

plt.savefig("bird_track.png", dpi=150, bbox_inches="tight")
print("Saved plot to bird_track.png -- open it and look!")