from dataclasses import dataclass


@dataclass
class OpenAIConfig:
    model: str = "gpt-4-turbo"
    temperature: float = 0.25
    max_tokens: int = 1024
    top_p: float = 0.96
