import streamlit as st
import pandas as pd
import requests
import plotly.express as px
from geopy.geocoders import Nominatim
import time
import os  # <--- Added this

# ---------------------------------------------------------
# CONFIGURATION
# ---------------------------------------------------------
# Step 3 Update: Use Environment Variable for Docker, default to localhost for manual runs
API_URL = os.getenv("API_URL", "http://127.0.0.1:8000/api/v1/latest")
REFRESH_RATE = 3

st.set_page_config(page_title="Urban Pulse Global", layout="wide")

# Initialize Geocoder
geolocator = Nominatim(user_agent="urban_pulse_app")

# ---------------------------------------------------------
# SIDEBAR SEARCH
# ---------------------------------------------------------
st.sidebar.title("🌍 Global Monitoring")
st.sidebar.markdown("Search for any city to inspect its sensor network.")

# Text Input for City Search
search_query = st.sidebar.text_input("Enter City Name:", "World View")
search_btn = st.sidebar.button("Search Location")

# Default Map Settings
map_center = {"lat": 20.0, "lon": 0.0}
zoom_level = 1

# ---------------------------------------------------------
# GEOCODING LOGIC
# ---------------------------------------------------------
if search_query and search_query != "World View":
    try:
        location = geolocator.geocode(search_query)
        if location:
            map_center = {"lat": location.latitude, "lon": location.longitude}
            zoom_level = 10
            st.sidebar.success(f"Found: {location.address}")
        else:
            st.sidebar.error("⚠️ City not found.")
    except Exception as e:
        st.sidebar.warning("Geocoding service busy. Try again.")

# ---------------------------------------------------------
# DATA FETCH (WITH ERROR PRINTING)
# ---------------------------------------------------------
def fetch_data():
    try:
        response = requests.get(API_URL)
        if response.status_code == 200:
            return pd.DataFrame(response.json())
        else:
            st.error(f"⚠️ API Error: {response.status_code}")
            return pd.DataFrame()
    except Exception as e:
        # 🚨 THIS WILL SHOW US THE REAL ERROR
        st.error(f"❌ Connection Error: {e}")
        return pd.DataFrame()

df = fetch_data()

# ---------------------------------------------------------
# MAIN UI
# ---------------------------------------------------------
st.title("🏙️ Urban Pulse: Global Sensor Network")

if not df.empty:
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.subheader(f"Live Map: {search_query}")
        fig = px.scatter_mapbox(
            df,
            lat="latitude",
            lon="longitude",
            # Handle missing 'city' column gracefully
            hover_name="city" if "city" in df.columns else "sensor_id",
            color="aqi",
            size="aqi",
            color_continuous_scale=px.colors.diverging.RdYlGn[::-1],
            size_max=15,
            zoom=zoom_level,
            center=map_center,
            mapbox_style="carto-positron"
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("📊 Live Stats")
        avg_aqi = df["aqi"].mean()
        max_aqi = df["aqi"].max()
        
        st.metric("Global Avg AQI", f"{avg_aqi:.0f}")
        st.metric("Worst Recorded AQI", max_aqi)
        
        st.write("### Recent Readings")
        # Show columns that actually exist
        cols_to_show = ["sensor_id", "aqi"]
        if "city" in df.columns:
            cols_to_show.insert(1, "city")
            
        st.dataframe(
            df[cols_to_show].sort_values(by="aqi", ascending=False).head(10),
            use_container_width=True,
            hide_index=True
        )
else:
    st.warning("Waiting for data stream...")
    if st.button("Retry Connection"):
        st.rerun()