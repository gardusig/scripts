from typer.testing import CliRunner

from kirby.cli.remove_app import remove_app

runner = CliRunner()


def test_remove_success(monkeypatch):
    removed = []
    monkeypatch.setattr("kirby.cli.remove_app.remove_file",
                        lambda path: removed.append(path))
    result = runner.invoke(remove_app, ["foo.txt"])
    assert result.exit_code == 0
    assert removed == ["foo.txt"]


def test_remove_empty():
    result = runner.invoke(remove_app, ["   "])
    assert result.exit_code == 1
    assert "Empty string provided." in result.stdout
