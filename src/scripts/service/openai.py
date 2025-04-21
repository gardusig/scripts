import os
from openai import OpenAI
from dotenv import load_dotenv
from rich import print

load_dotenv()


def get_ai_response(instructions: str, input: str):
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ OPENAI_API_KEY is not set.")
        return

    client = OpenAI(api_key=api_key)
    print("📨 Sending request to OpenAI...\n")

    try:
        response = client.responses.create(
            model="gpt-4o",
            instructions=instructions,
            input=input,
        )
        print("✅ Response received:\n")
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"❌ Failed to get response: {e}")
