from dataclasses import dataclass


@dataclass
class OpenAIConfig:
    model: str = "gpt-4o"
    temperature: float = 0.2
    max_tokens: int = 8192
    top_p: float = 0.96
