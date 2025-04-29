from sasori.db.shared_file_db import (
    append_shared_file,
    clear_shared_files,
    remove_shared_file,
    summary_shared_files,
    undo_shared_files,
)
import typer
from sasori.util.file_util import get_all_files

file_app = typer.Typer(name="file", help="Manage your shared-file history")


@file_app.command("add")
def add_file(path: str = typer.Argument(..., help="Path to append")):
    """Append a file to the shared history."""
    try:
        for file in get_all_files(path):
            append_shared_file(file)
    except Exception as e:
        typer.secho(f"❌ Failed to add file(s): {e}", fg="red", err=True)
        raise


@file_app.command("remove")
def remove_file(path: str = typer.Argument(..., help="Path to remove")):
    """Remove a file from the shared history."""
    try:
        remove_shared_file(path)
    except Exception as e:
        typer.secho(f"❌ Failed to remove file: {e}", fg="red", err=True)
        raise


@file_app.command("clear")
def clear_files():
    """Clear the entire shared-file history."""
    try:
        clear_shared_files()
    except Exception as e:
        typer.secho(f"❌ Failed to clear shared-file history: {e}", fg="red", err=True)
        raise


@file_app.command("list")
def list_files():
    """Show a summary of your shared-file history."""
    try:
        summary = summary_shared_files()
        typer.echo(summary)
    except Exception as e:
        typer.secho(f"❌ Failed to list shared-file history: {e}", fg="red", err=True)
        raise


@file_app.command("undo")
def undo_file():
    """Undo the last change to your shared-file history."""
    try:
        undo_shared_files()
    except Exception as e:
        typer.secho(f"❌ Failed to undo last change: {e}", fg="red", err=True)
        raise
