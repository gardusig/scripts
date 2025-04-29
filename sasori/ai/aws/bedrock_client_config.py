from dataclasses import dataclass

from sasori.ai.ai_client_config import AIConfig


@dataclass
class BedrockClientConfig(AIConfig):
    model: str
    temperature: float = 0.25
    max_tokens: int = 4096
    top_p: float = 0.96
