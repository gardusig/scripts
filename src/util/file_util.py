# util/file_util.py
from __future__ import annotations

import fnmatch
import logging
import os
import sys
import hashlib
from pathlib import Path
from typing import Iterable, Sequence

from rich.logging import RichHandler

log = logging.getLogger(__name__)
logging.basicConfig(level="INFO", handlers=[RichHandler()])

# ────────────────────────────────────────────────────────────────────
# constants
# ────────────────────────────────────────────────────────────────────
DEFAULT_IGNORES: tuple[str, ...] = (
    "__pycache__",
    "*.py[co]",
    "*.egg-info",
    ".DS_Store",
    ".git",
    ".venv",
    "venv",
    "build",
    "dist",
    ".copyignore",
    ".env",
    "LICENSE",
    "*.webp",
    "*.jpe?g",
)

CACHE_DIR = Path.home() / ".cache" / "cli_history"
CACHE_DIR.mkdir(parents=True, exist_ok=True)

# ────────────────────────────────────────────────────────────────────
# session helpers
# ────────────────────────────────────────────────────────────────────


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


def create_session_file(name: str) -> Path:
    """Return a file path under ~/.cache/cli_history/ incorporating the session id."""
    return CACHE_DIR / f"{name}.{get_session_id()}.json"


# ────────────────────────────────────────────────────────────────────
# ignore helpers
# ────────────────────────────────────────────────────────────────────
def should_ignore(path_part: str, patterns: Sequence[str] = DEFAULT_IGNORES) -> bool:
    return any(fnmatch.fnmatch(path_part, pat) for pat in patterns)


# ────────────────────────────────────────────────────────────────────
# file discovery
# ────────────────────────────────────────────────────────────────────
def get_all_files(root: str | Path, ignore_patterns: Sequence[str] = DEFAULT_IGNORES) -> list[str]:
    """
    Recursively collect *text* files under `root`, honouring ignore patterns.

    Returns **absolute paths** as strings.
    """
    root = Path(root).expanduser().resolve()
    if not root.exists():
        log.warning("⛔️ Path does not exist: %s", root)
        return []

    paths: list[str] = []

    for path in root.rglob("*"):
        rel = path.relative_to(root)
        if should_ignore(rel.name, ignore_patterns) or should_ignore(str(rel), ignore_patterns):
            log.debug("⏭️  Skipping ignored: %s", rel)
            continue
        if path.is_file():
            paths.append(str(path))
    return paths


# ────────────────────────────────────────────────────────────────────
# file <-> string helpers
# ────────────────────────────────────────────────────────────────────
_MAX_MB = 1


def stringify_file_contents(files: Iterable[str]) -> dict[str, str]:
    """
    Read files into memory (≤ 1 MiB each). Returns {path: contents}.
    """
    result: dict[str, str] = {}
    for p in files:
        path = Path(p)
        try:
            if path.stat().st_size > _MAX_MB * 1024 * 1024:
                log.warning("⚠️  %s bigger than %d MB; skipped.", path, _MAX_MB)
                continue
            text = path.read_text(encoding="utf-8", errors="replace").strip()
            result[str(path)] = text
        except Exception as err:
            log.error("Error reading %s: %s", path, err)
    log.info("📄 Read %d file(s)", len(result))
    return result


# ────────────────────────────────────────────────────────────────────
# write helpers
# ────────────────────────────────────────────────────────────────────
def rewrite_file(file_path: str, content: str) -> None:
    """
    Overwrite `file_path` with `content`, creating parent dirs as needed.
    """
    from db.file_db import append_file  # late import to dodge circular refs

    path = Path(file_path).expanduser()
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        log.info("✅ Rewrote %s", path)
        append_file(str(path))
    except Exception as err:
        log.error("❌ Error writing %s: %s", path, err)
