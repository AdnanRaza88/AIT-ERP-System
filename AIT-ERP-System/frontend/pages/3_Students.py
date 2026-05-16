import streamlit as st
import pandas as pd
from frontend.styles.theme import inject, hero, brand_sidebar
from frontend.components.auth_ui import require_auth, logout_button
from frontend.components.api_client import api_get, api_put

st.set_page_config(page_title="Students • AiT", layout="wide")
inject(st); require_auth()
brand_sidebar(st, role=st.session_state.get("role", "")); logout_button()
hero(st, "Students", "Search, filter and manage student profiles.")

c1, c2 = st.columns([3, 1])
search = c1.text_input("Search by name")
dept = c2.text_input("Filter by department")

rows = api_get("/api/students", params={"search": search or None, "department": dept or None}) or []

if rows:
    df = pd.DataFrame(rows)
    st.dataframe(df, use_container_width=True, hide_index=True)
else:
    st.info("No students found.")

st.markdown("### Update Student")
sid = st.text_input("Student ID (e.g. AIT-STD-2025-00001)")
if sid:
    s = api_get(f"/api/students/{sid}")
    if "student_id" in s:
        with st.form("update_form"):
            name = st.text_input("Full Name", s.get("full_name", ""))
            phone = st.text_input("Phone", s.get("phone", ""))
            email = st.text_input("Email", s.get("email", ""))
            status = st.selectbox("Status", ["active", "suspended", "graduated"],
                                  index=0 if s.get("status") == "active" else 0)
            if st.form_submit_button("Save"):
                api_put(f"/api/students/{sid}",
                        {"full_name": name, "phone": phone, "email": email, "status": status})
                st.success("Updated.")