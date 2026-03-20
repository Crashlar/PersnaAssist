from src.persnaassist import AudioRecorder
from src.persnaassist import WhisperEngine
from src.persnaassist import TTSEngine

from src.persnaassist import get_logger
from src.persnaassist import PersnaAssistException

import sys
from src.persnaassist import DatabaseManager, init_db

import sys

logger = get_logger(__name__)


def main():
    try:
        logger.info("Starting PersnaAssist...")
        
        init_db()
        db = DatabaseManager()
        logger.info("Database initialized")

        # Initialize components
        recorder = AudioRecorder()
        stt = WhisperEngine()
        tts = TTSEngine()

        logger.info("All components initialized successfully")

        # Step 1: Record audio
        logger.info("Recording audio from microphone...")
        audio = recorder.record_seconds(duration=3)

        # Step 2: Speech to text
        logger.info("Transcribing audio...")
        text = stt.transcribe(audio)

        logger.info(f"User said: {text}")

        # Step 3: Dummy response (LLM later)
        response = f"You said: {text}"

        logger.info(f"Assistant response: {response}")

        #  Step 4: Save to DB
        db.save_conversation(text, response)
        logger.info("Conversation saved to database")

        #  Step 5: Fetch last 3 conversations
        history = db.get_last_conversations(limit=3)

        logger.info("Last conversations from DB:")
        for convo in history:
            logger.info(f"{convo.user_input} → {convo.assistant_response}")

        # Step 6: Speak
        logger.info("Converting response to speech...")
        tts.speak(response)

        logger.info("Execution completed successfully")

        db.close()

    except Exception as e:
        logger.error("Error occurred in main pipeline", exc_info=True)
        raise PersnaAssistException(e, sys)


if __name__ == "__main__":
    main()