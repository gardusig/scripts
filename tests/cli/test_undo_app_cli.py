from typer.testing import CliRunner

from kirby.cli.undo_app import undo_app

runner = CliRunner()


def test_undo_instruction(monkeypatch):
    called = {"flag": False}
    monkeypatch.setattr("kirby.cli.undo_app.undo_instructions",
                        lambda: called.update(flag=True))
    result = runner.invoke(undo_app, ["instruction"])
    assert result.exit_code == 0
    assert called["flag"]


def test_undo_file(monkeypatch):
    called = {"flag": False}
    monkeypatch.setattr("kirby.cli.undo_app.undo_files",
                        lambda: called.update(flag=True))
    result = runner.invoke(undo_app, ["file"])
    assert result.exit_code == 0
    assert called["flag"]
