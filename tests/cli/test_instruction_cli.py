import pytest
from typer.testing import CliRunner

from kirby.cli import instruction_cli
from kirby.cli.app_cli import app

runner = CliRunner()

# ───────────────────────── fixtures ──────────────────────────


@pytest.fixture
def spy_clear(monkeypatch):
    called = {"flag": False}

    def _fake():
        called["flag"] = True

    monkeypatch.setattr(instruction_cli, "clear_instructions", _fake)
    return called


@pytest.fixture
def spy_undo(monkeypatch):
    called = {"flag": False}

    def _fake():
        called["flag"] = True

    monkeypatch.setattr(instruction_cli, "undo_instructions", _fake)
    return called


# ────────────────────────── tests ────────────────────────────
def test_instruction_clear_calls_db(spy_clear):
    result = runner.invoke(app, ["instruction", "clear"])
    assert result.exit_code == 0
    assert spy_clear["flag"]


def test_instruction_undo_calls_db(spy_undo):
    result = runner.invoke(app, ["instruction", "undo"])
    assert result.exit_code == 0
    assert spy_undo["flag"]


def test_instruction_list_prints_summary(monkeypatch):
    monkeypatch.setattr(
        instruction_cli, "summary_instruction", lambda: "foo\nbar\nbaz\n"
    )
    result = runner.invoke(app, ["instruction", "list"])
    assert result.exit_code == 0
    assert "foo" in result.output and "baz" in result.output
