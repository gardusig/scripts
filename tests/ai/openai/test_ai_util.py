from typing import Optional
from kirby.ai.ai_client_factory import get_ai_client, AI_CLIENTS
import pytest
from kirby.ai.ai_client_config import AIConfig
from kirby.ai.ai_client import AIClient


# ─────────────────────────── get_ai_client ────────────────────────────
def test_get_ai_client_env_unset(monkeypatch):
    monkeypatch.delenv("AI_CLIENT", raising=False)
    with pytest.raises(RuntimeError):
        get_ai_client()


def test_get_ai_client_unsupported(monkeypatch):
    monkeypatch.setenv("AI_CLIENT", "gpt420")
    with pytest.raises(ValueError):
        get_ai_client()


@pytest.mark.parametrize("name,cls", AI_CLIENTS.items())
def test_get_ai_client_supported(monkeypatch, name, cls):
    monkeypatch.setenv("AI_CLIENT", name)
    client = get_ai_client()
    assert isinstance(client, cls)


# ─────────────────────────── _latest_prompt ───────────────────────────
def test_latest_prompt(monkeypatch):
    # note: trailing blanks after 'line 1' are preserved by _latest_prompt()
    monkeypatch.setattr(
        ai_client_factory,
        "get_latest_instructions",
        lambda: [
            " line 1 ",
            " line 2",
            "line 3 ",
            "line 4",
            "line 5   ",
        ],
    )
    assert ai_client_factory._latest_prompt() == " line 1 \n line 2\nline 3 \nline 4\nline 5   "


# ────────────────────────── build_context ─────────────────────────────
def test_build_context_merges_and_calls_stringify(monkeypatch):
    monkeypatch.setattr(ai_client_factory, "get_latest_files", lambda: {"tracked.txt"})
    called = {}

    def fake_stringify(paths):
        called["paths"] = set(paths)
        return {p: "content" for p in paths}

    monkeypatch.setattr(ai_client_factory, "stringify_file_contents", fake_stringify)

    ctx = ai_client_factory.build_context({"extra.py"})
    assert ctx == {"tracked.txt": "content", "extra.py": "content"}
    assert called["paths"] == {"tracked.txt", "extra.py"}


# ─────────────────────────── send_message ─────────────────────────────
def test_send_message_passes_through(monkeypatch):
    monkeypatch.setattr(ai_client_factory, "build_context", lambda *_: {"ctx": "C"})
    monkeypatch.setattr(ai_client_factory, "_latest_prompt", lambda: "PROMPT")

    captured = {}

    class DummyClient(AIClient):
        def get_response(
            self,
            instructions: Optional[list[str]] = None,
            context: dict[str, str] = {},
            final_prompt: Optional[str] = None,
            config: Optional[AIConfig] = None,
        ) -> str:
            captured.update(
                dict(
                    instructions=instructions,
                    context=context,
                    prompt=final_prompt,
                    config=config,
                )
            )
            return "ok"

    resp = ai_client_factory.send_message(
        DummyClient(), instructions=["ins"], files={"file.txt"})

    assert resp == "ok"
    assert captured["instructions"] == ["ins"]
    assert captured["context"] == {"ctx": "C"}
    assert captured["prompt"] == "PROMPT"
