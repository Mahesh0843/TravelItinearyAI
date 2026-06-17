# app.py
import streamlit as st
import uuid
from datetime import datetime, date

from ui.input_form import show_form
from ui.toggle_panel import show_toggles
from ui.show_plan import display_plan
from ui.show_alert import show_alert
from services.save_load import save_trip, load_trip, test_db
from graph.workflow import main_graph
from graph.update_workflow import update_graph
from graph.state import TripData

st.set_page_config(page_title="Travel Planner", layout="wide")
st.title("🗺️ Personalized Travel Itinerary Planner")

# Session state init
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())
if "trip" not in st.session_state:
    st.session_state.trip = None
if "generated" not in st.session_state:
    st.session_state.generated = False
if "saved" not in st.session_state:
    st.session_state.saved = False

# Sidebar: MongoDB test
with st.sidebar:
    
    if st.button("Test Database"):
        if test_db():
            st.success("MongoDB OK")
        else:
            st.error("MongoDB error")

# Main form
form_data = show_form()
toggles = show_toggles()

if form_data["submitted"]:
    # Build initial state
    state: TripData = {
        "city": form_data["city"],
        "start": form_data["start"],
        "end": form_data["end"],
        "travelers": form_data["travelers"],
        "start_loc": form_data["start_loc"],
        "likes": form_data["likes"],
        "budget":form_data["budget"],
        "switches": toggles,
        "days": 0,
        "home_coords": None,
        "places": [],
        "forecast": None,
        "today_weather": None,
        "plan": None,
        # "rentals": None,
        "output_text": None,
        "warning": None,
        "error": None,
        "is_update": False,
        "bad_weather": False,
    }
    with st.spinner("Planning your trip..."):
        result = main_graph.invoke(state)
    if result.get("error"):
        st.error(result["error"])
    else:
        st.session_state.trip = result
        st.session_state.generated = True
        st.session_state.saved = False
        st.rerun()

if st.session_state.generated and st.session_state.trip:
    trip = st.session_state.trip
    display_plan(trip.get("output_text", ""), trip.get("plan"),trip.get("forecast"))
    show_alert(trip.get("warning"))

    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 Regenerate"):
            st.session_state.generated = False
            st.rerun()
    with col2:
        if not st.session_state.saved:
            if st.button("💾 Finalize & Save"):
                doc = {
                    "session_id": st.session_state.session_id,
                    "city": trip["city"],
                    "start": trip["start"].isoformat(),
                    "end": trip["end"].isoformat(),
                    "travelers": trip["travelers"],
                    "start_loc": trip["start_loc"],
                    "likes": trip["likes"],
                    "switches": trip["switches"],
                    "plan": trip["plan"],
                    "budget": trip["budget"],
                    # "rentals": trip["rentals"],
                    "output_text": trip["output_text"],
                    "created_at": datetime.utcnow().isoformat()
                }
                save_trip(doc)
                st.session_state.saved = True
                st.success("Itinerary saved! Copy your session ID:")
                st.code(st.session_state.session_id)

    # Real‑time update button (only if weather alerts are on)
    if trip.get("switches", {}).get("weather_on", False):
        if st.button("☁️ Check for weather updates"):
            # Prepare update state using saved trip
            update_state = {
                **trip,
                "is_update": True,
                "bad_weather": False,
                "warning": None
            }
            with st.spinner("Checking..."):
                updated = update_graph.invoke(update_state)
            if updated.get("warning"):
                st.warning(updated["warning"])
                if updated.get("plan"):
                    st.session_state.trip["plan"] = updated["plan"]
                    st.session_state.trip["output_text"] = updated.get("output_text", trip["output_text"])
                    st.rerun()
            else:
                st.success("No weather issues today!")

# Load existing trip section
with st.expander("Load a saved trip"):
    sid = st.text_input("Session ID")
    if st.button("Load"):
        doc = load_trip(sid)
        if doc:
            # Convert string dates back to date objects
            doc["start"] = date.fromisoformat(doc["start"])
            doc["end"] = date.fromisoformat(doc["end"])
            doc["is_update"] = False
            doc["bad_weather"] = False
            doc["warning"] = None
            st.session_state.trip = doc
            st.session_state.generated = True
            st.session_state.saved = True
            st.rerun()
        else:
            st.error("No trip found")