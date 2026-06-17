# agents/get_rentals.py
from services.scrape import get_rentals as scrape_rentals

def get_rentals(location):
    return scrape_rentals(location)