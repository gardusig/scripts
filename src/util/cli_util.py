from service.ai_interface import AIClient
from service.openai import OpenAIClient
from service.aws_bedrock import AWSBedrockClient
import os


def get_ai_client() -> AIClient:
    client = os.getenv("AI_CLIENT")
    if client == "openai":
        return OpenAIClient()
    if client == "aws_bedrock":
        return AWSBedrockClient()
    raise Exception(f'client not implemented {client}')
