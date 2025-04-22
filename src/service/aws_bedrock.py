from service.ai_interface import AIClient


class AWSBedrockClient(AIClient):
    def __init__(self):
        pass

    def get_response(self, instructions: str, input: str, model: str) -> str:
        return "AWS Bedrock response"
