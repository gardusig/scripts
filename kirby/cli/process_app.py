
from kirby.db.process_file_db import (
    append_processing_file,
    clear_processing_files,
    remove_processing_file,
    summary_processing_files,
    undo_processing_files,
)
import typer
from kirby.util.file_util import get_all_files

process_app = typer.Typer(name="process", help="Manage your processing-file history")


@process_app.command("add")
def add_file(path: str = typer.Argument(..., help="Path to append")):
    """Append a file to the processing queue."""
    typer.secho(f'🐛 Starting to add files from: {path}', fg='blue')
    for file in get_all_files(path):
        typer.secho(f'ℹ️ Adding file to processing queue: {file}', fg='green')
        append_processing_file(file)
    typer.secho('✅ Finished adding files to processing queue.', fg='green')


@process_app.command("remove")
def remove_file(path: str = typer.Argument(..., help="Path to remove")):
    """Remove a file from the processing queue."""
    typer.secho(f'🐛 Starting to remove file: {path}', fg='blue')
    remove_processing_file(path)
    typer.secho(f'✅ Removed file from processing queue: {path}', fg='green')


@process_app.command("clear")
def clear_files():
    """Clear the entire processing-file history."""
    typer.secho('🐛 Clearing all processing-file history…', fg='blue')
    clear_processing_files()
    typer.secho('✅ Cleared all processing-file history.', fg='green')


@process_app.command("list")
def list_files():
    """Show a summary of your processing-file history."""
    typer.secho('🐛 Listing processing-file history…', fg='blue')
    summary = summary_processing_files()
    typer.secho('✅ Listed processing-file history.', fg='green')
    typer.echo(summary)


@process_app.command("undo")
def undo_file():
    """Undo the last change to your processing-file history."""
    typer.secho('🐛 Undoing last change to processing-file history…', fg='blue')
    undo_processing_files()
    typer.secho('✅ Undid last change to processing-file history.', fg='green')
