"""Structured logging utilities with secret redaction."""
import logging
import re
import sys
from typing import Any

# Patterns to sanitize in logs
SECRET_PATTERNS = [
    re.compile(r"(sk-[a-zA-Z0-9_\-]{20,})"),
    re.compile(r"(key-[a-zA-Z0-9_\-]{20,})"),
    re.compile(r"(Bearer\s+[a-zA-Z0-9_\-\.]{20,})", re.IGNORECASE),
    re.compile(r"(['\"]?api[_-]?key['\"]?\s*[:=]\s*['\"])([^'\"]+)(['\"])", re.IGNORECASE),
]


class SafeFormatter(logging.Formatter):
    """Custom formatter that redacts sensitive keys and credentials."""

    def format(self, record: logging.LogRecord) -> str:
        msg = super().format(record)
        for pattern in SECRET_PATTERNS:
            msg = pattern.sub("[REDACTED_SECRET]", msg)
        return msg


def setup_logger(name: str = "gridwise", level: str = "INFO") -> logging.Logger:
    """Initialize and configure a secure application logger."""
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, level.upper(), logging.INFO))

    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(
            SafeFormatter("[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
        )
        logger.addHandler(handler)

    return logger


logger = setup_logger()
