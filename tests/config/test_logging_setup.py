import logging

import pytest
from rich.logging import RichHandler

from kirby.config import log_setup


# ───── helpers ────────────────────────────────────────────────────────────────
@pytest.fixture(autouse=True)
def isolated_logging():
    """Clear all handlers between tests to avoid bleed-over."""
    yield
    logging.shutdown()
    for lg in logging.root.manager.loggerDict.values():
        if isinstance(lg, logging.Logger):
            lg.handlers.clear()
    logging.getLogger().handlers.clear()


# ───── tests ─────────────────────────────────────────────────────────────────
@pytest.mark.parametrize("lvl", ["INFO", "WARNING"])
def test_root_has_richhandler(tmp_path, monkeypatch, lvl):
    monkeypatch.setattr(log_setup, "LOG_DIR", tmp_path)
    log_setup.setup_logging(lvl)

    root = logging.getLogger()
    assert any(isinstance(h, RichHandler) for h in root.handlers)


def test_get_log_file_handler(tmp_path, monkeypatch, caplog):
    monkeypatch.setattr(log_setup, "LOG_DIR", tmp_path)

    handler = log_setup.get_log_file_handler("my.module")
    assert isinstance(handler, logging.Handler)

    logger = logging.getLogger("my.module")
    logger.addHandler(handler)
    logger.setLevel("DEBUG")

    with caplog.at_level("DEBUG", logger="my.module"):
        logger.debug("hello world")

    assert "hello world" in caplog.text

    # tidy-up
    logger.removeHandler(handler)
    handler.close()
