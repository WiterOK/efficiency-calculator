from tqdm import tqdm
import apifetcher
import height
from timestamps import GenerateUnixTimestamps, NormalizeYear

class WeatherService:
    def __init__(self, lat, lon, api_key):
        self.lat = lat
        self.lon = lon
        self.api_key = api_key

    def get_elevation(self):
        return height.get_elevation(self.lat, self.lon)

    def get_yearly_weather(self, year):
        data = apifetcher.load_from_cache(self.lat, self.lon, year)
        if data: return data

        data = []
        for dt in tqdm(GenerateUnixTimestamps(year), desc="API Data"):
            data.extend(apifetcher.GetMeteodata(self.lat, self.lon, dt, self.api_key))
        
        data = NormalizeYear(data, year)
        apifetcher.save_to_cache(self.lat, self.lon, year, data)
        return data