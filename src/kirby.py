# from db.file_db import clear_files, summary_files
# from logging_setup import setup_logging
# import typer
# from cli.file_cli import file_app
# from util.ai_util import get_ai_client, parse_code_response, send_message
# from cli.instruction_cli import instruction_app
# from dotenv import load_dotenv
# import pyperclip


# def build_app() -> typer.Typer:
#     app = typer.Typer(help="Main application with subcommands.")
#     app.add_typer(file_app, name="file", help="Manage resources (clipboard).")
#     app.add_typer(instruction_app, name="instruction", help="AI Instruction Analysis.")
#     return app


# load_dotenv()
# setup_logging()
# app = build_app()


# @app.command(help="Clear all instructions and files")
# def clear():
#     clear_instructions()
#     clear_files()


# @app.command(help="Preview instructions and files")
# def preview():
#     print(summary_instruction())
#     print(summary_files())


# @app.command(help="Append an instruction")
# def eat(string: str = typer.Argument(..., help="Instruction to append")):
#     if not string.strip():
#         print("⚠️ Empty instruction provided.")
#         raise typer.Exit(code=1)
#     append_instruction(string)


# @app.command(help="Append instruction from clipboard")
# def eat_clipboard():
#     string = pyperclip.paste()
#     if not string.strip():
#         print("⚠️ Empty instruction provided.")
#         raise typer.Exit(code=1)
#     append_instruction(string)


# @app.command(help="?")
# def copy():
#     string = '\n'.join([summary_instruction(), summary_files()])
#     pyperclip.copy(string)


# @app.command(help="Response JSON format analysis")
# def ask():
#     ai_client = get_ai_client()
#     response = send_message(ai_client)
#     print(response)


# @app.command(help="?")
# def unit_test():
#     instructions = load_instructions([
#         "unit_testing.json",
#         "response/response_json_format.json",
#     ])
#     ai_client = get_ai_client()
#     response = send_message(ai_client, instructions)
#     file_map = parse_code_response(response)
#     rewrite_files(file_map, ['tests'])


# if __name__ == "__main__":
#     app()
