from pathlib import Path
from typing import List
import pytest
from typer.testing import CliRunner
from kirby.cli import file_cli


runner = CliRunner()


@pytest.fixture
def monkey_append(monkeypatch) -> list[Path]:
    recorded: List[Path] = []

    def fake_append(path: str) -> None:
        recorded.append(Path(path))

    monkeypatch.setattr(file_cli, "append_file", fake_append)
    return recorded


@pytest.fixture
def monkey_remove(monkeypatch) -> list[str]:
    removed: List[str] = []

    def fake_remove(path: str) -> None:
        removed.append(path)

    monkeypatch.setattr(file_cli, "remove_file", fake_remove)
    return removed


def test_clear_calls_clear_files(monkeypatch):
    called = {"flag": False}

    def fake_clear() -> None:
        called["flag"] = True

    monkeypatch.setattr(file_cli, "clear_files", fake_clear)
    result = runner.invoke(file_cli.file_app, ["clear"])
    assert result.exit_code == 0
    assert called["flag"]


@pytest.mark.parametrize(
    "user_input, expanded",
    [
        ("a.py", ["a.py"]),
        ("src/", ["src/x.py", "src/y.py"]),
    ],
)
def test_add_happy_path(user_input, expanded, monkeypatch, monkey_append):
    monkeypatch.setattr(file_cli, "get_all_files", lambda s: expanded)
    result = runner.invoke(file_cli.file_app, ["add", user_input])
    assert result.exit_code == 0
    assert [p.as_posix() for p in monkey_append] == expanded


def test_add_rejects_empty(monkeypatch):
    monkeypatch.setattr(
        file_cli, "get_all_files", lambda _: (_ for _ in ()).throw(RuntimeError)
    )
    result = runner.invoke(file_cli.file_app, ["add", "  "])
    assert result.exit_code == 1
    assert "Empty string" in result.output


def test_remove_happy_path(monkey_remove):
    result = runner.invoke(file_cli.file_app, ["remove", "obsolete.txt"])
    assert result.exit_code == 0
    assert monkey_remove == ["obsolete.txt"]


def test_remove_rejects_empty():
    result = runner.invoke(file_cli.file_app, ["remove", "  "])
    assert result.exit_code == 1
    assert "Empty string" in result.output


def test_undo_calls_undo_files(monkeypatch):
    called = {"flag": False}

    def fake_undo() -> None:
        called["flag"] = True

    monkeypatch.setattr(file_cli, "undo_files", fake_undo)
    result = runner.invoke(file_cli.file_app, ["undo"])
    assert result.exit_code == 0
    assert called["flag"]


def test_list_prints_summary(monkeypatch):
    monkeypatch.setattr(file_cli, "summary_files", lambda: "alpha\nbeta\n")
    result = runner.invoke(file_cli.file_app, ["list"])
    assert result.exit_code == 0
    assert "alpha" in result.output and "beta" in result.output
