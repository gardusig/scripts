from pathlib import Path

from kirby.db.process_file_db import get_processing_files

from kirby.util.file_util import find_repo_root, rewrite_files, source_to_test_path
from kirby.instruction.instructions.response_format import RESPONSE_FORMAT_INSTRUCTION
from kirby.instruction.instructions.unit_test import UNIT_TEST_INSTRUCTION
from kirby.ai.ai_client_factory import get_ai_client
from kirby.util.string_util import parse_code_response
import typer


code_app = typer.Typer(
    name="code",
    invoke_without_command=True,
)


@code_app.command("unit-test")
def create_tests(
    force: bool = typer.Option(
        False,
        "--force",
        help="Skip prompts and overwrite tests unconditionally.",
    ),
):
    repo_root = find_repo_root()
    for filepath in get_processing_files():
        try:
            create_test(force, filepath, repo_root)
        except Exception as e:
            typer.secho(
                f"⚠️  Failed to create test for {filepath!r}: {e}",
                fg="yellow",
            )


def create_test(force: bool, filepath: str, repo_root: Path):
    if filepath.endswith("__init__.py"):
        return
    src = Path(filepath)
    dest = source_to_test_path(src, repo_root)
    ai_client = get_ai_client()
    response = ai_client.send_message(
        instructions=[
            RESPONSE_FORMAT_INSTRUCTION,
            UNIT_TEST_INSTRUCTION,
        ],
        prompt_files=[src, dest],
        final_prompt=f'Focus only on creating a test for "{filepath}"',
    )
    file_map = parse_code_response(response)
    rewrite_files(files=file_map, force=force)
