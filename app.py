import sys
from src.persnaassist.utils.exceptions import PersnaAssistException
from src.persnaassist.utils.logger import get_logger



if __name__ == "__main__":
    logger = get_logger(__name__)
    try:
        logger.info("Application started")
        x = 10 / 0
    except Exception as e:
        logger.error("numerator is not divisible by zero")
        raise PersnaAssistException(e, sys)