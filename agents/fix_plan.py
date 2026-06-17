# agents/fix_plan.py
from agents.get_places import get_pois

def fix_plan(plan, weather, city, likes):
    if not weather or weather.get("condition") not in ["rain", "storm", "snow"]:
        return plan, None
    if not plan:
        return plan, "No plan to fix"
    # assume first day is today (simplified)
    today = plan[0]
    bad_words = ["park", "garden", "shrine", "temple", "hiking", "beach"]
    to_replace = [i for i, act in enumerate(today["activities"])
                  if any(w in act["name"].lower() for w in bad_words)]
    if not to_replace:
        return plan, None
    new_pois = get_pois(city, likes)
    used = {act["name"] for day in plan for act in day["activities"]}
    alt = [p for p in new_pois if p["name"] not in used][:len(to_replace)]
    if not alt:
        return plan, "No indoor alternatives found"
    for j, idx in enumerate(to_replace):
        p = alt[j]
        today["activities"][idx] = {
            "name": p["name"],
            "time": today["activities"][idx]["time"],
            "coords": [p["lat"], p["lon"]],
            "map_url": f"https://www.openstreetmap.org/?mlat={p['lat']}&mlon={p['lon']}",
            "notes": "Indoor alternative due to weather"
        }
    return plan, f"Weather alert: {weather['condition']}. Swapped outdoor activities."