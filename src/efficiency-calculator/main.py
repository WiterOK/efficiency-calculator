from apifetcher import load_from_cache, save_to_cache, GetMeteodata
from timestamps import NormalizeYear, GenerateUnixTimestamps
import config

LAT = 48.45
LON = 35.02
# hardcoded for now, needs to be in config.py later
YEAR = 2023
API_KEY = config.OpenWeatherAPIKey()

# Try cache first
hourly_data = load_from_cache(LAT, LON, YEAR)

if hourly_data is None:
    print("No cache for those properties; fetching from OpenWeather")

    hourly_data = []
    daily_timestamps = GenerateUnixTimestamps(YEAR)

    for dt in daily_timestamps:
        day_hours = GetMeteodata(LAT, LON, dt, API_KEY)
        hourly_data.extend(day_hours)

    hourly_data = NormalizeYear(hourly_data, YEAR)

    save_to_cache(LAT, LON, YEAR, hourly_data)

else:
    print("Loaded from cache")
    print("Data for this entry can be found at", config.CachePath())
    # print(hourly_data)

print(len(hourly_data))  # needs to be 8760
