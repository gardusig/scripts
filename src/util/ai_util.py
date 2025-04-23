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
):
    instructions = build_instructions(instructions)
    context = build_context(files)
    return ai_client.get_response(instructions, context)


def build_instructions(instructions: Optional[str] = None) -> str:
    latest_instruction = get_latest_instruction()
    if instructions:
        return latest_instruction + instructions
    return latest_instruction


def build_context(files: Optional[set[str]] = None) -> str:
    if not files:
        files = set()
    for file in get_latest_files():
        files.add(file)
    return stringify_file_contents(files)


def build_message() -> str:
    instructions = build_instructions()
    context = build_context()
    return f"instructions:\n{instructions}\n\ncontext:\n{context}"


def extract_first_code_block(response: str) -> str:
    match = re.search(r"```(?:\w+)?\n(.*)```", response, re.DOTALL)
    if match:
        return match.group(1).strip()
    return response.strip()


def handle_code_change_response(response: str):
    code_block = extract_first_code_block(response)
    files: dict[str, str] = json.loads(code_block)
    rewrite_files(files)
