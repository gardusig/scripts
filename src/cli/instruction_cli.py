from db.instruction_db import append_instruction, clear_instructions, summary_instruction, undo_instruction
import typer


instruction_app = typer.Typer(help="instruction processing")


@instruction_app.command()
def clear():
    clear_instructions()


@instruction_app.command()
def add(string: str = typer.Argument(..., help="instruction to append")):
    append_instruction(string)


@instruction_app.command()
def undo():
    undo_instruction()


@instruction_app.command()
def list():
    summary_instruction()
