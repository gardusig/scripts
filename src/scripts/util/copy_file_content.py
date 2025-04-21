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
    ".copyignore"
]


def should_ignore(name, ignore_patterns):
    return any(fnmatch.fnmatch(name, pattern) for pattern in ignore_patterns)


def copy_file_contents_recursively(path: str, ignore_patterns=DEFAULT_IGNORES) -> str:
    output = []

    def traverse(current_path):
        name = os.path.basename(current_path)
        if should_ignore(name, ignore_patterns):
            print(f"⏭️ Skipping ignored: {current_path}")
            return
        if os.path.isfile(current_path):
            try:
                print(f"📄 Reading: {current_path}")
                with open(current_path, "r", encoding="utf-8") as f:
                    content = f.read().strip()
                output.append(f"{current_path}:\n\n```\n{content}\n```")
            except Exception as e:
                output.append(f"{current_path} (Error reading file: {e})")
        elif os.path.isdir(current_path):
            for entry in sorted(os.listdir(current_path)):
                traverse(os.path.join(current_path, entry))

    traverse(path)
    return "\n\n".join(output)
