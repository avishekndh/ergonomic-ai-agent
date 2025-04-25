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

- [Flexispot EN1 Electric Standing Desk](https://www.amazon.com/Flexispot-Standing-Adjustable-Electric-Blacktop/dp/B07H2W9Y3W)
- [Samsonite Lumbar Support Pillow](https://www.amazon.com/Back-Cushion-Lumbar-Support-Pillow/dp/B01IJNJAZ0)
- [Amazon Basics Monitor Riser](https://www.amazon.com/AmazonBasics-Adjustable-Computer-Monitor-Riser/dp/B00X4SCCFG)

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
st.markdown("Describe your workspace or any discomfort you're experiencing, and I'll provide ergonomic advice and product suggestions if needed.")

user_input = st.text_input("💬 How can I assist you today?")

# ─────────────────────────────────────────────
# ✅ 6. Message handling
if st.button("Get Ergonomic Advice"):
    if not user_input.strip():
        st.warning("⚠️ Please enter a description of your workspace or discomfort.")
    else:
        with st.spinner("Analyzing your input..."):
            try:
                # First message: inject role + user input
                if not st.session_state.agent_initialized:
                    prompt = f"{agent_intro}\n\nUser: {user_input}"
                    response = st.session_state.chat.send_message(prompt)
                    st.session_state.agent_initialized = True
                else:
                    response = st.session_state.chat.send_message(user_input)

                st.success("✅ Here's your ergonomic advice:")
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
