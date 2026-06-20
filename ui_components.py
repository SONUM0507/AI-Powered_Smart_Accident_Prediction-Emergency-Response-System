import streamlit as st
import plotly.express as px

def render_header():
    """Renders the main header and subtitle for the application."""
    st.markdown('<div class="title">🚦 AI-Powered Smart Accident Prediction & Emergency Response Assistant</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">AI Prediction • Emergency Intelligence • Hospital Mapping • Smart Analytics</div>', unsafe_allow_html=True)

def render_metrics():
    """Renders the top level metrics."""
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Accident Records", "3000+")
    with col2:
        st.metric("AI Status", "Active")
    with col3:
        st.metric("Emergency System", "Online")

def render_input_section(df):
    """Renders the user input section for prediction."""
    if df.empty:
        return None, None, None, None, None, None, None, None
        
    st.markdown("## 🚨 Accident Risk Prediction")
    left, right = st.columns(2)
    
    with left:
        weather = st.selectbox("Weather Condition", df["Weather_Condition"].unique())
        road = st.selectbox("Road Type", df["Road_Type"].unique())
        vehicle = st.selectbox("Vehicle Type", df["Vehicle_Type"].unique())
        traffic = st.selectbox("Traffic Level", df["Traffic_Level"].unique())
        lighting = st.selectbox("Light Condition", df["Light_Condition"].unique())
        
    with right:
        speed = st.slider("Speed Limit", 20, 150, 60)
        age = st.slider("Driver Age", 18, 80, 30)
        alcohol_ui = st.selectbox("Alcohol Involved", ["Yes", "No"])
        alcohol = 1 if alcohol_ui == "Yes" else 0
        
        seatbelt_ui = st.selectbox("Seatbelt/Helmet Used", ["Yes", "No"])
        seatbelt = 1 if seatbelt_ui == "Yes" else 0
        
    return weather, road, vehicle, traffic, lighting, speed, age, alcohol, seatbelt

def render_location_section():
    """Renders the location input section."""
    st.markdown("## 📍 Accident Location")
    loc1, loc2 = st.columns(2)
    with loc1:
        latitude = st.number_input("Latitude", value=22.3072)
    with loc2:
        longitude = st.number_input("Longitude", value=73.1812)
    return latitude, longitude
