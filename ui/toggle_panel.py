import streamlit as st
def show_toggles():
    with st.expander("Optional features (turn on/off)"):
        weather_on = st.checkbox("Live weather & traffic alerts", value=True)
        alerts_on = st.checkbox("Send notifications", value=True)
    return {
        "weather_on": weather_on,
        "alerts_on": alerts_on
    }