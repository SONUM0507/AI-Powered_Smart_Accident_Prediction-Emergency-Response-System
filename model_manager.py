import joblib
import pandas as pd
import streamlit as st
from config import MODEL_PATH, ENCODERS_PATH

@st.cache_resource
def load_model_and_encoders():
    """Loads the pre-trained machine learning model and label encoders."""
    try:
        model = joblib.load(MODEL_PATH)
        encoders = joblib.load(ENCODERS_PATH)
        return model, encoders
    except FileNotFoundError:
        st.error("Model or Encoders not found. Please ensure the 'models' directory exists and contains the necessary files.")
        return None, None

def prepare_input_data(encoders, weather, road, vehicle, traffic, lighting, speed, age, alcohol, seatbelt):
    """Prepares and encodes the input data for prediction."""
    return pd.DataFrame([{
        "Weather_Condition": encoders["Weather_Condition"].transform([weather])[0],
        "Road_Type": encoders["Road_Type"].transform([road])[0],
        "Vehicle_Type": encoders["Vehicle_Type"].transform([vehicle])[0],
        "Traffic_Level": encoders["Traffic_Level"].transform([traffic])[0],
        "Light_Condition": encoders["Light_Condition"].transform([lighting])[0],
        "Speed_kmph": speed,
        "Driver_Age": age,
        "Alcohol_Involved": alcohol,
        "Seatbelt_Helmet_Used": seatbelt
    }])

def predict_accident_severity(model, encoders, input_data):
    """Predicts the accident severity and determines the risk level."""
    prediction = model.predict(input_data)[0]
    severity = encoders["Accident_Severity"].inverse_transform([prediction])[0]
    
    if severity == "Minor":
        risk = "🟢 LOW RISK"
    elif severity == "Serious":
        risk = "🟠 MEDIUM RISK"
    else:
        risk = "🔴 HIGH RISK"
        
    return severity, risk
