import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from timestamps import NormalizeYear
import config

# for caching
import json
from pathlib import Path

CACHE_DIR = config.CachePath()
CACHE_DIR.mkdir(parents=True, exist_ok=True)

# Reuse connections + retry transient failures to avoid hanging the PHP request.
_RETRY = Retry(
    total=3,
    connect=3,
    read=3,
    status=3,
    backoff_factor=0.5,
    status_forcelist=(429, 500, 502, 503, 504),
    allowed_methods=("GET",),
    raise_on_status=False,
)

_SESSION = requests.Session()
_SESSION.mount("https://", HTTPAdapter(max_retries=_RETRY))
_SESSION.mount("http://", HTTPAdapter(max_retries=_RETRY))

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
    response = _SESSION.get(url, timeout=10)
    # If we got a non-2xx response, surface a helpful error.
    if not response.ok:
        raise RuntimeError(
            f"OpenWeather request failed ({response.status_code}): {response.text[:200]}"
        )

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
