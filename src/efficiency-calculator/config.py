import os

LAT = 48.45
LON = 35.02
R = 40  # радіус ротора, м

YEAR = 2023

def OpenWeatherAPIKey():
    api_key = os.environ["OPENWEATHER_API_KEY"]
    return api_key

def CachePath():
    cachepath = "~/efficiency-calculator/src/efficiency-calculator/cache/openweather/"
    return cachepath