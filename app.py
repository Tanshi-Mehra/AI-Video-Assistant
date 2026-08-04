import streamlit as st
import time
from dotenv import load_dotenv
from core.rag_engine import ask_question
from main import run_pipeline

load_dotenv()

# ─── Page Config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AI Video Assistant",
    page_icon="🎞️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Custom CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,500;9..144,600;9..144,700&family=Inter:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500;600&display=swap');

/* ── Tokens ── */
:root {
    --bg: #F7F6F1;
    --surface: #FFFFFF;
    --surface-2: #EFEDE3;
    --border: #DFDBCC;
    --ink: #1B1C18;
    --ink-muted: #7A7A6E;
    --accent: #2445B0;
    --accent-soft: #E7ECFA;
    --accent-2: #C97A2B;
    --accent-2-soft: #FBEBD6;
    --success: #2F7D4F;
    --success-soft: #E4F2E9;
    --danger: #B23B3B;
    --danger-soft: #FBE7E7;
}

/* ── Global ── */
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    background-color: var(--bg) !important;
    color: var(--ink) !important;
}
.stApp { background: var(--bg) !important; }

h1, h2, h3, h4, h5, h6 {
    font-family: 'Fraunces', serif !important;
    color: var(--ink) !important;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: var(--surface) !important;
    border-right: 1px solid var(--border) !important;
}
[data-testid="stSidebar"] * { color: var(--ink) !important; }

.side-mark {
    font-family: 'Fraunces', serif;
    font-size: 1.5rem;
    font-weight: 700;
    line-height: 1.15;
}
.side-mark span { color: var(--accent); }

.side-label {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.68rem;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: var(--ink-muted);
    margin: 1.4rem 0 0.5rem 0;
}

/* ── Hero ── */
.hero-title {
    font-family: 'Fraunces', serif;
    font-size: clamp(2.1rem, 4.6vw, 3.4rem);
    font-weight: 700;
    letter-spacing: -0.02em;
    line-height: 1.08;
    margin: 0;
    color: var(--ink);
}
.hero-title span { color: var(--accent); }

.hero-sub {
    font-family: 'Inter', sans-serif;
    font-size: 1rem;
    color: var(--ink-muted);
    margin-top: 0.6rem;
    max-width: 46ch;
}

.hero-wave { margin: 1.4rem 0 0.4rem 0; }

/* ── Section eyebrow (numbered, real reading order) ── */
.eyebrow {
    display: flex;
    align-items: center;
    gap: 0.55rem;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.72rem;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: var(--ink-muted);
    padding-bottom: 0.7rem;
    margin-bottom: 0.9rem;
    border-bottom: 1px solid var(--border);
}
.eyebrow .idx { color: var(--accent); font-weight: 600; }

/* ── Cards ── */
.card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 1.5rem;
    margin-bottom: 1rem;
    box-shadow: 0 1px 2px rgba(27,28,24,0.03);
    transition: box-shadow 0.2s, border-color 0.2s;
}
.card:hover {
    border-color: #C8C4B4;
    box-shadow: 0 4px 14px rgba(27,28,24,0.06);
}
.card-content {
    font-size: 0.92rem;
    line-height: 1.75;
    color: var(--ink);
}

/* ── Badges ── */
.badge {
    display: inline-block;
    padding: 0.22rem 0.65rem;
    border-radius: 5px;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.68rem;
    font-weight: 500;
    letter-spacing: 0.06em;
}
.badge-accent { background: var(--accent-soft); color: var(--accent); }
.badge-amber  { background: var(--accent-2-soft); color: var(--accent-2); }
.badge-green  { background: var(--success-soft); color: var(--success); }

/* ── Inputs & Buttons ── */
.stTextInput > div > div > input,
.stSelectbox > div > div {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: 7px !important;
    color: var(--ink) !important;
    font-family: 'Inter', sans-serif !important;
}
.stTextInput > div > div > input:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 3px var(--accent-soft) !important;
}

.stButton > button {
    background: var(--ink) !important;
    color: var(--bg) !important;
    border: none !important;
    border-radius: 7px !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.88rem !important;
    padding: 0.55rem 1.4rem !important;
    transition: transform 0.15s, background 0.15s !important;
}
.stButton > button:hover {
    background: var(--accent) !important;
    transform: translateY(-1px) !important;
}
.stButton > button[kind="secondary"] {
    background: var(--surface) !important;
    color: var(--ink) !important;
    border: 1px solid var(--border) !important;
}
.stButton > button[kind="secondary"]:hover {
    background: var(--surface-2) !important;
    color: var(--ink) !important;
}

