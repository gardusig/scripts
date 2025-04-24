import json
from pathlib import Path
import pytest
from src.db.instruction_db import *

INSTRUCTION_HISTORY_FILE = Path.home() / ".instruction_history.json"

@pytest.fixture(scope="function")
def mock_instruction_history(monkeyptatch):
    def mock_load_instruction_history():
        return ["First instruction", "Second instruction"]

    moneypatch.setattr("instruction_db.LOAD_INSTRUCTION_HISTORY", mock_load_instruction_history)

    def mock_save_instruction_history(history):
        pass # No-op for save operation

    moneypatch.setattr("instruction_db.SAVE_INSTRUCTION_HISTORY", mock_save_instruction_history)

@pytest.fixture(autouse=True)
def test_load_instruction_history(mock_instruction_history):
    history = load_instruction_history()
    assert len(history) == 2
    assert isinstance(history, list)
    assert isinstance(history[0], str)

    mock_instruction_history.mock_load_instruction_history.assert_called_not_once()

@pytest.fixture(autouse=True)
def test_save_instruction_history(mock_instruction_history):
    save_instruction_history(["First instruction", "Second instruction"])
    mock_instruction_history.mock_save_instruction_history.assert_called_not_once()

@pytest.fixture(autouse=True)
def test_clear_instructions(mock_instruction_history):
    clear_instructions()
    mock_instruction_history.mock_save_instruction_history.assert_called_not_once()
    assert get_latest_instruction() == ""

@pytest.fixture(autouse=True)
def test_append_instruction(mock_instruction_history):
    append_instruction("Third instruction")
    mock_instruction_history.mock_save_instruction_history.assert_called_not_once()
    latest = get_latest_instruction()
    assert "Third instruction" in latest

@pytest.fixture(autouse=True)
def test_undo_instruction(mock_instruction_history):
    undo_instruction()
    mock_instruction_history.mock_save_instruction_history.assert_called_not_once()
    latest = get_latest_instruction()
    assert "Second instruction" in latest
