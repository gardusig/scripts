import typer
from scripts.cli.file_cli import file_app
from scripts.util.file_util import stringify_file_contents
from scripts.cli.instruction_cli import instruction_app
from scripts.service.ai_interface import AIClient
from scripts.service.openai import OpenAIClient
from scripts.db.instruction_db import get_latest_instruction
from scripts.db.file_db import get_latest_files

app = typer.Typer(help="Main application with subcommands.")
app.add_typer(file_app, name="file",
              help="Manage resources (clipboard).")
app.add_typer(instruction_app, name="instruction",
              help="AI Instruction Analysis.")

ai_client: AIClient = OpenAIClient()


@app.command()
def analyze():
    instructions = get_latest_instruction()
    files = get_latest_files()
    input_text = stringify_file_contents(files)
    result = ai_client.get_response(instructions, input_text)
    print(result)


if __name__ == "__main__":
    app()
