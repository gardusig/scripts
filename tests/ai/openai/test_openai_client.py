import pytest
from unittest.mock import MagicMock, patch
from ai.openai.openai_client import OpenAIClient


@pytest.fixture
def mock_openai():
    with patch("ai.openai.openai_client.OpenAI") as MockOpenAI:
        yield MockOpenAI


def test_openai_client_initialization_without_api_key(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    with pytest.raises(RuntimeError, match="❌ OPENAI_API_KEY is not set."):
        OpenAIClient()


def test_openai_client_initialization_with_api_key(monkeypatch, mock_openai):
    monkeypatch.setenv("OPENAI_API_KEY", "test_key")
    client = OpenAIClient()
    assert client.client is not None
    mock_openai.assert_called_once_with(api_key="test_key")


def test_build_messages():
    client = OpenAIClient()
    instructions = ["Follow the instructions carefully."]
    files = {"file1.txt": "Content of file 1", "file2.txt": "Content of file 2"}
    final_prompt = "What is your response?"

    messages = client.build_messages(instructions, files, final_prompt)

    assert len(messages) == 4  # Adjusted to match the actual number of messages
    assert messages[0] == {
        "role": "system",
        "content": "Follow the instructions carefully.",
    }
    assert messages[1] == {
        "role": "user",
        "content": "--- File: file1.txt ---\n```Content of file 1```",
    }
    assert messages[2] == {
        "role": "user",
        "content": "--- File: file2.txt ---\n```Content of file 2```",
    }
    assert messages[3] == {"role": "user", "content": "What is your response?"}


def test_get_response(mock_openai, monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "test_key")
    mock_client = MagicMock()
    mock_openai.return_value = mock_client
    mock_response = MagicMock()
    mock_response.choices = [MagicMock(message=MagicMock(content="Test response"))]
    mock_client.chat.completions.create.return_value = mock_response

    client = OpenAIClient()
    response = client.get_response(
        instructions=["Instruction"],
        context={"file.txt": "File content"},
        final_prompt="Final prompt",
        model="gpt-4o",
        temperature=0.2,
        max_tokens=4096,
        top_p=0.96,
    )

    assert response == "Test response"
    mock_client.chat.completions.create.assert_called_once()
