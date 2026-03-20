import sys
import os

# Fix import path
sys.path.append(os.path.abspath("src"))

from persnaassist.pipeline.assistant import VoiceAssistant
from persnaassist.db.database import init_db


def main():
    print("Starting test...")

    # Initialize DB
    init_db()

    assistant = VoiceAssistant()

    # ✅ Run only once (safe test)
    assistant.run_once()


if __name__ == "__main__":
    main()