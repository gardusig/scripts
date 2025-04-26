from __future__ import annotations

import typer
import pyperclip
from pyperclip import PyperclipException

from kirby.db.file_db import clear_files, summary_files
from kirby.db.instruction_db import (
    append_instruction,
    clear_instructions,
    summary_instruction,
)
from kirby.ai.ai_client_factory import get_ai_client
from kirby.util.file_util import rewrite_files
from kirby.util.string_util import parse_code_response
from kirby.cli.file_cli import file_app
from kirby.cli.instruction_cli import instruction_app

app = typer.Typer(help="🧰 Kirby CLI – manage instructions & files")
app.add_typer(file_app, name="file", help="Manage resources (clipboard).")
app.add_typer(instruction_app, name="instruction", help="AI Instruction Analysis.")

# ───────────────────────── helpers ────────────────────────── #


def _clipboard_get() -> str:
    try:
        return pyperclip.paste()
    except PyperclipException:
        typer.echo("⚠️  Clipboard not available on this system.", err=True)
        raise typer.Exit(1)


def _clipboard_set(text: str) -> None:
    try:
        pyperclip.copy(text)
    except PyperclipException:
        print(text)
        typer.echo("⚠️  Clipboard not available; printed instead.", err=True)


# ───────────────────────── commands ───────────────────────── #


@app.command()
def clear():
    """Clear instructions and/or files."""
    clear_instructions()
    clear_files()


@app.command(name="show")
def preview():
    """Display current instructions and files."""
    typer.echo(summary_instruction())
    typer.echo(summary_files())


@app.command(name="add")
def add_instruction(text: str = typer.Argument(..., help="Instruction line")):
    """Append an instruction string."""
    text = text.strip()
    if not text:
        typer.echo("⚠️  Empty instruction provided.", err=True)
        raise typer.Exit(1)
    append_instruction(text)


@app.command(name="add-clip")
def add_instruction_from_clipboard():
    """Append instruction from kirby.clipboard contents."""
    add_instruction(_clipboard_get())


@app.command(name="copy")
def copy_summary():
    """Copy a combined summary (instructions + files) to clipboard."""
    _clipboard_set("\n".join([summary_instruction(), summary_files()]))


@app.command(name="unit-test")
def create_tests():
    ai_client = get_ai_client()
    response = ai_client.send_message()
    file_map = parse_code_response(response)
    rewrite_files(file_map)


@app.command(name="code")
def update_code():
    ai_client = get_ai_client()
    response = ai_client.send_message()
    file_map = parse_code_response(response)
    rewrite_files(file_map)
