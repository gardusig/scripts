from dataclasses import dataclass


@dataclass
class BedrockConfig:
    temperature: float = 0.7
    max_tokens: int = 4096
    top_p: float = 0.9
    anthropic_version: str = "bedrock-2023-05-31"
