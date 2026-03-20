from pathlib import Path
import logging

# ==============================
# CONFIGURATION
# ==============================

# Package name (lowercase recommended for Python packages)
PACKAGE_NAME = "persnaassist"

# Root directory (IMPORTANT: current project directory)
ROOT_DIR = Path(".")

# ==============================
# FILE STRUCTURE
# ==============================

structure = [
    # Root level files
    "app.py",
    "main.py",
    "setup.py",
    "README.md",
    "requirements.txt",
    ".gitignore",
    "LICENSE",
    ".env",
    "config/config.yaml",

    # Main package
    f"src/{PACKAGE_NAME}/__init__.py",

    # Audio
    f"src/{PACKAGE_NAME}/audio/recorder.py",
    f"src/{PACKAGE_NAME}/audio/player.py",

    # STT
    f"src/{PACKAGE_NAME}/stt/whisper_engine.py",

    # LLM
    f"src/{PACKAGE_NAME}/llm/llm_client.py",

    # TTS
    f"src/{PACKAGE_NAME}/tts/tts_engine.py",

    # Database
    f"src/{PACKAGE_NAME}/db/database.py",

    # Pipeline
    f"src/{PACKAGE_NAME}/pipeline/assistant.py",

    # Utils (inside package)
    f"src/{PACKAGE_NAME}/utils/logger.py",
    f"src/{PACKAGE_NAME}/utils/exceptions.py",
]

# ==============================
# LOGGING CONFIG
# ==============================

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s: %(message)s"
)

# ==============================
# TEMPLATE CREATION FUNCTION
# ==============================

def create_template():
    """
    Create missing project files and folders
    without overwriting existing ones.
    """

    for file_path in structure:
        full_path = ROOT_DIR / file_path

        # Create parent directories if they don't exist
        if not full_path.parent.exists():
            full_path.parent.mkdir(parents=True, exist_ok=True)
            logging.info(f"Created directory: {full_path.parent}")

        # Create file only if it does not exist
        if not full_path.exists():
            full_path.touch()
            logging.info(f"Created file: {full_path}")
        else:
            logging.info(f"Skipped (already exists): {full_path}")


# ==============================
# ENTRY POINT
# ==============================

if __name__ == "__main__":
    create_template()
    print("Template sync completed successfully.")