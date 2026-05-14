# AiT — AL-KHAIR INSTITUTE OF TECHNOLOGY ERP

A production-grade institute management ERP built with FastAPI, Streamlit, SQLAlchemy and a Python data-science stack.

## Features
- JWT-secured FastAPI backend with role-based access control
- Admissions workflow (entry test → recommendation → approval → student creation)
- Students, Teachers, Attendance, Fees, Exams, HR/Recruitment modules
- AI assistant (rule-based, FastAPI endpoint, extensible knowledge base)
- Analytics powered by Pandas / NumPy / Plotly
- Neumorphism + glassmorphism Streamlit UI (green & white)

## Quickstart

```bash
python -m venv .venv && source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt