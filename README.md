
# Kirby CLI 🧰

Welcome to **Kirby CLI** – your friendly, pink command-line assistant for wrangling prompts, files, and AI-powered workflows! Kirby CLI helps you manage prompt histories, file queues, and more, so you can focus on what matters: getting things done (and maybe having a little fun along the way).

<div align="center">
  <img src="./media/kirby-eat.webp" alt="kirby-eat" height="200" />
  <img src="./media/kirby-work.gif" alt="kirby-work" height="200" />
</div>

## Table of Contents 📚

- [Kirby CLI 🧰](#kirby-cli-)
  - [Table of Contents 📚](#table-of-contents-)
  - [Features ✨](#features-)
  - [Installation \& Setup 🚀](#installation--setup-)
    - [Install Python (macOS example)](#install-python-macos-example)
    - [Set up Kirby CLI](#set-up-kirby-cli)
  - [Environment Configuration 🔐](#environment-configuration-)
  - [CLI Usage 🛠️](#cli-usage-️)
    - [Prompt Management 💡](#prompt-management-)
    - [File Management 📁](#file-management-)
    - [Processing Queue ⚙️](#processing-queue-️)
    - [Code Generation 🤖](#code-generation-)
    - [Global Commands 🌎](#global-commands-)
  - [Example Workflow 🔄](#example-workflow-)
  - [Contributing 🤝](#contributing-)
  - [Questions? Bugs? 💬](#questions-bugs-)

## Features ✨

- **Prompt history management**: Add, remove, list, undo, and clear prompts for your AI workflows.
- **File queueing**: Track files to share or process with AI, with full undo/clear support.
- **Clipboard integration**: Instantly add prompts from your clipboard.
- **Code generation**: Auto-generate unit tests or README files using your favorite LLM.
- **Batch operations**: Clear or show all tracked items in one go.
- **Undo support**: Oops? Undo your last action for prompts, files, or processing queues.

## Installation & Setup 🚀

### Install Python (macOS example)

```bash
brew install python
python3 -m pip install --upgrade pip
python3 -m pip install virtualenv
```

### Set up Kirby CLI

```bash
cd kirbyCLI
python3 -m venv venv
source venv/bin/activate
pip install -e .
```

For development tools:

```bash
pip install -e ".[dev]"
```

## Environment Configuration 🔐

Kirby CLI uses OpenAI (or other LLM) APIs. Set your API key in a `.env` file at the project root:

```env
OPENAI_API_KEY=sk-...
```

Or export it in your shell:

```bash
export OPENAI_API_KEY=sk-...
```

## CLI Usage 🛠️

Invoke Kirby CLI with:

```bash
python -m kirby [COMMANDS...]
```

Or, if installed as a script:

```bash
kirby [COMMANDS...]
```

### Prompt Management 💡

Manage your prompt history for AI interactions:

- **Add a prompt:**
  ```bash
  python -m kirby prompt add "Summarize the following text"
  ```

- **Remove a prompt:**
  ```bash
  python -m kirby prompt remove "Summarize the following text"
  ```

- **List all prompts:**
  ```bash
  python -m kirby prompt list
  ```

- **Undo last prompt change:**
  ```bash
  python -m kirby prompt undo
  ```

- **Clear all prompts:**
  ```bash
  python -m kirby prompt clear
  ```

- **Add prompt from clipboard:**
  ```bash
  python -m kirby clipboard
  ```

### File Management 📁

Track files you want to share with your LLM:

- **Add a file or directory:**
  ```bash
  python -m kirby file add path/to/file_or_folder
  ```

- **Remove a file:**
  ```bash
  python -m kirby file remove path/to/file
  ```

- **List shared files:**
  ```bash
  python -m kirby file list
  ```

- **Undo last file change:**
  ```bash
  python -m kirby file undo
  ```

- **Clear all shared files:**
  ```bash
  python -m kirby file clear
  ```

### Processing Queue ⚙️

Queue files for processing (e.g., for test generation):

- **Add file(s) to process:**
  ```bash
  python -m kirby process add path/to/file_or_folder
  ```

- **Remove file from process queue:**
  ```bash
  python -m kirby process remove path/to/file
  ```

- **List processing files:**
  ```bash
  python -m kirby process list
  ```

- **Undo last processing change:**
  ```bash
  python -m kirby process undo
  ```

- **Clear processing queue:**
  ```bash
  python -m kirby process clear
  ```

### Code Generation 🤖

Let Kirby and your LLM do the heavy lifting:

- **Generate unit tests for queued files:**
  ```bash
  python -m kirby code unit-test
  ```

- **Generate a README.md for your project:**
  ```bash
  python -m kirby code readme
  ```

  Add `--force` to overwrite existing files without confirmation.

### Global Commands 🌎

- **Show all prompts, shared files, and processing files:**
  ```bash
  python -m kirby show
  ```

- **Clear everything (prompts, shared files, processing files):**
  ```bash
  python -m kirby clear
  ```

## Example Workflow 🔄

Let's say you want to generate tests for your codebase:

```bash
# Add files to process
python -m kirby process add src/my_module.py

# Add a prompt for the LLM
python -m kirby prompt add "Write comprehensive unit tests."

# Generate tests
python -m kirby code unit-test

# Review the generated tests in your project!
```

Or, to quickly create a README:

```bash
python -m kirby code readme
```

## Contributing 🤝

Kirby loves new friends! If you'd like to contribute:

1. Fork the repo 🍴
2. Create a new branch: `git checkout -b feature/my-feature`
3. Make your changes and add tests
4. Submit a pull request 🚀

## Questions? Bugs? 💬

Open an issue or start a discussion on the [GitHub repo](https://github.com/your-org/kirbyCLI). Kirby is always hungry for feedback!

<div align="center">
  <img src="./media/kirby-cook.gif" alt="kirby-cook" height="100" />
  <br>
  <b>Kirby CLI – Eat. Cook. Automate. Repeat.</b>
</div>
