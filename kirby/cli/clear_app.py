from kirby.db.file_db import clear_files
from kirby.db.instruction_db import clear_instructions
import typer


clear_app = typer.Typer(
    name="clear",
)


@clear_app.command("instructions", help="Clear only instructions")
def clear_only_instructions():
    clear_instructions()


@clear_app.command("files", help="Clear only files")
def clear_only_files():
    clear_files()
