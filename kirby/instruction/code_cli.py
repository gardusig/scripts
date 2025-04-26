CODE_CLI_INSTRUCTIONS = [
    "For each instruction file in the instructions directory (e.g., `code_cli.json`, `unit_test.json`, `api_contract.json`), extract the filename (without extension) and treat it as a command identifier.",
    "Create a Python function named exactly after the filename (e.g., `def code_cli():`) that will act as the CLI entry point for this instruction set.",
    "Within each function, load the corresponding instruction file and pass its contents to the analysis engine or AI interface.",
    "Ensure the function includes a docstring describing its purpose, derived from the filename and instruction file summary.",
    "Use a CLI framework `typer`, register each of these functions as a command using the filename as the CLI command (e.g., `cli_app.command('code_cli')(code_cli)`).",
]
