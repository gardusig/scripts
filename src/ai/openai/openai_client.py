import os
from ai.ai_client_interface import AIClient
from ai.openai.openai_config import OpenAIConfig
from openai import OpenAI


class OpenAIClient(AIClient):
    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise RuntimeError("❌ OPENAI_API_KEY is not set.")
        self.client = OpenAI(api_key=api_key)

    def build_prompt(self, instructions: str, input: str) -> str:
        instructions = instructions.strip()
        input = input.strip()
        return f"{instructions}\n\n---\n\n{input}"

    def get_response(self, instructions: str, input: str, **kwargs) -> str:
        try:
            config = OpenAIConfig(**kwargs)
            prompt = self.build_prompt(instructions, input)

            print(f"📨 Sending request to {config.model}...")
            print(prompt)

            response = self.client.chat.completions.create(
                model=config.model,
                messages=[
                    {"role": "user", "content": prompt}
                ],
                temperature=config.temperature,
                max_tokens=config.max_tokens,
                top_p=config.top_p,
            )

            result = response.choices[0].message.content
            print(f"✅ Response received from {config.model}")
            if not result:
                raise Exception("empty response")
            return result.strip()
        except Exception as e:
            raise RuntimeError(f"❌ Failed to get response: {e}")
