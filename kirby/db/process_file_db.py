from kirby.db.file_history_db import FileHistoryStore


_proc_store = FileHistoryStore("processing_history", "🔄 Processing files")


def clear_processing_files() -> None:
    _proc_store.clear()


def append_processing_file(path: str) -> None:
    _proc_store.append(path)


def remove_processing_file(path: str) -> None:
    _proc_store.remove(path)


def undo_processing_files() -> None:
    _proc_store.undo()


def summary_processing_files() -> str:
    return _proc_store.summary()


def get_processing_files() -> set[str]:
    return _proc_store.latest_set()
