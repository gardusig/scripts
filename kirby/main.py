from dotenv import load_dotenv
from kirby.log import setup_logging
from kirby.cli.app import app


def main():
    load_dotenv()
    setup_logging()
    app()


if __name__ == "__main__":
    main()
