"""MediFlow AI Assistant - blue, ChatGPT-style Streamlit interface."""

"""MediFlow AI Assistant - blue, ChatGPT-style Streamlit interface."""

import html
import os
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv

from src.rag_pipeline import RAGPipeline

load_dotenv()
KB_DIR = Path(__file__).parent / "knowledge_base"

st.set_page_config(
    page_title="MediFlow AI",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded",
)


def get_config_value(name: str):
    """Read a setting from environment variables or Streamlit secrets."""
    value = os.getenv(name)
    if value:
        return value.strip()
    try:
        value = st.secrets.get(name)
        return str(value).strip() if value else None
    except Exception:
        return None


# Allow GEMINI_MODEL to be configured in Streamlit Community Cloud secrets too.
configured_model = get_config_value("GEMINI_MODEL")
if configured_model:
    os.environ["GEMINI_MODEL"] = configured_model

# ---------------- DESIGN ----------------

st.markdown(r"""
<style>
:root {
    color-scheme: light;
    --blue: #3478D4;
    --blue-dark: #245BA8;
    --blue-light: #E3EEFF;
    --ink: #263D59;
    --muted: #687F9D;
    --border: #DCE7F5;
    --page: #F3F7FD;
    --white: #FFFFFF;
}

html, body, [data-testid="stAppViewContainer"],
[data-testid="stMain"], .stApp {
    background: var(--page) !important;
    color: var(--ink) !important;
}
header[data-testid="stHeader"] {
    background: rgba(243, 247, 253, .96) !important;
}
[data-testid="stMainBlockContainer"] {
    max-width: 900px;
    padding-top: 1.5rem;
    padding-bottom: 7rem;
}
#MainMenu, footer, [data-testid="stDecoration"],
[data-testid="stStatusWidget"] {
    display: none !important;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: #EAF1FB !important;
    border-right: 1px solid #D9E5F4 !important;
}
section[data-testid="stSidebar"] > div { padding: 1.2rem 1rem; }
.sidebar-brand {
    display: flex; align-items: center; gap: 11px;
    padding: 8px 4px 22px;
}
.sidebar-logo {
    width: 44px; height: 44px; border-radius: 13px;
    background: #D8E8FF; display: flex;
    justify-content: center; align-items: center; font-size: 23px;
}
.sidebar-name { color: #245BA8 !important; font-size: 18px; font-weight: 800; }
.sidebar-caption { color: #68809F !important; font-size: 12px; }
.sidebar-label {
    color: #6682A5 !important; font-size: 11px; font-weight: 800;
    letter-spacing: 1.1px; margin: 22px 0 11px;
}
.document-item {
    padding: 10px 11px; margin: 6px 0; background: #F7FAFF;
    border: 1px solid #DCE7F5; border-radius: 9px;
    font-size: 12px; color: #355578 !important;
}
.sidebar-note { font-size: 12px; color: #536D8D !important; line-height: 1.8; }
section[data-testid="stSidebar"] .stMarkdown,
section[data-testid="stSidebar"] .stMarkdown p,
section[data-testid="stSidebar"] .stCaption,
section[data-testid="stSidebar"] [data-testid="stCaptionContainer"] {
    color: #405B7C !important; font-size: 13px; line-height: 1.7;
}
section[data-testid="stSidebar"] h3 { color: #294D77 !important; font-size: 17px !important; }
section[data-testid="stSidebar"] .stButton > button {
    min-height: 43px; border-radius: 11px !important;
    font-size: 14px !important; font-weight: 650 !important;
}

/* Header and welcome */
.topbar {
    display: flex; align-items: center; justify-content: space-between;
    padding: 3px 0 17px; border-bottom: 1px solid #DCE7F5; margin-bottom: 25px;
}
.topbar-brand { color: #245BA8 !important; font-size: 16px; font-weight: 800; }
.topbar-status {
    color: #2863B0 !important; background: #E5F0FF;
    border: 1px solid #D1E2FA; padding: 7px 12px;
    border-radius: 20px; font-size: 11px; font-weight: 700;
}
.welcome { text-align: center; padding: 65px 15px 28px; }
.welcome-icon {
    height: 68px; width: 68px; display: flex; align-items: center;
    justify-content: center; background: #DFEBFF; border: 1px solid #D2E2FA;
    border-radius: 21px; font-size: 34px; margin: 0 auto 22px;
}
.welcome h1 {
    color: #244D83 !important; font-size: 32px !important;
    font-weight: 800; letter-spacing: -.8px; margin-bottom: 12px;
}
.welcome p { color: #627B9D !important; font-size: 16px !important; line-height: 1.8; }
.suggestion-heading { color: #365A86 !important; font-size: 14px; font-weight: 750; margin: 20px 0 12px; }

/* Buttons */
.stButton > button {
    background: #FFFFFF !important; color: #315D91 !important;
    border: 1px solid #D5E3F5 !important; border-radius: 12px !important;
    min-height: 58px; font-size: 14px !important; font-weight: 650 !important;
    text-align: left !important; transition: all .2s ease;
}
.stButton > button:hover {
    background: #E6F0FF !important; border-color: #9DBDEB !important;
    color: #245BA8 !important;
}

/* Chat and answer typography */
div[data-testid="stChatMessage"] {
    background: #FFFFFF !important; border: 1px solid #E1EAF5 !important;
    border-radius: 15px !important; box-shadow: 0 2px 9px rgba(35,75,120,.035);
    padding: 17px 20px !important; margin: 12px 0 15px !important; gap: 13px !important;
}
div[data-testid="stChatMessage"] [data-testid="stMarkdownContainer"],
div[data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] p,
div[data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] li,
div[data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] span {
    color: #30465F !important; opacity: 1 !important;
    font-size: 15.5px !important; line-height: 1.9 !important;
}
div[data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] strong {
    color: #245BA8 !important; font-size: 15.5px !important; font-weight: 750 !important;
}
div[data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] h1 {
    color: #244D83 !important; font-size: 26px !important;
}
div[data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] h2 {
    color: #244D83 !important; font-size: 23px !important;
}
div[data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] h3 {
    color: #315F98 !important; font-size: 19px !important;
}
div[data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] li { margin-bottom: 7px; }
div[data-testid="stChatMessage"] code {
    color: #245BA8 !important; background: #EDF3FC !important;
    border-radius: 5px; padding: 2px 5px;
}
div[data-testid="stChatMessage"] pre {
    background: #EDF3FC !important; border: 1px solid #DCE7F5; border-radius: 10px;
}
div[data-testid="stChatMessage"] pre code { color: #30465F !important; background: transparent !important; }

/* User message */
.user-row { display: flex; justify-content: flex-end; width: 100%; margin: 15px 0 20px; }
.user-bubble {
    background: #DFEBFF; border: 1px solid #D0E1FB; color: #244E83 !important;
    padding: 14px 19px; border-radius: 18px 18px 4px 18px;
    max-width: 78%; font-size: 15.5px; line-height: 1.85; overflow-wrap: anywhere;
}

/* Flowchart */
.flowchart-wrap {
    margin: 17px 0 12px; padding: 18px;
    background: #F5F8FE; border: 1px solid #DCE7F5; border-radius: 14px;
}
.flowchart-title {
    color: #315F98 !important; font-size: 13px; font-weight: 800;
    letter-spacing: .4px; margin-bottom: 13px;
}
.flow-node {
    display: flex; align-items: center; gap: 12px;
    background: #FFFFFF; border: 1px solid #D8E5F5;
    border-radius: 10px; padding: 11px 13px;
    color: #304D70 !important; font-size: 13px; line-height: 1.55;
}
.flow-number {
    flex: 0 0 25px; width: 25px; height: 25px;
    display: flex; align-items: center; justify-content: center;
    border-radius: 50%; background: #E3EEFF; color: #245BA8 !important;
    font-size: 11px; font-weight: 800;
}
.flow-arrow {
    text-align: center; color: #6D9BD5 !important;
    font-size: 19px; line-height: 1.4; height: 23px;
}
.flowchart-note { color: #7185A0 !important; font-size: 11px; margin-top: 12px; }

/* Sources */
div[data-testid="stExpander"] {
    background: #F7FAFF !important; border: 1px solid #DCE7F5 !important;
    border-radius: 11px !important; margin-top: 12px;
}
div[data-testid="stExpander"] summary,
div[data-testid="stExpander"] summary span {
    color: #38669D !important; font-size: 13px !important; font-weight: 700 !important;
}
div[data-testid="stExpander"] [data-testid="stMarkdownContainer"],
div[data-testid="stExpander"] [data-testid="stMarkdownContainer"] * {
    color: #405B7C !important; font-size: 13px !important; line-height: 1.7 !important;
}

/* Bottom composer */
[data-testid="stBottom"] {
    background: rgba(243,247,253,.97) !important; border-top: 1px solid #DCE7F5 !important;
}
[data-testid="stBottom"] > div { max-width: 900px !important; padding-top: 12px !important; }
[data-testid="stChatInput"] {
    background: #FFFFFF !important; border: 1px solid #C9D9EF !important;
    border-radius: 17px !important; box-shadow: 0 4px 18px rgba(35,75,120,.08) !important;
}
[data-testid="stChatInput"] textarea {
    color: #263D59 !important; -webkit-text-fill-color: #263D59 !important;
    background: #FFFFFF !important; font-size: 15.5px !important;
}
[data-testid="stChatInput"] textarea::placeholder {
    color: #879BB5 !important; -webkit-text-fill-color: #879BB5 !important;
}
[data-testid="stChatInput"] button { background: #3478D4 !important; color: #FFFFFF !important; border-radius: 10px !important; }

hr { border-color: #DCE7F5 !important; }
.stApp a { color: #286AC0 !important; }

@media (max-width: 700px) {
    [data-testid="stMainBlockContainer"] { padding: 1rem 1rem 6rem; }
    .welcome { padding-top: 35px; }
    .welcome h1 { font-size: 25px !important; }
    .user-bubble { max-width: 90%; }
    .topbar-status { font-size: 9px; }
}
</style>
""", unsafe_allow_html=True)

