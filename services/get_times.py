import requests
import streamlit as st

def get_travel_time(origin, destination):
    """Get walking time in minutes between two (lat, lon) points."""
    api_key = st.secrets["ors_api_key"]
    url = "https://api.openrouteservice.org/v2/matrix/foot-walking"
    headers = {"Authorization": api_key, "Content-Type": "application/json"}
    # ORS wants [lon, lat]
    locations = [[origin[1], origin[0]], [destination[1], destination[0]]]
    payload = {
        "locations": locations,
        "sources": [0],
        "destinations": [1],
        "metrics": ["duration"]
    }
    resp = requests.post(url, json=payload, headers=headers, timeout=30)
    resp.raise_for_status()
    data = resp.json()
    seconds = data["durations"][0][0]
    return seconds / 60  # minutes