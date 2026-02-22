import streamlit as st
import json
import os
from datetime import datetime
from llm import generate_response

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Ava – Local LLM Chat",
    layout="centered"
)

# ---------------- CSS ----------------
st.markdown("""
<style>
body { background-color: #0f172a; }
.chat-box { max-width: 750px; margin: auto; }
.user {
    background:#2563eb; color:white;
    padding:12px 16px; border-radius:16px;
    margin:10px 0; text-align:right;
}
.bot {
    background:#16a34a; color:white;
    padding:12px 16px; border-radius:16px;
    margin:10px 0;
}
.time { font-size:11px; color:#cbd5e1; }
</style>
""", unsafe_allow_html=True)

# ---------------- TITLE ----------------
st.title("🤖 Ava – Local Language Model")
st.caption("Secure • Private • Fully Local AI Chat")

HISTORY_FILE = "chat_history.json"

# ---------------- SESSION STATE ----------------
if "history" not in st.session_state:
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            st.session_state.history = json.load(f)
    else:
        st.session_state.history = []

# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.header("🗂 Chat Controls")

    if st.button("🆕 New Chat"):
        st.session_state.history = []
        if os.path.exists(HISTORY_FILE):
            os.remove(HISTORY_FILE)
        st.rerun()

    st.divider()
    st.subheader("📜 History")

    if st.session_state.history:
        for i, h in enumerate(st.session_state.history, 1):
            st.write(f"{i}. {h['question']}")
    else:
        st.info("No history yet")

# ---------------- CHAT DISPLAY ----------------
st.markdown("<div class='chat-box'>", unsafe_allow_html=True)

for chat in st.session_state.history:
    st.markdown(
        f"<div class='user'>{chat['question']}</div>"
        f"<div class='time'>{chat['time']}</div>",
        unsafe_allow_html=True
    )
    st.markdown(
        f"<div class='bot'>{chat['answer']}</div>",
        unsafe_allow_html=True
    )

st.markdown("</div>", unsafe_allow_html=True)

# ---------------- INPUT ----------------
user_input = st.text_input(
    "💬 Ask something",
    placeholder="Type and press Enter"
)

# ---------------- RESPONSE ----------------
if user_input:
    with st.spinner("🤖 Ava is thinking..."):
        answer = generate_response(user_input)

    entry = {
        "question": user_input,
        "answer": answer,
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    st.session_state.history.append(entry)

    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(st.session_state.history, f, indent=2)

    st.rerun()
