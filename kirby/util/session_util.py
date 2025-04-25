import hashlib
import os
from pathlib import Path
import sys

CACHE_DIR = Path.home() / ".cache" / "cli_history"
CACHE_DIR.mkdir(parents=True, exist_ok=True)


def create_session_file(name: str) -> Path:
    """Return a file path under ~/.cache/cli_history/ incorporating the session id."""
    return CACHE_DIR / f"{name}.{get_session_id()}.json"


def _hash(text: str) -> str:
    return hashlib.md5(text.encode()).hexdigest()[:8]


def get_session_id() -> str:
    """
    Return a stable hash for the current *terminal* session/pane.

    Order of precedence:
      1. $HISTORY_SESSION_ID   – explicit override (great for tests)
      2. controlling TTY path  – /dev/pts/N (Unix)
      3. $WT_SESSION           – Windows Terminal / VS-Code
      4. parent PID
    """
    raw = (
        os.getenv("HISTORY_SESSION_ID")
        or _try_pty()
        or os.getenv("WT_SESSION")
        or str(os.getppid())
    )
    return _hash(raw)


def _try_pty() -> str | None:
    try:
        return os.ttyname(sys.stdin.fileno())
    except Exception:
        return None
