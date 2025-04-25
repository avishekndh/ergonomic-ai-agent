import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv

# ─────────────────────────────────────────────
# ✅ Streamlit page setup
st.set_page_config(page_title="AI Ergonomic Consultant", page_icon="🪑")

# ─────────────────────────────────────────────
# ✅ Load API key from .env or Streamlit Secrets
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    st.error("❌ Gemini API key missing! Set it in .env or Streamlit Secrets.")
    st.stop()

genai.configure(api_key=api_key)

# ─────────────────────────────────────────────
# ✅ Define the agent's personality (instruction)
agent_role = (
    "You're an ergonomic consultant helping users improve their home office setup. "
    "Give clear, practical, simple suggestions to reduce pain and increase productivity."
)

# ─────────────────────────────────────────────
# ✅ Start Gemini chat only once per session
if "chat" not in st.session_state:
    model = genai.GenerativeModel("gemini-1.5-pro-latest")
    st.session_state.chat = model.start_chat()

# ─────────────────────────────────────────────
# ✅ UI layout
st.title("🪑 AI Ergonomic Home Office Consultant")
st.markdown("Describe your current work setup, and get personalized ergonomic tips!")

user_input = st.text_area("✏️ Tell me about your current desk/chair/monitor setup:")

# ─────────────────────────────────────────────
# ✅ Handle button click + first-time role injection
if st.button("Get Ergonomic Advice"):
    if not user_input.strip():
        st.warning("⚠️ Please describe your setup so I can help!")
    else:
        with st.spinner("Analyzing your workspace..."):
            try:
                if len(st.session_state.chat.history) == 0:
                    first_prompt = f"{agent_role}\n\nUser: {user_input}"
                    response = st.session_state.chat.send_message(first_prompt)
                else:
                    response = st.session_state.chat.send_message(user_input)

                st.success("✅ Here’s your personalized ergonomic advice:")
                st.markdown(response.text)

            except Exception as e:
                st.error(f"❌ Error: {e}")

# ─────────────────────────────────────────────
# ✅ Display conversation history
if st.session_state.chat.history:
    st.markdown("### 🧾 Conversation History")
    for msg in st.session_state.chat.history:
        text = msg.parts[0].text
        # Skip agent role prompt from display
        if "You're an ergonomic consultant" in text:
            continue
        if msg.role == "user":
            st.markdown(f"🧑‍💻 **You:** {text}")
        elif msg.role == "model":
            st.markdown(f"🤖 **ErgoBot:** {text}")
