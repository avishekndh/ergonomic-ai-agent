import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv

# ─────────────────────────────────────────────
# ✅ 1. Setup
st.set_page_config(page_title="AI Ergonomic Consultant", page_icon="🪑")

# ─────────────────────────────────────────────
# ✅ 2. Load API key
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    st.error("❌ Missing GEMINI_API_KEY. Set it in your .env or Streamlit Secrets.")
    st.stop()

genai.configure(api_key=api_key)

# ─────────────────────────────────────────────
# ✅ 3. Agent role prompt with product examples
agent_intro = """
You are an ergonomic assistant. Help users improve their home office setup.

Ask clarifying questions and give ergonomic suggestions.

If appropriate, include markdown links to ergonomic furniture. Use this format:

- [mesh ergonomic chair](https://amzn.to/mesh-chair)
- [adjustable sit-stand desk](https://amzn.to/standing-desk)
- [monitor riser](https://amzn.to/monitor-riser)
- [lumbar support pillow](https://amzn.to/lumbar-pillow)

Only suggest products when they’re clearly needed. Keep advice short, friendly, and helpful.
"""

# ─────────────────────────────────────────────
# ✅ 4. Start chat session
if "chat" not in st.session_state:
    model = genai.GenerativeModel("gemini-1.5-pro-latest")
    st.session_state.chat = model.start_chat()
    st.session_state.agent_initialized = False

# ─────────────────────────────────────────────
# ✅ 5. Interface
st.title("🪑 AI Ergonomic Home Office Consultant")
st.markdown("Tell me about your desk, chair, pain, posture... I’ll guide you toward comfort — and gear if you need it!")

user_input = st.text_input("💬 Describe your workspace or issue:")

# ─────────────────────────────────────────────
# ✅ 6. Message handling
if st.button("Get Ergonomic Advice"):
    if not user_input.strip():
        st.warning("⚠️ Please enter a description of your workspace or discomfort.")
    else:
        with st.spinner("Thinking..."):
            try:
                # First message: inject role + user input
                if not st.session_state.agent_initialized:
                    prompt = f"{agent_intro}\n\nUser: {user_input}"
                    response = st.session_state.chat.send_message(prompt)
                    st.session_state.agent_initialized = True
                else:
                    response = st.session_state.chat.send_message(user_input)

                st.success("✅ Here’s your ergonomic advice:")
                st.markdown(response.text)

            except Exception as e:
                st.error(f"❌ Error: {e}")

# ─────────────────────────────────────────────
# ✅ 7. Show full conversation history
if st.session_state.chat.history:
    st.markdown("### 📜 Conversation History")
    for msg in st.session_state.chat.history:
        text = msg.parts[0].text.strip()
        if agent_intro.strip() in text:
            continue  # hide system prompt
        if msg.role == "user":
            st.markdown(f"🧑‍💻 **You:** {text}")
        elif msg.role == "model":
            st.markdown(f"🤖 **ErgoBot:** {text}")
