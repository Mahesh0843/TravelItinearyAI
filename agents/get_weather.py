# agents/get_weather.py
import requests

# def get_forecast(lat, lon, start, end):
#     url = "https://api.open-meteo.com/v1/forecast"
#     params = {
#         "latitude": lat,
#         "longitude": lon,
#         "start_date": start.isoformat(),
#         "end_date": end.isoformat(),
#         "daily": "weathercode,temperature_2m_max",
#         "timezone": "auto"
#     }
#     resp = requests.get(url, params=params, timeout=10)
#     resp.raise_for_status()
#     data = resp.json()
#     daily = data.get("daily", {})
#     if not daily:
#         return []
#     codes = {
#         0: "clear", 1: "clear", 2: "cloudy", 3: "cloudy",
#         45: "fog", 51: "drizzle", 61: "rain", 63: "rain",
#         71: "snow", 80: "rain", 95: "storm"
#     }
#     result = []
#     for i, dt in enumerate(daily["time"]):
#         code = daily["weathercode"][i]
#         cond = codes.get(code, "unknown")
#         result.append({
#             "date": dt,
#             "condition": cond,
#             "temp": daily["temperature_2m_max"][i]
#         })
#     return result


import requests

def get_forecast(lat, lon, start, end):
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "start_date": start.isoformat(),
        "end_date": end.isoformat(),
        "daily": "weathercode,temperature_2m_max",
        "timezone": "auto"
    }
    
    # 1. Wrap the network request in a try-except block to handle SSL/Network drops
    try:
        resp = requests.get(url, params=params, timeout=10)
        resp.raise_for_status()
        data = resp.json()
    except requests.exceptions.RequestException as e:
        # Log the error safely without crashing LangGraph
        print(f"⚠️ Weather API request failed: {e}")
        return [] # Return an empty list so the downstream code doesn't break
        
    daily = data.get("daily", {})
    if not daily:
        return []
        
    codes = {
        0: "clear", 1: "clear", 2: "cloudy", 3: "cloudy",
        45: "fog", 51: "drizzle", 61: "rain", 63: "rain",
        71: "snow", 80: "rain", 95: "storm"
    }
    
    result = []
    for i, dt in enumerate(daily["time"]):
        code = daily["weathercode"][i]
        cond = codes.get(code, "unknown")
        result.append({
            "date": dt,
            "condition": cond,
            "temp": daily["temperature_2m_max"][i]
        })
        
    return result

    
    
    
def get_current(lat, lon):
    url = "https://api.open-meteo.com/v1/forecast"
    params = {"latitude": lat, "longitude": lon, "current_weather": True}
    resp = requests.get(url, params=params, timeout=10)
    resp.raise_for_status()
    data = resp.json()
    curr = data.get("current_weather", {})
    if not curr:
        return {}
    codes = {
        0: "clear", 1: "clear", 2: "cloudy", 3: "cloudy",
        45: "fog", 51: "drizzle", 61: "rain", 63: "rain",
        71: "snow", 80: "rain", 95: "storm"
    }
    code = curr.get("weathercode")
    return {
        "temperature": curr.get("temperature"),
        "condition": codes.get(code, "unknown")
    }