from db.instruction_db import (
    clear_instructions,
    summary_instruction,
    undo_instruction,
)
import typer


instruction_app = typer.Typer(help="Instruction processing CLI")


@instruction_app.command(help="Clear all instructions")
def clear():
    clear_instructions()


@instruction_app.command(help="Undo last instruction operation")
def undo():
    undo_instruction()


@instruction_app.command(help="List all instructions")
def list():
    print(summary_instruction())
