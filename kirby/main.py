from dotenv import load_dotenv
from kirby.cli.app import app
import typer


def main():
    load_dotenv()
    app()
    typer.secho("☑️  Kirby CLI finished execution.", fg="green")


if __name__ == "__main__":
    main()
