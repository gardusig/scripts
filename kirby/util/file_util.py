from __future__ import annotations
import os
import subprocess
import typer

from fnmatch import fnmatch
from pathlib import Path
from typing import OrderedDict, Sequence, Union


DEFAULT_IGNORES: tuple[str, ...] = (
    "__pycache__",
    "*.py[co]",
    "*.egg-info",
    ".DS_Store",
    ".git",
    "venv",
    ".env",
    ".pytest_cache",
    ".mypy_cache",
    "LICENSE",
    "*.webp",
    "*.jpe?g",
    "*.gif",
)

# ────────────────────────────────────────────────────────────────────
# ignore helpers
# ────────────────────────────────────────────────────────────────────


def should_ignore(name: str, patterns: Sequence[str] = DEFAULT_IGNORES) -> bool:
    """
    Returns True if `name` (a single path component or filename)
    matches any of the glob patterns.
    """
    return any(fnmatch(name, pat) for pat in patterns)


# ────────────────────────────────────────────────────────────────────
# file discovery
# ────────────────────────────────────────────────────────────────────
def get_all_files(
    root: Union[str, Path],
    ignore_patterns: Sequence[str] = DEFAULT_IGNORES,
) -> list[str]:
    root = Path(root).expanduser().resolve()

    if not root.exists():
        typer.echo(f"⛔️  Path does not exist: {root}", err=True)
        return []

    if root.is_file():
        return [str(root)]

    results: list[str] = []

    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if not should_ignore(d, ignore_patterns)]

        for fname in filenames:
            if should_ignore(fname, ignore_patterns):
                continue
            full = Path(dirpath) / fname
            results.append(str(full))

    return results


# ────────────────────────────────────────────────────────────────────
# file <-> string helpers
# ────────────────────────────────────────────────────────────────────
_MAX_MB = 1


def stringify_file_contents(
    files: Union[list[str], list[Path]], label: str = "Files"
) -> list[str]:
    """
    Read files into memory (≤ 1 MiB each). Returns {path: contents}.
    """
    if len(files) == 0:
        return []
    string_list = [f"📁 {label}:"]
    for filepath in files:
        try:
            text = stringify_file_content(filepath)
            if text != "":
                string_list.append(f"File: {filepath}\n```\n{text}\n```")
        except Exception as err:
            print("Error reading %s: %s", filepath, err)
    print("📄 Read %d file(s)", len(string_list) - 1)
    return string_list


def stringify_file_content(path: Union[str, Path]) -> str:
    try:
        if isinstance(path, str):
            path = Path(path)
        if path.stat().st_size > _MAX_MB * 1024 * 1024:
            print("⚠️  %s bigger than %d MB; skipped.", path, _MAX_MB)
            return ""
        text = path.read_text(encoding="utf-8", errors="replace").strip()
        print("📄 Read file(s) %s", path)
        return text
    except Exception as err:
        print("Error reading %s: %s", str(path), err)
        return ""


# ────────────────────────────────────────────────────────────────────
# write helpers
# ────────────────────────────────────────────────────────────────────


def rewrite_files(
    files: OrderedDict[str, str],
    force: bool = False,
) -> None:
    for path, content in files.items():
        if not force:
            if not typer.confirm(f"Overwrite {path}?"):
                typer.secho(f"✋  Skipped {path}", fg="cyan")
                continue
        rewrite_file(path, content)
        typer.secho(f"✅ Wrote {path}", fg="green")


def rewrite_file(file_path: str, content: str) -> None:
    """
    Overwrite `file_path` with `content`, creating parent dirs as needed.
    """

    path = Path(file_path).expanduser()
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        print("✅ Rewrote %s", path)
    except Exception as err:
        print("❌ Error writing %s: %s", path, err)


def find_repo_root() -> Path:
    """
    Try to find the git top-level; if that fails, fall back to cwd().
    """
    try:
        git_root = (
            subprocess.check_output(
                ["git", "rev-parse", "--show-toplevel"], stderr=subprocess.DEVNULL
            )
            .decode()
            .strip()
        )
        return Path(git_root)
    except Exception:
        return Path.cwd()


def source_to_test_path(
    src: Path,
    repo_root: Path,
    tests_dir: str = "tests",
) -> Path:
    """
    Given e.g. /…/kirbyCLI/kirby/cli/app.py
    produce  /…/kirbyCLI/tests/cli/test_app.py
    """
    rel = src.resolve().relative_to(repo_root)

    parts = rel.parts
    if len(parts) < 2:
        raise Exception("len(parts) < 2")
    relative_without_pkg = Path(*parts[1:])

    test_name = f"test_{relative_without_pkg.stem}{relative_without_pkg.suffix}"
    return repo_root / tests_dir / relative_without_pkg.parent / test_name
