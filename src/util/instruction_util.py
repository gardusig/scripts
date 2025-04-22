import json
from pathlib import Path


def load_instructions(instruction_path: str) -> str:
    try:
        path = Path.home() / instruction_path
        if not path.exists():
            print(f"⚠️ Instruction file '{instruction_path}' not found.")
            return ''
        with open(path, "r", encoding="utf-8") as f:
            instructions: list[str] = json.load(f)
            return '\n'.join(instructions)
    except Exception as e:
        print(
            f"❌ Failed to load instructions from '{instruction_path}.json': {e}")
        return ''
