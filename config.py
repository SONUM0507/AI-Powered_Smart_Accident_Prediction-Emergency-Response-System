import streamlit as st

# File paths
MODEL_PATH = "models/accident_model.pkl"
ENCODERS_PATH = "models/label_encoders.pkl"
ACCIDENT_DATA_PATH = "vadodara_accident_dataset.csv"
HOSPITAL_DATA_PATH = "hospital.csv"

# Page Configuration
PAGE_TITLE = "AI Accident Emergency Assistant"
LAYOUT = "wide"

def setup_page():
    """Sets up the Streamlit page configuration."""
    st.set_page_config(page_title=PAGE_TITLE, layout=LAYOUT, initial_sidebar_state="collapsed")

def load_css():
    """Loads custom CSS styles for the Streamlit application for a premium UI."""
    st.markdown("""
    <style>
    /* Import modern font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* Background gradient */
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%);
        color: #f8fafc;
    }

    /* Header typography */
    .title {
        text-align: center;
        font-size: 3.5rem;
        font-weight: 800;
        background: -webkit-linear-gradient(45deg, #38bdf8, #818cf8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
        padding-top: 2rem;
    }

    .subtitle {
        text-align: center;
        color: #94a3b8;
        font-size: 1.2rem;
        font-weight: 400;
        margin-bottom: 3rem;
        letter-spacing: 0.05em;
    }

    /* Stylish Metrics Container */
    div[data-testid="stMetric"] {
        background: rgba(30, 41, 59, 0.7);
        border: 1px solid rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-radius: 16px;
        padding: 20px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }

    div[data-testid="stMetric"]:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.3), 0 4px 6px -2px rgba(0, 0, 0, 0.1);
        border: 1px solid rgba(56, 189, 248, 0.5);
    }

    div[data-testid="stMetricValue"] {
        color: #38bdf8 !important;
        font-weight: 800;
    }
    
    div[data-testid="stMetricLabel"] {
        color: #cbd5e1 !important;
        font-weight: 600;
        font-size: 1.1rem;
    }

    /* Primary Button with glowing hover effect */
    .stButton > button {
        width: 100%;
        height: 55px;
        border-radius: 14px;
        background: linear-gradient(90deg, #2563eb, #3b82f6);
        color: white !important;
        font-size: 18px;
        font-weight: 600;
        border: none;
        box-shadow: 0 4px 15px rgba(37, 99, 235, 0.4);
        transition: all 0.3s ease;
        margin-top: 1rem;
        margin-bottom: 2rem;
    }

    .stButton > button:hover {
        background: linear-gradient(90deg, #1d4ed8, #2563eb);
        box-shadow: 0 6px 20px rgba(56, 189, 248, 0.6);
        transform: scale(1.02);
        color: white !important;
        border: none;
    }

    /* Result Cards / AI Response box */
    .ai-box {
        background: rgba(17, 24, 39, 0.8);
        backdrop-filter: blur(12px);
        padding: 25px;
        border-radius: 16px;
        border-left: 4px solid #818cf8;
        margin-top: 10px;
        margin-bottom: 30px;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.2);
        line-height: 1.6;
        color: #e2e8f0;
    }

    /* Subheaders */
    h2 {
        color: #f8fafc;
        font-weight: 600;
        padding-bottom: 0.5rem;
        margin-top: 2.5rem;
        margin-bottom: 1.5rem;
        font-size: 1.8rem;
    }
    
    /* BlockContainers max width */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 5rem;
        max-width: 1200px;
    }
    </style>
    """, unsafe_allow_html=True)
