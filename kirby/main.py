
from dotenv import load_dotenv
from kirby.cli.app import app
import typer

def main():
    typer.secho('🐛 Starting Kirby CLI…', fg='blue')
    load_dotenv()
    typer.secho('ℹ️  Environment variables loaded.', fg='green')
    app()
    typer.secho('✅ Kirby CLI finished execution.', fg='green')


if __name__ == "__main__":
    main()
