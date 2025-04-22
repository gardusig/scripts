from dataclasses import dataclass


@dataclass
class OpenAIConfig:
    model: str = "gpt-4o"
    temperature: float = 0.7
    max_tokens: int = 4096
    top_p: float = 0.9
