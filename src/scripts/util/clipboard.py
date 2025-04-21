import json
from pathlib import Path
import pyperclip

HISTORY_FILE = Path.home() / ".clipboard_history.json"


def get_preview(text: str) -> str:
    if len(text) <= 100:
        return text
    return (
        f"{text[:50]}\n\n"
        f"[...]\n\n"
        f"{text[-50:]}"
    )


def load_history() -> list[str]:
    if HISTORY_FILE.exists():
        try:
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"⚠️ Failed to load history: {e}")
    return [""]


def save_history(history: list[str]):
    try:
        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump(history, f, indent=2)
    except Exception as e:
        print(f"❌ Failed to save history: {e}")


def clear_clipboard():
    save_history([""])
    print("🧹 Clipboard cleared.")


def append_to_clipboard(text: str):
    if text == '':
        print("⚠️ No text to append.")
        return
    history = load_history()
    previous = history[-1]
    current = f'{previous}\n{text}' if previous != '' else text
    history.append(current)
    save_history(history)
    print(f"➕ Text appended to clipboard:\n{get_preview(text)}")


def override_clipboard(text: str):
    current = text
    history = load_history()
    history.append(current)
    save_history(history)
    print(f"✏️ Clipboard overridden to:\n{get_preview(text)}")


def undo_clipboard():
    history = load_history()
    if not history or history[-1] == '':
        print("⚠️ No clipboard history to undo.")
        return
    last = history.pop()
    save_history(history)
    print(f"↩️ Removed from clipboard:\n{get_preview(last)}")


def clipboard_summary():
    history = load_history()
    current = history[-1]
    print(f"Undo steps available: {len(history) - 1}")
    print(f"Current content preview:\n{get_preview(current)}")
    pyperclip.copy(current)
