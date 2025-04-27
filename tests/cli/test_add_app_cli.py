
import pyperclip
import pytest
from typer.testing import CliRunner

from kirby.cli.add_app import add_app

runner = CliRunner()


@pytest.fixture
def append_calls(monkeypatch):
    calls = []
    monkeypatch.setattr("kirby.cli.add_app.append_instruction",
                        lambda text: calls.append(("ins", text)))
    monkeypatch.setattr("kirby.cli.add_app.append_file",
                        lambda path: calls.append(("file", path)))
    return calls


def test_add_clipboard(monkeypatch, append_calls):
    # stub the private helper
    monkeypatch.setattr("kirby.cli.add_app._clipboard_get", lambda: "kappa")
    result = runner.invoke(add_app, ["clipboard"])
    assert result.exit_code == 0
    assert append_calls == [("ins", "kappa")]


def test_add_clipboard_no_clipboard(monkeypatch):
    monkeypatch.setattr(
        "pyperclip.paste", lambda: (
            _ for _ in ()).throw(pyperclip.PyperclipException()))
    result = runner.invoke(add_app, ["clipboard"])
    assert result.exit_code == 1
    assert "⚠️  Clipboard not available on this system." in result.output


def test_add_file(monkeypatch, append_calls):
    monkeypatch.setattr("kirby.cli.add_app.get_all_files",
                        lambda path: ["file1.txt", "file2.txt"])
    result = runner.invoke(add_app, ["file", "test_path"])
    assert result.exit_code == 0
    assert append_calls == [("file", "file1.txt"), ("file", "file2.txt")]


def test_add_file_empty_string():
    result = runner.invoke(add_app, ["file", ""])
    assert result.exit_code == 1
    assert "⚠️ Empty string provided." in result.output
