from __future__ import annotations

from instruction.unit_test import UNIT_TEST_INSTRUCTIONS
import pyperclip
import typer
from pyperclip import PyperclipException

from db.file_db import clear_files, summary_files
from db.instruction_db import (
    append_instruction,
    clear_instructions,
    summary_instruction,
)
from instruction.response_format import RESPONSE_FORMAT_INSTRUCTIONS
from util.ai_util import get_ai_client, send_message
from util.file_util import rewrite_files
from util.string_util import parse_code_response
from cli.file_cli import file_app
from cli.instruction_cli import instruction_app

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
def clear(
    instructions: bool = typer.Option(True, "--instructions/--no-instructions"),
    files: bool = typer.Option(True, "--files/--no-files"),
):
    """Clear instructions and/or files."""
    if instructions:
        clear_instructions()
    if files:
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
def add_from_clipboard():
    """Append instruction from clipboard contents."""
    add_instruction(_clipboard_get())


@app.command(name="copy")
def copy_summary():
    """Copy a combined summary (instructions + files) to clipboard."""
    _clipboard_set("\n".join([summary_instruction(), summary_files()]))


@app.command(name="unit-test")
def create_tests():
    instructions = []
    instructions.extend(RESPONSE_FORMAT_INSTRUCTIONS)
    instructions.extend(UNIT_TEST_INSTRUCTIONS)

    ai_client = get_ai_client()
    response = send_message(ai_client, instructions)
    file_map = parse_code_response(response)
    rewrite_files(file_map)


@app.command(name="code")
def update_code():
    instructions = []
    instructions.extend(RESPONSE_FORMAT_INSTRUCTIONS)
    ai_client = get_ai_client()
    response = send_message(ai_client, instructions)
    file_map = parse_code_response(response)
    rewrite_files(file_map)
