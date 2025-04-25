from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Optional

from kirby.ai.ai_client_config import AIConfig


class AIClient(ABC):
    @abstractmethod
    def get_response(
        self,
        instructions: Optional[list[str]] = None,
        context: dict[str, str] = {},
        final_prompt: Optional[str] = None,
        config: Optional[AIConfig] = None,
    ) -> str:
        pass
