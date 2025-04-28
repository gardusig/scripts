
import hashlib
import os
from pathlib import Path
import sys
import typer

CACHE_DIR = Path.home() / ".cache" / "cli_history"
CACHE_DIR.mkdir(parents=True, exist_ok=True)


def create_session_file(name: str) -> Path:
    """Return a file path under ~/.cache/cli_history/ incorporating the session id."""
    typer.secho(f'ℹ️ Creating session file for: {name}', fg='green')
    session_file = CACHE_DIR / f"{name}.{get_session_id()}.json"
    typer.secho(f'✅ Session file path: {session_file}', fg='green')
    return session_file


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
    typer.secho('🐛 Determining session ID…', fg='blue')
    try:
        raw = (
            os.getenv("HISTORY_SESSION_ID")
            or _try_pty()
            or os.getenv("WT_SESSION")
            or str(os.getppid())
        )
        session_id = _hash(raw)
        typer.secho(f'✅ Session ID determined: {session_id}', fg='green')
        return session_id
    except Exception as e:
        typer.secho(f'❌ Failed to determine session ID: {e}', fg='red', err=True)
        raise


def _try_pty() -> str | None:
    try:
        return os.ttyname(sys.stdin.fileno())
    except Exception as e:
        typer.secho(f'⚠️  Could not get TTY name: {e}', fg='yellow', err=True)
        return None
