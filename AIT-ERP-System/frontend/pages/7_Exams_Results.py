import streamlit as st
import pandas as pd
from frontend.styles.theme import inject, hero, brand_sidebar
from frontend.components.auth_ui import require_auth, logout_button
from frontend.components.api_client import api_get, api_post

st.set_page_config(page_title="Exams • AiT", layout="wide")
inject(st); require_auth()
brand_sidebar(st, role=st.session_state.get("role", "")); logout_button()
hero(st, "Exams & Results", "Enter exam marks; GPA and grades are computed automatically.")

tab1, tab2 = st.tabs(["Add Result", "Result Records"])

with tab1:
    with st.form("exam_form"):
        sid = st.text_input("Student ID")
        etype = st.selectbox("Exam Type", ["entry", "mid", "final"])
        course = st.text_input("Course")
        level = st.text_input("Level")
        total = st.number_input("Total Marks", 1, 1000, 100)
        obtained = st.number_input("Obtained", 0, 1000, 0)
        remarks = st.text_input("Remarks")
        if st.form_submit_button("Save Result"):
            r = api_post("/api/exams", {
                "student_id": sid, "exam_type": etype, "course": course,
                "level": level, "total": int(total), "obtained": int(obtained), "remarks": remarks
            })
            st.success(f"Grade: {r.get('grade')} • GPA: {r.get('gpa')}")

with tab2:
    sid = st.text_input("Filter by Student ID")
    rows = api_get("/api/exams", params={"student_id": sid or None}) or []
    if rows:
        st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
    else:
        st.info("No results recorded.")