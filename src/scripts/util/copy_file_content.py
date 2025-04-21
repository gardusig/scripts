import os


def copy_file_contents_recursively(path: str) -> str:
    output = []

    def traverse(current_path):
        if os.path.isfile(current_path):
            try:
                with open(current_path, "r", encoding="utf-8") as f:
                    content = f.read().strip()
                rel_path = os.path.relpath(current_path, start=path)
                output.append(f"{rel_path}:\n\n```\n{content}\n```")
            except Exception as e:
                output.append(f"{current_path} (Error reading file: {e})")
        elif os.path.isdir(current_path):
            for entry in sorted(os.listdir(current_path)):
                traverse(os.path.join(current_path, entry))

    traverse(path)
    return "\n\n".join(output)
