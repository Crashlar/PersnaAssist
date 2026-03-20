from src.persnaassist.audio.recorder import AudioRecorder
from src.persnaassist.stt.whisper_engine import WhisperEngine
from src.persnaassist.tts.tts_engine import TTSEngine
from src.persnaassist.llm.llm_client import LLMClient
from src.persnaassist.db.database import DatabaseManager

from src.persnaassist.utils.logger import get_logger

logger = get_logger(__name__)


class VoiceAssistant:
    def __init__(self):
        logger.info("Initializing Voice Assistant...")

        self.recorder = AudioRecorder()
        self.stt = WhisperEngine()
        self.tts = TTSEngine()
        self.llm = LLMClient()
        self.db = DatabaseManager()

        logger.info("All components initialized")

    def build_context(self, history):
        """
        Convert DB history into LLM context
        """
        context = ""
        for convo in reversed(history):
            context += f"User: {convo.user_input}\nAssistant: {convo.assistant_response}\n"
        return context

    def run_once(self):
        """
        Single interaction cycle
        """

        #  Record
        logger.info("Listening...")
        audio = self.recorder.record_seconds(3)

        #  STT
        logger.info("Transcribing...")
        text = self.stt.transcribe(audio)

        if not text:
            logger.warning("No speech detected")
            return

        logger.info(f"User: {text}")

        #  Get memory
        history = self.db.get_last_conversations(limit=5)
        context = self.build_context(history)

        #  LLM
        logger.info("Generating response...")
        response = self.llm.generate_response(text, context)

        logger.info(f"Assistant: {response}")

        #  Save to DB
        self.db.save_conversation(text, response)

        #  Speak
        logger.info("Speaking...")
        self.tts.speak(response)

    def run(self):
        """
        Continuous assistant loop
        """
        logger.info("Assistant started (Press Ctrl+C to stop)")

        try:
            while True:
                self.run_once()

        except KeyboardInterrupt:
            logger.info("Assistant stopped by user")
            self.db.close()