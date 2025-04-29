from __future__ import annotations

from pathlib import Path
from typing import Any, Optional, Union

import typer

from sasori.db.shared_file_db import get_shared_files

from sasori.db.prompt_db import get_latest_prompts
from sasori.util.file_util import stringify_file_contents

from sasori.util.string_util import get_instruction_strings

from sasori.instruction.instruction_model import Instruction

from sasori.ai.ai_client_config import AIConfig

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
        prompt_files: Optional[Union[list[str], list[Path]]] = None,
        final_prompt: Optional[str] = None,
    ) -> str:
        try:
            messages = self._format_messages(
                instructions=instructions,
                prompt_files=prompt_files,
                final_prompt=final_prompt,
            )
            response = self.get_response(
                messages=messages,
            )
            typer.secho("☑️ Received response from AI client", fg="green")
            return response
        except Exception as e:
            typer.secho(
                f"❌ Failed to send message to AI client: {e}", fg="red", err=True
            )
            raise

    def _format_messages(
        self,
        instructions: Optional[list[Instruction]] = None,
        prompt_files: Optional[Union[list[str], list[Path]]] = None,
        final_prompt: Optional[str] = None,
    ) -> list[dict[str, Any]]:
        msgs: list[dict[str, Any]] = []
        try:
            if instructions:
                instruction_strings = get_instruction_strings(instructions)
                msgs.append(
                    {
                        "role": "system",
                        "content": "\n".join(instruction_strings),
                    }
                )
            shared_files = get_shared_files()
            if shared_files:
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
                prompt_files_content = stringify_file_contents(prompt_files)
                msgs.append(
                    {
                        "role": "user",
                        "content": "\n".join(prompt_files_content),
                    }
                )
            prompts = get_latest_prompts()
            if prompts:
                msgs.append(
                    {
                        "role": "user",
                        "content": "\n".join(prompts),
                    }
                )
            if final_prompt:
                msgs.append(
                    {
                        "role": "user",
                        "content": final_prompt,
                    }
                )
            typer.secho("☑️ Message formatting complete", fg="green")
            return msgs
        except Exception as e:
            typer.secho(f"❌ Failed to format messages: {e}", fg="red", err=True)
            raise
