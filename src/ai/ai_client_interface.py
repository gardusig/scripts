from abc import ABC, abstractmethod
from typing import Optional


class AIClient(ABC):
    @abstractmethod
    def get_response(self, instructions: Optional[str], context: dict[str, str], last_messages: str, **kwargs) -> str:
        pass
