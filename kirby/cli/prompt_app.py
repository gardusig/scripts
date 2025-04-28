
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
    typer.secho('🐛 Starting to add prompt…', fg='blue')
    try:
        append_prompt(prompt)
        typer.secho('✅ Prompt added to history.', fg='green')
    except Exception as e:
        typer.secho(f'❌ Failed to add prompt: {e}', fg='red', err=True)
        raise


@prompt_app.command("remove")
def remove(prompt: str = typer.Argument(..., help="Prompt text to remove")):
    """Remove an existing prompt from history."""
    typer.secho('🐛 Starting to remove prompt…', fg='blue')
    try:
        remove_prompt(prompt)
        typer.secho('✅ Prompt removed from history.', fg='green')
    except Exception as e:
        typer.secho(f'❌ Failed to remove prompt: {e}', fg='red', err=True)
        raise


@prompt_app.command("clear")
def clear():
    """Clear all prompts from history."""
    typer.secho('🐛 Clearing all prompts…', fg='blue')
    try:
        clear_prompts()
        typer.secho('✅ All prompts cleared from history.', fg='green')
    except Exception as e:
        typer.secho(f'❌ Failed to clear prompts: {e}', fg='red', err=True)
        raise


@prompt_app.command("list")
def list_():
    """Show a summary of all stored prompts."""
    typer.secho('🐛 Listing all prompts…', fg='blue')
    try:
        summary = summary_prompts()
        typer.secho('✅ Prompts listed below:', fg='green')
        typer.echo(summary)
    except Exception as e:
        typer.secho(f'❌ Failed to list prompts: {e}', fg='red', err=True)
        raise


@prompt_app.command("undo")
def undo():
    """Undo the last change to prompt history."""
    typer.secho('🐛 Undoing last prompt change…', fg='blue')
    try:
        undo_prompts()
        typer.secho('✅ Last prompt change undone.', fg='green')
    except Exception as e:
        typer.secho(f'❌ Failed to undo prompt change: {e}', fg='red', err=True)
        raise
