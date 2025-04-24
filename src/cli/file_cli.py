import typer
from db.file_db import (
    clear_files,
    append_file,
    remove_file,
    undo_files,
    summary_files,
)
from util.file_util import get_all_files
from cli.app_cli import app


file_app = typer.Typer(help="📁 File path management CLI")
app.add_typer(file_app, name="file", help="Manage resources (clipboard).")


@file_app.command(help="Clear all files")
def clear():
    clear_files()


@file_app.command(help="Add a file path")
def add(string: str = typer.Argument(..., help="File path to append")):
    string = string.strip()
    if not string:
        print("⚠️ Empty string provided.")
        raise typer.Exit(code=1)
    files = get_all_files(string)
    for file in files:
        append_file(file)


@file_app.command(help="Remove a file path")
def remove(string: str = typer.Argument(..., help="File path to append")):
    string = string.strip()
    if not string:
        print("⚠️ Empty string provided.")
        raise typer.Exit(code=1)
    remove_file(string)


@file_app.command(help="Undo last file operation")
def undo():
    undo_files()


@file_app.command(help="List all files")
def list():
    print(summary_files())
