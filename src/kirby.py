from db.file_db import clear_files
from db.instruction_db import clear_instructions
import typer
from cli.file_cli import file_app
from util.ai_util import build_message, get_ai_client, send_message
from cli.instruction_cli import instruction_app
from cli.code_cli import code_app
from dotenv import load_dotenv
import pyperclip

app = typer.Typer(help="Main application with subcommands.")
app.add_typer(file_app, name="file",
              help="Manage resources (clipboard).")
app.add_typer(instruction_app, name="instruction",
              help="AI Instruction Analysis.")
app.add_typer(code_app, name="?",
              help="?")

load_dotenv()


@app.command()
def evaluate():
    ai_client = get_ai_client()
    response = send_message(ai_client)
    print(response)


@app.command()
def clear():
    clear_instructions()
    clear_files()


@app.command()
def clipboard():
    message = build_message()
    pyperclip.copy(message)


if __name__ == "__main__":
    app()
