from pymongo import MongoClient
import streamlit as st

@st.cache_resource
def _get_db():
    client = MongoClient(st.secrets["mongodb_uri"])
    return client["travel_planner"]

def save_trip(data):
    """Save a finalized trip to MongoDB."""
    db = _get_db()
    return db.trips.insert_one(data).inserted_id

def load_trip(session_id):
    """Load a trip by session_id."""
    db = _get_db()
    return db.trips.find_one({"session_id": session_id})

def test_db():
    """Check if MongoDB is reachable."""
    try:
        db = _get_db()
        db.test.insert_one({"x": 1})
        db.test.delete_one({"x": 1})
        return True
    except:
        return False