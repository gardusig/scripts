import typer
from util.instruction_util import load_instructions
from util.ai_util import send_message
from util.cli_util import get_ai_client

code_app = typer.Typer(help="📁 Code management CLI")


@code_app.command()
def evaluate():
    instructions = load_instructions("./resources/instructions/code.json")
    if not instructions:
        print("⚠️ No instructions were loaded.")
        return
    ai_client = get_ai_client()
    response = send_message(ai_client, instructions)
    print(response)
