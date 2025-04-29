import typer
from sasori.db.prompt_db import (
    append_prompt,
    remove_prompt,
    clear_prompts,
    summary_prompts,
    undo_prompts,
)

prompt_app = typer.Typer(name="prompt", help="Manage your AI prompt history")


@prompt_app.command("add")
def add(prompt: str = typer.Argument(..., help="Prompt text to append")):
    """Append a new prompt to history."""
    try:
        append_prompt(prompt)
    except Exception as e:
        typer.secho(f"❌ Failed to add prompt: {e}", fg="red", err=True)
        raise


@prompt_app.command("remove")
def remove(prompt: str = typer.Argument(..., help="Prompt text to remove")):
    """Remove an existing prompt from history."""
    try:
        remove_prompt(prompt)
    except Exception as e:
        typer.secho(f"❌ Failed to remove prompt: {e}", fg="red", err=True)
        raise


@prompt_app.command("clear")
def clear():
    """Clear all prompts from history."""
    try:
        clear_prompts()
    except Exception as e:
        typer.secho(f"❌ Failed to clear prompts: {e}", fg="red", err=True)
        raise


@prompt_app.command("list")
def list_():
    """Show a summary of all stored prompts."""
    try:
        summary = summary_prompts()
        typer.echo(summary)
    except Exception as e:
        typer.secho(f"❌ Failed to list prompts: {e}", fg="red", err=True)
        raise


@prompt_app.command("undo")
def undo():
    """Undo the last change to prompt history."""
    try:
        undo_prompts()
    except Exception as e:
        typer.secho(f"❌ Failed to undo prompt change: {e}", fg="red", err=True)
        raise
