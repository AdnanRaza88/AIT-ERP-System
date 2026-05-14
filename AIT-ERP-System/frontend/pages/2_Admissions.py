import streamlit as st
from frontend.styles.theme import inject, hero, brand_sidebar
from frontend.components.auth_ui import require_auth, logout_button
from frontend.components.api_client import api_get, api_post

st.set_page_config(page_title="Admissions • AiT", layout="wide")
inject(st); require_auth()
brand_sidebar(st, role=st.session_state.get("role", "")); logout_button()
hero(st, "Admissions", "Manage entry tests, applications and approvals.")

DEPTS = ["AI & Data Science", "Python Development", "Web Development", "Game Development",
         "Cyber Security", "Software Architecture", "Graphic Designing & Video Editing",
         "English Language", "Arabic Language"]
LEVELS = ["IT Level 0", "Level 1", "Level 2", "Level 3"]
SHIFTS = ["Morning", "Afternoon", "Evening"]

tab1, tab2, tab3 = st.tabs(["New Application", "Pending Approvals", "Entry Tests"])

with tab1:
    with st.form("admission_form"):
        c1, c2, c3 = st.columns(3)
        full_name = c1.text_input("Full Name *")
        father_name = c2.text_input("Father Name")
        gender = c3.selectbox("Gender", ["Male", "Female", "Other"])

        c1, c2, c3 = st.columns(3)
        dob = c1.text_input("Date of Birth", placeholder="YYYY-MM-DD")
        cnic = c2.text_input("CNIC / B-Form")
        phone = c3.text_input("Phone")

        c1, c2, c3 = st.columns(3)
        whatsapp = c1.text_input("WhatsApp")
        email = c2.text_input("Email")
        city = c3.text_input("City")

        address = st.text_area("Address")
        prev_qual = st.text_input("Previous Qualification")

        c1, c2, c3 = st.columns(3)
        department = c1.selectbox("Department", DEPTS)
        course = c2.text_input("Course", value=department)
        level = c3.selectbox("Target Level", LEVELS, index=1)

        c1, c2 = st.columns(2)
        shift = c1.selectbox("Shift", SHIFTS)
        test_required = c2.checkbox("Take Entry Test", value=True,
                                    help="Uncheck if student wants to enroll directly into IT Level 0")

        if st.form_submit_button("Submit Application"):
            payload = {
                "full_name": full_name, "father_name": father_name, "gender": gender,
                "dob": dob, "cnic": cnic, "phone": phone, "whatsapp": whatsapp,
                "email": email or None, "address": address, "city": city,
                "previous_qualification": prev_qual, "department": department,
                "course": course, "level": level, "shift": shift,
                "test_required": test_required,
            }
            r = api_post("/api/admissions", payload)
            if "admission_id" in r:
                st.success(f"Application submitted. ID: {r['admission_id']}")
            else:
                st.error(r.get("error", "Failed"))

with tab2:
    rows = api_get("/api/admissions") or []
    pending = [r for r in rows if r.get("approval_status") == "pending"]
    if not pending:
        st.info("No pending applications.")
    for r in pending:
        with st.container():
            st.markdown(f"""<div class="ait-card">
                <b>{r['full_name']}</b> &nbsp; <span class="ait-pill">{r['admission_id']}</span><br/>
                {r['department']} • {r['course']} • {r['level']} • {r['shift']}<br/>
                Test: {r.get('test_status','-')} ({r.get('test_marks',0)}) — Recommended: {r.get('recommended_level') or '-'}
              </div>""", unsafe_allow_html=True)
            c1, c2, _ = st.columns([1, 1, 6])
            if c1.button("Approve", key=f"ap_{r['admission_id']}"):
                api_post(f"/api/admissions/{r['admission_id']}/approve", {})
                st.rerun()
            if c2.button("Reject", key=f"rj_{r['admission_id']}"):
                api_post(f"/api/admissions/{r['admission_id']}/reject", {})
                st.rerun()

with tab3:
    rows = api_get("/api/admissions") or []
    pending_test = [r for r in rows if r.get("test_required") and r.get("test_status") == "pending"]
    if not pending_test:
        st.info("No entry tests pending.")
    for r in pending_test:
        st.markdown(f"**{r['full_name']}** — {r['admission_id']}")
        marks = st.number_input(f"Marks for {r['admission_id']}", 0, 100, 0, key=f"m_{r['admission_id']}")
        if st.button("Submit Result", key=f"s_{r['admission_id']}"):
            res = api_post("/api/admissions/test-result",
                           {"admission_id": r["admission_id"], "test_marks": int(marks)})
            st.success(f"Result: {res.get('test_status')} — Recommended: {res.get('recommended_level')}")
            st.rerun()