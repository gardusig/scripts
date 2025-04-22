import json
from pathlib import Path


def load_instructions(instruction_path: Path) -> list[str]:
    try:
        if not instruction_path.exists():
            print(f"⚠️ Instruction file '{instruction_path}.json' not found.")
            return []
        with open(instruction_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(
            f"❌ Failed to load instructions from '{instruction_path}.json': {e}")
        return []
