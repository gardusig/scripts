from dataclasses import dataclass
from sasori.ai.aws.bedrock_client_config import BedrockClientConfig

ANTHROPIC_VERSION: str = "bedrock-2023-05-31"


@dataclass
class ClaudeClientConfig(BedrockClientConfig):
    model: str
    anthropic_version = ANTHROPIC_VERSION


@dataclass
class Claude35ClientConfig(ClaudeClientConfig):
    model: str = "us.anthropic.claude-3-sonnet-20240229-v1:0"


@dataclass
class Claude37ClientConfig(ClaudeClientConfig):
    model: str = "anthropic.claude-3-7-20230430-v1:0"
