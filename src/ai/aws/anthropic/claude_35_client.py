from ai.aws.anthropic.claude_client import ClaudeClient


class Claude3SonnetClient(ClaudeClient):
    def get_model_id(self) -> str:
        return "anthropic.claude-3-sonnet-20240229-v1:0"
