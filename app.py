import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv

# ─────────────────────────────────────────────
# ✅ 1. App config
st.set_page_config(page_title="AI Ergonomic Consultant", page_icon="🪑")

# ─────────────────────────────────────────────
# ✅ 2. Load key
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    st.error("❌ No API key found in .env or Streamlit Secrets.")
    st.stop()

genai.configure(api_key=api_key)

# ─────────────────────────────────────────────
# ✅ 3. Product-friendly prompt (inserted once)
agent_intro = """
You are a helpful ergonomic AI assistant. Your goal is to help users improve their home office setup.

✅ Ask follow-up questions if needed.
✅ Suggest ergonomic improvements.
✅ If appropriate, recommend ergonomic products using markdown links (example: [chair](https://amzn.to/chair123)).
✅ Keep advice friendly, clear, and short. Don’t recommend a product every time — only when it makes sense.

Example:
"If you're experiencing wrist pain, consider a wrist rest like [this gel pad](https://amzn.to/example)."
"""

# ─────────────────────────────────────────────
# ✅ 4. Start Gemini chat if new
if "chat" not in st.session_state:
    model = genai.GenerativeModel("gemini-1.5-pro-latest")
    st.session_state.chat = model.start_chat()
    st.session_state.agent_initialized = False

# ─────────────────────────────────────────────
# ✅ 5. Interface
st.title("🪑 AI Ergonomic Home Office Consultant")
st.markdown("Tell me about your desk, chair, pain, posture... and I'll guide you toward comfort (and gear if needed).")

user_input = st.text_input("💬 How can I help improve your workspace today?")

# ─────────────────────────────────────────────
# ✅ 6. Handle message with smart intro
if st.button("Get Ergonomic Advice"):
    if not user_input.strip():
        st.warning("⚠️ Please describe your workspace!")
    else:
        with st.spinner("Thinking ergonomically..."):
            try:
                # Add role prompt only for the very first message
                if not st.session_state.agent_initialized:
                    first_msg = f"{agent_intro}\n\nUser: {user_input}"
                    response = st.session_state.chat.send_message(first_msg)
                    st.session_state.agent_initialized = True
                else:
                    response = st.session_state.chat.send_message(user_input)

                st.success("✅ Here's your advice:")
                st.markdown(response.text)

            except Exception as e:
                st.error(f"❌ Error: {e}")

# ─────────────────────────────────────────────
# ✅ 7. Display chat history
if st.session_state.chat.history:
    st.markdown("### 🧾 Conversation History")
    for msg in st.session_state.chat.history:
        text = msg.parts[0].text.strip()
        if agent_intro.strip() in text:
            continue  # Skip initial role prompt
        if msg.role == "user":
            st.markdown(f"🧑‍💻 **You:** {text}")
        elif msg.role == "model":
            st.markdown(f"🤖 **ErgoBot:** {text}")
