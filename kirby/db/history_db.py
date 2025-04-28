
import json
from contextlib import suppress
from pathlib import Path
from typing import Callable, Generic, List, TypeVar
import typer

T = TypeVar("T")


class HistoryDB(Generic[T]):
    """
    JSON-file-backed stack of snapshots.
    `push()` adds a new snapshot; `undo()` pops the latest one.
    """

    def __init__(
        self,
        file_path: Path,
        *,
        empty: T,
        normalise: Callable[[T], T] | None = None,
        pretty: Callable[[T], str] | None = None,
    ) -> None:
        self._file = file_path
        self._empty = empty
        self._normalise = normalise or (lambda x: x)
        self._pretty = pretty or json.dumps

        # bootstrap file with one empty snapshot
        if not self._file.exists():
            typer.secho(f'ℹ️  Bootstrapping history file: {self._file}', fg='green')
            self._save([self._empty])

    # ───── public API ────────────────────────────────────────────────

    def latest(self) -> T:
        typer.secho(f'ℹ️  Fetching latest snapshot from: {self._file}', fg='green')
        return self._load()[-1]

    def push(self, snapshot: T) -> None:
        typer.secho(f'ℹ️  Pushing new snapshot to history: {self._file}', fg='green')
        history = self._load()
        history.append(self._normalise(snapshot))
        self._save(history)
        typer.secho(f'✅ Snapshot pushed.', fg='green')

    def undo(self) -> bool:
        typer.secho(f'ℹ️  Attempting undo in history: {self._file}', fg='green')
        history = self._load()
        if len(history) <= 1:
            typer.secho('⚠️  No more snapshots to undo.', fg='yellow')
            return False
        history.pop()
        self._save(history)
        typer.secho('✅ Undo successful.', fg='green')
        return True

    def clear(self) -> None:
        typer.secho(f'ℹ️  Clearing history: {self._file}', fg='green')
        self._save([self._empty])
        typer.secho('✅ History cleared.', fg='green')

    def summary(self) -> str:
        typer.secho(f'ℹ️  Generating summary for latest snapshot.', fg='green')
        return self._pretty(self.latest())

    # ───── private helpers ───────────────────────────────────────────

    def _load(self) -> List[T]:
        try:
            with open(self._file, "r", encoding="utf-8") as f:
                typer.secho(f'ℹ️  Loading history from file: {self._file}', fg='green')
                return json.load(f)
        except Exception as e:
            typer.secho(f'⚠️  Failed to load {self._file.name}; resetting. Error: {e}', fg='yellow', err=True)
            return [self._empty]

    def _save(self, history: List[T]) -> None:
        try:
            with open(self._file, "w", encoding="utf-8") as f:
                typer.secho(f'ℹ️  Saving history to file: {self._file}', fg='green')
                json.dump(history, f, indent=2)
                typer.secho(f'✅ History saved.', fg='green')
        except Exception as e:
            typer.secho(f'❌ Failed to save {self._file.name}: {e}', fg='red', err=True)
