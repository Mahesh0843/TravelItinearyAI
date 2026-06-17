from graph.state import TripData
from agents.get_prefs import parse_inputs
from agents.get_places import get_pois
from agents.order import order_activities as build_route_plan
from agents.add_maps import add_maps as enrich_maps
from agents.write_plan import write_plan as generate_plan_text
from agents.get_weather import get_forecast, get_current
# from agents.get_rentals import get_rentals as fetch_rentals_data
from services.geocode import get_coords as geocode_address
from datetime import date

def parse_inputs(state: TripData):
    days = (state["end"] - state["start"]).days + 1
    return {"days": days}

def get_places(state: TripData):
    pois = get_pois(state["city"], state["likes"])
    return {"places": pois}

def get_coords(state: TripData):
    lat, lon = geocode_address(state["start_loc"])
    return {"home_coords": [lat, lon]}

def get_weather(state: TripData):
    if not state["switches"].get("weather_on", False):
        return {"forecast": None, "today_weather": None}
    lat, lon = state.get("home_coords", [0,0])
    if state.get("is_update", False):
        now = get_current(lat, lon)
        bad = ["rain", "storm", "snow"]
        bad_weather = now.get("condition", "").lower() in bad
        return {"today_weather": now, "bad_weather": bad_weather}
    else:
        fc = get_forecast(lat, lon, state["start"], state["end"])
        return {"forecast": fc}

def order_activities(state: TripData):
    plan =build_route_plan(
        home=state["home_coords"],
        pois=state["places"],
        days=state["days"],
        forecast=state.get("forecast")
    )
    return {"plan": plan}

def add_maps(state: TripData):
    if state.get("plan"):
        enriched = enrich_maps(state["plan"])
        return {"plan": enriched}
    return {}

# def get_rentals(state: TripData):
#     if state["switches"].get("rent_on", False):
#         rent =fetch_rentals_data(state["hotel"])
#         return {"rentals": rent}
#     return {"rentals": None}

def write_plan(state: TripData):
    text = generate_plan_text(
        city=state["city"],
        start=state["start"],
        end=state["end"],
        travelers=state["travelers"],
        start_loc=state["start_loc"],
        likes=state["likes"],
        places=state["places"],
        plan=state.get("plan"),
        forecast=state.get("forecast"),
        budget=state.get("budget","medium")
    )
    return {"output_text": text}

def fix_plan(state: TripData):
    plan = state.get("plan")
    now = state.get("today_weather")
    if not plan or not now:
        return {"warning": "No data to fix"}
    today = date.today().isoformat()
    idx = None
    for i, day in enumerate(plan):
        if day["date"] == today:
            idx = i
            break
    if idx is None:
        return {"warning": "No activities today"}
    bad = ["rain", "storm", "snow"]
    if now.get("condition", "").lower() not in bad:
        return {"warning": None}
    
    # find outdoor activities
    acts = plan[idx]["activities"]
    outdoor = ["park", "garden", "hiking", "beach", "shrine"]
    to_replace = [i for i, a in enumerate(acts) if any(k in a["name"].lower() for k in outdoor)]
    if not to_replace:
        return {"warning": None}
    
    # get alternatives
    new = get_pois(state["city"], state["likes"])
    used = {a["name"] for day in plan for a in day["activities"]}
    alt = [p for p in new if p["name"] not in used][:len(to_replace)]
    if not alt:
        return {"warning": "No alternatives found"}
    
    for j, a in enumerate(alt):
        acts[to_replace[j]] = {
            "name": a["name"],
            "time": acts[to_replace[j]]["time"],
            "coords": [a["lat"], a["lon"]],
            "map_url": f"https://www.openstreetmap.org/?mlat={a['lat']}&mlon={a['lon']}",
            "notes": "Indoor alternative due to weather"
        }
    plan[idx]["activities"] = acts
    warn = f"Weather: {now['condition']}. Swapped outdoor activities."
    return {"plan": plan, "warning": warn}

def send_alert(state: TripData):
    if state["switches"].get("alerts_on", False) and state.get("warning"):
        return {"output_text": state["warning"]}
    return {"output_text": None}