import typer
from cli.file_cli import file_app
from util.cli_util import get_ai_client
from util.ai_util import send_message
from cli.instruction_cli import instruction_app
from dotenv import load_dotenv
from db.instruction_db import clear_instructions
from db.file_db import clear_files

app = typer.Typer(help="Main application with subcommands.")
app.add_typer(file_app, name="file",
              help="Manage resources (clipboard).")
app.add_typer(instruction_app, name="instruction",
              help="AI Instruction Analysis.")

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


if __name__ == "__main__":
    app()
