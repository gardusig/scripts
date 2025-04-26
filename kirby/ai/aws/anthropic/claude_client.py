from __future__ import annotations
from typing import Any, Optional, cast

from kirby.ai.ai_client_config import AIConfig

from kirby.ai.aws.anthropic.claude_client_config import Claude37ClientConfig, ClaudeClientConfig
from kirby.ai.aws.bedrock_client import BedrockClient


class ClaudeClient(BedrockClient):
    def __init__(self, config: Optional[AIConfig] = None):
        if not config:
            config = Claude37ClientConfig()
        super().__init__(config)

    def _format_request_body(
        self,
        messages: list[dict[str, Any]]
    ) -> dict[str, Any]:
        self.config = cast(ClaudeClientConfig, self.config)
        return {
            "anthropic_version": self.config.anthropic_version,
            "model": self.config.model,
            "max_tokens": self.config.max_tokens,
            "temperature": self.config.temperature,
            "top_p": self.config.top_p,
            "messages": messages,
        }

    def _parse_response(self, raw: dict[str, Any]) -> str:
        return raw["content"][0]["text"]
