import requests

def get_coords(address):
    """Turn an address into (lat, lon)."""
    url = "https://nominatim.openstreetmap.org/search"
    params = {"q": address, "format": "json", "limit": 1}
    headers = {"User-Agent": "TravelPlanner/1.0"}
    resp = requests.get(url, params=params, headers=headers, timeout=10)
    resp.raise_for_status()
    data = resp.json()
    if not data:
        raise ValueError(f"Address not found: {address}")
    lat = float(data[0]["lat"])
    lon = float(data[0]["lon"])
    return lat, lon