/* ── Pipeline status (sidebar) ── */
.stage-row {
    display: flex;
    align-items: center;
    gap: 0.7rem;
    padding: 0.55rem 0.7rem;
    background: var(--surface-2);
    border-radius: 7px;
    margin: 0.35rem 0;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.75rem;
}
.stage-num {
    font-weight: 600;
    color: var(--ink-muted);
    width: 1.4rem;
}
.stage-dot { width: 7px; height: 7px; border-radius: 50%; flex-shrink: 0; }
.dot-active  { background: var(--accent); animation: pulse 1.4s infinite; }
.dot-done    { background: var(--success); }
.dot-pending { background: var(--border); }
@keyframes pulse { 0%, 100% { opacity: 1; } 50% { opacity: 0.35; } }

/* ── Chat ── */
.chat-container {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 1.25rem;
    max-height: 420px;
    overflow-y: auto;
    margin-bottom: 1rem;
}
.chat-msg { margin-bottom: 1rem; display: flex; flex-direction: column; gap: 0.25rem; }
.chat-label {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: var(--ink-muted);
}
.chat-bubble {
    display: inline-block;
    padding: 0.6rem 1rem;
    border-radius: 9px;
    font-size: 0.88rem;
    line-height: 1.6;
    max-width: 90%;
}
.user-bubble { background: var(--ink); color: var(--bg); align-self: flex-end; }
.bot-bubble  { background: var(--accent-soft); color: var(--ink); align-self: flex-start; }

/* ── Divider ── */
hr { border: none !important; border-top: 1px solid var(--border) !important; margin: 1.6rem 0 !important; }

/* ── Transcript box (monospace, reads like a raw feed) ── */
.transcript-box {
    background: var(--surface-2);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 1.1rem;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.78rem;
    line-height: 1.8;
    max-height: 300px;
    overflow-y: auto;
    color: var(--ink);
    white-space: pre-wrap;
    word-break: break-word;
}

/* ── Streamlit element restyling ── */
.stProgress > div > div > div { background: var(--accent) !important; }
.stSpinner > div { border-top-color: var(--accent) !important; }
[data-testid="stMarkdownContainer"] p { color: var(--ink) !important; }
label { color: var(--ink-muted) !important; font-size: 0.8rem !important; }
[data-testid="stAlert"] { border-radius: 8px !important; }

::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: var(--bg); }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: var(--accent); }
</style>
""", unsafe_allow_html=True)

# ─── Session State Init ──────────────────────────────────────────────────────────
for key, default in {
    "result": None,
    "chat_history": [],
    "processing": False,
    "pipeline_done": False,
    "pipeline_steps": {},
}.items():
    if key not in st.session_state:
        st.session_state[key] = default

# ─── Helpers ────────────────────────────────────────────────────────────────────
def stage_status(steps: dict, key: str) -> str:
    s = steps.get(key, "pending")
    if s == "active": return "dot-active"
    if s == "done":   return "dot-done"
    return "dot-pending"

def render_stage_row(num: str, label: str, key: str):
    css = stage_status(st.session_state.pipeline_steps, key)
    st.markdown(f"""
    <div class="stage-row">
        <span class="stage-num">{num}</span>
        <div class="stage-dot {css}"></div>
        <span>{label}</span>
    </div>""", unsafe_allow_html=True)

def eyebrow(idx: str, label: str):
    st.markdown(f"""
    <div class="eyebrow"><span class="idx">{idx}</span><span>{label}</span></div>
    """, unsafe_allow_html=True)

WAVEFORM_SVG = """
<svg class="hero-wave" width="220" height="28" viewBox="0 0 220 28" fill="none" xmlns="http://www.w3.org/2000/svg">
  <g fill="#2445B0">
    <rect x="0"   y="10" width="3" height="8"  rx="1.5"/>
    <rect x="7"   y="4"  width="3" height="20" rx="1.5"/>
    <rect x="14"  y="12" width="3" height="4"  rx="1.5"/>
    <rect x="21"  y="0"  width="3" height="28" rx="1.5"/>
    <rect x="28"  y="8"  width="3" height="12" rx="1.5"/>
    <rect x="35"  y="6"  width="3" height="16" rx="1.5"/>
  </g>
  <g fill="#C97A2B">
    <rect x="45"  y="11" width="3" height="6"  rx="1.5"/>
    <rect x="52"  y="2"  width="3" height="24" rx="1.5"/>
    <rect x="59"  y="9"  width="3" height="10" rx="1.5"/>
    <rect x="66"  y="5"  width="3" height="18" rx="1.5"/>
  </g>
  <g fill="#DFDBCC">
    <rect x="76"  y="10" width="3" height="8"  rx="1.5"/>
    <rect x="83"  y="4"  width="3" height="20" rx="1.5"/>
    <rect x="90"  y="12" width="3" height="4"  rx="1.5"/>
    <rect x="97"  y="0"  width="3" height="28" rx="1.5"/>
    <rect x="104" y="8"  width="3" height="12" rx="1.5"/>
    <rect x="111" y="6"  width="3" height="16" rx="1.5"/>
    <rect x="118" y="11" width="3" height="6"  rx="1.5"/>
    <rect x="125" y="2"  width="3" height="24" rx="1.5"/>
    <rect x="132" y="9"  width="3" height="10" rx="1.5"/>
    <rect x="139" y="5"  width="3" height="18" rx="1.5"/>
    <rect x="146" y="10" width="3" height="8"  rx="1.5"/>
    <rect x="153" y="4"  width="3" height="20" rx="1.5"/>
    <rect x="160" y="12" width="3" height="4"  rx="1.5"/>
    <rect x="167" y="0"  width="3" height="28" rx="1.5"/>
    <rect x="174" y="8"  width="3" height="12" rx="1.5"/>
    <rect x="181" y="6"  width="3" height="16" rx="1.5"/>
    <rect x="188" y="11" width="3" height="6"  rx="1.5"/>
    <rect x="195" y="2"  width="3" height="24" rx="1.5"/>
    <rect x="202" y="9"  width="3" height="10" rx="1.5"/>
    <rect x="209" y="5"  width="3" height="18" rx="1.5"/>
    <rect x="216" y="10" width="3" height="8"  rx="1.5"/>
  </g>
