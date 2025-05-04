import streamlit as st
from core.api import ask_claude
from core.uploader import upload_file  # ⬅️ our new upload module

st.set_page_config(page_title="myGPT - Claude Sonnet", layout="wide")

st.title("🧠 myGPT (Claude Sonnet)")

# 🔼 Upload Document (PDF/CSV)
uploaded_file = upload_file()

# 🧠 Claude Q&A Interface
st.subheader("💬 Ask Claude")

if "messages" not in st.session_state:
    st.session_state["messages"] = []

user_input = st.text_input("You:", key="input")

if st.button("Ask") and user_input.strip():
    st.session_state["messages"].append(("You", user_input))

    # For now, use Claude directly (no RAG logic yet)
    answer = ask_claude(user_input)
    st.session_state["messages"].append(("Claude", answer))

# Chat history display
for sender, message in st.session_state["messages"]:
    st.markdown(f"**{sender}:** {message}")
