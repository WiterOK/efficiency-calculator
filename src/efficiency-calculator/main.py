from apifetcher import load_from_cache, save_to_cache, GetMeteodata
from timestamps import NormalizeYear, GenerateUnixTimestamps

LAT = 48.45
LON = 35.02
YEAR = 2022
API_KEY = "YOUR_API_KEY"

# 1️⃣ Try cache
hourly_data = load_from_cache(LAT, LON, YEAR)

if hourly_data is None:
    print("Cache miss → fetching from OpenWeather")

    hourly_data = []
    daily_timestamps = GenerateUnixTimestamps(YEAR)

    for dt in daily_timestamps:
        day_hours = GetMeteodata(LAT, LON, dt, API_KEY)
        hourly_data.extend(day_hours)

    hourly_data = NormalizeYear(hourly_data, YEAR)

    save_to_cache(LAT, LON, YEAR, hourly_data)

else:
    print("Loaded from cache")

print(len(hourly_data))  # always 8760
