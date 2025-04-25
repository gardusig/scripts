from dataclasses import dataclass

from kirby.ai.ai_client_config import AIConfig


@dataclass
class OpenAIConfig(AIConfig):
    model: str = "gpt-4o"
    temperature: float = 0.25
    max_tokens: int = 4096
    top_p: float = 0.96
