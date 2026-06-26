import streamlit as st
import os
import html
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(
    page_title="ShareGuard SQL — by GP CUBE",
    page_icon="🛡️",
    layout="wide"
)

# ── Custom CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=Inter:wght@400;500&family=JetBrains+Mono:wght@400;500&display=swap');

:root {
    --bg:           #080C16;
    --surface:      #0D1425;
    --border:       #1A2640;
    --border-hi:    #2A3A5C;
    --cyan:         #00D4FF;
    --cyan-dim:     #007A99;
    --violet:       #7C3AED;
    --success:      #10F5A0;
    --warning:      #FFB800;
    --text-primary: #E2EDFF;
    --text-muted:   #6B7FA3;
    --text-dim:     #2A3A5C;
    --glow-cyan:    0 0 24px rgba(0, 212, 255, 0.25);
}

/* ── Base ── */
.stApp {
    background-color: var(--bg) !important;
    font-family: 'Inter', sans-serif;
}
.stApp > header { background: transparent !important; }
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 1.5rem !important; max-width: 1200px; }
h1, h2, h3 { font-family: 'Space Grotesk', sans-serif !important; color: var(--text-primary) !important; }
p, li { color: var(--text-primary) !important; }
hr { border-color: var(--border) !important; margin: 1.2rem 0 !important; }

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background-color: var(--surface) !important;
    border-right: 1px solid var(--border) !important;
}
[data-testid="stSidebar"] * { color: var(--text-primary) !important; }
[data-testid="stSidebar"] code {
    background: rgba(0,212,255,0.08) !important;
    color: var(--cyan) !important;
    border-radius: 4px; padding: 1px 5px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.78rem;
}

/* ── Text Area ── */
.stTextArea textarea {
    background-color: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    color: var(--text-primary) !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.95rem !important;
}
.stTextArea textarea:focus {
    border-color: var(--cyan) !important;
    box-shadow: var(--glow-cyan) !important;
}

/* ── Buttons ── */
.stButton > button {
    background: linear-gradient(135deg, #00B8D9, #6D28D9) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 8px !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.88rem !important;
    letter-spacing: 0.3px !important;
    transition: all 0.2s ease !important;
}
.stButton > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: var(--glow-cyan) !important;
    color: #fff !important;
}

/* ── Streamlit alerts ── */
.stAlert { border-radius: 8px !important; }

/* ─────────────────────────────────────────────────────────────
   CUSTOM COMPONENTS
───────────────────────────────────────────────────────────── */

/* Header Banner */
.sg-header {
    background: linear-gradient(135deg, var(--surface) 0%, #0B1628 100%);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1.4rem 1.8rem;
    margin-bottom: 1.5rem;
    position: relative;
    overflow: hidden;
}
.sg-header::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0; height: 2px;
    background: linear-gradient(90deg, var(--cyan), var(--violet), var(--cyan));
    background-size: 200% 100%;
    animation: header-shimmer 4s linear infinite;
}
@keyframes header-shimmer {
    0%   { background-position: -200% 0; }
    100% { background-position:  200% 0; }
}
.sg-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1.7rem;
    font-weight: 700;
    background: linear-gradient(90deg, var(--cyan) 0%, #A78BFA 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin: 0 0 0.25rem 0;
    letter-spacing: -0.3px;
    display: inline-block;
}
.sg-badge {
    display: inline-block;
    background: rgba(0,212,255,0.08);
    border: 1px solid rgba(0,212,255,0.25);
    color: var(--cyan);
    font-size: 0.65rem;
    font-family: 'JetBrains Mono', monospace;
    padding: 2px 7px; border-radius: 4px;
    margin-left: 0.6rem;
    vertical-align: middle;
    letter-spacing: 0.8px;
    -webkit-text-fill-color: var(--cyan);
}
.sg-subtitle {
    color: var(--text-muted);
    font-size: 0.87rem;
    margin: 0;
    font-family: 'Inter', sans-serif;
    -webkit-text-fill-color: var(--text-muted);
}

/* Section label */
.sg-label {
    color: var(--text-muted);
    font-size: 0.72rem;
    font-family: 'JetBrains Mono', monospace;
    letter-spacing: 1.2px;
    text-transform: uppercase;
    margin-bottom: 0.4rem;
    -webkit-text-fill-color: var(--text-muted);
}

/* Result Card */
.sg-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1.4rem 1.6rem;
    margin: 1rem 0;
    position: relative;
    overflow: hidden;
}
.sg-card::before {
    content: '';
    position: absolute;
    left: 0; top: 0; bottom: 0; width: 3px;
    background: linear-gradient(180deg, var(--cyan), var(--violet));
    border-radius: 3px 0 0 3px;
}

/* Question display */
.sg-q-label {
    color: var(--cyan);
    font-size: 0.68rem;
    font-family: 'JetBrains Mono', monospace;
    letter-spacing: 1.2px;
    text-transform: uppercase;
    margin-bottom: 0.3rem;
    -webkit-text-fill-color: var(--cyan);
}
.sg-q-text {
    color: var(--text-primary);
    font-size: 0.97rem;
    font-weight: 500;
    font-family: 'Space Grotesk', sans-serif;
    margin-bottom: 1.2rem;
    line-height: 1.5;
    -webkit-text-fill-color: var(--text-primary);
}

