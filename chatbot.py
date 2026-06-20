import google.generativeai as genai
import logging

import os

# Configure Gemini API
# NOTE: For production, it's recommended to load this from environment variables
api_key = os.getenv("GEMINI_API_KEY", "AIzaSyAZJ15T8D4SZgSlhCMcZkxLzzW_9Insf4k")
genai.configure(api_key=api_key)

# Initialize the model once
try:
    model = genai.GenerativeModel("gemini-1.5-flash")
except Exception as e:
    logging.error(f"Failed to initialize Gemini model: {e}")
    model = None

def ask_ai(question: str) -> str:
    """
    Asks the Google Generative AI model for emergency response advice.
    
    Args:
        question (str): The details of the accident.
        
    Returns:
        str: The AI's response and recommendations.
    """
    if model is None:
        return "AI model is currently unavailable."
        
    prompt = f"""
    You are an AI Emergency Response Assistant.

    Answer professionally about:
    - road accidents
    - emergency response
    - hospital suggestions
    - road safety
    - accident prevention

    User Context / Question:
    {question}
    """

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        logging.error(f"Error during AI generation: {e}")
        return "Sorry, I encountered an error while processing your request. Please seek immediate professional medical help."