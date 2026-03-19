import logging
import os
from datetime import datetime

# ==============================
# CREATE LOG DIRECTORY
# ==============================

LOGS_DIR = os.path.join(os.getcwd(), "logs")
os.makedirs(LOGS_DIR, exist_ok=True)

# ==============================
# CREATE LOG FILE NAME
# ==============================

LOG_FILE = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"
LOG_FILE_PATH = os.path.join(LOGS_DIR, LOG_FILE)

# ==============================
# LOGGER SETUP FUNCTION
# ==============================

def get_logger(name: str) -> logging.Logger:
    """
    Creates and returns a configured logger.
    """

    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # Prevent duplicate logs
    if logger.handlers:
        return logger

    # File handler
    file_handler = logging.FileHandler(LOG_FILE_PATH)
    file_handler.setLevel(logging.INFO)

    # Console handler (for debugging)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    # Log format
    formatter = logging.Formatter(
        "[ %(asctime)s ] %(lineno)d %(name)s - %(levelname)s - %(message)s"
    )

    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # Add handlers
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger