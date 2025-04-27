import typer
from kirby.db.file_db import (
    append_shared_file,
    remove_shared_file,
    clear_shared_files,
    summary_shared_files,
    undo_shared_files,
)

file_app = typer.Typer(name="file", help="Manage your shared-file history")


@file_app.command("add")
def add_file(path: str = typer.Argument(..., help="Path to append")):
    """Append a file to the shared history."""
    append_shared_file(path)


@file_app.command("remove")
def remove_file(path: str = typer.Argument(..., help="Path to remove")):
    """Remove a file from the shared history."""
    remove_shared_file(path)


@file_app.command("clear")
def clear_files():
    """Clear the entire shared-file history."""
    clear_shared_files()


@file_app.command("list")
def list_files():
    """Show a summary of your shared-file history."""
    typer.echo(summary_shared_files())


@file_app.command("undo")
def undo_file():
    """Undo the last change to your shared-file history."""
    undo_shared_files()
