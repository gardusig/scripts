import typer
from sasori.db.html_db import (
    append_html_url,
    clear_html_urls,
    remove_html_url,
    summary_html_urls,
    undo_html_urls,
)

html_app = typer.Typer(name="html", help="Manage your HTML URL history")


@html_app.command("add")
def add_url(url: str = typer.Argument(..., help="URL to append")):
    """Append a URL to the HTML history."""
    try:
        append_html_url(url)
    except Exception as e:
        typer.secho(f"❌ Failed to add URL: {e}", fg="red", err=True)
        raise


@html_app.command("remove")
def remove_url(url: str = typer.Argument(..., help="URL to remove")):
    """Remove a URL from the HTML history."""
    try:
        remove_html_url(url)
    except Exception as e:
        typer.secho(f"❌ Failed to remove URL: {e}", fg="red", err=True)
        raise


@html_app.command("clear")
def clear_urls():
    """Clear the entire HTML URL history."""
    try:
        clear_html_urls()
    except Exception as e:
        typer.secho(f"❌ Failed to clear HTML URL history: {e}", fg="red", err=True)
        raise


@html_app.command("list")
def list_urls():
    """Show a summary of your HTML URL history."""
    try:
        summary = summary_html_urls()
        typer.echo(summary)
    except Exception as e:
        typer.secho(f"❌ Failed to list HTML URL history: {e}", fg="red", err=True)
        raise


@html_app.command("undo")
def undo_url():
    """Undo the last change to your HTML URL history."""
    try:
        undo_html_urls()
    except Exception as e:
        typer.secho(f"❌ Failed to undo last change: {e}", fg="red", err=True)
        raise
