import json
from pathlib import Path
import pytest
from db import file_db

FILE_SET_HISTORY = Path.home() / ".file_set_history.json"


@pytest.fixture(scope='function')
def mock_file_history(monkeypatch):
    def mock_load_file_history():
        return [["file1.txt", "file2.txt"], ["file3.txt"]]
    monkeypatch.setattr("src.db.file_db.load_file_history", mock_load_file_history)

    def mock_save_file_history(history):
        pass  # No-op for save operation
    monkeypatch.setattr("src.db.file_db.save_file_history", mock_save_file_history)


@pytest.mark.parametrize(
    "test_load_file_history",
    [[], [["file1.txt", "file2.txt"], ["file3.txt"]]]
)
def test_load_file_history(mock_file_history, expected_history):
    history = file_db.load_file_history()
    assert history == expected_history

    assert isinstance(history, list)
    assert all(isinstance(h, list) for h in history)


@pytest.mark.parametrize(
    "test_save_file_history",
    [[["file1.txt", "file2.txt"], ["file3.txt"]]]
)
def test_save_file_history(mock_file_history, file_history):
    file_db.save_file_history(file_history)
    # Check that the save function was simply called without errors


@pytest.mark.parametrize(
    "test_get_latest_files",
    [[["file1.txt", "file2.txt"]]]
)
def test_get_latest_files(mock_file_history):
    latest = file_db.get_latest_files()
    assert len(latest) == 2
    assert "file1.txt" in latest
    assert "file2.txt" in latest

    # Check that the get latest function was simply called without errors


def test_clear_files(mock_file_history):
    file_db.clear_files()
    assert file_db.get_latest_files() == set()

    # Check that the clear function was simply called without errors


@pytest.mark.parametrize(
    "test_append_file",
    [["file4.txt"]])
def test_append_file(mock_file_history, file_added):
    file_db.append_file(file_added)
    latest = file_db.get_latest_files()
    assert len(latest) == 3
    assert "file4.txt" in latest

    # Check that the append function was simply called without errors


@pytest.mark.parametrize(
    "test_undo-files",
    [["file1.txt", "file2.txt"]]
)
def test_undo_files(mock_file_history):
    file_db.undo_files()
    latest = file_db.get_latest_files()
    assert len(latest) == 2
    assert "file1.txt" in latest
    assert "file2.txt" in latest

    # Check that the undo function was simply called without errors
