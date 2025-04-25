import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv

# ✅ First Streamlit command: page config
st.set_page_config(page_title="AI Ergonomic Consultant", page_icon="🪑")

# ✅ Load environment variables
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

# ✅ Validate API Key
if not api_key:
    st.error("❌ API key missing! Please check your .env file.")
    st.stop()

# ✅ Configure Gemini
genai.configure(api_key=api_key)

# ✅ Load Gemini model
model = genai.GenerativeModel("gemini-1.5-pro-latest")

# ✅ Streamlit App Layout
st.title("🪑 AI Ergonomic Home Office Consultant")
st.markdown("Describe your current work setup, and get personalized ergonomic tips!")

# ✅ Text input from user
user_input = st.text_area("✏️ Tell me about your current desk/chair/monitor setup:")

# ✅ Handle button click
if st.button("Get Ergonomic Advice"):
    if not user_input.strip():
        st.warning("⚠️ Please describe your setup so I can help!")
    else:
        with st.spinner("Thinking and analyzing your workspace..."):
            try:
                # Build the prompt for Gemini
                prompt = (
                    f"You are an expert ergonomic consultant. "
                    f"A user describes their workspace: '{user_input}'. "
                    f"Give clear, practical, easy-to-follow ergonomic advice to improve their comfort and productivity."
                )
                # Generate the content
                response = model.generate_content(prompt)

                # Show the response
                st.success("✅ Here’s your personalized ergonomic advice:")
                st.markdown(response.text)

            except Exception as e:
                st.error(f"❌ Oops, something went wrong:\n\n{e}")
