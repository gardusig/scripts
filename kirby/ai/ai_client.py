from __future__ import annotations

import logging
from typing import Any, Optional

from kirby.db.file_db import get_latest_files
from kirby.db.instruction_db import get_latest_instructions
from kirby.util.file_util import stringify_file_contents

from kirby.ai.ai_client_config import AIConfig

from abc import ABC, abstractmethod

logger = logging.getLogger(__name__)


class AIClient(ABC):
    def __init__(self, config: AIConfig):
        self.config = config

    @abstractmethod
    def get_response(self, messages: Any) -> str:
        pass

    def send_message(
        self,
        instructions: Optional[list[str]] = None,
        additional_files: Optional[set[str]] = None,
        final_prompt: Optional[str] = None,
    ) -> str:
        file_context = self._build_file_context(additional_files)
        messages = self._format_messages(
            instructions=instructions,
            files=file_context,
            final_prompt=final_prompt,
        )
        response = self.get_response(
            messages=messages,
        )
        return response

    def _format_messages(
        self,
        instructions: Optional[list[str]] = None,
        files: dict[str, str] = {},
        final_prompt: Optional[str] = None,
    ) -> list[dict[str, Any]]:
        msgs: list[dict[str, Any]] = []
        if instructions:
            msgs.append(
                {
                    "role": "system",
                    "content": "\n".join(instructions),
                }
            )
        for fname, content in files.items():
            msgs.append(
                {
                    "role": "user",
                    "content": f"--- File: {fname} ---\n```{content}```",
                }
            )
        if final_prompt:
            msgs.append(
                {
                    "role": "user",
                    "content": final_prompt.strip(),
                }
            )
        return msgs

    def _get_latest_prompt(self) -> str:
        return "\n".join(get_latest_instructions())

    def _build_file_context(self, files: Optional[set[str]] = None) -> dict[str, str]:
        file_set = set(files or ())
        file_set.update(get_latest_files())
        return stringify_file_contents(file_set)
