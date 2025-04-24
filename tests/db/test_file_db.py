import logging
from typing import List

import pytest

from db import file_db
from db.history_db import HistoryDB


@pytest.fixture(autouse=True)
def isolate_db(monkeypatch, tmp_path):
    fp = tmp_path / "file_hist.json"
    fresh = HistoryDB[List[str]](fp, empty=[])
    monkeypatch.setattr(file_db, "_file_db", fresh, raising=True)
    yield


def test_append_and_get(monkeypatch):
    file_db.append_file("foo.txt")
    file_db.append_file("bar.txt")
    assert file_db.get_latest_files() == {"foo.txt", "bar.txt"}


def test_append_duplicate(caplog):
    caplog.set_level(logging.WARNING, logger="db.file_db")
    file_db.append_file("dup.txt")
    file_db.append_file("dup.txt")
    assert file_db.get_latest_files() == {"dup.txt"}


def test_remove_and_undo(caplog):
    file_db.append_file("a.txt")
    file_db.append_file("b.txt")
    assert file_db.get_latest_files() == {"a.txt", "b.txt"}

    file_db.remove_file("a.txt")
    assert file_db.get_latest_files() == {"b.txt"}

    file_db.undo_files()
    assert file_db.get_latest_files() == {"a.txt", "b.txt"}


def test_clear():
    file_db.append_file("x.txt")
    assert file_db.get_latest_files() == {"x.txt"}
    file_db.clear_files()
    assert file_db.get_latest_files() == set()
