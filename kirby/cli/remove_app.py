import typer
from kirby.db.file_db import remove_file


remove_app = typer.Typer(name="remove")


@remove_app.command(help="Remove a file path")
def remove(string: str = typer.Argument(..., help="File path to append")):
    string = string.strip()
    if not string:
        print("⚠️ Empty string provided.")
        raise typer.Exit(code=1)
    remove_file(string)
