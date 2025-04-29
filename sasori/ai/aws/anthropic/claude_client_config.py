from dataclasses import dataclass
from sasori.ai.aws.bedrock_client_config import BedrockClientConfig

ANTHROPIC_VERSION: str = "bedrock-2023-05-31"


@dataclass
class ClaudeClientConfig(BedrockClientConfig):
    model: str
    anthropic_version = ANTHROPIC_VERSION


@dataclass
class Claude35ClientConfig(ClaudeClientConfig):
    model: str = "us.anthropic.claude-3-5-sonnet-20241022-v2:0"


@dataclass
class Claude37ClientConfig(ClaudeClientConfig):
    model: str = "us.anthropic.claude-3-7-sonnet-20250219-v1:0"
