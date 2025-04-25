from __future__ import annotations

import json
from abc import ABC, abstractmethod
from typing import Any, Optional, cast

import boto3
from botocore.exceptions import BotoCoreError, ClientError

from kirby.ai.ai_client_config import AIConfig
from kirby.ai.ai_client_interface import AIClient
from kirby.ai.aws.bedrock_client_config import BedrockClientConfig


class BedrockClient(AIClient, ABC):
    MAX_TOKENS = 4096

    def __init__(self, *, region: str = "us-east-1") -> None:
        try:
            self.client = boto3.client("bedrock-runtime", region_name=region)
        except (BotoCoreError, ClientError) as exc:
            raise RuntimeError(f"❌ Unable to create Bedrock client: {exc}") from exc

    # ─────────────── model-specific hooks ─────────────── #
    @abstractmethod
    def _model_id(self) -> str: ...

    @abstractmethod
    def _format_request_body(
        self,
        instructions: Optional[list[str]] = None,
        context: dict[str, str] = {},
        final_prompt: Optional[str] = None,
        config: Optional[BedrockClientConfig] = None,
    ) -> dict[str, Any]: ...

    @abstractmethod
    def _parse_response(self, raw: dict[str, Any]) -> str: ...

    # ────────────────── public API ────────────────── #
    def get_response(
        self,
        instructions: Optional[list[str]] = None,
        context: dict[str, str] = {},
        final_prompt: Optional[str] = None,
        config: Optional[AIConfig] = None,
    ) -> str:
        body = self._format_request_body(
            instructions=instructions,
            context=context,
            final_prompt=final_prompt,
            config=cast(BedrockClientConfig, config),
        )

        try:
            print(f"📨  {self._model_id()} → Bedrock …")
            resp = self.client.invoke_model(
                modelId=self._model_id(),
                body=json.dumps(body),
                contentType="application/json",
                accept="application/json",
            )
            payload = json.loads(resp["body"].read())
            return self._parse_response(payload).strip()
        except (BotoCoreError, ClientError) as exc:
            raise RuntimeError(f"❌ Bedrock request failed: {exc}") from exc
