import requests

INTEREST_TAGS = {
    "Temples & Shrines": [
        "historic=shrine",
        "historic=temple",
        "amenity=place_of_worship"
    ],

    "Nature & Parks": [
        "leisure=park",
        "natural=wood",
        "leisure=garden"
    ],

    "Museums": [
        "tourism=museum",
        "amenity=arts_centre"
    ],

    "Food & Markets": [
        "amenity=restaurant",
        "amenity=cafe"
    ],

    "Shopping": [
        "shop=clothes",
        "shop=department_store"
    ],

    "Nightlife": [
        "amenity=bar",
        "amenity=nightclub"
    ],

    "Historical Sites": [
        "historic=castle",
        "historic=memorial"
    ],

    "Beaches": [
        "natural=beach"
    ],

    "Art Galleries": [
        "tourism=gallery"
    ]
}


def _get_city_box(city):

    url = "https://nominatim.openstreetmap.org/search"

    params = {
        "q": city,
        "format": "json",
        "limit": 1
    }

    headers = {
        "User-Agent": "TravelPlanner/1.0"
    }

    resp = requests.get(
        url,
        params=params,
        headers=headers,
        timeout=10
    )

    resp.raise_for_status()

    data = resp.json()

    if not data:
        raise ValueError(f"City not found: {city}")

    bbox = data[0]["boundingbox"]

    south, north, west, east = map(float, bbox)

    return south, west, north, east


def get_pois(city, likes):

    if not likes:
        return []

    tags = []

    for interest in likes:

        if interest in INTEREST_TAGS:
            tags.extend(INTEREST_TAGS[interest])
    unique_tags = list(set(tags))

    if not unique_tags:
        return []

    south, west, north, east = _get_city_box(city)
    query_lines = []

    for tag in unique_tags:

        line = (
            f'nwr[{tag}]'
            f'({south},{west},{north},{east});'
        )

        query_lines.append(line)

    query_body = "\n".join(query_lines)

    query = f"""
    [out:json][timeout:25];
    (
    {query_body}
    );
    out center 40;
    """

    url = "https://overpass-api.de/api/interpreter"

    headers = {
        "User-Agent": "TravelPlanner/1.0"
    }

    resp = requests.post(
        url,
        data=query,
        headers=headers,
        timeout=120
    )

    resp.raise_for_status()

    data = resp.json()

    pois = []

    for elem in data.get("elements", []):

        tags_data = elem.get("tags", {})

        name = tags_data.get("name", "Unnamed")

        lat = elem.get("lat")

        lon = elem.get("lon")

        if not lat or not lon:

            center = elem.get("center", {})

            lat = center.get("lat")
            lon = center.get("lon")

        if lat and lon:

            pois.append({
                "name": name,
                "lat": lat,
                "lon": lon
            })

    return pois
