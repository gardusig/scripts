from db.file_db import clear_files, summary_files
from db.instruction_db import append_instruction, clear_instructions, summary_instruction
import typer
from cli.file_cli import file_app
from util.ai_util import build_message
from cli.instruction_cli import instruction_app
from cli.digest_cli import digest_app
from dotenv import load_dotenv
import pyperclip

app = typer.Typer(help="Main application with subcommands.")
app.add_typer(file_app, name="file", help="Manage resources (clipboard).")
app.add_typer(instruction_app, name="instruction", help="AI Instruction Analysis.")
app.add_typer(digest_app, name="digest", help="Code Digest Tools.")

load_dotenv()

@app.command(help="Clear all instructions and files")
def clear():
    clear_instructions()
    clear_files()

@app.command(help="Copy built message to clipboard")
def clipboard():
    message = build_message()
    pyperclip.copy(message)

@app.command(help="Preview instructions and files")
def preview():
    summary_instruction()
    summary_files()

@app.command(help="Append an instruction")
def eat(string: str = typer.Argument(..., help="Instruction to append")):
    if not string.strip():
        print("⚠️ Empty instruction provided.")
        raise typer.Exit(code=1)
    append_instruction(string)

@app.command(help="Append instruction from clipboard")
def eat_clipboard():
    string = pyperclip.paste()
    if not string.strip():
        print("⚠️ Empty instruction provided.")
        raise typer.Exit(code=1)
    append_instruction(string)

if __name__ == "__main__":
    app()