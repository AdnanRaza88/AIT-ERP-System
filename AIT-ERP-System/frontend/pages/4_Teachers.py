import streamlit as st
import pandas as pd
from frontend.styles.theme import inject, hero, brand_sidebar
from frontend.components.auth_ui import require_auth, logout_button
from frontend.components.api_client import api_get, api_post

st.set_page_config(page_title="Teachers • AiT", layout="wide")
inject(st); require_auth()
brand_sidebar(st, role=st.session_state.get("role", "")); logout_button()
hero(st, "Teachers", "Manage faculty profiles and course assignments.")

tab1, tab2 = st.tabs(["Faculty Directory", "Add Teacher"])

with tab1:
    rows = api_get("/api/teachers") or []
    if rows:
        st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
    else:
        st.info("No teachers yet.")

with tab2:
    with st.form("teacher_form"):
        name = st.text_input("Full Name *")
        email = st.text_input("Email *")
        phone = st.text_input("Phone")
        qual = st.text_input("Qualification")
        exp = st.number_input("Experience (years)", 0, 50, 0)
        dept = st.text_input("Department")
        courses = st.text_input("Courses Assigned (comma-separated)")
        salary = st.number_input("Salary (PKR)", 0, 1000000, 50000, step=1000)
        if st.form_submit_button("Add Teacher"):
            r = api_post("/api/teachers", {
                "full_name": name, "email": email, "phone": phone,
                "qualification": qual, "experience_years": int(exp),
                "department": dept, "courses_assigned": courses, "salary": int(salary),
            })
            if "teacher_id" in r:
                st.success(f"Teacher added: {r['teacher_id']}")
            else:
                st.error(r.get("error", "Failed"))