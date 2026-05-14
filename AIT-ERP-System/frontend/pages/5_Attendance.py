import streamlit as st
import pandas as pd
from datetime import date
from frontend.styles.theme import inject, hero, brand_sidebar
from frontend.components.auth_ui import require_auth, logout_button
from frontend.components.api_client import api_get, api_post

st.set_page_config(page_title="Attendance • AiT", layout="wide")
inject(st); require_auth()
brand_sidebar(st, role=st.session_state.get("role", "")); logout_button()
hero(st, "Attendance", "Mark and review daily attendance records.")

tab1, tab2 = st.tabs(["Mark Attendance", "View History"])

with tab1:
    c1, c2, c3, c4 = st.columns(4)
    ptype = c1.selectbox("Type", ["student", "teacher"])
    pid = c2.text_input("Person ID")
    d = c3.date_input("Date", value=date.today())
    status = c4.selectbox("Status", ["present", "absent", "leave"])
    remarks = st.text_input("Remarks")
    if st.button("Save Attendance"):
        api_post("/api/attendance", {
            "person_type": ptype, "person_id": pid, "date": str(d),
            "status": status, "remarks": remarks
        })
        st.success("Attendance recorded.")

with tab2:
    pid = st.text_input("Lookup by Person ID")
    if pid:
        rows = api_get(f"/api/attendance/{pid}") or []
        if rows:
            st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
        else:
            st.info("No records.")