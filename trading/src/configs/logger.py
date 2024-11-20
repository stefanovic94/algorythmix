import logging
import sys
from typing import Any

from .settings import get_settings

settings = get_settings()


def get_logger(file_name: str) -> Any:
    logger = logging.getLogger(file_name)
    match settings.LOGGING_LEVEL:
        case "debug":
            logger.setLevel(logging.DEBUG)
        case "info":
            logger.setLevel(logging.INFO)
        case "warning":
            logger.setLevel(logging.WARNING)
        case "error":
            logger.setLevel(logging.ERROR)
        case "critical":
            logger.setLevel(logging.CRITICAL)
    extra = {
        "env": settings.ENVIRONMENT.lower(),
        "appname": settings.APP_NAME,
    }
    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(appname)s | %(filename)s%(lineno)s >>> %(message)s"
    )
    logging_handlers = [
        # logging.FileHandler("debug.log"),
        logging.StreamHandler(sys.stdout)
    ]
    for handler in logging_handlers:
        handler.setFormatter(formatter)
    for handler in logging_handlers:
        logger.addHandler(handler)
    logger = logging.LoggerAdapter(logger, extra)

    # Creating a handler
    def handle_unhandled_exception(exc_type, exc_value, exc_traceback):
        if issubclass(exc_type, KeyboardInterrupt):
            # Will call default excepthook
            sys.__excepthook__(exc_type, exc_value, exc_traceback)
            return
        # Create a critical level log message with info from the except hook.
        logger.critical(
            "Unhandled exception", exc_info=(exc_type, exc_value, exc_traceback)
        )

    return logger
