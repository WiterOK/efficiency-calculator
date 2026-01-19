import os
from pathlib import Path

LAT = 48.45
LON = 35.02
R = 40  # радіус ротора, м

YEAR = 2025

def OpenWeatherAPIKey():
    api_key = os.environ["OPENWEATHER_API_KEY"]
    return api_key

def CachePath():
    return Path(__file__).resolve().parent / "cache" / "openweather"