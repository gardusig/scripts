import logging
import pytest
from pathlib import Path

import db.instruction_db as instr_db
from db.history_db import HistoryDB


@pytest.fixture(autouse=True)
def fresh_history(tmp_path: Path, monkeypatch):
    store_file: Path = tmp_path / "instruction_history.json"

    new_db = HistoryDB[list[str]](
        store_file,
        empty=[],
        normalise=lambda l: [ln.rstrip() for ln in l if ln.strip()],
        pretty=lambda l: (
            "\n".join(["📜 instructions:"] + [f"- {ln}" for ln in l])
            if l
            else "(none)"
        ),
    )
    monkeypatch.setattr(instr_db, "_instruction_db", new_db)

    # mute real file-based log handlers
    instr_db.log.handlers.clear()
    instr_db.log.addHandler(logging.NullHandler())

    yield


# ──────────────────────── helper for reading state quickly ───────────────────
def _latest():
    """Shorthand to fetch current list without caring about order."""
    return instr_db.get_latest_instructions()


# ───────────────────────── tests ─────────────────────────────────────────────

def test_append_and_latest(caplog):
    with caplog.at_level(logging.INFO):
        instr_db.append_instruction("  foo  ")

    assert _latest() == ["foo"]
    assert any("Added instruction" in rec.message for rec in caplog.records)


def test_append_duplicate(caplog):
    instr_db.append_instruction("bar")
    with caplog.at_level(logging.WARNING):
        instr_db.append_instruction("bar")

    assert _latest() == ["bar"]
    assert any("already present" in rec.message for rec in caplog.records)


def test_remove_instruction(caplog):
    instr_db.append_instruction("a")
    instr_db.append_instruction("b")
    with caplog.at_level(logging.INFO):
        instr_db.remove_instruction("a")

    assert _latest() == ["b"]
    assert any("Removed instruction" in rec.message for rec in caplog.records)


def test_remove_nonexistent(caplog):
    instr_db.append_instruction("only-one")
    with caplog.at_level(logging.WARNING):
        instr_db.remove_instruction("ghost")

    # unchanged
    assert _latest() == ["only-one"]
    assert any("not tracked" in rec.message for rec in caplog.records)


def test_undo_flow():
    instr_db.append_instruction("v1")
    instr_db.append_instruction("v2")
    assert _latest() == ["v1", "v2"]

    instr_db.undo_instructions()
    assert _latest() == ["v1"]

    instr_db.undo_instructions()
    assert _latest() == []


def test_clear():
    instr_db.append_instruction("something")
    instr_db.clear_instructions()
    assert _latest() == []


def test_summary_formats():
    assert instr_db.summary_instruction() == "(none)"

    instr_db.append_instruction("do X")
    instr_db.append_instruction("do Y")
    summary = instr_db.summary_instruction()

    assert summary.startswith("📜 instructions:")
    assert "- do X" in summary and "- do Y" in summary
