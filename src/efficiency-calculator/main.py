from tqdm import tqdm
from apifetcher import load_from_cache, save_to_cache, GetMeteodata
from timestamps import NormalizeYear, GenerateUnixTimestamps
from kwh_calculator import calculate_year_energy
import config

LAT = config.LAT
LON = config.LON
YEAR = config.YEAR
R = config.R
API_KEY = config.OpenWeatherAPIKey()

# Try cache first
hourly_data = load_from_cache(LAT, LON, YEAR)

if hourly_data is None:
    print("No cache for those properties; fetching from OpenWeather")

    hourly_data = []
    daily_timestamps = GenerateUnixTimestamps(YEAR)

    for dt in tqdm(daily_timestamps, desc="Fetching OpenWeather data"):
        day_hours = GetMeteodata(LAT, LON, dt, API_KEY)
        hourly_data.extend(day_hours)  

    hourly_data = NormalizeYear(hourly_data, YEAR)

    save_to_cache(LAT, LON, YEAR, hourly_data)

else:
    print("Loaded from cache")
    print("Data for this entry can be found at", config.CachePath())
    # print(hourly_data)

year_energy = calculate_year_energy(hourly_data, R)

print(len(hourly_data))
print(year_energy)  # needs to be 8760