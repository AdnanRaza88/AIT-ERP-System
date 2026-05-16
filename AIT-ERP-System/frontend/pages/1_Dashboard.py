import streamlit as st
from frontend.styles.theme import inject, hero, brand_sidebar, metric_card
from frontend.components.auth_ui import require_auth, logout_button
from frontend.components.api_client import api_get

st.set_page_config(page_title="Dashboard • AiT", layout="wide")
inject(st); require_auth()
brand_sidebar(st, role=st.session_state.get("role", "")); logout_button()
hero(st, "Smart Dashboard", "Real-time overview of institute operations.")

ov = api_get("/api/analytics/overview") or {}
c1, c2, c3, c4 = st.columns(4)
with c1: metric_card(st, "Students", ov.get("total_students", 0), "enrolled")
with c2: metric_card(st, "Teachers", ov.get("total_teachers", 0), "active")
with c3: metric_card(st, "Revenue", f"PKR {ov.get('total_revenue', 0):,}", "lifetime")
with c4: metric_card(st, "Dues", f"PKR {ov.get('pending_dues', 0):,}", "pending")