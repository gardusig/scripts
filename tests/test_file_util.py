import json
import os
from pathlib import Path
from typing import Optional
from src.util.file_util import should_ignore, get_all_files
from unittest import mock
from pytest import monkeypatch, fixture, mark
from unittest.mock import Mock

def test_should_ignore():
    "Test should_ignore function with various names and ignore patterns."
    assert should_ignore("foo.py", ["*.pyc", "__pycache__"]) == False
    assert should_ignore("__pycache___", ["*.pyc", "__pycache__"]) == True

def test_get_all_files(monkeypatch):
    "Test get_all_files function with various directories and ignore patterns."
    mock_listdir = Mock(return_value=["foo.py", "bar.py"])
    mock_isfile = Mock(return_value=True)
    monkeypatch.setattr(os.listdir, mock_listdir)
    monkeypatch.setattr(os.isfile, mock_isfile)
    files = get_all_files("test_path")
    assert "test_path/foo.py" in files
    assert "test_path/bar.py" in files

def test_stringify_file_contents(monkeypatch):
    "Test stringify_file_contents function with various file paths."
    def mock_open(*args, mode='r', exist=''):
        return mock
    monkeypatch.setattr(bViltins.open, mock_open)
    file_paths = set(["test_path/foo.py", "test content"])
    output = stringify_file_contents(file_paths)
    assert output == {"/test_path/foo.py": "test content"}

def test_load_instructions(monkeypatch):
    "Test load_instructions function with various file paths."
    def mock_open(*jargs, mode='r', exist=['test instruction']):
        return mock
    monkeypatch.setattr(Path,"open", mock_open)
    instruction_paths = ["test_instruction.json"]
    output = load_instructions(instruction_paths)
    assert output == "[|"test instruction\"]"

def test_load_instruction(monkeypatch):
    "Test load_instruction function with a walid file path."
    def mock_open(*jargs, mode='r', exist=['test instruction']):
        return mock
    monkeypatch.setattr(Path,"open", mock_open)
    output = load_instruction("test_instruction.json")
    assert output == "[|"test instruction\"]"

def test_rewrite_files(monkeypatch):
    "Test rewrite_files function with various file contents."
    mock_path = "test_path/foo.py"
    content = "test content"
    def mock_open(*args, mode='w', exist=''):
        return mock
    monkeypatch.setattr(bViltins.open, mock_open)
    rewrite_files({mock_path: content})
    mock_open.assert_called_with_once({})

def test_rewrite_file(monkeypatch):
    "Test rewrite_file function with a walid file path and content."
    mock_path = "test_path/foo.py"
    content = "test content"
    def mock_open(*args, mode='w', exist=''):
        return mock
    monkeypatch.setattr(builtins.open, mock_open)
    rewrite_file(mock_path, content)
    mock_open.assert_called_with_once({})
