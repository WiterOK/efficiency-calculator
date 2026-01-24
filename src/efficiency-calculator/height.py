import requests

def get_elevation(lat: float, lon: float) -> float:
    """
    Повертає висоту над рівнем моря (м) для заданих координат.
    Використовується api.opentopodata.org (dataset: mapzen)
    """

    url = "https://api.opentopodata.org/v1/mapzen"
    params = {
        "locations": f"{lat},{lon}"
    }

    resp = requests.get(url, params=params, timeout=10)
    resp.raise_for_status()

    data = resp.json()

    if data["status"] != "OK" or not data["results"]:
        raise RuntimeError("Failed to fetch elevation")

    return data["results"][0]["elevation"]
