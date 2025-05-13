from __future__ import annotations

import typer
from sasori.db.history_db import HistoryDB
from sasori.util.session_util import create_session_file


class HtmlHistoryStore:
    def __init__(self, name: str, pretty_label: str):
        self.name = name
        self._db: HistoryDB[list[str]] = HistoryDB(
            create_session_file(name),
            empty=[],
            normalise=lambda urls: sorted({url.strip() for url in urls if url.strip()}),
            pretty=lambda urls: (
                f"{pretty_label}:\n" + "\n".join(f"- {url}" for url in urls) or "(none)"
            ),
        )

    def _snap(self) -> list[str]:
        return list(self._db.latest())

    def clear(self) -> None:
        self._db.clear()

    def append(self, url: str) -> None:
        u = url.strip()
        if not u:
            typer.secho("⚠️  Empty URL — nothing added.", fg="yellow")
            return
        urls = self._snap()
        if u in urls:
            typer.secho(f"⚠️  URL already present: {u}", fg="yellow")
            return
        urls.append(u)
        self._db.push(urls)

    def remove(self, url: str) -> None:
        u = url.strip()
        if not u:
            typer.secho("⚠️  Empty URL — nothing removed.", fg="yellow")
            return
        urls = self._snap()
        try:
            urls.remove(u)
        except ValueError:
            typer.secho(f"⚠️  URL not tracked: {u}", fg="yellow")
            return
        self._db.push(urls)

    def undo(self) -> None:
        if self._db.undo():
            typer.secho("↩️ Reverted last change.", fg="green")
        else:
            typer.secho("⚠️  Nothing to undo.", fg="yellow")

    def summary(self) -> str:
        return self._db.summary()

    def latest_set(self) -> set[str]:
        return set(self._db.latest())


# ───── instantiate the HTML store ────────────────────────────

_html_store = HtmlHistoryStore("html_history", "🌐 HTML URLs")


# ───── public API for HTML URLs ───────────────────────────────


def clear_html_urls() -> None:
    _html_store.clear()
    typer.secho("✅ HTML URLs cleared.", fg="green")


def append_html_url(url: str) -> None:
    _html_store.append(url)
    typer.secho(f"✅ HTML URL appended: {url}", fg="green")


def remove_html_url(url: str) -> None:
    _html_store.remove(url)
    typer.secho(f"✅ HTML URL removed: {url}", fg="green")


def undo_html_urls() -> None:
    _html_store.undo()
    typer.secho("✅ Undo completed for HTML URLs.", fg="green")


def summary_html_urls() -> str:
    summary = _html_store.summary()
    return summary


def get_html_urls() -> set[str]:
    urls = _html_store.latest_set()
    return urls
