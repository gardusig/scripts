from __future__ import annotations

from kirby.db.history_db import HistoryDB
from kirby.util.session_util import create_session_file


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
        print(f"🧹 {self.name} cleared.")

    def append(self, path: str) -> None:
        p = path.strip()
        if not p:
            print("⚠️  Empty path — nothing added.")
            return
        files = self._snap()
        if p in files:
            print(f"⚠️  Path already present: {p}")
            return
        files.append(p)
        self._db.push(files)
        print(f"➕ Added {p}")

    def remove(self, path: str) -> None:
        p = path.strip()
        if not p:
            print("⚠️  Empty path — nothing removed.")
            return
        files = self._snap()
        try:
            files.remove(p)
        except ValueError:
            print(f"⚠️  Path not tracked: {p}")
            return
        self._db.push(files)
        print(f"➖ Removed {p}")

    def undo(self) -> None:
        if self._db.undo():
            print("↩️ Reverted last change.")
        else:
            print("⚠️  Nothing to undo.")

    def summary(self) -> str:
        return self._db.summary()

    def latest_set(self) -> set[str]:
        return set(self._db.latest())
