import json
from pathlib import Path

FILE_SET_HISTORY = Path.home() / ".file_set_history.json"


def load_file_history() -> list[list[str]]:
    if FILE_SET_HISTORY.exists():
        try:
            with open(FILE_SET_HISTORY, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"⚠️ Failed to load file history: {e}")
    return [[]]


def save_file_history(history: list[list[str]]):
    try:
        with open(FILE_SET_HISTORY, "w", encoding="utf-8") as f:
            json.dump(history, f, indent=2)
    except Exception as e:
        print(f"❌ Failed to save file history: {e}")


def get_latest_files() -> set[str]:
    history = load_file_history()
    return set(history[-1]) if history else set()


def clear_files():
    save_file_history([[]])
    print("🧹 File set cleared.")


def append_file(path: str):
    path = path.strip()
    if not path:
        print("⚠️ No file path to append.")
        return
    current = get_latest_files()
    current.add(path)
    history = load_file_history()
    history.append(sorted(current))
    save_file_history(history)
    print(f"➕ File path added: {path}")


def undo_files():
    history = load_file_history()
    if len(history) <= 1:
        print("⚠️ No file history to undo.")
        return
    history.pop()
    save_file_history(history)
    print("↩️ Reverted last added file.")


def summary_files():
    latest = get_latest_files()
    print(f"📁 File set size: {len(latest)}")
    for p in sorted(latest):
        print(f" - {p}")
