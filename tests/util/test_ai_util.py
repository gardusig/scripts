import json
import base64
import pytest

from util.ai_util import (
    get_ai_client,
    send_message,
    build_context,
    parse_code_response,
)
from ai.openai.openai_client import OpenAIClient
from ai.aws.anthropic.claude_35_client import Claude3SonnetClient
from ai.ai_client_interface import AIClient


class DummyClient(AIClient):
    def __init__(self):
        self.called = False
        self.args = None
        self.kwargs = None

    def get_response(self, instructions=None, context=None, last_messages=None, **kwargs):
        self.called = True
        self.args = {
            "instructions": instructions,
            "context": context,
            "last_messages": last_messages,
        }
        self.kwargs = kwargs
        return "DUMMY_RESPONSE"


@pytest.mark.parametrize("name,cls", [
    ("openai", OpenAIClient),
    ("claude_3_sonnet", Claude3SonnetClient),
])
def test_get_ai_client_valid(monkeypatch, name, cls):
    monkeypatch.setenv("AI_CLIENT", name)
    client = get_ai_client()
    assert isinstance(client, cls)


def test_get_ai_client_missing(monkeypatch):
    monkeypatch.delenv("AI_CLIENT", raising=False)
    with pytest.raises(RuntimeError) as exc:
        get_ai_client()
    assert "No client name provided" in str(exc.value)


def test_get_ai_client_unsupported(monkeypatch):
    monkeypatch.setenv("AI_CLIENT", "foobar")
    with pytest.raises(ValueError) as exc:
        get_ai_client()
    msg = str(exc.value)
    assert "unsupported" in msg
    assert "openai" in msg and "claude_3_sonnet" in msg


def test_get_ai_client_whitespace(monkeypatch):
    monkeypatch.setenv("AI_CLIENT", "   ")
    with pytest.raises(ValueError) as exc:
        get_ai_client()
    msg = str(exc.value)
    assert "unsupported" in msg


@pytest.fixture(autouse=True)
def stub_dbs_and_files(monkeypatch):
    monkeypatch.setattr("util.ai_util.get_latest_instruction", lambda: "STORED_PROMPT")
    monkeypatch.setattr("util.ai_util.get_latest_files", lambda: {"f1.py", "f2.txt"})
    monkeypatch.setattr(
        "util.ai_util.stringify_file_contents",
        lambda paths: {p: f"CONT({p})" for p in sorted(paths)}
    )
    yield


def test_build_context_with_files():
    result = build_context({"X.py"})
    assert result == {
        "X.py": "CONT(X.py)",
        "f1.py": "CONT(f1.py)",
        "f2.txt": "CONT(f2.txt)",
    }


def test_build_context_none():
    result = build_context(None)
    assert result == {
        "f1.py": "CONT(f1.py)",
        "f2.txt": "CONT(f2.txt)",
    }


def test_send_message(monkeypatch):
    dummy = DummyClient()
    monkeypatch.setenv("AI_CLIENT", "openai")
    out = send_message(
        ai_client=dummy,
        instructions="ADHOC_PROMPT",
        files={"C.py"}
    )
    assert out == "DUMMY_RESPONSE"
    assert dummy.called
    assert dummy.args == {
        "instructions": "ADHOC_PROMPT",
        "context": {"C.py": "CONT(C.py)", "f1.py": "CONT(f1.py)", "f2.txt": "CONT(f2.txt)"},
        "last_messages": "STORED_PROMPT",
    }


def test_send_message_empty(monkeypatch):
    dummy = DummyClient()
    out = send_message(ai_client=dummy)
    assert out == "DUMMY_RESPONSE"
    assert dummy.args == {
        "instructions": None,
        "context": {"f1.py": "CONT(f1.py)", "f2.txt": "CONT(f2.txt)"},
        "last_messages": "STORED_PROMPT",
    }


def make_base64json_fenced(data: dict[str, str]) -> str:
    """
    Converts a file map to a base64json fenced block,
    encoding each file content individually.
    """
    encoded_map = {
        k: base64.b64encode(v.encode("utf-8")).decode("utf-8")
        for k, v in data.items()
    }
    return f"```base64json\n{json.dumps(encoded_map)}\n```"


def test_parse_code_response_basic():
    data = {"a.py": "print('hello')", "b.txt": "world"}
    response = make_base64json_fenced(data)
    out = parse_code_response(response)
    assert out == data


def test_parse_code_response_no_fence():
    with pytest.raises(RuntimeError, match="No ```base64json``` fenced block"):
        parse_code_response("no block here")


def test_parse_code_response_invalid_json_block():
    invalid_json = "```base64json\n{not valid}\n```"
    with pytest.raises(RuntimeError, match="Failed to parse base64json block"):
        parse_code_response(invalid_json)


def test_parse_code_response_invalid_b64_value():
    bad_map = json.dumps({"file.py": "!!badb64!!"})
    response = f"```base64json\n{bad_map}\n```"
    with pytest.raises(ValueError, match="Failed to decode file `file.py`"):
        parse_code_response(response)


def test_parse_code_response_empty_map():
    empty = f"```base64json\n{{}}\n```"
    out = parse_code_response(empty)
    assert out == {}


def test_parse_code_response_invalid_utf8(monkeypatch):
    bad_utf8_bytes = b'\xff\xfe\xfd'
    b64 = base64.b64encode(bad_utf8_bytes).decode()
    payload = {"weird.py": b64}
    response = f"```base64json\n{json.dumps(payload)}\n```"
    result = parse_code_response(response)
    assert "weird.py" in result
    assert "�" in result["weird.py"]  # replacement character
    assert result["weird.py"].startswith("�") or "\ufffd" in result["weird.py"]
