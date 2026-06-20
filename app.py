import streamlit as st
from streamlit_folium import st_folium

from config import setup_page, load_css
from data_manager import load_accident_data, load_hospital_data
from model_manager import load_model_and_encoders, prepare_input_data, predict_accident_severity
from ui_components import (
    render_header, 
    render_metrics, 
    render_input_section, 
    render_location_section
)
from map_utils import find_nearest_hospital, create_emergency_map
from chatbot import ask_ai

def main():
    # Setup page configurations and CSS
    setup_page()
    load_css()

    # Load resources
    df = load_accident_data()
    hospitals = load_hospital_data()
    model, encoders = load_model_and_encoders()

    # If essential resources failed to load, stop execution safely
    if df.empty or model is None:
        st.warning("Please resolve data and model loading issues to use the application.")
        return

    # UI Header & Metrics
    render_header()
    render_metrics()

    # Inputs
    weather, road, vehicle, traffic, lighting, speed, age, alcohol, seatbelt = render_input_section(df)
    
    if weather is None: # Input section failed because data is empty
        return
        
    latitude, longitude = render_location_section()

    # Prediction Action
    if st.button("🚨 Predict Accident Risk"):
        
        # Prepare data and predict
        input_data = prepare_input_data(
            encoders, weather, road, vehicle, traffic, lighting, speed, age, alcohol, seatbelt
        )
        
        severity, risk = predict_accident_severity(model, encoders, input_data)
        
        # Initialize dictionary to hold results in session state
        results = {
            "severity": severity,
            "risk": risk,
            "latitude": latitude,
            "longitude": longitude
        }

        # AI Response Generation
        ai_prompt = f"""
        Accident Details:
        Weather: {weather}
        Road Type: {road}
        Vehicle Type: {vehicle}
        Traffic Level: {traffic}
        Lighting: {lighting}
        Speed: {speed}
        Driver Age: {age}
        Alcohol: {"Yes" if alcohol else "No"}
        Seatbelt/Helmet: {"Yes" if seatbelt else "No"}

        Predicted Severity:
        {severity}

        Give concise emergency advice and safety recommendations based on this context.
        """
        
        with st.spinner("AI is analyzing the situation and generating emergency response..."):
            try:
                results["ai_response"] = ask_ai(ai_prompt)
            except Exception as e:
                results["ai_response"] = "Failed to generate AI response. Please check API key and network connection."

        # Nearest Hospital
        nearest_hospital, nearest_distance = find_nearest_hospital((latitude, longitude), hospitals)
        results["nearest_hospital"] = nearest_hospital
        results["nearest_distance"] = nearest_distance
        
        # Save to session state so it persists across map interactions
        st.session_state.prediction_results = results


    # Display Results if they exist in session state
    if "prediction_results" in st.session_state:
        res = st.session_state.prediction_results
        
        # UI Results
        st.markdown("## 🧠 AI Risk Analysis")
        r1, r2 = st.columns(2)
        with r1:
            st.success(f"Predicted Severity: **{res['severity']}**")
        with r2:
            st.error(f"Risk Level: **{res['risk']}**")

        # AI Response
        st.markdown("## 🤖 AI Emergency Response")
        st.markdown(
            f'<div class="ai-box"><p style="color:white; font-size: 16px;">{res["ai_response"]}</p></div>', 
            unsafe_allow_html=True
        )

        # Nearest Hospital and Mapping
        nearest_h = res["nearest_hospital"]
        
        if nearest_h is not None:
            st.markdown("## 🏥 Nearest Emergency Hospital")
            h1, h2 = st.columns(2)
            with h1:
                st.info(f"Hospital: **{nearest_h['Hospital']}**")
            with h2:
                st.warning(f"Distance: **{res['nearest_distance']:.2f} KM**")

            # Map Visualization
            st.markdown("## 🗺 Emergency Response Map")
            emergency_map = create_emergency_map(res["latitude"], res["longitude"], nearest_h)
            st_folium(emergency_map, width=1200, height=500)

if __name__ == "__main__":
    main()