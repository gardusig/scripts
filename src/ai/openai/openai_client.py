import os
from typing import Optional
from openai import OpenAI
from ai.ai_client_interface import AIClient
from rich import print
from ai.openai.openai_config import OpenAIConfig


class OpenAIClient(AIClient):
    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise RuntimeError("❌ OPENAI_API_KEY is not set.")
        self.client = OpenAI(api_key=api_key)

    def format_request_body(self, instructions: str, input: str, config: Optional[OpenAIConfig] = None) -> dict:
        if not config:
            config = OpenAIConfig()
        return {
            "model": config.model,
            "messages": [
                {"role": "system", "content": instructions},
                {"role": "user", "content": input},
            ],
            "temperature": config.temperature,
            "max_tokens": config.max_tokens,
            "top_p": config.top_p,
        }

    def parse_response(self, response) -> str:
        return response.choices[0].message.content.strip()

    def get_response(self, instructions: str, input: str, **kwargs) -> str:
        print("📨 Sending request to OpenAI...\n")
        try:
            config = OpenAIConfig(**kwargs) if kwargs else OpenAIConfig()
            request_body = self.format_request_body(
                instructions, input, config)
            response = self.client.chat.completions.create(**request_body)
            result = self.parse_response(response)
            print(f"✅ Response received from {config.model}\n")
            return result
        except Exception as e:
            raise RuntimeError(f"❌ Failed to get response: {e}")
