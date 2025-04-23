import os
from typing import Optional
from ai.ai_client_interface import AIClient
from ai.openai.openai_config import OpenAIConfig
from openai import OpenAI


class OpenAIClient(AIClient):
    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise RuntimeError("❌ OPENAI_API_KEY is not set.")
        self.client = OpenAI(api_key=api_key)

    def format_request_body(
        self, instructions: str, input: str, config: Optional[OpenAIConfig] = None
    ) -> dict:
        if not config:
            config = OpenAIConfig()

        messages = []
        if instructions.strip():
            messages.append({"role": "system", "content": instructions.strip()})
        if input.strip():
            messages.append({"role": "user", "content": input.strip()})

        return {
            "model": config.model,
            "messages": messages,
            "temperature": config.temperature,
            "max_tokens": config.max_tokens,
            "top_p": config.top_p,
        }

    def parse_response(self, response) -> str:
        return response.choices[0].message.content.strip()

    def get_response(self, instructions: str, input: str, **kwargs) -> str:
        try:
            config = OpenAIConfig(**kwargs) if kwargs else OpenAIConfig()
            request_body = self.format_request_body(instructions, input, config)
            print(f"📨 Sending request to {config.model}...")
            response = self.client.chat.completions.create(**request_body)
            result = self.parse_response(response)
            print(f"✅ Response received from {config.model}")
            return result
        except Exception as e:
            raise RuntimeError(f"❌ Failed to get response: {e}")
