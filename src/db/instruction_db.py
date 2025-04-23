import json
from pathlib import Path

INSTRUCTION_HISTORY_FILE = Path.home() / ".instruction_history.json"


def load_instruction_history() -> list[str]:
    if INSTRUCTION_HISTORY_FILE.exists():
        try:
            with open(INSTRUCTION_HISTORY_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"⚠️ Failed to load instruction history: {e}")
    return [""]


def save_instruction_history(history: list[str]):
    try:
        with open(INSTRUCTION_HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump(history, f, indent=2)
    except Exception as e:
        print(f"❌ Failed to save instruction history: {e}")


def clear_instructions():
    save_instruction_history([""])
    print("🧹 Instructions cleared.")


def append_instruction(text: str):
    if text == "":
        print("⚠️ No text to append.")
        return
    history = load_instruction_history()
    previous = history[-1]
    current = f"{previous}\n{text}" if previous != "" else text
    history.append(current)
    save_instruction_history(history)
    print("➕ Text appended to instructions.")


def get_latest_instruction() -> str:
    history = load_instruction_history()
    return history[-1] if history else ""


def undo_instruction():
    history = load_instruction_history()
    if not history or history[-1] == "":
        print("⚠️ No instructions history to undo.")
        return
    history.pop()
    save_instruction_history(history)
    print("↩️ Removed last added instruction")


def summary_instruction():
    history = load_instruction_history()
    current = history[-1]
    print(f"Instructions:\n{current}")
