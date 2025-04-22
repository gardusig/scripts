import typer
from db.instruction_db import (
    clear_instructions,
    append_instruction,
    undo_instruction,
    summary_instruction,
)

instruction_app = typer.Typer(help="AI instruction processing")


@instruction_app.command()
def clear():
    clear_instructions()


@instruction_app.command()
def add(string: str = typer.Argument(..., help="File path to append")):
    append_instruction(string)


@instruction_app.command()
def undo():
    undo_instruction()


@instruction_app.command()
def list():
    summary_instruction()
