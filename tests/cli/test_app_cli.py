from __future__ import annotations

from unittest.mock import MagicMock

from instruction.response.response_format import RESPONSE_FORMAT_INSTRUCTIONS
from instruction.unit_test import UNIT_TEST_INSTRUCTIONS
import pytest
import typer
from typer.testing import CliRunner

from cli import app_cli

runner = CliRunner()

# ───────────────────────── helpers ────────────────────────── #


def _invoke(args: list[str] | str, **runner_kwargs):
    """Utility: invoke CLI and return (result, stdout-stripped)."""
    res = runner.invoke(app_cli.app, args, **runner_kwargs)
    return res, res.stdout.strip()


# ───────────────────────── _clipboard_get / _clipboard_set ────────────────── #

def test_clipboard_get_success(monkeypatch):
    monkeypatch.setattr(app_cli.pyperclip, "paste", lambda: "hi")
    assert app_cli._clipboard_get() == "hi"


def test_clipboard_get_failure(monkeypatch):
    def boom():
        raise app_cli.PyperclipException("no display")

    monkeypatch.setattr(app_cli.pyperclip, "paste", boom)
    with pytest.raises(typer.Exit):
        app_cli._clipboard_get()


def test_clipboard_set_success(monkeypatch):
    sink = {}
    monkeypatch.setattr(app_cli.pyperclip, "copy", sink.setdefault)
    app_cli._clipboard_set("abc")
    assert "abc" in sink


def test_clipboard_set_failure(monkeypatch, capsys):
    def boom(_):
        raise app_cli.PyperclipException()

    monkeypatch.setattr(app_cli.pyperclip, "copy", boom)
    app_cli._clipboard_set("xyz")
    captured = capsys.readouterr()
    assert "xyz" in captured.out
    assert "Clipboard not available" in captured.err


# ───────────────────────── clear command ──────────────────── #

@pytest.mark.parametrize(
    ("flags", "expect_ins", "expect_files"),
    [
        ([], True, True),
        (["--no-instructions"], False, True),
        (["--no-files"], True, False),
    ],
)
def test_clear(monkeypatch, flags, expect_ins, expect_files):
    cleared = {"ins": False, "files": False}

    monkeypatch.setattr(app_cli, "clear_instructions",
                        lambda: cleared.update(ins=True))
    monkeypatch.setattr(app_cli, "clear_files", lambda: cleared.update(files=True))

    res, _ = _invoke(["clear", *flags])
    assert res.exit_code == 0
    assert cleared["ins"] is expect_ins
    assert cleared["files"] is expect_files


# ───────────────────────── add / add-clip commands ─────────────────── #

def test_add_instruction_success(monkeypatch):
    recorded = {}

    def fake_append(arg):
        recorded["arg"] = arg

    monkeypatch.setattr(app_cli, "append_instruction", fake_append)

    res, _ = _invoke(["add", "  hello  "])
    assert res.exit_code == 0
    assert recorded["arg"] == "hello"


def test_add_instruction_empty():
    res, out = _invoke(["add", "  "])
    assert res.exit_code == 1
    assert "Empty instruction" in out


def test_add_clipboard(monkeypatch):
    monkeypatch.setattr(app_cli, "_clipboard_get", lambda: "from clip")
    called = {}

    monkeypatch.setattr(app_cli, "append_instruction",
                        lambda txt: called.setdefault("val", txt))

    res, _ = _invoke("add-clip")
    assert res.exit_code == 0
    assert called["val"] == "from clip"


# ───────────────────────── copy command ──────────────────── #

def test_copy_summary(monkeypatch):
    monkeypatch.setattr(app_cli, "summary_instruction", lambda: "INS")
    monkeypatch.setattr(app_cli, "summary_files", lambda: "FILES")

    buff = {}
    monkeypatch.setattr(app_cli, "_clipboard_set",
                        lambda txt: buff.setdefault("v", txt))

    _invoke("copy")
    assert buff["v"] == "INS\nFILES"


# ───────────────────────── unit-test command ──────────────────── #

def test_create_tests(monkeypatch):
    monkeypatch.setattr(app_cli, "get_ai_client", lambda: "dummy_client")

    send_spy = MagicMock(return_value="raw-response")
    monkeypatch.setattr(app_cli, "send_message", send_spy)

    parsed = {"tests/test_sample.py": "assert 1"}
    monkeypatch.setattr(app_cli, "parse_code_response", lambda _: parsed)

    res, _ = _invoke("unit-test")

    send_spy.assert_called_once_with(
        "dummy_client", RESPONSE_FORMAT_INSTRUCTIONS + UNIT_TEST_INSTRUCTIONS)
    assert res.exit_code == 0


def test_preview(monkeypatch):
    monkeypatch.setattr(app_cli, "summary_instruction", lambda: "INS-LIST")
    monkeypatch.setattr(app_cli, "summary_files", lambda: "FILE-LIST")

    res, out = _invoke("show")
    assert res.exit_code == 0
    assert out.splitlines() == ["INS-LIST", "FILE-LIST"]


def test_copy_summary_no_clipboard(monkeypatch, capsys):
    monkeypatch.setattr(app_cli, "summary_instruction", lambda: "I")
    monkeypatch.setattr(app_cli, "summary_files", lambda: "F")

    def boom(_):
        raise app_cli.PyperclipException()

    monkeypatch.setattr(app_cli.pyperclip, "copy", boom)

    res, out = _invoke("copy")

    assert res.exit_code == 0
    assert "I\nF" in out
