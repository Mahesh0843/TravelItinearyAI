# agents/add_maps.py
def add_maps(plan):
    for day in plan:
        for act in day["activities"]:
            if "map_url" not in act:
                lat, lon = act["coords"]
                act["map_url"] = f"https://www.openstreetmap.org/?mlat={lat}&mlon={lon}"
    return plan