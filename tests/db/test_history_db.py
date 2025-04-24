import json
from db.history_db import HistoryDB


def test_history_db_push_undo_clear(tmp_path):
    fp = tmp_path / "hist.json"

    db = HistoryDB[list[str]](fp, empty=[])
    assert db.latest() == []

    db.push(["a"])
    assert db.latest() == ["a"]

    db.push(["a", "b"])
    assert db.latest() == ["a", "b"]

    assert db.undo() is True
    assert db.latest() == ["a"]

    assert db.undo() is True
    assert db.latest() == []

    assert db.undo() is False

    db.push(["x"])
    db.clear()
    assert db.latest() == []

    on_disk = json.loads(fp.read_text())
    assert on_disk == [[]]


def test_history_db_normalise(tmp_path):
    fp = tmp_path / "hist2.json"

    db = HistoryDB[list[str]](
        fp,
        empty=[],
        normalise=lambda lst: sorted(set(lst)),
    )
    db.push(["b", "a", "b"])
    assert db.latest() == ["a", "b"]
