from kirby.db.file_db import get_latest_files
from kirby.util.file_util import rewrite_files, stringify_file_contents
from kirby.instruction.instructions.response_format import RESPONSE_FORMAT_INSTRUCTION
from kirby.instruction.instructions.unit_test import UNIT_TEST_INSTRUCTION
from kirby.ai.ai_client_factory import get_ai_client
from kirby.util.string_util import parse_code_response
import typer


code_app = typer.Typer(
    name="code",
    invoke_without_command=True,
)

ai_client = get_ai_client()


@code_app.command(name="unit-test")
def create_tests():
    for filepath in get_latest_files():
        if filepath.startswith("tests/"):
            continue
        create_test(filepath)


def create_test(filepath: str):
    file_dict = stringify_file_contents(filepath)
    file_contents = ["📁 files:"]
    for fname, content in file_dict.items():
        file_contents.append(f"File: {fname}\n```\n{content}\n```")
    response = ai_client.send_message(
        instructions=[
            RESPONSE_FORMAT_INSTRUCTION,
            UNIT_TEST_INSTRUCTION,
        ],
        files_contents=file_contents,
    )
    file_map = parse_code_response(response)
    rewrite_files(file_map)
