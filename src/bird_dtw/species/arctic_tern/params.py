# arctic_tern/params.py

MIGRATION_SPEEDS = {
    "northbound_km_per_day": 520,  # Egevang et al. 2010, Table 2
    "northbound_range": (390, 670),
    "southbound_km_per_day": 330,  # Egevang et al. 2010, Table 2
    "southbound_range": (280, 390),
    "antarctica_zone_km_per_day": 63,  # molt/foraging phase
}

STOPOVER_DURATION_DAYS = {
    "north_atlantic": 24.6,  # Egevang et al. 2010, Table 1
    "north_atlantic_range": (10, 30),
}

GPS_SAMPLING_INTERVAL_HOURS = 12  # 2 fixes per day, Egevang et al. 2010

# Window constraint for DTW based on route variation
# Alerstam et al. 2019: Baltic terns ranged 89-207°E
WINDOW_SIZE = 4  # Allow ~4 GPS pings of drift