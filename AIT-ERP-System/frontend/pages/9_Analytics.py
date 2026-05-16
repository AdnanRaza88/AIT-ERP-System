import streamlit as st
import pandas as pd
import plotly.express as px
from frontend.styles.theme import inject, hero, brand_sidebar
from frontend.components.auth_ui import require_auth, logout_button
from frontend.components.api_client import api_get

st.set_page_config(page_title="Analytics • AiT", layout="wide")
inject(st); require_auth()
brand_sidebar(st, role=st.session_state.get("role", "")); logout_button()
hero(st, "Analytics", "Operational insights powered by Pandas & NumPy.")

ov = api_get("/api/analytics/overview") or {}
att = api_get("/api/analytics/attendance") or {}
courses = api_get("/api/analytics/courses") or []
enroll = api_get("/api/analytics/enrollment") or []
results = api_get("/api/analytics/results") or {}

c1, c2 = st.columns(2)
with c1:
    st.markdown("#### Course Distribution")
    if courses:
        df = pd.DataFrame(courses)
        fig = px.pie(df, names="course", values="students", hole=0.55,
                     color_discrete_sequence=px.colors.sequential.Greens_r)
        fig.update_layout(showlegend=True, height=360, margin=dict(t=10, b=10))
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No data yet.")

with c2:
    st.markdown("#### Enrollment Growth")
    if enroll:
        df = pd.DataFrame(enroll)
        fig = px.area(df, x="month", y="count", color_discrete_sequence=["#10b981"])
        fig.update_layout(height=360, margin=dict(t=10, b=10))
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No data yet.")

c3, c4 = st.columns(2)
with c3:
    st.markdown("#### Attendance Composition")
    df_att = pd.DataFrame([
        {"status": "Present", "pct": att.get("present_pct", 0)},
        {"status": "Absent",  "pct": att.get("absent_pct", 0)},
        {"status": "Leave",   "pct": att.get("leave_pct", 0)},
    ])
    fig = px.bar(df_att, x="status", y="pct", color="status",
                 color_discrete_sequence=["#10b981", "#ef4444", "#f59e0b"])
    fig.update_layout(height=360, showlegend=False, margin=dict(t=10, b=10))
    st.plotly_chart(fig, use_container_width=True)

with c4:
    st.markdown("#### Exam Performance")
    st.metric("Average Score", results.get("avg_score", 0))
    st.metric("Pass Rate", f"{results.get('pass_rate', 0)}%")
    st.metric("Total Revenue", f"PKR {ov.get('total_revenue', 0):,}")