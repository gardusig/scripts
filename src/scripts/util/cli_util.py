import typer
from enum import Enum
import pyperclip
from scripts.util.copy_file_content import copy_file_contents_recursively


class Source(str, Enum):
    clipboard = "clipboard"
    message = "message"
    filepath = "filepath"


def resolve_text(source: Source, message: str = None, path: str = None) -> str:
    if source == Source.clipboard:
        return read_from_clipboard()
    elif source == Source.message:
        return read_from_message(message)
    elif source == Source.filepath:
        return copy_file_contents_recursively(path)
    else:
        raise typer.BadParameter("Unknown source.")


def read_from_clipboard() -> str:
    return pyperclip.paste().strip()


def read_from_message(message: str = None) -> str:
    if not message:
        raise typer.BadParameter(
            "Message is required when source is 'message'.")
    return message.strip()
