from util.file_util import stringify_file_contents
from db.instruction_db import get_latest_instruction
from db.file_db import get_latest_files
from service.ai_interface import AIClient


def send_message(ai_client: AIClient, instructions: str = None, files: set[str] = None):
    instructions = build_instructions(instructions)
    context = build_context(files)
    return ai_client.get_response(instructions, context)


def build_instructions(instructions: str = None) -> str:
    latest_instruction = get_latest_instruction()
    return f'{instructions}"\n"' if instructions else '' + latest_instruction


def build_context(files: set[str] = None) -> str:
    if not files:
        files = set()
    for file in get_latest_files():
        files.add(file)
    return stringify_file_contents(files)
