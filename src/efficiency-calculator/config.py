import os

def OpenWeatherAPIKey():
    api_key = os.environ["OPENWEATHER_API_KEY"]
    return api_key

def CachePath():
    cachepath = "~/efficiency-calculator/src/efficiency-calculator/cache/openweather/"
    return cachepath