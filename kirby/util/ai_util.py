from __future__ import annotations

import logging
import os
from typing import Optional

from kirby.ai.ai_client_config import AIConfig
from kirby.ai.ai_client_interface import AIClient
from kirby.ai.aws.anthropic.claude_client import ClaudeClient
from kirby.ai.openai.openai_client import OpenAIClient
from kirby.db.file_db import get_latest_files
from kirby.db.instruction_db import get_latest_instructions
from kirby.util.file_util import stringify_file_contents

logger = logging.getLogger(__name__)

# ──────────────────────── AI-client registry ──────────────────────────
AI_CLIENTS: dict[str, type[AIClient]] = {
    "openai": OpenAIClient,
    # "claude": ClaudeClient,
}


def get_ai_client() -> AIClient:
    """Instantiate the client named in $AI_CLIENT."""
    client_name = (os.getenv("AI_CLIENT") or "").strip().lower()
    if not client_name:
        raise RuntimeError("⛔️  AI_CLIENT environment variable not set.")

    try:
        return AI_CLIENTS[client_name]()
    except KeyError as exc:
        raise ValueError(
            f"❌ Unsupported AI_CLIENT '{client_name}'. "
            f"Supported: {list(AI_CLIENTS.keys())}"
        ) from exc


# ───────────────────────── prompt + context helpers ─────────────────────────


def _latest_prompt() -> str:
    """Join the most-recent instruction snapshot into one prompt."""
    return "\n".join(get_latest_instructions())


def build_context(files: Optional[set[str]] = None) -> dict[str, str]:
    """Return {path: content} for the given file set ∪ latest tracked files."""
    file_set = set(files or ())
    file_set.update(get_latest_files())
    return stringify_file_contents(file_set)


def send_message(
    ai_client: AIClient,
    instructions: Optional[list[str]] = None,
    files: Optional[set[str]] = None,
    config: Optional[AIConfig] = None,
) -> str:
    """High-level helper used by the CLI layer."""
    response = ai_client.get_response(
        instructions=instructions,
        context=build_context(files),
        final_prompt=_latest_prompt(),
        config=config,
    )
    return response
