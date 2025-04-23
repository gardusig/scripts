import base64
import json
import re
from typing import Optional
from ai.ai_client_interface import AIClient
from ai.aws.anthropic.claude_35_client import Claude3SonnetClient
from ai.openai.openai_client import OpenAIClient
import os
from db.file_db import get_latest_files
from util.file_util import rewrite_files, stringify_file_contents
from db.instruction_db import get_latest_instruction


def get_ai_client() -> AIClient:
    client = os.getenv("AI_CLIENT")
    if not client:
        raise Exception("client not set on .env")
    if client == "openai":
        return OpenAIClient()
    if client == "claude_3_sonnet":
        return Claude3SonnetClient()
    raise Exception(f"client not implemented {client}")


def send_message(
    ai_client: AIClient,
    instructions: Optional[str] = None,
    files: Optional[set[str]] = None,
) -> str:
    context = build_context(files)
    last_messages = get_latest_instruction()
    response = ai_client.get_response(instructions, context, last_messages)
    return response


def build_context(files: Optional[set[str]] = None) -> dict[str, str]:
    if not files:
        files = set()
    for file in get_latest_files():
        files.add(file)
    return stringify_file_contents(files)


def extract_first_code_block(response: str) -> str:
    match = re.search(r"```(?:\w+)?\n(.*)```", response, re.DOTALL)
    if match:
        return match.group(1).strip()
    return response.strip()


def handle_code_change_response(response: str):
    code_block = extract_first_code_block(response)
    try:
        files_b64: dict[str, str] = json.loads(code_block)
    except json.JSONDecodeError as e:
        raise RuntimeError(f"Invalid JSON from model: {e}")
    decoded_files: dict[str, str] = {}
    for path, b64_content in files_b64.items():
        try:
            raw_bytes = base64.b64decode(b64_content)
            decoded_files[path] = raw_bytes.decode("utf-8")
        except Exception as err:
            raise RuntimeError(f"Failed to decode `{path}`: {err}")
    rewrite_files(decoded_files)
