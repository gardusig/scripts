from dataclasses import dataclass

from sasori.ai.ai_client_config import AIConfig


@dataclass
class OpenAIConfig(AIConfig):
    model: str = "gpt-4.1"
    temperature: float = 0.24
    max_tokens: int = 4096 * 2
    top_p: float = 0.96
