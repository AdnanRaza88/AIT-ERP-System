import streamlit as st
from components.api_client import login


def require_auth():
    if "token" not in st.session_state:
        render_login()
        st.stop()


def render_login():
    st.markdown("""
      <div class="ait-hero" style="max-width:520px; margin: 60px auto;">
        <h1>Welcome to AiT</h1>
        <p>Sign in to access the institute management portal.</p>
      </div>
    """, unsafe_allow_html=True)

    with st.container():
        col = st.columns([1, 2, 1])[1]
        with col:
            email = st.text_input("Email", value="admin@ait.edu")
            password = st.text_input("Password", type="password", value="admin123")
            if st.button("Sign in", use_container_width=True):
                resp = login(email, password)
                if "access_token" in resp:
                    st.session_state["token"] = resp["access_token"]
                    st.session_state["role"] = resp["role"]
                    st.session_state["user"] = resp["full_name"]
                    st.session_state["email"] = resp["email"]
                    st.rerun()
                else:
                    st.error("Invalid credentials")


def logout_button():
    if st.sidebar.button("Sign out", use_container_width=True):
        for k in ["token", "role", "user", "email"]:
            st.session_state.pop(k, None)
        st.rerun()
