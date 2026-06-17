# agents/get_prefs.py
def parse_inputs(city, start, end, travelers, start_loc, likes):
    days = (end - start).days + 1
    return {
        "city": city,
        "start": start,
        "end": end,
        "days": days,
        "travelers": travelers,
        "start_loc": start_loc,
        "likes": likes
    }