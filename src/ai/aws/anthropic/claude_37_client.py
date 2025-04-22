from ai.aws.anthropic.claude_client import ClaudeClient


class Claude37Client(ClaudeClient):
    def get_model_id(self) -> str:
        return "anthropic.claude-3-7-20230430-v1:0"
