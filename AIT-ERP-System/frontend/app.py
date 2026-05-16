import streamlit as st
from styles.theme import inject, brand_sidebar, hero, metric_card
from components.auth_ui import require_auth, logout_button
from components.api_client import login
from frontend.components.auth_ui import require_auth, logout_button
from frontend.components.api_client import api_get

st.set_page_config(page_title="AiT ERP", page_icon="🟢", layout="wide", initial_sidebar_state="expanded")
inject(st)
require_auth()

brand_sidebar(st, role=st.session_state.get("role", "user"))
st.sidebar.markdown(f"**Signed in as**  \n{st.session_state.get('user')}")
logout_button()

hero(st, f"Welcome back, {st.session_state.get('user', 'User')}",
     "Your unified control center for AL-KHAIR INSTITUTE OF TECHNOLOGY.")

ov = api_get("/api/analytics/overview")
att = api_get("/api/analytics/attendance")
res = api_get("/api/analytics/results")

c1, c2, c3, c4 = st.columns(4)
with c1: metric_card(st, "Total Students", ov.get("total_students", 0), "active enrollments")
with c2: metric_card(st, "Total Teachers", ov.get("total_teachers", 0), "faculty members")
with c3: metric_card(st, "Revenue Collected", f"PKR {ov.get('total_revenue', 0):,}", "all-time")
with c4: metric_card(st, "Pending Dues", f"PKR {ov.get('pending_dues', 0):,}", "outstanding")

st.markdown("###")
c5, c6, c7 = st.columns(3)
with c5: metric_card(st, "Avg Attendance", f"{att.get('present_pct', 0)}%", "across all sessions")
with c6: metric_card(st, "Avg Exam Score", res.get("avg_score", 0), "all results")
with c7: metric_card(st, "Pass Rate", f"{res.get('pass_rate', 0)}%", "across all exams")

st.markdown("###")
st.markdown(
    """<div class="ait-card">
         <h3 style="margin-top:0;">Navigation</h3>
         <p style="color:#64748b;">Use the sidebar to navigate between modules: Admissions, Students, Teachers, Attendance, Fees, Exams, HR, Analytics and the AI Assistant.</p>
       </div>""",
    unsafe_allow_html=True,
)

st.markdown(
    """<div id="ait-chat-fab" onclick="window.location.href='/AI_Assistant'">💬</div>""",
    unsafe_allow_html=True,
)
