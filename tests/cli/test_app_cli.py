from __future__ import annotations

from unittest.mock import MagicMock

import pyperclip

import pytest
import typer
from typer.testing import CliRunner

from kirby.cli import app_cli

runner = CliRunner()

# ───────────────────────── helpers ────────────────────────── #


def _invoke(args: list[str] | str, **runner_kwargs):
    """Utility: invoke CLI and return (result, stdout-stripped)."""
    res = runner.invoke(app_cli.app, args, **runner_kwargs)
    return res, res.stdout.strip()


# ───────────────────────── _clipboard_get / _clipboard_set ────────────────── #


def test_clipboard_get_success(monkeypatch):
    monkeypatch.setattr(pyperclip, "paste", lambda: "hi")
    assert app_cli._clipboard_get() == "hi"


def test_clipboard_get_failure(monkeypatch):
    def boom():
        raise app_cli.PyperclipException("no display")

    monkeypatch.setattr(pyperclip, "paste", boom)
    with pytest.raises(typer.Exit):
        app_cli._clipboard_get()


def test_clipboard_set_success(monkeypatch):
    sink = {}
    monkeypatch.setattr(pyperclip, "copy", sink.setdefault)
    app_cli._clipboard_set("abc")
    assert "abc" in sink


def test_clipboard_set_failure(monkeypatch, capsys):
    def boom(_):
        raise app_cli.PyperclipException()

    monkeypatch.setattr(pyperclip, "copy", boom)
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

    monkeypatch.setattr(app_cli, "clear_instructions", lambda: cleared.update(ins=True))
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
    monkeypatch.setattr(app_cli, "_clipboard_get", lambda: "from kirby.clip")
    called = {}

    monkeypatch.setattr(
        app_cli, "append_instruction", lambda txt: called.setdefault("val", txt)
    )

    res, _ = _invoke("add-clip")
    assert res.exit_code == 0
    assert called["val"] == "from kirby.clip"


# ───────────────────────── copy command ──────────────────── #


def test_copy_summary(monkeypatch):
    monkeypatch.setattr(app_cli, "summary_instruction", lambda: "INS")
    monkeypatch.setattr(app_cli, "summary_files", lambda: "FILES")

    buff = {}
    monkeypatch.setattr(
        app_cli, "_clipboard_set", lambda txt: buff.setdefault("v", txt)
    )

    _invoke("copy")
    assert buff["v"] == "INS\nFILES"


# ───────────────────────── unit-test command ──────────────────── #


def test_create_tests(monkeypatch):
    dummy_client = MagicMock()
    send_spy = dummy_client.send_message
    send_spy.return_value = "raw-response"

    monkeypatch.setattr(app_cli, "get_ai_client", lambda: dummy_client)
    parsed = {"tests/test_sample.py": "assert 1"}
    monkeypatch.setattr(app_cli, "parse_code_response", lambda _: parsed)
    monkeypatch.setattr(app_cli, "rewrite_files", lambda _: None)

    res, _ = _invoke("unit-test")
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

    monkeypatch.setattr(pyperclip, "copy", boom)

    res, out = _invoke("copy")

    assert res.exit_code == 0
    assert "I\nF" in out
