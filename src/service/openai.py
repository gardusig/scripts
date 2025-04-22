import os
from openai import OpenAI
from service.ai_interface import AIClient
from rich import print


class OpenAIClient(AIClient):
    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise RuntimeError("❌ OPENAI_API_KEY is not set.")
        self.client = OpenAI(api_key=api_key)

    def get_response(self, instructions: str, input: str, model: str = "gpt-4o") -> str:
        print("📨 Sending request to OpenAI...\n")
        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": instructions},
                    {"role": "user", "content": input},
                ],
            )
            print("✅ Response received:\n")
            return response.choices[0].message.content.strip()
        except Exception as e:
            raise RuntimeError(f"❌ Failed to get response: {e}")
