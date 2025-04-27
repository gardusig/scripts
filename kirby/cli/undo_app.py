from kirby.db.file_db import undo_files
from kirby.db.instruction_db import undo_instructions
import typer


undo_app = typer.Typer(name="undo")


@undo_app.command(name="instruction", help="Undo last instruction operation")
def undo_instruction():
    undo_instructions()


@undo_app.command(name="file")
def undo_file():
    undo_files()
