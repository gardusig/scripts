# db/instruction_db.py
from __future__ import annotations

import logging
from typing import List, Set

from db.history_db import HistoryDB
from logging_setup import get_log_file_handler
from util.file_util import create_session_file

log = logging.getLogger(__name__)
log.addHandler(get_log_file_handler(__name__))

# ───── underlying generic store ─────────────────────────────────────
_instruction_db: HistoryDB[List[str]] = HistoryDB(
    create_session_file("instruction_history"),
    empty=[],
    # strip trailing whitespace, drop blank lines – duplicates allowed
    normalise=lambda lines: [ln.strip() for ln in lines if ln.strip()],
    pretty=lambda lines: (
        "\n".join(["📜 instructions:"] + [f"- {ln}" for ln in lines])
        if lines
        else "(none)"
    ),
)

# ---------- internal helper ----------------------------------------


def _snap() -> List[str]:
    """Return a *copy* of the current snapshot so we can mutate safely."""
    return list(_instruction_db.latest())


# ───── public helpers consumed by your CLI ──────────────────────────


def clear_instructions() -> None:
    _instruction_db.clear()
    log.info("🧹 Instruction list cleared.")


def append_instruction(line: str) -> None:
    text = line.strip()
    if not text:
        log.warning("⚠️  Empty instruction — nothing added.")
        return
    instructions = _snap()
    if text in instructions:
        log.warning(f"⚠️  Instruction already present: {text}")
        return
    instructions.append(text)
    _instruction_db.push(instructions)
    log.info(f"➕ Added instruction: {text}")


def remove_instruction(line: str) -> None:
    text = line.strip()
    if not text:
        log.warning("⚠️  Empty instruction — nothing removed.")
        return
    instructions = _snap()
    try:
        instructions.remove(text)
    except ValueError:
        log.warning(f"⚠️  Instruction not tracked: {text}")
        return
    _instruction_db.push(instructions)
    log.info(f"➖ Removed instruction: {text}")


def undo_instructions() -> None:
    if _instruction_db.undo():
        log.info("↩️ Reverted last change.")
    else:
        log.warning("⚠️  Nothing to undo.")


def summary_instruction() -> str:
    return _instruction_db.summary()


def get_latest_instructions() -> List[str]:
    """Convenience for other modules that need the current set."""
    return list(_instruction_db.latest())
