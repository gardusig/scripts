from logging.config import dictConfig
from pathlib import Path


LOG_DIR = Path.home() / ".cache" / "kirby_logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)


def setup_logging():
    dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "minimal": {"format": "%(message)s"},
                "level": {"format": "[%(levelname)s] %(message)s"},
                "named": {"format": "[%(levelname)s] %(name)s: %(message)s"},
                "detailed": {
                    "format": (
                        "%(asctime)s [%(levelname)s] %(name)s:%(lineno)d"
                        "— %(message)s"
                    )
                },
            },
            "handlers": {
                "console": {
                    "class": "rich.logging.RichHandler",
                    "level": "INFO",
                    "formatter": "minimal",
                    "show_time": False,
                    "rich_tracebacks": True,
                },
                "file": {
                    "class": "logging.FileHandler",
                    "level": "INFO",
                    "formatter": "detailed",
                    "filename": str(LOG_DIR / "kirby.log"),
                    "encoding": "utf-8",
                },
            },
            "root": {
                "handlers": ["console", "file"],
                "level": "INFO",
            },
        }
    )
