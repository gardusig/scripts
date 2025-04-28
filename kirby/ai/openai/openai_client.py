
import os
from typing import Iterable, Optional

import typer

from kirby.ai.ai_client_config import AIConfig
from kirby.ai.ai_client import AIClient
from kirby.ai.openai.openai_config import OpenAIConfig
from openai import OpenAI
from openai.types.chat import ChatCompletionMessageParam


class OpenAIClient(AIClient):
    def __init__(self, config: Optional[AIConfig] = None):
        if config is None:
            config = OpenAIConfig()
        super().__init__(config)
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            typer.secho('❌ OPENAI_API_KEY is not set.', fg='red', err=True)
            raise RuntimeError("❌ OPENAI_API_KEY is not set.")
        self.client = OpenAI(api_key=api_key)

    def get_response(
        self,
        messages: Iterable[ChatCompletionMessageParam],
    ) -> str:
        typer.secho(f'📨 Sending request to {self.config.model}...', fg='blue')
        response = self.client.chat.completions.create(
            model=self.config.model,
            temperature=self.config.temperature,
            max_tokens=self.config.max_tokens,
            top_p=self.config.top_p,
            messages=messages,
        )
        result = response.choices[0].message.content or ""
        typer.secho(f'✅ Response received from {self.config.model}', fg='green')
        return result.strip()
