import sys


def error_message_detail(error: Exception, error_details: sys) -> str:
    """
    Extract detailed error information including file name, line number, and message.
    """

    _, _, exc_tb = error_details.exc_info()

    # Safety check (important)
    if exc_tb is None:
        return f"Error: {str(error)} (No traceback available)"

    file_name = exc_tb.tb_frame.f_code.co_filename
    line_number = exc_tb.tb_lineno

    return (
        f"Error occurred in script [{file_name}] "
        f"at line [{line_number}] "
        f"with message [{str(error)}]"
    )


class PersnaAssistException(Exception):
    """
    Custom exception class with detailed error tracking.
    """

    def __init__(self, error: Exception, error_details: sys):
        super().__init__(str(error))
        self.error_message = error_message_detail(error, error_details)

    def __str__(self):
        return self.error_message