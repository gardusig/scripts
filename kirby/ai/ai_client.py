from __future__ import annotations

import logging
from typing import Any, Optional

from kirby.util.string_util import get_instruction_strings

from kirby.instruction.instruction_model import Instruction

from kirby.db.instruction_db import get_latest_instructions
from kirby.util.file_util import get_file_contents

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
        instructions: Optional[list[Instruction]] = None,
        files_contents: Optional[list[str]] = None,
    ) -> str:
        messages = self._format_messages(
            instructions=instructions, files_contents=files_contents)
        print(messages)
        response = self.get_response(
            messages=messages,
        )
        return response

    def _format_messages(
        self,
        instructions: Optional[list[Instruction]] = None,
        files_contents: Optional[list[str]] = None,
    ) -> list[dict[str, Any]]:
        msgs: list[dict[str, Any]] = []
        msgs.append({
            "role": "system",
            "content": "\n".join(get_instruction_strings(instructions)),
        })
        if not files_contents:
            files_contents = get_file_contents()
        msgs.append({
            "role": "user",
            "content": "\n".join(files_contents),
        })
        msgs.append({
            "role": "user",
            "content": "\n".join(get_latest_instructions()),
        })
        return msgs
