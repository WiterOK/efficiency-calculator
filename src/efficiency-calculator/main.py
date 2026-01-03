from mio import GetMeteodata
import os

api_key = os.environ["OPENWEATHER_API_KEY"]

data = GetMeteodata(67, 67, api_key)