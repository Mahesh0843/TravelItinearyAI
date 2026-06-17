import streamlit as st

def show_alert(warning_text):
    if warning_text:
        st.warning(f"⚠️ {warning_text}")
    else:
        st.success("No disruptions – enjoy your trip!")