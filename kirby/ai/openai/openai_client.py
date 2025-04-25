import os
from typing import Optional
from kirby.ai.ai_client_config import AIConfig
from kirby.ai.ai_client_interface import AIClient
from kirby.ai.openai.openai_config import OpenAIConfig
from openai import OpenAI
from openai.types.chat import ChatCompletionMessageParam


class OpenAIClient(AIClient):
    def __init__(self) -> None:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise RuntimeError("❌ OPENAI_API_KEY is not set.")
        self.client = OpenAI(api_key=api_key)

    def build_messages(
        self,
        instructions: Optional[list[str]],
        files: dict[str, str],
        final_prompt: Optional[str],
    ) -> list[ChatCompletionMessageParam]:
        msgs: list[ChatCompletionMessageParam] = []
        if instructions:
            msgs.append({"role": "system", "content": "\n".join(instructions)})
        for fname, content in files.items():
            msgs.append(
                {
                    "role": "user",
                    "content": (f"--- File: {fname} ---\n" f"```{content}```"),
                }
            )
        if final_prompt:
            msgs.append(
                {
                    "role": "user",
                    "content": final_prompt.strip()
                }
            )
        return msgs

    def get_response(
        self,
        instructions: Optional[list[str]] = None,
        context: dict[str, str] = {},
        final_prompt: Optional[str] = None,
        config: Optional[AIConfig] = None,
    ) -> str:
        if not config:
            config = OpenAIConfig()

        messages = self.build_messages(instructions, context, final_prompt)
        print(f"📨 Sending request to {config.model}...")
        response = self.client.chat.completions.create(
            model=config.model,
            temperature=config.temperature,
            max_tokens=config.max_tokens,
            top_p=config.top_p,
            messages=messages,
        )
        result = response.choices[0].message.content or ""
        print(f"✅ Response received from {config.model}")
        return result.strip()
