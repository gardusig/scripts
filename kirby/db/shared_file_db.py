
from kirby.db.file_history_db import FileHistoryStore
import typer

_shared_store = FileHistoryStore("file_set_history", "📁 Shared files")


def clear_shared_files() -> None:
    typer.secho('🐛 Clearing shared files…', fg='blue')
    _shared_store.clear()
    typer.secho('✅ Shared files cleared.', fg='green')


def append_shared_file(path: str) -> None:
    typer.secho(f'🐛 Appending shared file: {path}', fg='blue')
    _shared_store.append(path)
    typer.secho(f'✅ Shared file appended: {path}', fg='green')


def remove_shared_file(path: str) -> None:
    typer.secho(f'🐛 Removing shared file: {path}', fg='blue')
    _shared_store.remove(path)
    typer.secho(f'✅ Shared file removed: {path}', fg='green')


def undo_shared_files() -> None:
    typer.secho('🐛 Undoing last shared files operation…', fg='blue')
    _shared_store.undo()
    typer.secho('✅ Undo completed for shared files.', fg='green')


def summary_shared_files() -> str:
    typer.secho('🐛 Generating summary of shared files…', fg='blue')
    summary = _shared_store.summary()
    typer.secho('✅ Summary generated for shared files.', fg='green')
    return summary


def get_shared_files() -> set[str]:
    typer.secho('🐛 Fetching latest set of shared files…', fg='blue')
    files = _shared_store.latest_set()
    typer.secho('✅ Latest shared files fetched.', fg='green')
    return files
