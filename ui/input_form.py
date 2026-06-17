import streamlit as st
from datetime import date, timedelta

def show_form():
    with st.form("trip_form"):
        city = st.text_input("Destination city", value="Hyderabad")
        
        col1, col2 = st.columns(2)
        with col1:
            start = st.date_input("Start date", value=date.today())
            travelers = st.number_input("Number of travelers", min_value=1, value=2, step=1)
        with col2:
            end = st.date_input("End date", value=date.today() + timedelta(days=3))
            start_loc = st.text_input("Your starting location (hotel, station, etc.)", value="Adibatla")
        
        likes = st.multiselect(
            "What do you like?",
            ["Temples & Shrines", "Nature & Parks", "Museums", "Food & Markets",
             "Shopping", "Nightlife", "Historical Sites", "Beaches", "Art Galleries"],
            default=["Temples & Shrines"]
        )
        budget = st.selectbox(
    "Daily budget per person",
    ["low (< 5000)", "medium (5000 - 15000)", "high (> 15000)"],
    index=1  # default medium
)
        
        submitted = st.form_submit_button("Generate Itinerary")
        if submitted:
            return {
                "city": city,
                "start": start,
                "end": end,
                "travelers": travelers,
                "start_loc": start_loc,
                "likes": likes,
                "budget":budget,
                "submitted": True
            }
    return {"submitted": False}