/* SQL block */
.sg-sql-header {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    margin-bottom: 0.5rem;
}
.sg-sql-label {
    color: var(--cyan);
    font-size: 0.68rem;
    font-family: 'JetBrains Mono', monospace;
    letter-spacing: 1.2px;
    text-transform: uppercase;
    -webkit-text-fill-color: var(--cyan);
}
.sg-sql-line {
    flex: 1; height: 1px;
    background: linear-gradient(90deg, var(--cyan-dim), transparent);
}
.sg-sql-tag {
    color: var(--text-dim);
    font-size: 0.62rem;
    font-family: 'JetBrains Mono', monospace;
    letter-spacing: 0.8px;
    -webkit-text-fill-color: var(--text-dim);
}
.sg-sql-block {
    background: #050810;
    border: 1px solid var(--border);
    border-left: 3px solid var(--cyan);
    border-radius: 8px;
    padding: 1.1rem 1.3rem;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.8rem;
    line-height: 1.75;
    color: #B8CCE8;
    overflow-x: auto;
    white-space: pre;
    box-shadow: inset 0 0 40px rgba(0,212,255,0.02), var(--glow-cyan);
    margin-bottom: 1.2rem;
    -webkit-text-fill-color: #B8CCE8;
}

/* Info row */
.sg-info-row {
    display: grid;
    grid-template-columns: 3fr 2fr;
    gap: 1rem;
}
.sg-info-box {
    background: #060A12;
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 0.9rem 1.1rem;
}
.sg-info-box-label {
    font-size: 0.68rem;
    font-family: 'JetBrains Mono', monospace;
    letter-spacing: 1.2px;
    text-transform: uppercase;
    margin-bottom: 0.5rem;
    color: var(--text-muted);
    -webkit-text-fill-color: var(--text-muted);
}
.sg-info-box-text {
    color: var(--text-primary);
    font-size: 0.86rem;
    line-height: 1.65;
    font-family: 'Inter', sans-serif;
    -webkit-text-fill-color: var(--text-primary);
}
.sg-review-pass { border-left: 3px solid var(--success) !important; }
.sg-review-fail { border-left: 3px solid var(--warning) !important; }
.sg-review-pass .sg-info-box-label { color: var(--success) !important; -webkit-text-fill-color: var(--success) !important; }
.sg-review-fail .sg-info-box-label { color: var(--warning) !important; -webkit-text-fill-color: var(--warning) !important; }
.sg-review-icon { font-size: 1rem; margin-right: 0.3rem; }

/* Empty state */
.sg-empty {
    text-align: center;
    padding: 3.5rem 1rem;
    border: 1px dashed var(--border);
    border-radius: 12px;
    margin-top: 1rem;
}
.sg-empty-icon { font-size: 2.5rem; opacity: 0.3; margin-bottom: 0.8rem; }
.sg-empty-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1rem;
    color: var(--text-muted);
    margin-bottom: 0.3rem;
    -webkit-text-fill-color: var(--text-muted);
}
.sg-empty-sub {
    font-size: 0.82rem;
    color: var(--text-dim);
    -webkit-text-fill-color: var(--text-dim);
}
</style>
""", unsafe_allow_html=True)


# ── Helper: render result card ───────────────────────────────────────────────
def render_result_card(result: dict):
    review = result["review"] or "No review returned."
    is_pass = "✅" in review

    st.markdown(f"""
<div class="sg-card">
    <div class="sg-q-label">▸ QUERY</div>
    <div class="sg-q-text">{html.escape(result['question'])}</div>
