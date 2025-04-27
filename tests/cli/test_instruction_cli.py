from typer.testing import CliRunner

from kirby.cli.clear_app import clear_app
from kirby.cli.list_app import list_app
from kirby.cli.undo_app import undo_app

runner = CliRunner()


def test_instruction_clear_calls_db(monkeypatch):
    called = {"flag": False}

    def fake():
        called["flag"] = True

    # clear instructions now lives under clear_app
    monkeypatch.setattr("kirby.cli.clear_app.clear_instructions", fake)
    result = runner.invoke(clear_app, ["instructions"])
    assert result.exit_code == 0
    assert called["flag"]


def test_instruction_undo_calls_db(monkeypatch):
    called = {"flag": False}

    def fake():
        called["flag"] = True

    # undo instructions now under undo_app
    monkeypatch.setattr("kirby.cli.undo_app.undo_instructions", fake)
    result = runner.invoke(undo_app, ["instruction"])
    assert result.exit_code == 0
    assert called["flag"]


def test_instruction_list_prints_summary(monkeypatch):
    monkeypatch.setattr("kirby.cli.list_app.summary_instruction",
                        lambda: "foo\nbar\nbaz\n")
    result = runner.invoke(list_app, ["list"])
    assert result.exit_code == 0
    assert "foo" in result.stdout and "baz" in result.stdout
