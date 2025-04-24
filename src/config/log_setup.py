from __future__ import annotations

import logging
from logging.config import dictConfig
from pathlib import Path

LOG_DIR = Path.home() / ".cache" / "kirby_logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)


def setup_logging(level: str = "INFO") -> None:
    dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                # only plain formatter for files
                "plain": {
                    "format": "%(asctime)s  %(levelname)-8s  %(name)s: %(message)s"
                },
            },
            "handlers": {
                "console": {
                    "class": "rich.logging.RichHandler",
                    # RichHandler formats its own output
                    "level": level,
                    "rich_tracebacks": True,
                    "show_level": True,
                    "show_path": False,
                    "show_time": True,
                },
                "file": {
                    "class": "logging.FileHandler",
                    "formatter": "plain",
                    "filename": str(LOG_DIR / "app.log"),
                    "encoding": "utf-8",
                    "level": "DEBUG",
                },
            },
            "root": {
                "level": level,
                "handlers": ["console", "file"],
            },
        }
    )


def get_log_file_handler(module_name: str, level: str = "DEBUG") -> logging.Handler:
    """Return a `<module>.log` rotating file handler (call once per module)."""
    from logging.handlers import RotatingFileHandler

    handler = RotatingFileHandler(
        LOG_DIR / f"{module_name}.log",
        maxBytes=2_000_000,
        backupCount=3,
        encoding="utf-8",
    )
    handler.setLevel(level)
    handler.setFormatter(
        logging.Formatter("%(asctime)s  %(levelname)-8s  %(name)s: %(message)s")
    )
    return handler
