import streamlit as st
import pandas as pd
from frontend.styles.theme import inject, hero, brand_sidebar
from frontend.components.auth_ui import require_auth, logout_button
from frontend.components.api_client import api_get, api_post

st.set_page_config(page_title="Fees • AiT", layout="wide")
inject(st); require_auth()
brand_sidebar(st, role=st.session_state.get("role", "")); logout_button()
hero(st, "Fees & Invoices", "Generate invoices, track payments and dues.")

tab1, tab2 = st.tabs(["Generate Invoice", "Records"])

with tab1:
    with st.form("fee_form"):
        sid = st.text_input("Student ID")
        month = st.text_input("Month (e.g. 2025-01)")
        amount = st.number_input("Amount", 0, 1000000, 15000, step=500)
        paid = st.number_input("Paid Amount", 0, 1000000, 0, step=500)
        method = st.selectbox("Method", ["cash", "bank_transfer", "card", "online"])
        if st.form_submit_button("Create Invoice"):
            r = api_post("/api/fees", {
                "student_id": sid, "month": month, "amount": int(amount),
                "paid_amount": int(paid), "method": method
            })
            st.success(f"Invoice: {r.get('invoice_no')} • Status: {r.get('status')}")

with tab2:
    sid = st.text_input("Filter by Student ID")
    rows = api_get("/api/fees", params={"student_id": sid or None}) or []
    if rows:
        st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
    else:
        st.info("No records.")