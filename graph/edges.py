from graph.state import TripData

def need_weather(state: TripData):
    if state["switches"].get("weather_on", False):
        return "get_weather"
    return "skip"

# def need_rentals(state: TripData):
#     if state["switches"].get("rent_on", False):
#         return "get_rentals"
#     return "skip"

def need_fix(state: TripData):
    if state.get("is_update", False) and state.get("bad_weather", False):
        return "fix_plan"
    return "normal"