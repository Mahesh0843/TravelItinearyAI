from typing import TypedDict, List, Dict, Optional
from datetime import date

class TripData(TypedDict):
    # User input
    city: str
    start: date
    end: date
    travelers: int
    start_loc: str          # was "hotel"
    likes: List[str]
    budget: str
    
    # Switches
    switches: Dict[str, bool]   # weather_on, alerts_on, rent_on
    
    # Internal
    days: int
    home_coords: Optional[List[float]]
    places: List[Dict]
    forecast: Optional[List[Dict]]
    today_weather: Optional[Dict]
    plan: Optional[List[Dict]]
    # rentals: Optional[List[Dict]]
    output_text: Optional[str]
    warning: Optional[str]
    error: Optional[str]
    
    # Flags
    is_update: bool
    bad_weather: bool