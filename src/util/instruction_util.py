import json
from pathlib import Path
from typing import Optional


def load_instructions(instruction_path: str) -> Optional[str]:
    try:
        current_dir = Path(__file__).resolve().parent
        while current_dir != current_dir.root:
            if (current_dir / '.git').exists():
                break
            current_dir = current_dir.parent
        path = current_dir / 'src' / instruction_path
        if not path.exists():
            print(f"⚠️ Instruction file '{instruction_path}' not found.")
            return None
        with open(path, "r", encoding="utf-8") as f:
            instructions: list[str] = json.load(f)
            print(f"Loaded instructions from: {path}")
            return '\n'.join(instructions)
    except Exception as e:
        print(f"❌ Failed to load instructions from '{instruction_path}': {e}")
        return None
