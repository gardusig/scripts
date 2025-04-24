import logging
import logging.handlers

from logging_setup import get_log_file_handler, setup_logging
import logging_setup


def test_root_has_richhandler(tmp_path, monkeypatch):
    # point LOG_DIR at a temporary path and make sure it exists
    monkeypatch.setattr("logging_setup.LOG_DIR", tmp_path)
    tmp_path.mkdir(parents=True, exist_ok=True)

    setup_logging("INFO")

    root = logging.getLogger()
    assert any(
        h.__class__.__name__ == "RichHandler" for h in root.handlers
    ), "RichHandler missing from root logger"


def test_get_log_file_handler(tmp_path, monkeypatch):
    monkeypatch.setattr("logging_setup.LOG_DIR", tmp_path)
    tmp_path.mkdir(exist_ok=True, parents=True)

    setup_logging(level="DEBUG")
    handler = get_log_file_handler("my.module")

    logger = logging.getLogger("my.module")
    logger.addHandler(handler)
    logger.debug("hello world")

    handler.flush()
    log_file = tmp_path / "my.module.log"
    assert log_file.exists()
    assert "hello world" in log_file.read_text()


def test_rotating_handler_attrs(tmp_path, monkeypatch):
    monkeypatch.setattr("logging_setup.LOG_DIR", tmp_path)

    handler = get_log_file_handler("bar")
    assert isinstance(handler, logging.handlers.RotatingFileHandler)
    assert handler.maxBytes == 2_000_000
    assert handler.backupCount == 3


def test_plain_formatter_pattern():
    plain = logging_setup.logging.Formatter(
        "%(asctime)s  %(levelname)-8s  %(name)s: %(message)s"
    )
    record = logging.LogRecord(
        name="plain.test", level=logging.INFO, pathname=__file__,
        lineno=1, msg="hello", args=(), exc_info=None
    )
    formatted = plain.format(record)
    assert "plain.test: hello" in formatted
