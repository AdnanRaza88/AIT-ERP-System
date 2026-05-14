import requests
import streamlit as st

BASE_URL = st.secrets.get("API_BASE", "http://localhost:8000") if hasattr(st, "secrets") else "http://localhost:8000"


def _headers():
    token = st.session_state.get("token")
    return {"Authorization": f"Bearer {token}"} if token else {}


def login(email: str, password: str):
    r = requests.post(f"{BASE_URL}/api/auth/login",
                      data={"username": email, "password": password})
    return r.json() if r.ok else {"error": r.text}


def api_get(path: str, params: dict | None = None):
    r = requests.get(f"{BASE_URL}{path}", headers=_headers(), params=params or {})
    return r.json() if r.ok else {"error": r.text, "status": r.status_code}


def api_post(path: str, payload: dict):
    r = requests.post(f"{BASE_URL}{path}", headers=_headers(), json=payload)
    return r.json() if r.ok else {"error": r.text, "status": r.status_code}


def api_put(path: str, payload: dict):
    r = requests.put(f"{BASE_URL}{path}", headers=_headers(), json=payload)
    return r.json() if r.ok else {"error": r.text, "status": r.status_code}