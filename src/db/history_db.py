import json
from contextlib import suppress
import logging
from pathlib import Path
from typing import Callable, Generic, List, TypeVar

from logging_setup import get_log_file_handler

log = logging.getLogger(__name__)
log.addHandler(get_log_file_handler(__name__))

T = TypeVar("T")


class HistoryDB(Generic[T]):
    """
    JSON-file-backed stack of snapshots.
    `push()` adds a new snapshot; `undo()` pops the latest one.
    """

    def __init__(
        self,
        file_path: Path,
        *,
        empty: T,
        normalise: Callable[[T], T] | None = None,
        pretty: Callable[[T], str] | None = None,
    ) -> None:
        self._file = file_path
        self._empty = empty
        self._normalise = normalise or (lambda x: x)
        self._pretty = pretty or json.dumps

        # bootstrap file with one empty snapshot
        if not self._file.exists():
            self._save([self._empty])

    # ───── public API ────────────────────────────────────────────────

    def latest(self) -> T:
        return self._load()[-1]

    def push(self, snapshot: T) -> None:
        history = self._load()
        history.append(self._normalise(snapshot))
        self._save(history)

    def undo(self) -> bool:
        history = self._load()
        if len(history) <= 1:
            return False
        history.pop()
        self._save(history)
        return True

    def clear(self) -> None:
        self._save([self._empty])

    def summary(self) -> str:
        return self._pretty(self.latest())

    # ───── private helpers ───────────────────────────────────────────

    def _load(self) -> List[T]:
        with suppress(Exception):
            with open(self._file, "r", encoding="utf-8") as f:
                return json.load(f)
        log.warning(f"⚠️  Failed to load {self._file.name}; resetting.")
        return [self._empty]

    def _save(self, history: List[T]) -> None:
        try:
            with open(self._file, "w", encoding="utf-8") as f:
                json.dump(history, f, indent=2)
        except Exception as e:
            log.warning(f"❌ Failed to save {self._file.name}: {e}")
