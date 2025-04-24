from ai.aws.anthropic.claude_client import ClaudeClient


class Claude35Client(ClaudeClient):
    def get_model_id(self) -> str:
        return "anthropic.claude-3-sonnet-20240229-v1:0"
