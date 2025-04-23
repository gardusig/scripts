from db.file_db import clear_files, summary_files
from db.instruction_db import append_instruction, clear_instructions, summary_instruction
import typer
from cli.file_cli import file_app
from util.ai_util import get_ai_client, handle_code_change_response, send_message
from cli.instruction_cli import instruction_app
from cli.digest_cli import digest_app
from dotenv import load_dotenv
import pyperclip
from util.file_util import load_instructions

app = typer.Typer(help="Main application with subcommands.")
app.add_typer(file_app, name="file", help="Manage resources (clipboard).")
app.add_typer(instruction_app, name="instruction", help="AI Instruction Analysis.")
app.add_typer(digest_app, name="digest", help="Code Digest Tools.")

load_dotenv()


@app.command(help="Clear all instructions and files")
def clean():
    clear_instructions()
    clear_files()


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


@app.command(help="Response JSON format analysis")
def ask():
    instructions = load_instructions([
        "response/response_json_format.json",
    ])
    ai_client = get_ai_client()
    response = send_message(ai_client, instructions)
    handle_code_change_response(response)


if __name__ == "__main__":
    app()
