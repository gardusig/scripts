from __future__ import annotations
import logging

from kirby.db.history_db import HistoryDB
from kirby.util.session_util import create_session_file

log = logging.getLogger(__name__)


class PromptHistoryStore:
    def __init__(self, name: str, pretty_label: str):
        self.name = name
        self._db: HistoryDB[list[str]] = HistoryDB(
            create_session_file(self.name),
            empty=[],
            normalise=lambda lines: [ln.strip() for ln in lines if ln.strip()],
            pretty=lambda lines: (
                f"{pretty_label}:\n"
                + ("\n".join(f"- {ln}" for ln in lines) if lines else "(none)")
            ),
        )

    def _snap(self) -> list[str]:
        """Get a mutable copy of the latest prompt list."""
        return list(self._db.latest())

    def clear(self) -> None:
        self._db.clear()
        log.info(f"🧹 {self.name} cleared.")

    def append(self, prompt: str) -> None:
        p = prompt.strip()
        if not p:
            log.warning("⚠️  Empty prompt — nothing added.")
            return
        items = self._snap()
        if p in items:
            log.warning(f"⚠️  Prompt already present: {p}")
            return
        items.append(p)
        self._db.push(items)
        log.info(f"➕ Added prompt: {p}")

    def remove(self, prompt: str) -> None:
        p = prompt.strip()
        if not p:
            log.warning("⚠️  Empty prompt — nothing removed.")
            return
        items = self._snap()
        try:
            items.remove(p)
        except ValueError:
            log.warning(f"⚠️  Prompt not tracked: {p}")
            return
        self._db.push(items)
        log.info(f"➖ Removed prompt: {p}")

    def undo(self) -> None:
        if self._db.undo():
            log.info("↩️  Reverted last prompt change.")
        else:
            log.warning("⚠️  Nothing to undo.")

    def summary(self) -> str:
        return self._db.summary()

    def latest(self) -> list[str]:
        """Convenience for modules that need the current prompts."""
        return list(self._db.latest())


# ───── instantiate your prompt‐store ────────────────────────────

_prompt_store = PromptHistoryStore("prompt_history", "📜 Prompts")


# ───── public API for prompts ───────────────────────────────────


def clear_prompts() -> None:
    _prompt_store.clear()


def append_prompt(line: str) -> None:
    _prompt_store.append(line)


def remove_prompt(line: str) -> None:
    _prompt_store.remove(line)


def undo_prompts() -> None:
    _prompt_store.undo()


def summary_prompts() -> str:
    return _prompt_store.summary()


def get_latest_prompts() -> list[str]:
    return _prompt_store.latest()
