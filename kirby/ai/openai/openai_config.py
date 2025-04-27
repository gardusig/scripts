from dataclasses import dataclass

from kirby.ai.ai_client_config import AIConfig


@dataclass
class OpenAIConfig(AIConfig):
    model: str = "gpt-4-turbo"
    temperature: float = 0.24
    max_tokens: int = 4096
    top_p: float = 0.96
