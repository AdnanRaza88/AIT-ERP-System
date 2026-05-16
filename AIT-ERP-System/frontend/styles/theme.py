THEME_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

:root {
  --ait-green: #10b981;
  --ait-green-dark: #059669;
  --ait-green-soft: #d1fae5;
  --ait-bg: #f0f4f8;
  --ait-surface: #ffffff;
  --ait-text: #0f172a;
  --ait-muted: #64748b;
}

html, body, [class*="css"] {
  font-family: 'Inter', sans-serif !important;
  color: var(--ait-text);
}

.stApp {
  background: linear-gradient(135deg, #f0f4f8 0%, #e8f5ee 100%);
}

section[data-testid="stSidebar"] {
  background: rgba(255,255,255,0.85);
  backdrop-filter: blur(20px);
  border-right: 1px solid rgba(16,185,129,0.15);
}

.ait-hero {
  background: linear-gradient(135deg, #ffffff 0%, #f0fdf4 100%);
  border-radius: 24px;
  padding: 32px 36px;
  margin-bottom: 28px;
  box-shadow:
    20px 20px 60px #d4dde4,
    -20px -20px 60px #ffffff;
  border: 1px solid rgba(16,185,129,0.08);
}
.ait-hero h1 { margin:0; font-weight:800; font-size:28px; letter-spacing:-0.5px;}
.ait-hero p  { color: var(--ait-muted); margin-top:6px; }

.ait-card {
  background: var(--ait-surface);
  border-radius: 20px;
  padding: 22px 24px;
  box-shadow:
    12px 12px 32px rgba(212,221,228,0.55),
    -12px -12px 32px rgba(255,255,255,0.9);
  transition: transform .25s ease, box-shadow .25s ease;
  border: 1px solid rgba(16,185,129,0.06);
}
.ait-card:hover {
  transform: translateY(-4px);
  box-shadow:
    16px 16px 40px rgba(212,221,228,0.7),
    -16px -16px 40px rgba(255,255,255,1),
    0 0 0 1px rgba(16,185,129,0.18);
}

.ait-metric {
  display:flex; flex-direction:column; gap:6px;
}
.ait-metric .label { color: var(--ait-muted); font-size:13px; font-weight:500; text-transform:uppercase; letter-spacing:0.6px;}
.ait-metric .value { font-size:30px; font-weight:800; color: var(--ait-text);}
.ait-metric .delta { color: var(--ait-green-dark); font-size:12px; font-weight:600; }

.ait-pill {
  display:inline-block;
  padding: 4px 12px;
  border-radius: 999px;
  background: var(--ait-green-soft);
  color: var(--ait-green-dark);
  font-size: 12px;
  font-weight: 600;
}

.ait-brand {
  display:flex; align-items:center; gap:12px;
  padding: 14px 4px 22px;
}
.ait-brand .logo {
  width:44px; height:44px; border-radius:14px;
  background: linear-gradient(135deg, var(--ait-green) 0%, var(--ait-green-dark) 100%);
  display:flex; align-items:center; justify-content:center;
  color:white; font-weight:800; font-size:18px;
  box-shadow: 0 8px 24px rgba(16,185,129,0.35);
}
.ait-brand .meta h3 { margin:0; font-size:16px; font-weight:800;}
.ait-brand .meta span { color:var(--ait-muted); font-size:11px;}

div.stButton > button {
  background: linear-gradient(135deg, var(--ait-green) 0%, var(--ait-green-dark) 100%);
  color: white; border: none; border-radius: 12px;
  padding: 10px 22px; font-weight: 600;
  box-shadow: 0 6px 20px rgba(16,185,129,0.35);
  transition: all .2s ease;
}
div.stButton > button:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 28px rgba(16,185,129,0.45);
}

div[data-testid="stTextInput"] input,
div[data-testid="stNumberInput"] input,
div[data-testid="stDateInput"] input,
div[data-testid="stSelectbox"] div[data-baseweb="select"] {
  border-radius: 12px !important;
  border: 1px solid rgba(16,185,129,0.18) !important;
  background: #ffffff !important;
  box-shadow: inset 4px 4px 10px #eef2f7, inset -4px -4px 10px #ffffff;
}

.stDataFrame, .stTable {
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 8px 24px rgba(15,23,42,0.06);
}

#ait-chat-fab {
  position: fixed; bottom: 28px; right: 28px;
  width: 60px; height: 60px; border-radius: 50%;
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  display:flex; align-items:center; justify-content:center;
  color: white; font-size: 26px;
  box-shadow: 0 12px 32px rgba(16,185,129,0.5);
  cursor:pointer; z-index: 99999;
}
</style>
"""


def inject(st):
    st.markdown(THEME_CSS, unsafe_allow_html=True)


def hero(st, title: str, subtitle: str = ""):
    st.markdown(
        f"""<div class="ait-hero">
              <h1>{title}</h1>
              <p>{subtitle}</p>
            </div>""",
        unsafe_allow_html=True,
    )


def metric_card(st, label: str, value, delta: str = ""):
    st.markdown(
        f"""<div class="ait-card">
              <div class="ait-metric">
                <span class="label">{label}</span>
                <span class="value">{value}</span>
                <span class="delta">{delta}</span>
              </div>
            </div>""",
        unsafe_allow_html=True,
    )


def brand_sidebar(st, role: str = ""):
    st.sidebar.markdown(
        f"""<div class="ait-brand">
              <div class="logo">A</div>
              <div class="meta">
                <h3>AiT ERP</h3>
                <span>AL-KHAIR INSTITUTE OF TECHNOLOGY</span>
              </div>
            </div>
            <div class="ait-pill" style="margin-bottom:18px;">{role}</div>""",
        unsafe_allow_html=True,
    )