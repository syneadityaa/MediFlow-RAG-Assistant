"""MediFlow AI Assistant - Streamlit app."""
import os
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv

from src.rag_pipeline import RAGPipeline

load_dotenv()
KB_DIR = Path(__file__).parent / "knowledge_base"

st.set_page_config(page_title="MediFlow AI Assistant", page_icon="🩺", layout="wide")

DEEP_TEAL, LIGHT_TEAL = "#0F766E", "#E6F7F5"
st.markdown(
    f"""
    <style>
    .stApp {{ background: #ffffff; }}
    .banner {{ background: linear-gradient(135deg, {DEEP_TEAL}, #14B8A6); color: white;
              padding: 1.2rem 1.5rem; border-radius: 14px; margin-bottom: 1rem; }}
    .banner h1 {{ margin: 0; font-size: 1.7rem; color: white; }}
    .banner p {{ margin: .2rem 0 0; opacity: .92; }}
    [data-testid="stSidebar"] {{ background: {LIGHT_TEAL}; }}
    [data-testid="stChatMessage"] {{ border-radius: 12px; padding: .6rem .9rem; margin-bottom: .5rem; }}
    [data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) {{
        background: {LIGHT_TEAL}; border: 1px solid #B7E4DF; }}
    [data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarAssistant"]) {{
        background: #F8FAFA; border: 1px solid #E2E8F0; }}
    .stButton > button {{ border: 1px solid {DEEP_TEAL}; color: {DEEP_TEAL}; border-radius: 10px; }}
    .stButton > button:hover {{ background: {DEEP_TEAL}; color: white; }}
    </style>
    """,
    unsafe_allow_html=True,
)


def get_api_key():
    key = os.getenv("GEMINI_API_KEY")
    if key:
        return key
    try:
        return st.secrets.get("GEMINI_API_KEY")
    except Exception:
        return None


@st.cache_resource(show_spinner="Building the knowledge index (first run downloads the embedding model)...")
def load_pipeline() -> RAGPipeline:
    pipeline = RAGPipeline(KB_DIR)
    pipeline.build_index()
    return pipeline


try:
    pipeline = load_pipeline()
except Exception as exc:
    st.error(f"Could not build the knowledge base: {exc}")
    st.stop()

api_key = get_api_key()

# ---------------- Sidebar ----------------
with st.sidebar:
    st.markdown("### 🩺 MediFlow AI Assistant")
    st.write(
        "A RAG-based chatbot that answers questions about the **MediFlow** "
        "Smart Medical Appointment & Queue Optimization System."
    )
    st.markdown("**Knowledge documents**")
    for name in pipeline.list_documents():
        st.markdown(f"- 📄 `{name}`")
    st.markdown("---")
    st.caption(
        "Answers come only from the documents above. This assistant gives no medical "
        "diagnosis, treatment or medication advice."
    )
    if st.button("🗑️ Clear chat"):
        st.session_state.messages = []
        st.rerun()
    if not api_key:
        st.warning("GEMINI_API_KEY not found. Add it to .env or Streamlit secrets.")

# ---------------- Main ----------------
st.markdown(
    '<div class="banner"><h1>🩺 MediFlow AI Assistant</h1>'
    "<p>Ask me how MediFlow works: appointments, queues, dashboards and more.</p></div>",
    unsafe_allow_html=True,
)

if "messages" not in st.session_state:
    st.session_state.messages = []


def render_sources(sources):
    if sources:
        with st.expander("📚 Sources"):
            for s in sources:
                st.markdown(f"- `{s['source']}` → *{s['heading']}* (match {s['score']:.2f})")


for msg in st.session_state.messages:
    with st.chat_message(msg["role"], avatar="🧑" if msg["role"] == "user" else "🩺"):
        st.markdown(msg["content"])
        render_sources(msg.get("sources"))

if not st.session_state.messages:
    st.markdown("**Try asking:**")
    examples = [
        "How do I register on MediFlow?",
        "How do I book an appointment?",
        "What does CHECKED_IN mean?",
        "How can doctors manage appointments?",
    ]
    cols = st.columns(len(examples))
    for col, example in zip(cols, examples):
        if col.button(example, use_container_width=True):
            st.session_state.pending = example
            st.rerun()

question = st.chat_input("Ask a question about MediFlow...") or st.session_state.pop("pending", None)

if question:
    history = list(st.session_state.messages)
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user", avatar="🧑"):
        st.markdown(question)

    with st.chat_message("assistant", avatar="🩺"):
        with st.spinner("Searching the MediFlow documentation..."):
            try:
                result = pipeline.answer(question, history=history, api_key=api_key)
                answer, sources = result["answer"], result["sources"]
            except Exception as exc:
                answer, sources = f"⚠️ Sorry, something went wrong: {exc}", []
        st.markdown(answer)
        render_sources(sources)

    st.session_state.messages.append({"role": "assistant", "content": answer, "sources": sources})