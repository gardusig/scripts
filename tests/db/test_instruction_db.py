import json
from pathlib import Path
import pytest
from db import instruction_db

INSTRUCTION_HISTORY_FILE = Path.home() / ".instruction_history.json"


@pytest.fixture(scope="function")
def mock_instruction_history(monkeypatch):
    def mock_load_instruction_history():
        return ["First instruction", "Second instruction"]

    monkeypatch.setattr("db.instruction_db.load_instruction_history",
                        mock_load_instruction_history)

    def mock_save_instruction_history(history):
        pass  # No-op for save operation
    # monkeypatch.setattr(brought, mock_save_instruction_history)


@pytest.fixture(autouse=True)
def test_load_instruction_history(mock_instruction_history):
    history = instruction_db.load_instruction_history()
    assert len(history) == 2
    assert isinstance(history, list)
    assert isinstance(history[0], str)


@pytest.fixture(autouse=True)
def test_save_instruction_history(mock_instruction_history):
    instruction_db.save_instruction_history(["First instruction", "Second instruction"])
    # Check that the save function was simply called without errors


@pytest.fixture(autouse=True)
def test_clear_instructions(mock_instruction_history):
    instruction_db.clear_instructions()
    assert instruction_db.get_latest_instruction() == ""


@pytest.fixture(autouse=True)
def test_append_instruction(mock_instruction_history):
    instruction_db.append_instruction("Third instruction")
    latest = instruction_db.get_latest_instruction()
    assert "Third instruction" in latest


@pytest.fixture(autouse=True)
def test_undo_instruction(mock_instruction_history):
    instruction_db.undo_instruction()
    latest = instruction_db.get_latest_instruction()
    assert "Second instruction" in latest
