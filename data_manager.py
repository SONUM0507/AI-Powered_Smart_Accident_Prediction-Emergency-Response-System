import pandas as pd
import streamlit as st
from config import ACCIDENT_DATA_PATH, HOSPITAL_DATA_PATH

@st.cache_data
def load_accident_data():
    """Loads the main accident prediction dataset."""
    try:
        return pd.read_csv(ACCIDENT_DATA_PATH)
    except FileNotFoundError:
        st.error(f"Dataset not found at {ACCIDENT_DATA_PATH}. Please check the file path.")
        return pd.DataFrame()

@st.cache_data
def load_hospital_data():
    """Loads the hospital locations dataset."""
    try:
        return pd.read_csv(HOSPITAL_DATA_PATH)
    except FileNotFoundError:
        st.error(f"Dataset not found at {HOSPITAL_DATA_PATH}. Please check the file path.")
        return pd.DataFrame()
