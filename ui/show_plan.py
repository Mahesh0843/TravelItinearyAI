import streamlit as st
import folium
from streamlit_folium import st_folium

def display_plan(itinerary_text, daily_plan=None, forecast=None):
    st.markdown("## 📅 Your Itinerary")
    if itinerary_text:
        st.markdown(itinerary_text)
    else:
        st.warning("Itinerary text not available. Showing raw plan with map links.")
        if daily_plan:
            for day in daily_plan:
                st.markdown(f"**Day {day['day']}**")
                for act in day["activities"]:
                    map_markdown = f"[📍]({act['map_url']})"
                    st.markdown(f"- {act['time']} **{act['name']}** {map_markdown} {act.get('notes', '')}")
                if forecast and day['day']-1 < len(forecast):
                    fc = forecast[day['day']-1]
                    st.markdown(f"*Weather: {fc['condition']}, {fc['temp']}°C*")
    if daily_plan:
        st.markdown("### 📍 Map View")
        try:
            first_act = None
            for day in daily_plan:
                if day["activities"]:
                    first_act = day["activities"][0]
                    break
            if first_act and "coords" in first_act and len(first_act["coords"]) == 2:
                lat, lon = first_act["coords"]
                m = folium.Map(location=[lat, lon], zoom_start=13)
                for day in daily_plan:
                    for act in day["activities"]:
                        if "coords" in act and len(act["coords"]) == 2:
                            folium.Marker(
                                location=act["coords"],
                                popup=act["name"],
                                tooltip=act["name"]
                            ).add_to(m)
                st_folium(m, width=700, height=400)
            else:
                st.info("No valid coordinates for map.")
        except Exception as e:
            st.info(f"Map error: {e}")