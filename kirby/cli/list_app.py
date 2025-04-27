from kirby.db.instruction_db import summary_instruction
import typer
from kirby.db.file_db import summary_files


list_app = typer.Typer(name="list")


@list_app.command(name="files")
def list_files():
    print(summary_files())


@list_app.command(help="List all instructions")
def list():
    print(summary_instruction())
