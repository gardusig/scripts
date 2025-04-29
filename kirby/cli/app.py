from __future__ import annotations

from kirby.db.process_file_db import clear_processing_files, summary_processing_files
from kirby.db.shared_file_db import clear_shared_files, summary_shared_files
from kirby.db.prompt_db import append_prompt, clear_prompts, summary_prompts

import typer
import pyperclip
from pyperclip import PyperclipException

from kirby.cli.code_app import code_app
from kirby.cli.process_app import process_app
from kirby.cli.prompt_app import prompt_app
from kirby.cli.file_app import file_app

app = typer.Typer(help="🧰 Kirby CLI – manage instructions & files")
app.add_typer(code_app)
app.add_typer(file_app)
app.add_typer(process_app)
app.add_typer(prompt_app)


# ───────────────────────── helpers ────────────────────────── #


def _clipboard_get() -> str:
    try:
        typer.secho("ℹ️  Attempting to read from clipboard…", fg="green")
        result = pyperclip.paste()
        typer.secho("✅ Clipboard read successfully.", fg="green")
        return result
    except pyperclip.PyperclipException:
        typer.secho("❌  Clipboard not available on this system.", fg="red", err=True)
        raise typer.Exit(1)


def _clipboard_set(text: str) -> None:
    try:
        typer.secho("ℹ️  Attempting to write to clipboard…", fg="green")
        pyperclip.copy(text)
        typer.secho("✅ Clipboard updated successfully.", fg="green")
    except PyperclipException:
        typer.echo(text)
        typer.secho(
            "⚠️  Clipboard not available; printed instead.", fg="yellow", err=True
        )


# ───────────────────────── commands ───────────────────────── #


@app.command(name="show")
def preview():
    typer.echo(summary_prompts())
    typer.echo(summary_shared_files())
    typer.echo(summary_processing_files())


@app.command(name="clipboard")
def add_prompt_from_clipboard():
    append_prompt(_clipboard_get())


@app.command(name="add")
def add_prompt(text: str = typer.Argument(..., help="Prompt line")):
    """Append an prompt string."""
    text = text.strip()
    if not text:
        typer.secho("⚠️  Empty prompt provided.", fg="yellow", err=True)
        raise typer.Exit(1)
    append_prompt(text)


@app.command(name="clear")
def clear_all():
    clear_prompts()
    clear_shared_files()
    clear_processing_files()
