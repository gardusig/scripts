from kirby.db.file_db import append_file
import pyperclip
from kirby.util.file_util import get_all_files
from kirby.db.instruction_db import append_instruction
import typer


def _clipboard_get() -> str:
    try:
        return pyperclip.paste()
    except pyperclip.PyperclipException:
        typer.echo("⚠️  Clipboard not available on this system.", err=True)
        raise typer.Exit(1)


add_app = typer.Typer(
    name="add",
)


@add_app.command(name="clipboard")
def add_instruction_from_clipboard():
    append_instruction(_clipboard_get())


@add_app.command(name="file")
def add(string: str = typer.Argument(..., help="File path to append")):
    print(string)
    string = string.strip()
    if not string:
        print("⚠️ Empty string provided.")
        raise typer.Exit(code=1)
    files = get_all_files(string)
    for file in files:
        append_file(file)
