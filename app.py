"""
Streamlit UI for the Upwork API Support Bot.
Run with: streamlit run app.py
"""

import os
import streamlit as st
from dotenv import load_dotenv
from rag import query_rag

load_dotenv()

st.set_page_config(
    page_title="Upwork API Bot",
    page_icon="🤖",
    layout="centered"
)

# ── Custom CSS ────────────────────────────────────────────────
st.markdown("""
<style>
    /* Dark background */
    .stApp {
        background-color: #0f1117;
        color: #ffffff;
    }

    /* Main container */
    .block-container {
        padding-top: 2rem;
        max-width: 750px;
    }

    /* Input fields */
    .stTextInput > div > div > input {
        background-color: #1e2130;
        color: #ffffff;
        border: 1px solid #2e3250;
        border-radius: 8px;
        padding: 10px;
    }

    /* Button */
    .stButton > button {
        background-color: #1890ff;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 10px 24px;
        font-size: 15px;
        font-weight: 600;
        width: 100%;
        transition: background 0.2s;
    }
    .stButton > button:hover {
        background-color: #40a9ff;
        color: white;
    }

    /* Answer box */
    .answer-box {
        background-color: #1e2130;
        border-left: 4px solid #1890ff;
        border-radius: 8px;
        padding: 20px 24px;
        margin: 16px 0;
        font-size: 15px;
        line-height: 1.7;
        color: #e8e8e8;
    }

    /* Latency badge */
    .latency-badge {
        display: inline-block;
        background-color: #162032;
        color: #40a9ff;
        border: 1px solid #1890ff;
        border-radius: 20px;
        padding: 4px 14px;
        font-size: 13px;
        margin-top: 8px;
    }

    /* Section titles */
    .section-title {
        font-size: 13px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
        color: #888;
        margin-top: 24px;
        margin-bottom: 8px;
    }

    /* Expander */
    .streamlit-expanderHeader {
        background-color: #1e2130 !important;
        border-radius: 8px !important;
        color: #aaa !important;
    }

    /* Divider */
    hr {
        border-color: #2e3250;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #141620;
        border-right: 1px solid #2e3250;
    }
</style>
""", unsafe_allow_html=True)

# ── Sidebar ───────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### ⚙️ Configuration")
    st.markdown("---")

    api_key = os.getenv("DEEPINFRA_API_KEY", "")
    if not api_key:
        api_key = st.text_input("DeepInfra API Key", type="password", placeholder="Enter your key...")

    st.markdown("---")
    st.markdown("### 📌 Try These")
    q1 = "How long is an OAuth access token valid?"
    q2 = "Can Client Credentials Grant access private contracts?"
    q3 = "What is the Upwork API rate limit?"

    if st.button("OAuth token validity"):
        st.session_state["question"] = q1
    if st.button("Client Credentials Grant"):
        st.session_state["question"] = q2
    if st.button("API rate limit"):
        st.session_state["question"] = q3

    st.markdown("---")
    st.markdown("<small style='color:#555'>Powered by Meta-Llama + ChromaDB</small>", unsafe_allow_html=True)

# ── Main Area ─────────────────────────────────────────────────
st.markdown("## 🤖 Upwork API Support Bot")
st.markdown("<p style='color:#888; margin-top:-10px'>Answers based strictly on the official Upwork API documentation.</p>", unsafe_allow_html=True)
st.markdown("---")

# Question input
question = st.text_input(
    "Ask a question",
    value=st.session_state.get("question", ""),
    placeholder="e.g. How do I authenticate with OAuth2?",
    label_visibility="collapsed"
)

st.markdown("")
ask = st.button("🔍 Ask", use_container_width=True)

# ── Response ──────────────────────────────────────────────────
if ask:
    if not question:
        st.warning("Please type a question.")
    elif not api_key:
        st.warning("Please enter your API key in the sidebar.")
    else:
        with st.spinner("Searching documentation and generating answer..."):
            try:
                answer, sources, latency = query_rag(question, api_key)

                # Answer
                st.markdown("<div class='section-title'>Answer</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='answer-box'>{answer}</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='latency-badge'>⏱ {latency}s response time</div>", unsafe_allow_html=True)

                # Sources
                st.markdown("<div class='section-title'>Sources Used</div>", unsafe_allow_html=True)
                for i, chunk in enumerate(sources, 1):
                    with st.expander(f"📄 Source {i}"):
                        st.write(chunk)

            except Exception as e:
                st.error(f"Error: {e}")