from sasori.db.process_file_db import (
    append_processing_file,
    clear_processing_files,
    remove_processing_file,
    summary_processing_files,
    undo_processing_files,
)
import typer
from sasori.util.file_util import get_all_files

process_app = typer.Typer(name="process", help="Manage your processing-file history")


@process_app.command("add")
def add_file(path: str = typer.Argument(..., help="Path to append")):
    """Append a file to the processing queue."""
    for file in get_all_files(path):
        append_processing_file(file)


@process_app.command("remove")
def remove_file(path: str = typer.Argument(..., help="Path to remove")):
    """Remove a file from the processing queue."""
    for file in get_all_files(path):
        remove_processing_file(file)


@process_app.command("clear")
def clear_files():
    """Clear the entire processing-file history."""
    clear_processing_files()


@process_app.command("list")
def list_files():
    """Show a summary of your processing-file history."""
    summary = summary_processing_files()
    typer.echo(summary)


@process_app.command("undo")
def undo_file():
    """Undo the last change to your processing-file history."""
    undo_processing_files()
