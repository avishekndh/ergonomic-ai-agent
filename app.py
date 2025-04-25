import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv

# ─────────────────────────────────────────────
# ✅ 1. Streamlit page setup
st.set_page_config(page_title="AI Ergonomic Consultant", page_icon="🪑")

# ─────────────────────────────────────────────
# ✅ 2. Load Gemini API key from secrets or .env
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    st.error("❌ Missing API key! Make sure it's set in Streamlit Secrets.")
    st.stop()

genai.configure(api_key=api_key)

# ─────────────────────────────────────────────
# ✅ 3. Define agent personality (as instruction text)
agent_role = (
    "You're an ergonomic consultant helping users improve their home office setup. "
    "Give clear, practical, simple suggestions to reduce pain and increase productivity."
)

# ─────────────────────────────────────────────
# ✅ 4. Initialize chat object (no system role!)
if "chat" not in st.session_state:
    model = genai.GenerativeModel("gemini-1.5-pro-latest")
    st.session_state.chat = model.start_chat()

# ─────────────────────────────────────────────
# ✅ 5. UI elements
st.title("🪑 AI Ergonomic Home Office Consultant")
st.markdown("Describe your current work setup, and get personalized ergonomic tips!")

user_input = st.text_area("✏️ Tell me about your current desk/chair/monitor setup:")

# ─────────────────────────────────────────────
# ✅ 6. Generate response
if st.button("Get Ergonomic Advice"):
    if not user_input.strip():
        st.warning("⚠️ Please describe your setup so I can help!")
    else:
        with st.spinner("Thinking..."):
            try:
                full_prompt = f"{agent_role}\n\nUser: {user_input}"
                response = st.session_state.chat.send_message(full_prompt)
                st.success("✅ Here’s your personalized ergonomic advice:")
                st.markdown(response.text)
            except Exception as e:
                st.error(f"❌ Something went wrong:\n\n{e}")

# ─────────────────────────────────────────────
# ✅ 7. Optional: Show history
if "chat" in st.session_state and st.session_state.chat.history:
    st.markdown("### 🧾 Conversation History")
    for msg in st.session_state.chat.history:
        if msg.role == "user":
            st.markdown(f"🧑‍💻 **You:** {msg.parts[0].text}")
        elif msg.role == "model":
            st.markdown(f"🤖 **ErgoBot:** {msg.parts[0].text}")
