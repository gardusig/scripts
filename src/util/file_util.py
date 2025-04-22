import os
import fnmatch

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
    "LICENSE"
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


def stringify_file_contents(file_paths: list[str]) -> str:
    output = []
    for path in file_paths:
        try:
            with open(path, "r", encoding="utf-8") as f:
                content = f.read().strip()
            output.append(f"{path}:\n\n```\n{content}\n```")
        except Exception as e:
            output.append(f"{path} (Error reading file: {e})")
    print(f"📄 Read {len(file_paths)} file(s)")
    return "\n\n".join(output)
