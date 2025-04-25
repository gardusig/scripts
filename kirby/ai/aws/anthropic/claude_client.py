from __future__ import annotations
from typing import Any, Optional, cast

from kirby.ai.aws.bedrock_client_config import BedrockClientConfig
from kirby.ai.aws.anthropic.claude_client_config import Claude37ClientConfig, ClaudeClientConfig
from kirby.ai.aws.bedrock_client_interface import BedrockClient


class ClaudeClient(BedrockClient):
    def _format_request_body(
        self,
        instructions: Optional[list[str]] = None,
        context: dict[str, str] = {},
        final_prompt: Optional[str] = None,
        config: Optional[BedrockClientConfig] = None,
    ) -> dict[str, Any]:
        msgs: list[dict[str, Any]] = []

        if instructions:
            msgs.append(
                {
                    "role": "system",
                    "content": "\n".join(instructions),
                }
            )
        for fname, content in (context or {}).items():
            msgs.append(
                {
                    "role": "user",
                    "content": f"--- File: {fname} ---\n```{content}```",
                }
            )
        if final_prompt:
            msgs.append(
                {
                    "role": "user",
                    "content": final_prompt.strip(),
                }
            )
        config = cast(ClaudeClientConfig, config or Claude37ClientConfig())
        return {
            "anthropic_version": config.anthropic_version,
            "model": config.model,
            "max_tokens": config.max_tokens,
            "temperature": config.temperature,
            "top_p": config.top_p,
            "messages": msgs,
        }

    def _parse_response(self, raw: dict[str, Any]) -> str:
        return raw["content"][0]["text"]
