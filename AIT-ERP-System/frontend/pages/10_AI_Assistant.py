import streamlit as st
from frontend.styles.theme import inject, hero, brand_sidebar
from frontend.components.auth_ui import require_auth, logout_button
from frontend.components.api_client import api_post

st.set_page_config(page_title="AI Assistant • AiT", layout="wide")
inject(st); require_auth()
brand_sidebar(st, role=st.session_state.get("role", "")); logout_button()
hero(st, "AiT AI Assistant", "Ask anything about admissions, fees, courses, or policies.")

if "chat" not in st.session_state:
    st.session_state["chat"] = [
        {"role": "assistant", "content": "Hi! I'm the AiT Assistant. Ask me about admissions, fees, levels, or courses."}
    ]

for msg in st.session_state["chat"]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

prompt = st.chat_input("Type your question...")
if prompt:
    st.session_state["chat"].append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            r = api_post("/api/chatbot/ask", {"message": prompt})
            reply = r.get("reply", "I'm sorry, please try again.")
            st.markdown(reply)
    st.session_state["chat"].append({"role": "assistant", "content": reply})