from kirby.db.file_history_db import FileHistoryStore


_shared_store = FileHistoryStore("file_set_history", "📁 Shared files")


def clear_shared_files() -> None:
    _shared_store.clear()


def append_shared_file(path: str) -> None:
    _shared_store.append(path)


def remove_shared_file(path: str) -> None:
    _shared_store.remove(path)


def undo_shared_files() -> None:
    _shared_store.undo()


def summary_shared_files() -> str:
    return _shared_store.summary()


def get_shared_files() -> set[str]:
    return _shared_store.latest_set()
