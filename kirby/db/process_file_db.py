
from kirby.db.file_history_db import FileHistoryStore
import typer

_proc_store = FileHistoryStore("processing_history", "🔄 Processing files")

def clear_processing_files() -> None:
    typer.secho('🐛 Clearing processing files…', fg='blue')
    _proc_store.clear()
    typer.secho('✅ Processing files cleared.', fg='green')

def append_processing_file(path: str) -> None:
    typer.secho(f'🐛 Appending processing file: {path}', fg='blue')
    _proc_store.append(path)
    typer.secho(f'✅ Processing file appended: {path}', fg='green')

def remove_processing_file(path: str) -> None:
    typer.secho(f'🐛 Removing processing file: {path}', fg='blue')
    _proc_store.remove(path)
    typer.secho(f'✅ Processing file removed: {path}', fg='green')

def undo_processing_files() -> None:
    typer.secho('🐛 Undoing last processing files operation…', fg='blue')
    _proc_store.undo()
    typer.secho('✅ Undo completed for processing files.', fg='green')

def summary_processing_files() -> str:
    typer.secho('🐛 Generating summary of processing files…', fg='blue')
    summary = _proc_store.summary()
    typer.secho('✅ Summary generated for processing files.', fg='green')
    return summary

def get_processing_files() -> set[str]:
    typer.secho('🐛 Fetching latest set of processing files…', fg='blue')
    files = _proc_store.latest_set()
    typer.secho('✅ Latest set of processing files fetched.', fg='green')
    return files
