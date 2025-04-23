import typer
from db.file_db import (
    clear_files,
    append_file,
    undo_files,
    summary_files,
)
from util.file_util import get_all_files

file_app = typer.Typer(help="📁 File path management CLI")

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

@file_app.command(help="Undo last file operation")
def undo():
    undo_files()

@file_app.command(help="List all files")
def list():
    summary_files()

@file_app.command(help="Usage for file operations")
def usage():
    print("Usage examples for file operations:")
    print("- clear: Remove all tracked files.")
    print("- add: Append a new file path to the list.")