import requests
from timestamps import NormalizeYear
import config

# for caching
import json
from pathlib import Path

CACHE_DIR = config.CachePath()
CACHE_DIR.mkdir(parents=True, exist_ok=True)

def _cache_path(lat, lon, year):
    return CACHE_DIR / f"{lat:.4f}_{lon:.4f}_{year}.json"

def load_from_cache(lat, lon, year):
    path = _cache_path(lat, lon, year)
    if path.exists():
        with open(path, "r") as f:
            return json.load(f)
    return None

def save_to_cache(lat, lon, year, data):
    path = _cache_path(lat, lon, year)
    with open(path, "w") as f:
        json.dump(data, f)
# end caching

def GetMeteodata(lat, lon, dt, api_key):
    hourly_data = []

    url = BuildUrl(lat, lon, dt, api_key)
    response = requests.get(url)
    response.raise_for_status()

    data = response.json()

    # ВИПРАВЛЕННЯ: timemachine API повертає "data", а не "hourly"
    for hour in data.get("data", []):
        hourly_data.append({
            "ts": hour["dt"],
            "wind_speed": hour["wind_speed"],
            "wind_gust": hour.get("wind_gust")
        })

    return hourly_data


def BuildUrl(lat, lon, dt, api_key):
    return (
        "https://api.openweathermap.org/data/3.0/onecall/timemachine"
        f"?lat={lat}"
        f"&lon={lon}"
        f"&dt={dt}"
        "&units=metric"
        f"&appid={api_key}"
    )
