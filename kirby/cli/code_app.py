
from pathlib import Path

from kirby.instruction.instructions.typer_log import TYPER_LOG_INSTRUCTION
from kirby.instruction.instructions.mypy import MYPY_INSTRUCTION
from kirby.instruction.instructions.readme import README_INSTRUCTION
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
    typer.secho('🐛 Starting unit-test command…', fg='blue')
    repo_root = find_repo_root()
    for filepath in get_processing_files():
        try:
            typer.secho(f'ℹ️ Creating test for {filepath}', fg='green')
            create_test(force, filepath, repo_root)
            typer.secho(f'✅ Test created for {filepath}', fg='green')
        except Exception as e:
            typer.secho(
                f"⚠️  Failed to create test for {filepath!r}: {e}",
                fg="yellow",
                err=True,
            )
    typer.secho('✅ Finished unit-test command.', fg='green')

def create_test(force: bool, filepath: str, repo_root: Path):
    if filepath.endswith("__init__.py"):
        typer.secho(f'⚠️  Skipping __init__.py file: {filepath}', fg='yellow')
        return
    src = Path(filepath)
    dest = source_to_test_path(src, repo_root)
    typer.secho(f'ℹ️ Sending request to AI client for {filepath}', fg='green')
    ai_client = get_ai_client()
    response = ai_client.send_message(
        instructions=[
            RESPONSE_FORMAT_INSTRUCTION,
            UNIT_TEST_INSTRUCTION,
        ],
        prompt_files=[src, dest],
        final_prompt=f'Focus only on creating a test for "{filepath}"',
    )
    typer.secho(f'ℹ️ Parsing AI response for {filepath}', fg='green')
    file_map = parse_code_response(response)
    typer.secho(f'ℹ️ Rewriting files for {filepath}', fg='green')
    rewrite_files(files=file_map, force=force)
    typer.secho(f'✅ Finished processing {filepath}', fg='green')

@code_app.command("readme")
def create_readme(
    force: bool = typer.Option(
        False,
        "--force",
        help="Skip prompts and overwrite tests unconditionally.",
    ),
):
    typer.secho('🐛 Starting readme command…', fg='blue')
    ai_client = get_ai_client()
    typer.secho('ℹ️ Sending request to AI client for README.md', fg='green')
    response = ai_client.send_message(
        instructions=[
            RESPONSE_FORMAT_INSTRUCTION,
            README_INSTRUCTION,
        ],
        prompt_files=["./README.md"],
        final_prompt='Focus only on creating a single "README.md"',
    )
    typer.secho('ℹ️ Parsing AI response for README.md', fg='green')
    file_map = parse_code_response(response)
    typer.secho('ℹ️ Rewriting README.md', fg='green')
    rewrite_files(files=file_map, force=force)
    typer.secho('✅ Finished readme command.', fg='green')

@code_app.command("mypy")
def fix_mypy_errors(
    force: bool = typer.Option(
        False,
        "--force",
        help="Skip prompts and overwrite tests unconditionally.",
    ),
):
    typer.secho('🐛 Starting mypy command…', fg='blue')
    ai_client = get_ai_client()
    for filepath in get_processing_files():
        try:
            typer.secho(f'ℹ️ Sending request to AI client for mypy fixes in {filepath}', fg='green')
            response = ai_client.send_message(
                instructions=[
                    RESPONSE_FORMAT_INSTRUCTION,
                    MYPY_INSTRUCTION,
                ],
                prompt_files=[filepath],
                final_prompt=f"Focus on fixing only mypy errors related to {filepath}",
            )
            typer.secho(f'ℹ️ Parsing AI response for {filepath}', fg='green')
            file_map = parse_code_response(response)
            typer.secho(f'ℹ️ Rewriting files for {filepath}', fg='green')
            rewrite_files(files=file_map, force=force)
            typer.secho(f'✅ Mypy errors fixed for {filepath}', fg='green')
        except Exception as e:
            typer.secho(
                f"⚠️  Failed to fix mypy errors for {filepath!r}: {e}",
                fg="yellow",
                err=True,
            )
    typer.secho('✅ Finished mypy command.', fg='green')

@code_app.command("typer-log")
def improve_typer_logs(
    force: bool = typer.Option(
        False,
        "--force",
        help="Skip prompts and overwrite tests unconditionally.",
    ),
):
    typer.secho('🐛 Starting typer-log command…', fg='blue')
    ai_client = get_ai_client()
    for filepath in get_processing_files():
        if filepath.endswith("__init__.py"):
            typer.secho(f'⚠️  Skipping __init__.py file: {filepath}', fg='yellow')
            continue
        try:
            typer.secho(f'ℹ️ Sending request to AI client to improve typer logs in {filepath}', fg='green')
            response = ai_client.send_message(
                instructions=[
                    RESPONSE_FORMAT_INSTRUCTION,
                    TYPER_LOG_INSTRUCTION,
                ],
                prompt_files=[filepath],
                final_prompt=f"Focus on only {filepath}",
            )
            typer.secho(f'ℹ️ Parsing AI response for {filepath}', fg='green')
            file_map = parse_code_response(response)
            typer.secho(f'ℹ️ Rewriting files for {filepath}', fg='green')
            rewrite_files(files=file_map, force=force)
            typer.secho(f'✅ Typer logs improved for {filepath}', fg='green')
        except Exception as e:
            typer.secho(
                f"⚠️  Failed to improve typer logs for {filepath!r}: {e}",
                fg="yellow",
                err=True,
            )
    typer.secho('✅ Finished typer-log command.', fg='green')
