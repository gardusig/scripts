from __future__ import annotations

import json
from abc import ABC, abstractmethod
from typing import Any, cast

import boto3
from botocore.exceptions import BotoCoreError, ClientError
from sasori.ai.ai_client_config import AIConfig
from sasori.ai.aws.bedrock_client_config import BedrockClientConfig

from sasori.ai.ai_client import AIClient

import typer


class BedrockClient(AIClient, ABC):
    MAX_TOKENS = 4096

    def __init__(self, config: AIConfig, region: str = "us-east-1") -> None:
        super().__init__(config)
        try:
            self.client = boto3.client("bedrock-runtime", region_name=region)
            typer.secho(
                f"☑️ Bedrock client initialized in region: {region}",
                fg="green",
            )
        except (BotoCoreError, ClientError) as exc:
            typer.secho(
                f"❌ Unable to create Bedrock client: {exc}", fg="red", err=True
            )
            raise RuntimeError(f"Unable to create Bedrock client: {exc}") from exc

    @abstractmethod
    def _format_request_body(
        self,
        messages: list[dict[str, Any]],
    ) -> dict[str, Any]: ...

    @abstractmethod
    def _parse_response(
        self,
        raw: dict[str, Any],
    ) -> str: ...

    def get_response(self, messages: list[dict[str, Any]]) -> str:
        config = cast(BedrockClientConfig, self.config)
        body = self._format_request_body(
            messages=messages,
        )
        try:
            resp = self.client.invoke_model(
                modelId=config.model,
                body=json.dumps(body),
                contentType="application/json",
                accept="application/json",
            )
            typer.secho("☑️ Received response from Bedrock", fg="green")
            payload = json.loads(resp["body"].read())
            result = self._parse_response(payload).strip()
            typer.secho("☑️ Bedrock response returned to caller", fg="green")
            return result
        except (BotoCoreError, ClientError) as exc:
            typer.secho(f"❌ Bedrock request failed: {exc}", fg="red", err=True)
            raise RuntimeError(f"Bedrock request failed: {exc}") from exc
