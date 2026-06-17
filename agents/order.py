from services.get_times import get_travel_time

def order_activities(home, pois, days, forecast=None):
    if not pois:
        return []
    
    max_per_day = 4
    total_capacity = days * max_per_day
    if len(pois) > total_capacity:
        pois = pois[:total_capacity]
    
    result = []
    idx = 0
    for day_num in range(days):
        if idx >= len(pois):
            break
        day_pois = []
        while len(day_pois) < max_per_day and idx < len(pois):
            day_pois.append(pois[idx])
            idx += 1
        if not day_pois:
            continue
        
        # sort by distance from home (greedy start)
        times_from_home = []
        for p in day_pois:
            try:
                t = get_travel_time(home, (p["lat"], p["lon"]))
            except:
                t = 9999
            times_from_home.append((t, p))
        times_from_home.sort(key=lambda x: x[0])
        ordered = [p for _, p in times_from_home]
        
        activities = []
        prev_coords = home
        timings = ["9:00 AM", "11:30 AM", "2:00 PM", "4:30 PM"]
        for i, p in enumerate(ordered):
            if i >= len(timings):
                break
            travel_min = 0
            if i > 0:
                try:
                    travel_min = get_travel_time(prev_coords, (p["lat"], p["lon"]))
                except:
                    travel_min = 15
            prev_coords = (p["lat"], p["lon"])
            travel_text = f" ({int(travel_min)} min travel)" if travel_min > 0 else ""
            area = p.get("area", "city center")
            activities.append({
                "name": p["name"],
                "time": timings[i],
                "coords": [p["lat"], p["lon"]],
                "map_url": f"https://www.openstreetmap.org/?mlat={p['lat']}&mlon={p['lon']}",
                "notes": f"[{area}]{travel_text}"
            })
        result.append({
            "day": day_num + 1,
            "date": "",
            "activities": activities
        })
    return result