</div>
""", unsafe_allow_html=True)

    st.markdown('<div class="sg-sql-label" style="color:#00D4FF; font-family:monospace; font-size:0.72rem; letter-spacing:1.2px; text-transform:uppercase; margin-bottom:0.3rem;">📝 Generated SQL</div>', unsafe_allow_html=True)
    st.code(result["sql"] or "", language="sql")

    col_exp, col_rev = st.columns([3, 2])
    with col_exp:
        st.markdown('<div class="sg-sql-label" style="color:#6B7FA3; font-family:monospace; font-size:0.72rem; letter-spacing:1.2px; text-transform:uppercase; margin-bottom:0.3rem;">💬 Explanation</div>', unsafe_allow_html=True)
        st.markdown(result["explanation"] or "No explanation returned.")
    with col_rev:
        st.markdown('<div class="sg-sql-label" style="color:#6B7FA3; font-family:monospace; font-size:0.72rem; letter-spacing:1.2px; text-transform:uppercase; margin-bottom:0.3rem;">🔎 Self-Review</div>', unsafe_allow_html=True)
        if is_pass:
            st.success(review)
        else:
            st.warning(review)

    st.divider()

# ── API key ──────────────────────────────────────────────────────────────────
api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    try:
        api_key = st.secrets["GROQ_API_KEY"]
    except Exception:
        api_key = None

if not api_key:
    st.error("⚠️ No API key found. Set GROQ_API_KEY in .env or Streamlit secrets.")
    st.stop()

from rag import generate_sql


# ── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
<div style="padding: 0.5rem 0 1rem 0;">
    <div style="font-family:'Space Grotesk',sans-serif; font-size:1.1rem; font-weight:700;
                background:linear-gradient(90deg,#00D4FF,#A78BFA);
                -webkit-background-clip:text; -webkit-text-fill-color:transparent;
                background-clip:text;">
        🛡️ ShareGuard SQL
    </div>
    <div style="font-size:0.72rem; font-family:'JetBrains Mono',monospace;
                color:#6B7FA3; letter-spacing:0.8px; margin-top:0.2rem;
                -webkit-text-fill-color:#6B7FA3;">
        by GP CUBE · v2.0
    </div>
</div>
""", unsafe_allow_html=True)

    st.markdown("**📋 Schema Reference**")
    st.markdown("""
**FACT_WS_SESSIONS**
- STAT_ID, CALENDAR_D_KEY
- CUSTOMER_D_KEY, USER_D_KEY
- STAT_COLLECTED_DATE *(Timestamp)*
- EVENT_DATA *(VARIANT — JSON)*
  - `EVENT_DATA:windows_credential::VARCHAR`
  - `EVENT_DATA:computer_name::VARCHAR`

**DIM_USER**
- USER_D_KEY, UUID, LOGIN_ID
- FIRSTNAME, LASTNAME, FULL_NAME
- USER_PERMISSIONED *('Yes' = active)*
- ENTITLEMENT_TYPE

**DIM_CUSTOMER**
- CUSTOMER_D_KEY, A_NUMBER
- ACCOUNT, COUNTRY, REGION
- ORGANISATION_TYPE, CUSTOMER_CHANNEL

**DIM_CALENDAR**
- CALENDAR_D_KEY, CALENDAR_DATE
- YEAR, MONTH, MONTH_NAME, QUARTER
""")

    st.divider()
    st.markdown("**💡 Try these:**")
    examples = [
        "LOGIN_IDs with 2+ distinct Windows credentials, last 3 months",
        "Top 10 accounts by flagged LOGIN_IDs this quarter",
        "All sessions from APAC region with 3+ computer names",
        "Active EMEA users and their account info",
        "Inactive users still appearing in sessions",
    ]
    for ex in examples:
        st.markdown(f"<div style='font-size:0.78rem; color:#6B7FA3; padding:2px 0; -webkit-text-fill-color:#6B7FA3;'>› {ex}</div>",
                    unsafe_allow_html=True)


# ── Header ───────────────────────────────────────────────────────────────────
st.markdown("""
<div class="sg-header">
    <div>
        <span class="sg-title">🛡️ ShareGuard SQL</span>
        <span class="sg-badge">BETA</span>
        <span class="sg-badge" style="margin-left:0.3rem; border-color:rgba(124,58,237,0.3);
              background:rgba(124,58,237,0.08); color:#A78BFA;
              -webkit-text-fill-color:#A78BFA;">GROQ · LLAMA 3.3 70B</span>
    </div>
    <p class="sg-subtitle">by GP CUBE &nbsp;·&nbsp; Schema-aware Snowflake SQL generator with self-review</p>
</div>
""", unsafe_allow_html=True)


# ── Session state ────────────────────────────────────────────────────────────
if "history" not in st.session_state:
    st.session_state.history = []


# ── Input ────────────────────────────────────────────────────────────────────
st.markdown('<div class="sg-label">Describe what you want to find</div>', unsafe_allow_html=True)
user_question = st.text_area(
    label="question",
    placeholder="e.g. Show all LOGIN_IDs that have more than 2 distinct Windows credentials in the last 3 months",
    height=80,
    label_visibility="collapsed"
)

col1, col2 = st.columns([1, 5])
with col1:
    generate_btn = st.button("🛡️ Generate SQL", type="primary", use_container_width=True)
with col2:
    if st.button("🗑️ Clear history", use_container_width=True):
        st.session_state.history = []
        st.rerun()


# ── Generate ─────────────────────────────────────────────────────────────────
if generate_btn and user_question.strip():
    with st.spinner("Running schema-aware generation + self-review..."):
        result = generate_sql(user_question.strip())
    if result["error"]:
        st.error(f"❌ {result['error']}")
    else:
        st.session_state.history.insert(0, result)
elif generate_btn and not user_question.strip():
    st.warning("Enter a question first.")


# ── Results ───────────────────────────────────────────────────────────────────
if st.session_state.history:
    st.markdown(f'<div class="sg-label" style="margin-top:1rem;">{len(st.session_state.history)} result(s) — most recent first</div>',
                unsafe_allow_html=True)
    for result in st.session_state.history:
        render_result_card(result)
else:
    st.markdown("""
<div class="sg-empty">
    <div class="sg-empty-icon">🛡️</div>
    <div class="sg-empty-title">Ready to generate</div>
    <div class="sg-empty-sub">Enter a plain-English question above → get schema-aware Snowflake SQL + self-review</div>
</div>
""", unsafe_allow_html=True)