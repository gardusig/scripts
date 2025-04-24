import logging
import shutil
import pytest
from pathlib import Path

from util.file_util import (
    should_ignore,
    get_all_files,
    stringify_file_contents,
)

TEST_DIR = Path("/tmp/kirby_test")
TEST_FILE = TEST_DIR / "file.txt"
INSTRUCTION_FILE = TEST_DIR / "instruction.json"


@pytest.fixture(autouse=True)
def setup_and_cleanup():
    TEST_DIR.mkdir(parents=True, exist_ok=True)
    yield
    shutil.rmtree(TEST_DIR)


@pytest.mark.parametrize(
    "name, patterns, expected",
    [
        ("file.py", ["*.pyc"], False),
        ("__pycache__", ["__pycache__"], True),
        ("image.jpg", ["*.jpg"], True),
    ],
)
def test_should_ignore(name, patterns, expected):
    assert should_ignore(name, patterns) is expected


def test_get_all_files(tmp_path):
    TEST_DIR = tmp_path
    (TEST_DIR / "a.txt").write_text("hi")
    (TEST_DIR / "__pycache__").mkdir()
    (TEST_DIR / "__pycache__" / "ignored.pyc").write_text("ignored")

    files = [Path(p).resolve() for p in get_all_files(str(TEST_DIR))]

    assert (TEST_DIR / "a.txt").resolve() in files
    assert all("__pycache__" not in p.parts for p in files)


def test_stringify_file_contents():
    TEST_FILE.write_text("hello\n")
    result = stringify_file_contents({str(TEST_FILE)})
    assert result == {str(TEST_FILE): "hello"}


def test_stringify_file_contents_error(caplog):
    bad_path = TEST_DIR / "missing.txt"
    with caplog.at_level(logging.DEBUG):
        result = stringify_file_contents({str(bad_path)})
        assert result.get(str(bad_path), "") == ""
        assert any("Error reading" in rec.message for rec in caplog.records)
