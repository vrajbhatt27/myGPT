# app.py

import streamlit as st
from core.api import ask_claude

st.set_page_config(page_title="myGPT - Claude Sonnet", layout="wide")

st.title("🧠 myGPT (Claude Sonnet)")

if "messages" not in st.session_state:
    st.session_state["messages"] = []

user_input = st.text_input("You:", key="input")

if st.button("Ask") and user_input.strip():
    st.session_state["messages"].append(("You", user_input))
    answer = ask_claude(user_input)
    st.session_state["messages"].append(("Claude", answer))

# Chat history display
for sender, message in st.session_state["messages"]:
    st.markdown(f"**{sender}:** {message}")
