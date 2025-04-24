from abc import ABC, abstractmethod
from typing import Optional


class AIClient(ABC):
    @abstractmethod
    def get_response(self, instructions: Optional[list[str]], context: dict[str, str], final_prompt: str, **kwargs) -> str:
        pass
