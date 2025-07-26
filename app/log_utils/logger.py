from loguru import logger as loguru_logger
from pathlib import Path
import sys
from app.core import settings

LOG_DIR = Path(settings.logging_parent_folder)
LOG_DIR.mkdir(parents=True, exist_ok=True)


class Logger:
    _session_loggers = {}

    # --- Initialize system logger once ---
    loguru_logger.remove()
    loguru_logger.add(
        sys.stdout,
        level="INFO",
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
        "<level>{level: <8}</level> | "
        "<cyan>{name}</cyan>:<cyan>{function}</cyan> | "
        "{message}",
    )
    loguru_logger.add(
        LOG_DIR / "system_log.json",
        serialize=True,
        rotation="10 MB",
        retention="60 days",
        compression="zip",
        level="INFO",
        enqueue=False,
    )

    @staticmethod
    def log_system(message: str, level: str = "INFO"):
        """
        Logs a message at the specified level using the system logger.

        Args:
            message (str): The message to log.
            level (str): The logging level (e.g., "INFO", "DEBUG", "ERROR").
        """
        log_method = getattr(loguru_logger, level.lower(), None)
        if not log_method:
            log_method = loguru_logger.info
        log_method(message)

    @staticmethod
    def log_session(session_id: str, message: str, level: str = "INFO"):
        """
        Logs a message under a specific session_id.
        Creates a session-specific log file (if not already exists).

        Args:
            session_id (str): Unique identifier for the session.
            message (str): Log message.
            level (str): Logging level (default: INFO).
        Usage:
            Logger.session_logger("session_xyz", "User started flow")
        """
        if session_id not in Logger._session_loggers:
            session_log_path = LOG_DIR / f"session_{session_id}.json"
            bound_logger = loguru_logger.bind(session_id=session_id)
            bound_logger.add(
                session_log_path,
                serialize=True,
                rotation="5 MB",
                retention="7 days",
                compression="zip",
                level="INFO",
                enqueue=True,
            )
            Logger._session_loggers[session_id] = bound_logger

        logger = Logger._session_loggers[session_id]
        log_method = getattr(logger, level.lower(), logger.info)
        log_method(message)
