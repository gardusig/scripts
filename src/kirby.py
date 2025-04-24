from config.log_setup import setup_logging
from dotenv import load_dotenv
from cli.app_cli import app


def main():
    load_dotenv()
    setup_logging()
    app()


if __name__ == "__main__":
    main()
