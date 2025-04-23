import os
import base64
import json
import logging
from typing import Optional, Dict, Set

from ai.ai_client_interface import AIClient
from ai.aws.anthropic.claude_35_client import Claude3SonnetClient
from ai.openai.openai_client import OpenAIClient
from db.instruction_db import get_latest_instruction
from db.file_db import get_latest_files
from util.file_util import stringify_file_contents
from util.string_util import extract_base64json_block

logger = logging.getLogger(__name__)

AI_CLIENTS = {
    "openai": OpenAIClient,
    "claude_3_sonnet": Claude3SonnetClient,
}


def get_ai_client() -> AIClient:
    client_name = os.getenv("AI_CLIENT")
    if not client_name:
        raise RuntimeError("⛔️ No client name provided")
    client_class = AI_CLIENTS.get(client_name.strip())
    if client_class:
        return client_class()
    raise ValueError(
        f"❌ AI_CLIENT '{client_name}' not set or unsupported. Supported: {list(AI_CLIENTS.keys())}"
    )


def send_message(
    ai_client: AIClient,
    instructions: Optional[str] = None,
    files: Optional[Set[str]] = None,
) -> str:
    """
    Merges your stored instruction with any ad-hoc text, gathers file contents,
    and calls get_response with 'final_prompt' set to that merged text.
    """
    final_prompt = get_latest_instruction().strip()

    file_set = set(files or ())
    file_set.update(get_latest_files())
    context_map: Dict[str, str] = stringify_file_contents(file_set)

    return ai_client.get_response(
        instructions=instructions,
        context=context_map,
        last_messages=final_prompt,
    )


def build_context(files: Optional[Set[str]] = None) -> Dict[str, str]:
    """
    Convenience wrapper if you need to build the same context elsewhere.
    """
    file_set = set(files or ())
    file_set.update(get_latest_files())
    return stringify_file_contents(file_set)


def parse_code_response(response: str) -> dict[str, str]:
    """
    Extracts and decodes a base64-encoded JSON object from a `base64json` fenced block.
    Each value is expected to be base64-encoded UTF-8 text.
    """
    try:
        json_str = extract_base64json_block(response)
        filemap_b64: dict[str, str] = json.loads(json_str)
    except Exception as e:
        raise RuntimeError(f"❌ Failed to parse base64json block: {e}")

    decoded_files: dict[str, str] = {}
    for path, b64_content in filemap_b64.items():
        try:
            # Clean and decode base64 string
            raw_bytes = base64.b64decode(b64_content.encode("utf-8"), validate=True)
            if b"\x00" in raw_bytes:
                print(f"⚠️ Warning: {path} might be a binary file.")
            decoded = raw_bytes.decode("utf-8", errors="replace")
            decoded_files[path] = decoded
        except Exception as e:
            raise ValueError(f"❌ Failed to decode file `{path}`: {e}")

    print("✅ Decoded response:")
    for file, content in decoded_files.items():
        print(f"📄 {file} (len={len(content)}) preview: {repr(content[:80])}...")

    return decoded_files
