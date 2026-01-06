import os

def OpenWeatherAPIKey():
    api_key = os.environ["OPENWEATHER_API_KEY"]
    return api_key