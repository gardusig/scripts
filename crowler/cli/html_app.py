import typer
from crowler.cli.app_factory import create_crud_app
from crowler.db.html_db import (
    append_html_url,
    clear_html_urls,
    get_html_urls,
    remove_html_url,
    summary_html_urls,
    undo_html_urls,
)
from crowler.util.html_util import extract_html_data

html_app = create_crud_app(
    name="html",
    help_text="Manage your HTML URL history",
    add_fn=append_html_url,
    remove_fn=remove_html_url,
    clear_fn=clear_html_urls,
    list_fn=summary_html_urls,
    undo_fn=undo_html_urls,
    add_arg_name="link",
    add_arg_help="Link to append",
    remove_arg_name="link",
    remove_arg_help="Link to remove",
)


@html_app.command("parse")
def parse_urls():
    """Undo the last change to your HTML URL history."""
    for url in get_html_urls():
        try:
            html_data = extract_html_data(url)
            print(html_data)
        except Exception as e:
            typer.secho(f"❌ Failed to undo last change: {e}", fg="red", err=True)
            raise
