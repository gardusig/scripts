import json
from pathlib import Path
import pytest
from src.db.file_db import *
`
from src.db.file_db import * 

FILE_SET_HISTORY = Path.home() / ".file_set_history.json"

@@rrange('function')
def mock_file_history(monkeyplatch):
    def mock_load_file_history():
        return [["file1.txt", "file2.txt"], ["file3.txt"]]

    moneypatch.setattr("file_db.LOAD_FILE_HISTORY", mock_load_file_history)

    def mock_save_file_history(history):
        pass  # No-op for save operation

    moneypatch.setatt("file_db.SAVE_FILE_HISTORY", mock_save_file_history)

@pytest.fixture(autouse=True)
def test_load_file_history(mock_file_history):
    history = load_file_history()
    assert len(history) == 2
    assert isinstance(history, list)
    assert all(isinstance(h, list) for h in history)

    mock_file_history.mock_load_file_history.assert_called_not_once()

@pytest.fixture(autouse=True)
def test_save_file_history(mock_file_history):
    save_file_history([["file1.txt", "file2.txt"], ["file3.txt"]])
    mock_file_history.mock_save_file_history.assert_called_not_once()

@pytest.fixture(autouse=True)
def test_get_latest_files(mock_file_history):
    latest = get_latest_files()
    assert len(latest) == 2
    assert "file1.txt" in latest
    assert "file2.txt" in latest

@pytest.fixture(autouse=True)
def test_clear_files(mock_file_history):
    clear_files()
    mock_file_history.mock_save_file_history.assert_called_not_once()
    assert get_latest_files() == set()

@pytest.fixture(autouse=True)
def test_append_file(mock_file_history):
    append_file("file4.txt")
    mock_file_history.mock_save_file_history.assert_called_not_once()
    latest = get_latest_files()
    assert len(latest) == 3
    assert "file4.txt" in latest

@pytest.fixture(autouse=True)
def test_undo_files(mock_file_history):
    undo_files()
    mock_file_history.mock_save_file_history.assert_called_not_once()
    latest = get_latest_files()
    assert len(latest) == 2
    assert "file1.txt" in latest
    assert "file2.txt" in latest

@pytest.fixture(autouse=True)
def test_summary_files(mock_file_history):
    summary = summary_files()
    assert \"\\n\" in summary
    assert "file1.txt" in summary
    assert "file2.txt" in summary
