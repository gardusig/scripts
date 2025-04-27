from __future__ import annotations

from kirby.util.file_util import get_file_contents

from kirby.db.instruction_db import append_instruction, clear_instructions, summary_instruction
import typer
import pyperclip
from pyperclip import PyperclipException

from kirby.db.file_db import clear_files, summary_files
from kirby.cli.clear_app import clear_app
from kirby.cli.add_app import add_app
from kirby.cli.code_app import code_app
from kirby.cli.list_app import list_app
from kirby.cli.remove_app import remove_app
from kirby.cli.undo_app import undo_app

app = typer.Typer(help="🧰 Kirby CLI – manage instructions & files")
app.add_typer(add_app)
app.add_typer(clear_app)
app.add_typer(code_app)
app.add_typer(list_app)
app.add_typer(remove_app)
app.add_typer(undo_app)


# ───────────────────────── helpers ────────────────────────── #


def _clipboard_set(text: str) -> None:
    try:
        pyperclip.copy(text)
    except PyperclipException:
        print(text)
        typer.echo("⚠️  Clipboard not available; printed instead.", err=True)


# ───────────────────────── commands ───────────────────────── #


@app.command(name="show")
def preview():
    """Display current instructions and files."""
    typer.echo(summary_instruction())
    typer.echo(summary_files())


@app.command(name="copy")
def copy_summary():
    messages = [summary_instruction()]
    messages.extend(get_file_contents())
    _clipboard_set("\n".join(messages))


@app.command(name="eat")
def add_instruction(text: str = typer.Argument(..., help="Instruction line")):
    """Append an instruction string."""
    text = text.strip()
    if not text:
        typer.echo("⚠️  Empty instruction provided.", err=True)
        raise typer.Exit(1)
    append_instruction(text)


@app.command(name="poop")
def clear_all():
    clear_instructions()
    clear_files()
