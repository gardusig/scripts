
from unittest.mock import MagicMock
import pyperclip
from typer.testing import CliRunner

from kirby.cli.app import app

runner = CliRunner()

# ───────────────────────── helpers ────────────────────────── #


def _invoke(args: list[str] | str, **runner_kwargs):
    res = runner.invoke(app, args, **runner_kwargs)
    return res, res.stdout.strip()

# ───────────────────────── preview / show ────────────────────────── #


def test_preview(monkeypatch):
    monkeypatch.setattr("kirby.cli.app.summary_instruction", lambda: "INS-LIST")
    monkeypatch.setattr("kirby.cli.app.summary_files", lambda: "FILE-LIST")
    res, out = _invoke(["show"])
    assert res.exit_code == 0
    assert out.splitlines() == ["INS-LIST", "FILE-LIST"]

# ───────────────────────── copy command ────────────────────────── #


def test_copy_summary(monkeypatch):
    monkeypatch.setattr("kirby.cli.app.summary_instruction", lambda: "INS")
    monkeypatch.setattr("kirby.cli.app.get_file_contents", lambda: ["FILES"])

    buff = {}
    monkeypatch.setattr("kirby.cli.app._clipboard_set",
                        lambda txt: buff.setdefault("v", txt))

    _invoke(["copy"])
    assert buff["v"] == "INS\nFILES"


def test_copy_summary_no_clipboard(monkeypatch, capsys):
    monkeypatch.setattr("kirby.cli.app.summary_instruction", lambda: "I")
    monkeypatch.setattr("kirby.cli.app.get_file_contents", lambda: ["F"])

    class Boom(Exception):
        pass

    def boom(txt):
        raise pyperclip.PyperclipException()

    monkeypatch.setattr("pyperclip.copy", boom)

    res, out = _invoke(["copy"])
    # on failure, prints the text and echoes a warning
    assert res.exit_code == 0
    assert "I\nF" in out
    assert "Clipboard not available" in out

# ───────────────────────── add_instruction command ────────────────────────── #


def test_add_instruction(monkeypatch):
    mock_append_instruction = MagicMock()
    monkeypatch.setattr("kirby.cli.app.append_instruction", mock_append_instruction)

    res, out = _invoke(["eat", "Test instruction"])
    assert res.exit_code == 0
    mock_append_instruction.assert_called_once_with("Test instruction")


def test_add_instruction_empty(monkeypatch):
    mock_append_instruction = MagicMock()
    monkeypatch.setattr("kirby.cli.app.append_instruction", mock_append_instruction)

    res, out = _invoke(["eat", ""])
    assert res.exit_code == 1
    assert "Empty instruction provided." in out
    mock_append_instruction.assert_not_called()

# ───────────────────────── clear_all command ────────────────────────── #


def test_clear_all(monkeypatch):
    mock_clear_instructions = MagicMock()
    mock_clear_files = MagicMock()
    monkeypatch.setattr("kirby.cli.app.clear_instructions", mock_clear_instructions)
    monkeypatch.setattr("kirby.cli.app.clear_files", mock_clear_files)

    res, out = _invoke(["poop"])
    assert res.exit_code == 0
    mock_clear_instructions.assert_called_once()
    mock_clear_files.assert_called_once()
