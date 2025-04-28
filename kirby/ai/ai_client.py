
from __future__ import annotations

from pathlib import Path
from typing import Any, Optional

import typer

from kirby.db.shared_file_db import get_shared_files

from kirby.db.prompt_db import get_latest_prompts
from kirby.util.file_util import stringify_file_contents

from kirby.util.string_util import get_instruction_strings

from kirby.instruction.instruction_model import Instruction

from kirby.ai.ai_client_config import AIConfig

from abc import ABC, abstractmethod


class AIClient(ABC):
    def __init__(self, config: AIConfig):
        self.config = config

    @abstractmethod
    def get_response(self, messages: Any) -> str:
        pass

    def send_message(
        self,
        instructions: Optional[list[Instruction]] = None,
        prompt_files: Optional[list[str] | list[Path]] = None,
        final_prompt: Optional[str] = None,
    ) -> str:
        typer.secho('🐛 Preparing to send message to AI client…', fg='blue')
        messages = self._format_messages(
            instructions=instructions,
            prompt_files=prompt_files,
            final_prompt=final_prompt,
        )
        typer.secho('ℹ️ Messages formatted for AI client', fg='green')
        response = self.get_response(
            messages=messages,
        )
        typer.secho('✅ Received response from AI client', fg='green')
        return response

    def _format_messages(
        self,
        instructions: Optional[list[Instruction]] = None,
        prompt_files: Optional[list[str] | list[Path]] = None,
        final_prompt: Optional[str] = None,
    ) -> list[dict[str, Any]]:
        msgs: list[dict[str, Any]] = []
        if instructions:
            typer.secho('ℹ️ Formatting instruction strings for system message', fg='green')
            instruction_strings = get_instruction_strings(instructions)
            msgs.append(
                {
                    "role": "system",
                    "content": "\n".join(instruction_strings),
                }
            )
        shared_files = get_shared_files()
        if shared_files:
            typer.secho('ℹ️ Adding shared files context to messages', fg='green')
            shared_files_content = stringify_file_contents(
                list(shared_files), "File context"
            )
            msgs.append(
                {
                    "role": "user",
                    "content": "\n".join(shared_files_content),
                }
            )
        if prompt_files:
            typer.secho('ℹ️ Adding prompt files content to messages', fg='green')
            prompt_files_content = stringify_file_contents(prompt_files)
            msgs.append(
                {
                    "role": "user",
                    "content": "\n".join(prompt_files_content),
                }
            )
        prompts = get_latest_prompts()
        if prompts:
            typer.secho('ℹ️ Adding latest prompts to messages', fg='green')
            msgs.append(
                {
                    "role": "user",
                    "content": "\n".join(prompts),
                }
            )
        if final_prompt:
            typer.secho('ℹ️ Adding final prompt to messages', fg='green')
            msgs.append(
                {
                    "role": "user",
                    "content": final_prompt,
                }
            )
        typer.secho('✅ Message formatting complete', fg='green')
        return msgs
