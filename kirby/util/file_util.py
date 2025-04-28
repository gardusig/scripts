
from __future__ import annotations
import os
import subprocess
import typer

from fnmatch import fnmatch
from pathlib import Path
from typing import OrderedDict, Sequence


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
    root: str | Path,
    ignore_patterns: Sequence[str] = DEFAULT_IGNORES,
) -> list[str]:
    root = Path(root).expanduser().resolve()

    if not root.exists():
        typer.secho(f"❌  Path does not exist: {root}", fg="red", err=True)
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
    files: list[str] | list[Path], label: str = "Files"
) -> list[str]:
    """
    Read files into memory (≤ 1 MiB each). Returns {path: contents}.
    """
    if len(files) == 0:
        return []
    typer.secho(f'🐛 Starting to read {len(files)} file(s)…', fg='blue')
    string_list = [f"📁 {label}:"]
    for filepath in files:
        try:
            text = stringify_file_content(filepath)
            if text != "":
                string_list.append(f"File: {filepath}\n```\n{text}\n```")
        except Exception as err:
            typer.secho(f"❌  Error reading {filepath}: {err}", fg="red", err=True)
    typer.secho(f"📄 Read {len(string_list) - 1} file(s)", fg="green")
    return string_list


def stringify_file_content(path: str | Path) -> str:
    try:
        if isinstance(path, str):
            path = Path(path)
        if path.stat().st_size > _MAX_MB * 1024 * 1024:
            typer.secho(f"⚠️  {path} bigger than {_MAX_MB} MB; skipped.", fg="yellow")
            return ""
        text = path.read_text(encoding="utf-8", errors="replace").strip()
        typer.secho(f"📄 Read file(s) {path}", fg="green")
        return text
    except Exception as err:
        typer.secho(f"❌  Error reading {str(path)}: {err}", fg="red", err=True)
        return ""


# ────────────────────────────────────────────────────────────────────
# write helpers
# ────────────────────────────────────────────────────────────────────


def rewrite_files(
    files: OrderedDict[str, str],
    force: bool = False,
) -> None:
    typer.secho(f'🐛 Starting rewrite of {len(files)} file(s)…', fg='blue')
    for path, content in files.items():
        if not force:
            if not typer.confirm(f"Overwrite {path}?"):
                typer.secho(f"✋  Skipped {path}", fg="cyan")
                continue
        rewrite_file(path, content)
        typer.secho(f"✅ Wrote {path}", fg="green")
    typer.secho('✅ All file rewrites complete.', fg='green')


def rewrite_file(file_path: str, content: str) -> None:
    """
    Overwrite `file_path` with `content`, creating parent dirs as needed.
    """

    path = Path(file_path).expanduser()
    try:
        typer.secho(f'🐛 Writing file: {path}', fg='blue')
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        typer.secho(f"✅ Rewrote {path}", fg="green")
    except Exception as err:
        typer.secho(f"❌ Error writing {path}: {err}", fg="red", err=True)


def find_repo_root() -> Path:
    """
    Try to find the git top-level; if that fails, fall back to cwd().
    """
    try:
        typer.secho('🐛 Attempting to find git repo root…', fg='blue')
        git_root = (
            subprocess.check_output(
                ["git", "rev-parse", "--show-toplevel"], stderr=subprocess.DEVNULL
            )
            .decode()
            .strip()
        )
        typer.secho(f'✅ Found git repo root: {git_root}', fg='green')
        return Path(git_root)
    except Exception as err:
        typer.secho(f"⚠️  Could not find git repo root, using cwd: {err}", fg="yellow")
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
        typer.secho("❌  Path too short to determine test path.", fg="red", err=True)
        raise Exception("len(parts) < 2")
    relative_without_pkg = Path(*parts[1:])

    test_name = f"test_{relative_without_pkg.stem}{relative_without_pkg.suffix}"
    test_path = repo_root / tests_dir / relative_without_pkg.parent / test_name
    typer.secho(f"ℹ️  Source file {src} maps to test path {test_path}", fg="green")
    return test_path