# ---------------- PIPELINE ----------------

@st.cache_resource(show_spinner="Loading MediFlow knowledge base...")
def load_pipeline():
    pipeline = RAGPipeline(KB_DIR)
    pipeline.build_index()
    return pipeline


try:
    pipeline = load_pipeline()
except Exception as exc:
    st.error(f"Could not build knowledge base: {exc}")
    st.stop()


def get_api_key():
    return get_config_value("GEMINI_API_KEY")


api_key = get_api_key()

if "messages" not in st.session_state:
    st.session_state.messages = []

# ---------------- RENDER HELPERS ----------------

def render_user_message(content: str):
    safe_content = html.escape(content).replace("\n", "<br>")
    st.markdown(
        f'<div class="user-row"><div class="user-bubble">{safe_content}</div></div>',
        unsafe_allow_html=True,
    )


def render_flowchart(steps):
    """Render a compact vertical flowchart from grounded, plain-text steps."""
    if not steps or len(steps) < 2:
        return

    parts = [
        '<div class="flowchart-wrap">',
        '<div class="flowchart-title">PROCESS FLOW</div>',
    ]
    for index, step in enumerate(steps[:7], start=1):
        safe_step = html.escape(str(step))
        parts.append(
            '<div class="flow-node">'
            f'<span class="flow-number">{index}</span>'
            f'<span>{safe_step}</span>'
            '</div>'
        )
        if index < min(len(steps), 7):
            parts.append('<div class="flow-arrow">↓</div>')
    parts.append('<div class="flowchart-note">Sequence based on the MediFlow project documentation.</div>')
    parts.append('</div>')
    st.markdown("".join(parts), unsafe_allow_html=True)


