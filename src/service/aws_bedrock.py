import os
import boto3
from botocore.exceptions import BotoCoreError, ClientError
from service.ai_interface import AIClient
from rich import print


class AWSBedrockClient(AIClient):
    def __init__(self):
        try:
            self.client = boto3.client(
                'bedrock',
                region_name=os.getenv("AWS_REGION"),
            )
        except (BotoCoreError, ClientError) as e:
            raise RuntimeError(f"❌ Failed to create AWS Bedrock client: {e}")

    def get_response(self, instructions: str, input: str, model: str) -> str:
        print("📨 Sending request to AWS Bedrock...\n")
        try:
            response = self.client.invoke_model(
                ModelId=model,
                Prompt={
                    "instructions": instructions,
                    "input": input
                }
            )
            result = response.get('output', '')
            print("✅ Response received:\n")
            return result.strip()
        except (BotoCoreError, ClientError) as e:
            raise RuntimeError(
                f"❌ Failed to get response from AWS Bedrock: {e}")
