from typer.testing import CliRunner

from kirby.cli.list_app import list_app

runner = CliRunner()


def test_list_files(monkeypatch):
    monkeypatch.setattr("kirby.cli.list_app.summary_files", lambda: "F1\nF2")
    result = runner.invoke(list_app, ["files"])
    assert result.exit_code == 0
    assert "F1" in result.stdout and "F2" in result.stdout


def test_list_instructions(monkeypatch):
    monkeypatch.setattr("kirby.cli.list_app.summary_instruction", lambda: "I1\nI2")
    result = runner.invoke(list_app, ["list"])
    assert result.exit_code == 0
    assert "I1" in result.stdout and "I2" in result.stdout
