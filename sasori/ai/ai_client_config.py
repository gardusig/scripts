from typing import Protocol


class AIConfig(Protocol):
    temperature: float
    max_tokens: int
    top_p: float
    model: str
