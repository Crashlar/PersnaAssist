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
# PAGE CONFIGimport sys
import os
import streamlit as st
import time

# Fix path
sys.path.append(os.path.abspath("src"))

from persnaassist.pipeline.assistant import VoiceAssistant
from persnaassist.db.database import init_db
from persnaassist.utils.logger import get_logger

logger = get_logger(__name__)


# ==============================
# PAGE CONFIG
# ==============================
st.set_page_config(
    page_title="PersnaAssist Live",
    layout="wide"
)

# ==============================
# CUSTOM UI (FULLSCREEN STYLE)
# ==============================
st.markdown("""
<style>
body {
    background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
    color: white;
}

.center-box {
    text-align: center;
    margin-top: 100px;
}

.big-mic {
    font-size: 80px;
    padding: 30px;
    border-radius: 50%;
    background: #00c6ff;
    color: black;
}

.response-text {
    font-size: 28px;
    margin-top: 40px;
    font-weight: 500;
}
</style>
""", unsafe_allow_html=True)


# ==============================
# INIT SYSTEM
# ==============================
@st.cache_resource
def load_assistant():
    init_db()
    return VoiceAssistant()

assistant = load_assistant()


# ==============================
# SESSION STATE
# ==============================
if "live_mode" not in st.session_state:
    st.session_state.live_mode = False

if "response" not in st.session_state:
    st.session_state.response = ""


# ==============================
# HOME SCREEN
# ==============================
if not st.session_state.live_mode:

    st.markdown('<div class="center-box">', unsafe_allow_html=True)

    st.title("PersnaAssist")
    st.write("Tap to start live voice assistant")

    if st.button("🎤 Start Assistant", use_container_width=True):
        st.session_state.live_mode = True
        st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)


# ==============================
# LIVE MODE (LIKE GEMINI)
# ==============================
if st.session_state.live_mode:

    st.markdown("## 🎙️ Listening... (Say 'stop' to exit)")

    placeholder = st.empty()

    stop_flag = False

    while not stop_flag:
        try:
            logger.info("Continuous listening...")

            # 🎤 Record small chunk
            audio = assistant.recorder.record_seconds(3)

            text = assistant.stt.transcribe(audio)

            if not text:
                continue

            text = text.lower()
            logger.info(f"User: {text}")

            # STOP CONDITION
            if "stop" in text:
                stop_flag = True
                st.session_state.live_mode = False
                st.success("Assistant stopped")
                time.sleep(1)
                st.rerun()

            # CONTEXT
            history = assistant.db.get_last_conversations(limit=5)
            context = assistant.build_context(history)

            # 🤖 LLM
            response = assistant.llm.generate_response(text, context)

            st.session_state.response = response

            # SHOW RESPONSE (BIG STYLE)
            placeholder.markdown(
                f'<div class="response-text">{response}</div>',
                unsafe_allow_html=True
            )

            # SAVE
            assistant.db.save_conversation(text, response)

            # 🔊 SPEAK
            assistant.tts.speak(response)

        except Exception as e:
            logger.error("Live mode error", exc_info=True)
            break
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