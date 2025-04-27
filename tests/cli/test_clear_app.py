
from typer.testing import CliRunner
import pytest

from kirby.cli.clear_app import clear_app

runner = CliRunner()

def test_clear_only_instructions(monkeypatch):
    called = {"ins": False, "files": False}
    monkeypatch.setattr("kirby.db.instruction_db.clear_instructions",
                        lambda: called.update(ins=True))
    monkeypatch.setattr("kirby.db.file_db.clear_files",
                        lambda: called.update(files=True))
    result = runner.invoke(clear_app, ["instructions"])
    assert result.exit_code == 0
    assert called["ins"] and not called["files"]

def test_clear_only_files(monkeypatch):
    called = {"ins": False, "files": False}
    monkeypatch.setattr("kirby.db.instruction_db.clear_instructions",
                        lambda: called.update(ins=True))
    monkeypatch.setattr("kirby.db.file_db.clear_files",
                        lambda: called.update(files=True))
    result = runner.invoke(clear_app, ["files"])
    assert result.exit_code == 0
    assert not called["ins"] and called["files"]
