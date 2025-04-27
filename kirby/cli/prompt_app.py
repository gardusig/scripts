import typer
from kirby.db.prompt_db import (
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
    append_prompt(prompt)


@prompt_app.command("remove")
def remove(prompt: str = typer.Argument(..., help="Prompt text to remove")):
    """Remove an existing prompt from history."""
    remove_prompt(prompt)


@prompt_app.command("clear")
def clear():
    """Clear all prompts from history."""
    clear_prompts()


@prompt_app.command("list")
def list_():
    """Show a summary of all stored prompts."""
    typer.echo(summary_prompts())


@prompt_app.command("undo")
def undo():
    """Undo the last change to prompt history."""
    undo_prompts()
