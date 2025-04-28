
from kirby.db.shared_file_db import (
    append_shared_file,
    clear_shared_files,
    remove_shared_file,
    summary_shared_files,
    undo_shared_files,
)
import typer
from kirby.util.file_util import get_all_files

file_app = typer.Typer(name="file", help="Manage your shared-file history")


@file_app.command("add")
def add_file(path: str = typer.Argument(..., help="Path to append")):
    """Append a file to the shared history."""
    typer.secho(f'🐛 Starting to add file(s) from path: {path}', fg='blue')
    try:
        for file in get_all_files(path):
            typer.secho(f'ℹ️ Adding file to shared history: {file}', fg='green')
            append_shared_file(file)
        typer.secho('✅ File(s) added to shared history.', fg='green')
    except Exception as e:
        typer.secho(f'❌ Failed to add file(s): {e}', fg='red', err=True)
        raise


@file_app.command("remove")
def remove_file(path: str = typer.Argument(..., help="Path to remove")):
    """Remove a file from the shared history."""
    typer.secho(f'🐛 Starting to remove file from shared history: {path}', fg='blue')
    try:
        remove_shared_file(path)
        typer.secho('✅ File removed from shared history.', fg='green')
    except Exception as e:
        typer.secho(f'❌ Failed to remove file: {e}', fg='red', err=True)
        raise


@file_app.command("clear")
def clear_files():
    """Clear the entire shared-file history."""
    typer.secho('🐛 Starting to clear shared-file history…', fg='blue')
    try:
        clear_shared_files()
        typer.secho('✅ Shared-file history cleared.', fg='green')
    except Exception as e:
        typer.secho(f'❌ Failed to clear shared-file history: {e}', fg='red', err=True)
        raise


@file_app.command("list")
def list_files():
    """Show a summary of your shared-file history."""
    typer.secho('🐛 Listing shared-file history…', fg='blue')
    try:
        summary = summary_shared_files()
        typer.secho('✅ Shared-file history summary:', fg='green')
        typer.echo(summary)
    except Exception as e:
        typer.secho(f'❌ Failed to list shared-file history: {e}', fg='red', err=True)
        raise


@file_app.command("undo")
def undo_file():
    """Undo the last change to your shared-file history."""
    typer.secho('🐛 Undoing last change to shared-file history…', fg='blue')
    try:
        undo_shared_files()
        typer.secho('✅ Last change undone in shared-file history.', fg='green')
    except Exception as e:
        typer.secho(f'❌ Failed to undo last change: {e}', fg='red', err=True)
        raise
