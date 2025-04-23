from abc import ABC, abstractmethod
from typing import Optional
from ai.aws.bedrock_client import AbstractAWSBedrockClient, BedrockConfig


def build_prompt(instructions: str, input: str) -> str:
    instructions = instructions.strip()
    input = input.strip()
    return f"Instructions: {instructions}\n\nContext through files: {input}"


class ClaudeClient(AbstractAWSBedrockClient, ABC):
    @abstractmethod
    def get_model_id(self) -> str:
        pass

    def format_request_body(
        self, instructions: str, input: str, config: Optional[BedrockConfig] = None
    ) -> dict:
        if not config:
            config = BedrockConfig()
        return {
            "anthropic_version": config.anthropic_version,
            "max_tokens": config.max_tokens,
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": build_prompt(instructions, input),
                        }
                    ],
                }
            ],
            "temperature": config.temperature,
            "top_p": config.top_p,
        }

    def parse_response(self, response_body: dict) -> str:
        return response_body.get("content", [{}])[0].get("text", "")
