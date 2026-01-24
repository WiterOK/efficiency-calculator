import os
from pathlib import Path
from models import WindTurbine, TurbineType

LAT = 46.8483
LON = 31.0821
YEAR = 2023
ALPHA = 0.20

def OpenWeatherAPIKey():
    return os.environ.get("OPENWEATHER_API_KEY", "")

def CachePath():
    return Path(__file__).resolve().parent / "cache" / "openweather"

WITEROK = WindTurbine(
    name="WITeRoK",
    type=TurbineType.VAWT,
    height=2.5,
    width=1.0,
    hub_height=2.5,
    cp=0.3,
    nominal_speed=15.0,
    cut_in=2.0,
    cut_out=25.0
)

STANDARD_HAWT = WindTurbine(
    name="Industrial HAWT",
    type=TurbineType.HAWT,
    radius=81.0,         
    hub_height=125.0,    
    cp=0.45,              
    nominal_speed=11.0,    
    cut_in=3.0,             
    cut_out=25.0            
)