</svg>
"""

# ─── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="side-mark">Video<br><span>Assistant</span></div>', unsafe_allow_html=True)
    st.markdown("---")

    st.markdown('<div class="side-label">Source</div>', unsafe_allow_html=True)
    source = st.text_input("YouTube URL or File Path", placeholder="https://youtube.com/watch?v=... or /path/to/file.mp4", label_visibility="collapsed")

    st.markdown('<div class="side-label">Language</div>', unsafe_allow_html=True)
    language = st.selectbox("Language", ["english", "hinglish"], index=0, label_visibility="collapsed")

    st.markdown("<div style='height:0.6rem'></div>", unsafe_allow_html=True)
    run_btn = st.button("Run analysis  →", use_container_width=True)

    if st.session_state.pipeline_done:
        st.markdown('<div class="side-label">Pipeline</div>', unsafe_allow_html=True)
        for num, label, key in [
            ("01", "Audio processing", "audio"),
            ("02", "Transcription",    "transcript"),
            ("03", "Title generation", "title"),
            ("04", "Summarisation",    "summary"),
            ("05", "Extraction",       "extract"),
            ("06", "RAG engine",       "rag"),
        ]:
            render_stage_row(num, label, key)

# ─── Main Area ──────────────────────────────────────────────────────────────────
st.markdown('<div class="hero-title">AI Video <span>Assistant</span></div>', unsafe_allow_html=True)
st.markdown('<div class="hero-sub">Turn a recording into a transcript, a summary, and a running list of decisions — then ask it questions directly.</div>', unsafe_allow_html=True)
st.markdown(WAVEFORM_SVG, unsafe_allow_html=True)
st.markdown("---")

# ── Run Pipeline ────────────────────────────────────────────────────────────────
if run_btn:
    if not source.strip():
        st.error("Enter a YouTube URL or file path to continue.")
    else:
        st.session_state.pipeline_done = False
        st.session_state.result = None
        st.session_state.chat_history = []
        st.session_state.pipeline_steps = {}

        progress_placeholder = st.empty()

        def update_step(key, state):
            st.session_state.pipeline_steps[key] = state

        try:
            with progress_placeholder.container():
                st.info("Running the pipeline — see sidebar for live status.")

            # Single source of truth: the same run_pipeline() used by the CLI
            # in main.py. update_step just mirrors its progress into the UI.
            st.session_state.result = run_pipeline(source, language, on_step=update_step)
            st.session_state.pipeline_done = True
            progress_placeholder.success("Analysis complete.")
            time.sleep(0.5)
            progress_placeholder.empty()
            st.rerun()

        except Exception as e:
            for k in ["audio", "transcript", "title", "summary", "extract", "rag"]:
                if st.session_state.pipeline_steps.get(k) == "active":
                    st.session_state.pipeline_steps[k] = "pending"
            progress_placeholder.error(f"Something went wrong: {e}")

# ── Results ──────────────────────────────────────────────────────────────────────
if st.session_state.result:
    r = st.session_state.result

    # Title banner
    st.markdown(f"""
    <div class="card">
        <span class="badge badge-accent">Session</span>
        <div style="font-family:'Fraunces',serif;font-size:1.5rem;font-weight:600;color:var(--ink);margin-top:0.6rem">
            {r['title']}
        </div>
    </div>""", unsafe_allow_html=True)

    # Top row: summary + transcript
    col1, col2 = st.columns([3, 2], gap="medium")

    with col1:
        eyebrow("01", "Summary")
        st.markdown(f'<div class="card"><div class="card-content">{r["summary"]}</div></div>', unsafe_allow_html=True)

    with col2:
        eyebrow("02", "Transcript")
        with st.expander("View full transcript", expanded=False):
            st.markdown(f'<div class="transcript-box">{r["transcript"]}</div>', unsafe_allow_html=True)

    # Second row: action items | decisions | questions
    c1, c2, c3 = st.columns(3, gap="medium")

    with c1:
        eyebrow("03", "Action items")
        st.markdown(f'<div class="card"><div class="card-content">{r["action_items"]}</div></div>', unsafe_allow_html=True)

    with c2:
        eyebrow("04", "Decisions")
        st.markdown(f'<div class="card"><div class="card-content">{r["key_decisions"]}</div></div>', unsafe_allow_html=True)

    with c3:
        eyebrow("05", "Open questions")
        st.markdown(f'<div class="card"><div class="card-content">{r["open_questions"]}</div></div>', unsafe_allow_html=True)

    st.markdown("---")

    # ── RAG Chat ──────────────────────────────────────────────────────────────
    eyebrow("06", "Chat with the recording")

    # Chat history display
    if st.session_state.chat_history:
        chat_html = '<div class="chat-container">'
        for msg in st.session_state.chat_history:
            if msg["role"] == "user":
                chat_html += f"""
                <div class="chat-msg" style="align-items:flex-end">
                    <span class="chat-label">You</span>
                    <div class="chat-bubble user-bubble">{msg['content']}</div>
                </div>"""
            else:
                chat_html += f"""
                <div class="chat-msg" style="align-items:flex-start">
                    <span class="chat-label">Assistant</span>
                    <div class="chat-bubble bot-bubble">{msg['content']}</div>
                </div>"""
        chat_html += '</div>'
        st.markdown(chat_html, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="card" style="text-align:center;padding:2rem">
            <div style="color:var(--ink-muted);font-size:0.88rem">Ask anything about the transcript — decisions made, who owns what, what was left open.</div>
        </div>""", unsafe_allow_html=True)

    # Chat input
    chat_col1, chat_col2 = st.columns([5, 1], gap="small")
    with chat_col1:
        user_input = st.text_input("Your question", placeholder="What were the main decisions made?", label_visibility="collapsed")
    with chat_col2:
        send_btn = st.button("Send →", use_container_width=True)

    if send_btn and user_input.strip():
        with st.spinner("Thinking…"):
            answer = ask_question(r["rag_chain"], user_input.strip())
        st.session_state.chat_history.append({"role": "user", "content": user_input.strip()})
        st.session_state.chat_history.append({"role": "assistant", "content": answer})
        st.rerun()

    if st.session_state.chat_history:
        if st.button("Clear chat", type="secondary"):
            st.session_state.chat_history = []
            st.rerun()

else:
    # Empty state
    st.markdown("""
    <div class="card" style="padding:3rem 2rem;text-align:center">
        <div style="font-family:'Fraunces',serif;font-size:1.5rem;font-weight:600;color:var(--ink);margin-bottom:0.6rem">
            Ready when you are.
        </div>
        <div style="color:var(--ink-muted);font-size:0.9rem;max-width:420px;margin:0 auto;line-height:1.7">
            Paste a YouTube URL or local file path in the sidebar, choose a language, and select
            <strong>Run analysis</strong> to get a transcript, summary, and chat interface.
        </div>
        <div style="margin-top:1.75rem;display:flex;gap:0.6rem;flex-wrap:wrap;justify-content:center">
            <span class="badge badge-accent">Transcription</span>
            <span class="badge badge-amber">Summarisation</span>
            <span class="badge badge-green">RAG chat</span>
        </div>
    </div>""", unsafe_allow_html=True)
