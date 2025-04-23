import json
import shutil
import pytest
from pathlib import Path
from unittest.mock import patch

from util.file_util import (
    should_ignore,
    get_all_files,
    stringify_file_contents,
    load_instructions,
    rewrite_files,
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
    ]
)
def test_should_ignore(name, patterns, expected):
    assert should_ignore(name, patterns) is expected


def test_get_all_files():
    (TEST_DIR / "a.txt").write_text("hi")
    (TEST_DIR / "__pycache__").mkdir()
    (TEST_DIR / "__pycache__" / "ignored.pyc").write_text("ignored")

    files = get_all_files(str(TEST_DIR))
    assert str(TEST_DIR / "a.txt") in files
    assert all("__pycache__" not in f for f in files)


def test_stringify_file_contents():
    TEST_FILE.write_text("hello\n")
    result = stringify_file_contents({str(TEST_FILE)})
    assert result == {str(TEST_FILE): "hello"}


def test_stringify_file_contents_error(capfd):
    bad_path = TEST_DIR / "missing.txt"
    result = stringify_file_contents({str(bad_path)})
    out, _ = capfd.readouterr()
    assert "Error reading file" in out
    assert str(bad_path) not in result or result[str(bad_path)] == ""


def test_load_instructions(tmp_path):
    res_dir = tmp_path / "resources" / "instructions"
    res_dir.mkdir(parents=True)
    inst_path = res_dir / "instruction.json"
    inst_path.write_text(json.dumps(["Test one", "Test two"]))
    result = load_instructions(["instruction.json"], base_dir=res_dir)
    assert result == "Test oneTest two"


def test_rewrite_files():
    file_path = str(TEST_FILE)
    content = "new content"
    rewrite_files({file_path: content}, allowed_file_prefixes=[str(TEST_DIR)])
    assert TEST_FILE.read_text() == content
