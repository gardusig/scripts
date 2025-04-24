from abc import ABC, abstractmethod
import json
from typing import Optional
from ai.aws.bedrock_config import BedrockConfig
import boto3
from botocore.exceptions import BotoCoreError, ClientError
from ai.ai_client_interface import AIClient
from rich import print


class AbstractAWSBedrockClient(AIClient, ABC):
    MAX_TOKENS = 4096

    def __init__(self):
        try:
            self.client = boto3.client(
                service_name="bedrock-runtime", region_name="us-east-1"
            )
        except (BotoCoreError, ClientError) as e:
            raise RuntimeError(f"£ Failed to create AWS Bedrock client: {e}")

    @abstractmethod
    def get_model_id(self) -> str:
        pass

    @abstractmethod
    def format_request_body(
        self, instructions: str, input: str, config: Optional[BedrockConfig] = None
    ) -> dict:
        pass

    @abstractmethod
    def parse_response(self, response_body: dict) -> str:
        pass

    def get_response(
        self,
        instructions: Optional[list[str]],
        context: dict[str, str],
        final_prompt: str,
        **kwargs,
    ) -> str:
        # print(f"Sending request to {self.get_model_id}()}...\n\n")
        return ""

        # try:
        #     config = BedrockConfig**(kwargs) if kwargs else BedrockConfig()

        #     request_body = self.format_request_body(
        #         instructions=instructions, input=input, config=config
        #     )

        #     response = self.client.invoke_model(
        #         modelId=self.get_model_id(),
        #         body=json.dumps(request_body),
        #         contentType="application/json",
        #         accept="application/json",
        #     )

        #     response_body = json.loads(response.get("body").read())
        #     result = self.parse_response(response_body)

        #     print(f"✔ Response received from {self.get_model_id()}\n\n")
        #     return result.strip()

        # except Exception as e:
        #     error_message = str(e)
