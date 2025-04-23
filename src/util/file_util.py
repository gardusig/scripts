
import json
import os
import fnmatch
from pathlib import Path
from typing import Optional
from rich import print

DEFAULT_IGNORES = [
    "__pycache__",
    "*.pyc",
    "*.pyo",
    "*.egg-info",
    ".DS_Store",
    ".git",
    ".venv",
    "venv",
    "build",
    "dist",
    ".copyignore",
    ".env",
    "LICENSE",
    "*.webp",
    "*.jpg",
    "*.jpeg",
]


def should_ignore(name: str, ignore_patterns: list[str]) -> bool:
    return any(fnmatch.fnmatch(name, pattern) for pattern in ignore_patterns)


def get_all_files(path: str, ignore_patterns=DEFAULT_IGNORES) -> list[str]:
    files = []

    def traverse(current_path):
        name = os.path.basename(current_path)
        if should_ignore(name, ignore_patterns):
            print(f"⏭️ Skipping ignored: {current_path}")
            return
        if os.path.isfile(current_path):
            files.append(current_path)
        elif os.path.isdir(current_path):
            for entry in sorted(os.listdir(current_path)):
                traverse(os.path.join(current_path, entry))

    traverse(path)
    return files


def stringify_file_contents(file_paths: set[str]) -> dict[str, str]:
    output = {}
    for path in file_paths:
        try:
            with open(path, "r", encoding="utf-8") as f:
                output[path] = f.read().strip()
        except Exception as e:
            print(f"Error reading file: {path}, reason: {e})")
    print(f"📄 Read {len(file_paths)} file(s)")
    return output


def load_instructions(instruction_paths: list[str], base_dir: Optional[Path] = None) -> Optional[str]:
    result = ""
    for path in instruction_paths:
        text = load_instruction(path, base_dir)
        if text:
            result += text
    return result if result else None


def load_instruction(instruction_path: str, base_dir: Optional[Path] = None) -> Optional[str]:
    try:
        if base_dir is None:
            base_dir = Path(__file__).parent.parent / "resources/instructions"
        path = base_dir / instruction_path
        if not path.exists():
            print(f"⚠️ Instruction file '{instruction_path}' not found.")
            return None
        with open(path, "r", encoding="utf-8") as f:
            instructions: list[str] = json.load(f)
            return "".join(instructions)
    except Exception as e:
        print(f"❌ Failed to load instructions from '{instruction_path}': {e}")
        return None


def rewrite_files(content_dict: dict[str, str], allowed_file_prefixes: list[str] = []):
    for file_path, content in content_dict.items():
        if any(file_path.startswith(prefix) for prefix in allowed_file_prefixes):
            rewrite_file(file_path, content)


def rewrite_file(file_path: str, content: str):
    try:
        path = Path(file_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(content)
        print(f"✅ File rewritten: {file_path}")
    except Exception as e:
        print(f"❌ Error writing to {file_path}: {e}")
