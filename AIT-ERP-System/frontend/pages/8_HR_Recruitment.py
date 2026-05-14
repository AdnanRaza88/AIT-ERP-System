import streamlit as st
import pandas as pd
from frontend.styles.theme import inject, hero, brand_sidebar
from frontend.components.auth_ui import require_auth, logout_button
from frontend.components.api_client import api_get, api_post

st.set_page_config(page_title="HR • AiT", layout="wide")
inject(st); require_auth()
brand_sidebar(st, role=st.session_state.get("role", "")); logout_button()
hero(st, "HR & Recruitment", "Job postings, applicants and hiring pipeline.")

tab1, tab2, tab3 = st.tabs(["Open Jobs", "Post a Job", "Applicants"])

with tab1:
    jobs = api_get("/api/hr/jobs") or []
    if jobs:
        st.dataframe(pd.DataFrame(jobs), use_container_width=True, hide_index=True)
    else:
        st.info("No jobs posted.")

with tab2:
    with st.form("job_form"):
        title = st.text_input("Title *")
        dept = st.text_input("Department")
        ptype = st.selectbox("Position Type", ["Teacher", "Assistant Trainer", "Office Staff", "Lab Staff"])
        desc = st.text_area("Description")
        if st.form_submit_button("Publish Job"):
            r = api_post("/api/hr/jobs", {"title": title, "department": dept,
                                          "position_type": ptype, "description": desc})
            st.success(f"Published: {r.get('title')}")

with tab3:
    apps = api_get("/api/hr/applicants") or []
    if apps:
        st.dataframe(pd.DataFrame(apps), use_container_width=True, hide_index=True)
        aid = st.number_input("Applicant ID to hire", 0, 999999, 0)
        if st.button("Mark as Hired") and aid:
            api_post(f"/api/hr/applicants/{int(aid)}/hire", {})
            st.success("Hired.")
            st.rerun()
    else:
        st.info("No applicants yet.")