def render_sources(sources):
    if not sources:
        return
    with st.expander("📚 Sources used"):
        for source in sources:
            filename = html.escape(str(source.get("source", "Document")))
            heading = html.escape(str(source.get("heading", "Section")))
            score = source.get("score")
            score_text = f" (match: {score:.2f})" if isinstance(score, (int, float)) else ""
            st.markdown(f"- **{filename}** — {heading}{score_text}")


def render_assistant_message(message):
    with st.chat_message("assistant", avatar="🩺"):
        st.markdown(message.get("content", ""))
        render_flowchart(message.get("flowchart", []))
        render_sources(message.get("sources", []))

# ---------------- SIDEBAR ----------------

with st.sidebar:
    st.markdown("""
    <div class="sidebar-brand">
        <div class="sidebar-logo">🩺</div>
        <div>
            <div class="sidebar-name">MediFlow AI</div>
            <div class="sidebar-caption">Your project assistant</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("＋  New chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.markdown('<div class="sidebar-label">YOUR KNOWLEDGE BASE</div>', unsafe_allow_html=True)
    with st.expander(f"📚 Documents ({len(pipeline.list_documents())})", expanded=False):
        for name in pipeline.list_documents():
            safe_name = html.escape(name)
            st.markdown(f'<div class="document-item">📄 &nbsp; {safe_name}</div>', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown('<div class="sidebar-label">ABOUT MEDIFLOW AI</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="sidebar-note">An intelligent assistant for the MediFlow Smart '
        'Medical Appointment &amp; Queue Optimization System.</div>',
        unsafe_allow_html=True,
    )
    st.markdown("---")
    st.markdown(
        '<div class="sidebar-note">Answers are grounded in project documents. '
        'Medical diagnosis and treatment advice are not provided.</div>',
        unsafe_allow_html=True,
    )
    if not api_key:
        st.warning("GEMINI_API_KEY not found. Check your .env file.")

# ---------------- TOP BAR ----------------

st.markdown("""
<div class="topbar">
    <div class="topbar-brand">🩺 &nbsp; MediFlow Assistant</div>
    <div class="topbar-status">● Knowledge base connected</div>
</div>
""", unsafe_allow_html=True)

# ---------------- WELCOME ----------------

if not st.session_state.messages:
    st.markdown("""
    <div class="welcome">
        <div class="welcome-icon">🩺</div>
        <h1>How can I help you today?</h1>
        <p>Ask me anything about MediFlow. I'll find answers from the project's documentation.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="suggestion-heading">Explore MediFlow</div>', unsafe_allow_html=True)
    examples = [
        "How do I register on MediFlow?",
        "How do I book an appointment?",
        "What does CHECKED_IN mean?",
        "How can doctors manage appointments?",
    ]
    col1, col2 = st.columns(2)
    for index, example in enumerate(examples):
        with (col1 if index % 2 == 0 else col2):
            if st.button(example, key=f"suggestion_{index}", use_container_width=True):
                st.session_state.pending = example
                st.rerun()

# ---------------- CHAT HISTORY ----------------

for message in st.session_state.messages:
    if message.get("role") == "user":
        render_user_message(message.get("content", ""))
    else:
        render_assistant_message(message)

# ---------------- NEW MESSAGE ----------------

pending_question = st.session_state.pop("pending", None)
question = st.chat_input("Message MediFlow AI...") or pending_question

if question:
    history = list(st.session_state.messages)
    st.session_state.messages.append({"role": "user", "content": question})
    render_user_message(question)

    with st.chat_message("assistant", avatar="🩺"):
        with st.spinner("Looking through MediFlow documentation..."):
            try:
                result = pipeline.answer(
                    question,
                    history=history,
                    api_key=api_key,
                )
                answer = result.get("answer", "I couldn't prepare an answer.")
                sources = result.get("sources", [])
                flowchart = result.get("flowchart", [])
            except Exception as exc:
                answer = (
                    "Sorry, I couldn't generate an answer right now.\n\n"
                    f"**Error:** {exc}"
                )
                sources = []
                flowchart = []

        st.markdown(answer)
        render_flowchart(flowchart)
        render_sources(sources)

    st.session_state.messages.append({
        "role": "assistant",
        "content": answer,
        "sources": sources,
        "flowchart": flowchart,
    })
