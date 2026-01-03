import requests
import os

def GetMeteodata(lat, lon, api_key):
    url = (
    "https://api.openweathermap.org/data/3.0/onecall"
    f"?lat={lat}"
    f"&lon={lon}"
    "&exclude=minutely,current,alerts"
    "&units=metric"
    f"&appid={api_key}"
    )

    response = requests.get(url)
    print(f"Status Code: {response.status_code}") # 200 = everything works
    return response
