import typer
from scripts.util.cli_util import Source, resolve_text

from scripts.util.clipboard import (
    clear_clipboard,
    append_to_clipboard,
    override_clipboard,
    undo_clipboard,
    clipboard_summary,
)

app = typer.Typer(help="🧠 Clipboard utilities")


@app.command()
def clear():
    """Clear the clipboard and history"""
    clear_clipboard()


@app.command()
def append(
    from_: Source = typer.Option(..., "--from", help="Source of input"),
    message: str = typer.Option(None, help="Message to append"),
    path: str = typer.Option(None, help="Filepath to append content from"),
):
    """Append to clipboard from clipboard, message, or filepath"""
    text = resolve_text(from_, message, path)
    append_to_clipboard(text)


@app.command()
def override(
    from_: Source = typer.Option(..., "--from", help="Source of input"),
    message: str = typer.Option(None, help="Message to override with"),
    path: str = typer.Option(None, help="Filepath to override content from"),
):
    """Override clipboard from clipboard, message, or filepath"""
    text = resolve_text(from_, message, path)
    override_clipboard(text)


@app.command()
def undo():
    """Undo last clipboard change"""
    undo_clipboard()


@app.command()
def summary():
    """Show clipboard preview and history depth"""
    clipboard_summary()


if __name__ == "__main__":
    app()
