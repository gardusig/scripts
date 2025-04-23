import os
import re
import json
import base64
import logging
from typing import Optional, Dict, Set

from ai.ai_client_interface import AIClient
from ai.aws.anthropic.claude_35_client import Claude3SonnetClient
from ai.openai.openai_client import OpenAIClient
from db.instruction_db import get_latest_instruction
from db.file_db import get_latest_files
import util.file_util as file_util
from util.file_util import stringify_file_contents

logger = logging.getLogger(__name__)


def get_ai_client() -> AIClient:
    client = os.getenv("AI_CLIENT")
    if client == "openai":
        return OpenAIClient()
    if client == "claude_3_sonnet":
        return Claude3SonnetClient()
    raise RuntimeError("❌ AI_CLIENT not set or unsupported")


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
        last_messages=final_prompt
    )


def build_context(files: Optional[Set[str]] = None) -> Dict[str, str]:
    """
    Convenience wrapper if you need to build the same context elsewhere.
    """
    file_set = set(files or ())
    file_set.update(get_latest_files())
    return stringify_file_contents(file_set)


def extract_json_blob(response: str) -> str:
    """
    Extracts and returns just the `{...}` payload from the first ```json ... ``` block.
    Raises if no such block is found.
    """
    pattern = re.compile(
        r"```json\s*"             # opening fence
        r"(?P<blob>\{[\s\S]*?\})"  # capture the JSON object
        r"\s*```",                # closing fence
        re.DOTALL
    )
    m = pattern.search(response)
    if not m:
        raise RuntimeError("⛔️ No ```json … ``` block found in assistant response")
    return m.group("blob")


def handle_code_change_response(response: str):
    """
    1) Extracts the JSON blob
    2) Parses it as { path: base64_string }
    3) Cleans & Base64-decodes each string
    4) UTF-8 decodes with replacement on errors
    5) Calls rewrite_files on the result map
    """
    json_blob = extract_json_blob(response)

    try:
        files_b64: Dict[str, str] = json.loads(json_blob)
    except json.JSONDecodeError as e:
        raise RuntimeError(f"Invalid JSON from model: {e}")

    decoded_files: Dict[str, str] = {}
    for path, b64_content in files_b64.items():
        # skip invalid types
        if not isinstance(path, str) or not isinstance(b64_content, str):
            logger.warning("Skipping invalid entry: %r → %r", path, b64_content)
            continue

        # skip entries without a file extension
        if "." not in path:
            continue

        # Remove any stray whitespace/newlines
        clean_b64 = "".join(b64_content.split())

        # Decode Base64
        try:
            raw = base64.b64decode(clean_b64)
        except Exception as err:
            raise RuntimeError(f"Failed to Base64-decode `{path}`: {err}")

        # Decode to UTF-8, replacing invalid bytes
        text = raw.decode("utf-8", errors="replace")
        decoded_files[path] = text

    if not decoded_files:
        raise RuntimeError(
            "No valid base64-encoded file entries found in model response")

    # Write the files out
    file_util.rewrite_files(decoded_files)
