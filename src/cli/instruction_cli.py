from db.instruction_db import (
    append_instruction,
    clear_instructions,
    summary_instruction,
    undo_instruction,
)
import pyperclip
import typer

instruction_app = typer.Typer(help="instruction processing")


@instruction_app.command()
def clear():
    clear_instructions()


@instruction_app.command()
def add(string: str = typer.Argument(..., help="instruction to append")):
    if not string.strip():
        print("⚠️ Empty instruction provided.")
        raise typer.Exit(code=1)
    append_instruction(string)


@instruction_app.command()
def add_clipboard():
    string = pyperclip.paste()
    if not string.strip():
        print("⚠️ Empty instruction provided.")
        raise typer.Exit(code=1)
    append_instruction(string)


@instruction_app.command()
def undo():
    undo_instruction()


@instruction_app.command()
def list():
    summary_instruction()
