from db.instruction_db import (
    clear_instructions,
    summary_instruction,
    undo_instructions,
)
import typer
from cli.app_cli import app


instruction_app = typer.Typer(help="Instruction processing CLI")
app.add_typer(instruction_app, name="instruction", help="AI Instruction Analysis.")


@instruction_app.command(help="Clear all instructions")
def clear():
    clear_instructions()


@instruction_app.command(help="Undo last instruction operation")
def undo():
    undo_instructions()


@instruction_app.command(help="List all instructions")
def list():
    print(summary_instruction())
