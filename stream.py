import sys
import os
import streamlit as st
import time

# Fix import path
sys.path.append(os.path.abspath("src"))

from persnaassist.pipeline.assistant import VoiceAssistant
from persnaassist.db.database import init_db
from persnaassist.utils.logger import get_logger

logger = get_logger(__name__)


# ==============================
# PAGE CONFIG
# ==============================
st.set_page_config(
    page_title="PersnaAssist",
    page_icon="🎙️",
    layout="centered"
)

# ==============================
# CUSTOM CSS (Gemini Style)
# ==============================
st.markdown("""
<style>
.main {
    text-align: center;
}

.mic-button {
    font-size: 60px;
    padding: 20px;
    border-radius: 50%;
    background: #111;
    color: white;
    border: none;
}

.response-box {
    margin-top: 30px;
    padding: 20px;
    border-radius: 12px;
    background: #f5f5f5;
    font-size: 18px;
}

.user-box {
    margin-top: 20px;
    font-size: 16px;
    color: gray;
}
</style>
""", unsafe_allow_html=True)


# ==============================
# INIT SYSTEM
# ==============================
@st.cache_resource
def load_assistant():
    logger.info("Initializing assistant...")
    init_db()
    return VoiceAssistant()


assistant = load_assistant()


# ==============================
# SESSION STATE
# ==============================
if "last_user" not in st.session_state:
    st.session_state.last_user = ""

if "last_response" not in st.session_state:
    st.session_state.last_response = ""


# ==============================
# HEADER
# ==============================
st.markdown("## 🎙️ PersnaAssist")
st.markdown("Speak naturally. I’m listening...")

st.write("")


# ==============================
# MIC BUTTON (CENTER)
# ==============================
col1, col2, col3 = st.columns([1,2,1])

with col2:
    if st.button("🎤 Tap to Speak", use_container_width=True):
        try:
            logger.info("Recording started...")

            with st.spinner("Listening..."):
                audio = assistant.recorder.record_seconds(3)

            with st.spinner("Understanding..."):
                text = assistant.stt.transcribe(audio)

            if not text:
                st.warning("Didn't catch that, try again")
            else:
                st.session_state.last_user = text

                # Context
                history = assistant.db.get_last_conversations(limit=5)
                context = assistant.build_context(history)

                with st.spinner("Thinking..."):
                    response = assistant.llm.generate_response(text, context)

                st.session_state.last_response = response

                # Save
                assistant.db.save_conversation(text, response)

                # Speak
                assistant.tts.speak(response)

        except Exception as e:
            logger.error("Error in voice UI", exc_info=True)
            st.error("Something went wrong")


# ==============================
# DISPLAY USER + RESPONSE
# ==============================
if st.session_state.last_user:
    st.markdown(
        f'<div class="user-box">You: {st.session_state.last_user}</div>',
        unsafe_allow_html=True
    )

if st.session_state.last_response:
    st.markdown(
        f'<div class="response-box">{st.session_state.last_response}</div>',
        unsafe_allow_html=True
    )


# ==============================
# FOOTER ACTIONS
# ==============================
st.write("")

col1, col2 = st.columns(2)

with col1:
    if st.button("🔄 Reset"):
        st.session_state.last_user = ""
        st.session_state.last_response = ""
        st.rerun()

with col2:
    if st.button("📝 Switch to Chat Mode"):
        st.switch_page("stream.py")  # optional if multi-page