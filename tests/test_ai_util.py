import json
import base64
import pytest

from util.ai_util import (
    get_ai_client,
    extract_json_blob,
    handle_code_change_response
)
from ai.openai.openai_client import OpenAIClient
from ai.aws.anthropic.claude_35_client import Claude3SonnetClient


def test_get_ai_client_openai(monkeypatch):
    monkeypatch.setenv("AI_CLIENT", "openai")
    client = get_ai_client()
    assert isinstance(client, OpenAIClient)


def test_get_ai_client_claude(monkeypatch):
    monkeypatch.setenv("AI_CLIENT", "claude_3_sonnet")
    client = get_ai_client()
    assert isinstance(client, Claude3SonnetClient)


def test_get_ai_client_invalid(monkeypatch):
    monkeypatch.delenv("AI_CLIENT", raising=False)
    with pytest.raises(RuntimeError):
        get_ai_client()


def test_extract_json_blob_valid():
    response = 'prefix ```json\n{"foo":"bar"}\n``` suffix'
    blob = extract_json_blob(response)
    assert blob == '{"foo":"bar"}'


def test_extract_json_blob_missing():
    response = 'no JSON fencing here'
    with pytest.raises(RuntimeError):
        extract_json_blob(response)


class DummyRewrite:
    def __init__(self):
        self.written = None

    def __call__(self, files_map):
        self.written = files_map


@pytest.fixture(autouse=True)
def patch_rewrite(monkeypatch):
    dummy = DummyRewrite()
    monkeypatch.setattr('util.file_util.rewrite_files', dummy)
    return dummy


def make_b64_response(entries: dict[str, str]) -> str:
    enc_map = {path: base64.b64encode(content.encode()).decode()
               for path, content in entries.items()}
    payload = json.dumps(enc_map)
    return f'```json\n{payload}\n```'


def test_handle_code_change_response_basic(patch_rewrite):
    entries = {"test.py": "print('hello')"}
    resp = make_b64_response(entries)
    handle_code_change_response(resp)
    assert patch_rewrite.written == entries


def test_handle_invalid_json(patch_rewrite):
    resp = '```json\n{invalid json}\n```'
    with pytest.raises(RuntimeError):
        handle_code_change_response(resp)


def test_handle_invalid_base64(patch_rewrite):
    bad = {"file.py": "not_base64!!!"}
    payload = json.dumps(bad)
    resp = f'```json\n{payload}\n```'
    with pytest.raises(RuntimeError):
        handle_code_change_response(resp)


def test_handle_skips_non_str(patch_rewrite):
    mixed = {
        "good.py": "b2s=",
        "bad_val": 123,
        456: "b2s="
    }
    payload = json.dumps(mixed)
    resp = f'```json\n{payload}\n```'
    handle_code_change_response(resp)
    # Only "good.py" should be written
    assert patch_rewrite.written == {"good.py": "ok"}


def test_handle_replacement_on_bad_utf8(patch_rewrite):
    raw = b'\xff\xfe\xfd'
    b64 = base64.b64encode(raw).decode()
    payload = json.dumps({"bad.dat": b64})
    resp = f'```json\n{payload}\n```'
    handle_code_change_response(resp)
    written = patch_rewrite.written
    assert "\ufffd" in written["bad.dat"]
