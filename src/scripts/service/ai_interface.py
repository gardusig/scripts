from abc import ABC, abstractmethod


class AIClient(ABC):
    @abstractmethod
    def get_response(self, instructions: str, input: str) -> str:
        pass
