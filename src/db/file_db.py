from __future__ import annotations
import logging

from db.history_db import HistoryDB
from config.log_setup import get_log_file_handler
from util.file_util import create_session_file

log = logging.getLogger(__name__)
log.addHandler(get_log_file_handler(__name__))


# ───── underlying generic store ─────────────────────────────────────

_file_db: HistoryDB[list[str]] = HistoryDB(
    create_session_file("file_set_history"),
    empty=[],
    normalise=lambda lst: sorted({p.strip() for p in lst if p.strip()}),
    pretty=lambda lst: "\n".join(["📁 files:"] + [f"- {p}" for p in lst]) or "(none)",
)

# ---------- internal helper ----------------------------------------


def _snap() -> list[str]:
    """Return a *copy* of the current snapshot so we can mutate safely."""
    return list(_file_db.latest())

# ───── public helpers consumed by your CLI ──────────────────────────


def clear_files() -> None:
    _file_db.clear()
    log.info("🧹 File set cleared.")


def append_file(path: str) -> None:
    p = path.strip()
    if not p:
        log.warning("⚠️  Empty path — nothing added.")
        return
    files = _snap()
    if p in files:
        log.warning(f"⚠️  Path already present: {p}")
        return
    files.append(p)
    _file_db.push(files)
    log.info(f"➕ Added {p}")


def remove_file(path: str) -> None:
    p = path.strip()
    if not p:
        log.warning("⚠️  Empty path — nothing removed.")
        return
    files = _snap()
    try:
        files.remove(p)
    except ValueError:
        log.warning(f"⚠️  Path not tracked: {p}")
        return
    _file_db.push(files)
    log.info(f"➖ Removed {p}")


def undo_files() -> None:
    if _file_db.undo():
        log.info("↩️ Reverted last change.")
    else:
        log.warning("⚠️  Nothing to undo.")


def summary_files() -> str:
    return _file_db.summary()


def get_latest_files() -> set[str]:
    """Convenience for other modules that need the current set."""
    return set(_file_db.latest())
