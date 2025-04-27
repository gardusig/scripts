from __future__ import annotations
import logging

from kirby.db.history_db import HistoryDB
from kirby.util.session_util import create_session_file

log = logging.getLogger(__name__)


class FileHistoryStore:
    def __init__(self, name: str, pretty_label: str):
        self.name = name
        self._db: HistoryDB[list[str]] = HistoryDB(
            create_session_file(name),
            empty=[],
            normalise=lambda lst: sorted({p.strip() for p in lst if p.strip()}),
            pretty=lambda lst: (
                f"{pretty_label}:\n" + "\n".join(f"- {p}" for p in lst) or "(none)"
            ),
        )

    def _snap(self) -> list[str]:
        return list(self._db.latest())

    def clear(self) -> None:
        self._db.clear()
        log.info(f"🧹 {self.name} cleared.")

    def append(self, path: str) -> None:
        p = path.strip()
        if not p:
            log.warning("⚠️  Empty path — nothing added.")
            return
        files = self._snap()
        if p in files:
            log.warning(f"⚠️  Path already present: {p}")
            return
        files.append(p)
        self._db.push(files)
        log.info(f"➕ Added {p}")

    def remove(self, path: str) -> None:
        p = path.strip()
        if not p:
            log.warning("⚠️  Empty path — nothing removed.")
            return
        files = self._snap()
        try:
            files.remove(p)
        except ValueError:
            log.warning(f"⚠️  Path not tracked: {p}")
            return
        self._db.push(files)
        log.info(f"➖ Removed {p}")

    def undo(self) -> None:
        if self._db.undo():
            log.info("↩️ Reverted last change.")
        else:
            log.warning("⚠️  Nothing to undo.")

    def summary(self) -> str:
        return self._db.summary()

    def latest_set(self) -> set[str]:
        return set(self._db.latest())


# ───── instantiate two separate stores ────────────────────────────

_shared_store = FileHistoryStore("file_set_history", "📁 Shared files")
_proc_store = FileHistoryStore("processing_history", "🔄 Processing files")


# ───── public API for “shared files” ────────────────────────────


def clear_shared_files() -> None:
    _shared_store.clear()


def append_shared_file(path: str) -> None:
    _shared_store.append(path)


def remove_shared_file(path: str) -> None:
    _shared_store.remove(path)


def undo_shared_files() -> None:
    _shared_store.undo()


def summary_shared_files() -> str:
    return _shared_store.summary()


def get_shared_files() -> set[str]:
    return _shared_store.latest_set()


# ───── public API for “processing files” ────────────────────────


def clear_processing_files() -> None:
    _proc_store.clear()


def append_processing_file(path: str) -> None:
    _proc_store.append(path)


def remove_processing_file(path: str) -> None:
    _proc_store.remove(path)


def undo_processing_files() -> None:
    _proc_store.undo()


def summary_processing_files() -> str:
    return _proc_store.summary()


def get_processing_files() -> set[str]:
    return _proc_store.latest_set()
