import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Streamlit setup
st.set_page_config(page_title="AI Ergonomic Consultant", page_icon="🪑")

# Load .env or secret key
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

# Define agent personality (will make it dynamic later!)
agent_role = "You're an ergonomic consultant helping users improve their home office setup to reduce discomfort and improve productivity."

# Initialize chat if it doesn’t exist
if "chat" not in st.session_state:
    model = genai.GenerativeModel("gemini-1.5-pro-latest")
    st.session_state.chat = model.start_chat(history=[
        {"role": "system", "parts": [agent_role]}
    ])
