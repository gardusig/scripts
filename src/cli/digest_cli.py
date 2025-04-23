import typer
from util.ai_util import get_ai_client, handle_code_change_response, send_message
from util.file_util import load_instructions


digest_app = typer.Typer(help="📁 Code management CLI")


@digest_app.command(help="Review the repository")
def repository_review():
    instructions = load_instructions([
        "code/code_standards.json",
        "repository_review.json",
    ])
    ai_client = get_ai_client()
    response = send_message(ai_client, instructions)
    print(response)


@digest_app.command(help="Comprehensive code review")
def code_review():
    instructions = load_instructions([
        "code/code_standards.json",
        "code/code_review.json",
        "response/response_json_format.json",
    ])
    ai_client = get_ai_client()
    response = send_message(ai_client, instructions)
    handle_code_change_response(response)


@digest_app.command(help="Basic code analysis")
def code_analysis():
    instructions = load_instructions([
        "code/code_standards.json",
        "response/response_json_format.json",
    ])
    ai_client = get_ai_client()
    response = send_message(ai_client, instructions)
    handle_code_change_response(response)


@digest_app.command(help="CLI code analysis")
def cli_analysis():
    instructions = load_instructions([
        "code/code_standards.json",
        "response/response_json_format.json",
    ])
    ai_client = get_ai_client()
    response = send_message(ai_client, instructions)
    handle_code_change_response(response)


@digest_app.command(help="CLI code analysis")
def code_cli():
    instructions = load_instructions([
        "code/code_cli.json",
        "response/response_json_format.json",
    ])
    ai_client = get_ai_client()
    response = send_message(ai_client, instructions)
    handle_code_change_response(response)


@digest_app.command(help="CLI code analysis")
def instruction():
    instructions = load_instructions([
        "instruction_review.json",
        "response/response_json_format.json",
    ])
    ai_client = get_ai_client()
    response = send_message(ai_client, instructions)
    handle_code_change_response(response)
