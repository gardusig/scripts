from db.instruction_db import (
    append_instruction,
    clear_instructions,
    summary_instruction,
    undo_instruction,
)
import pyperclip
import typer

instruction_app = typer.Typer(help="Instruction processing CLI")

@instruction_app.command(help="Clear all instructions")
def clear():
    clear_instructions()

@instruction_app.command(help="Add a new instruction")
def add(string: str = typer.Argument(..., help="Instruction to append")):
    if not string.strip():
        print("⚠️ Empty instruction provided.")
        raise typer.Exit(code=1)
    append_instruction(string)

@instruction_app.command(help="Add instruction from clipboard")
def add_clipboard():
    string = pyperclip.paste()
    if not string.strip():
        print("⚠️ Empty instruction provided.")
        raise typer.Exit(code=1)
    append_instruction(string)

@instruction_app.command(help="Undo last instruction operation")
def undo():
    undo_instruction()

@instruction_app.command(help="List all instructions")
def list():
    summary_instruction()

@instruction_app.command(help="Usage for each resource")
def usage():
    print("Usage examples for each resource:")
    print("- repository_review.json: Conduct a comprehensive review of the codebase.")
    print("- unit_testing.json: Develop comprehensive unit tests for each function and class.")
    print("- performance_optimization.json: Identify performance bottlenecks through profiling.")