
# Sasori 🧰

Welcome to **Sasori** – command-line toolkit for managing prompts, files, and AI-powered workflows! Sasori helps you organize prompt histories, file queues, and code-gen tasks, so you can focus on what matters: getting things done (with a sprinkle of fun).

<div align="center">
  <img src="https://raw.githubusercontent.com/gardusig/sasori-cli/main/media/sasori.png" alt="eat" height="200" />
</div>

## 📚 Table of Contents

- [Sasori 🧰](#sasori-)
  - [📚 Table of Contents](#-table-of-contents)
  - [✨ Features](#-features)
  - [🔄 Example Workflow](#-example-workflow)
  - [🚀 Installation \& Setup](#-installation--setup)
    - [macOS: Python \& Homebrew](#macos-python--homebrew)
    - [Project Setup](#project-setup)
  - [🔐 Environment Configuration](#-environment-configuration)
  - [🛠️ CLI Usage](#️-cli-usage)
    - [💡 Prompt Management](#-prompt-management)
    - [📁 File Management](#-file-management)
    - [⚙️ Processing Queue](#️-processing-queue)
    - [🤖 Code Generation](#-code-generation)
    - [🌎 Global Commands](#-global-commands)

## ✨ Features

- **Prompt history management:** Add, remove, list, undo, and clear prompts for your AI workflows.
- **File queueing:** Track files to share or process with AI, with full undo/clear support.
- **Clipboard integration:** Instantly add prompts from your clipboard.
- **Code generation:** Auto-generate unit tests or README files using your favorite LLM.
- **Batch operations:** Clear or show all tracked items in one go.
- **Undo support:** Oops? Undo your last action for prompts, files, or processing queues.

## 🔄 Example Workflow

Let's say you want to generate tests for your codebase:

```
# Add files to process
sasori process add src/my_module.py

# Add a prompt for the LLM
sasori prompt add "Write comprehensive unit tests."

# Generate tests
sasori code unit-test

# Review the generated tests in your project!
```

Or, to quickly create a README:

```
sasori code readme
```

## 🚀 Installation & Setup

### macOS: Python & Homebrew

```bash
brew install python
python3 -m pip install --upgrade pip
python3 -m pip install virtualenv
```

### Project Setup

Clone and set up your environment:

```bash
git clone https://github.com/gardusig/sasori-cli.git
cd sasori-cli
python3 -m venv venv
source venv/bin/activate
pip install -e .
pip install -e ".[dev]"
```

For development tools:

```bash
pip install -e ".[dev]"
```

## 🔐 Environment Configuration

Sasori uses OpenAI (or other LLM) APIs. Set your API key in a `.env` file at the project root:

```env
OPENAI_API_KEY=sk-...
```

Or export it in your shell:

```bash
export OPENAI_API_KEY=sk-...
```

## 🛠️ CLI Usage

Invoke Sasori CLI with:

```bash
python -m sasori [COMMANDS...]
```

Or, if installed as a script:

```bash
sasori [COMMANDS...]
```

### 💡 Prompt Management

Manage your prompt history for AI interactions:

- **Add a prompt:**
  ```
  sasori prompt add "Summarize the following text"
  ```

- **Remove a prompt:**
  ```
  sasori prompt remove "Summarize the following text"
  ```

- **List all prompts:**
  ```
  sasori prompt list
  ```

- **Undo last prompt change:**
  ```
  sasori prompt undo
  ```

- **Clear all prompts:**
  ```
  sasori prompt clear
  ```

- **Add prompt from clipboard:**
  ```
  sasori clipboard
  ```

### 📁 File Management

Track files you want to share with your LLM:

- **Add a file or directory:**
  ```
  sasori file add path/to/file_or_folder
  ```

- **Remove a file:**
  ```
  sasori file remove path/to/file
  ```

- **List shared files:**
  ```
  sasori file list
  ```

- **Undo last file change:**
  ```
  sasori file undo
  ```

- **Clear all shared files:**
  ```
  sasori file clear
  ```

### ⚙️ Processing Queue

Queue files for processing (e.g., for test generation):

- **Add file(s) to process:**
  ```
  sasori process add path/to/file_or_folder
  ```

- **Remove file from process queue:**
  ```
  sasori process remove path/to/file
  ```

- **List processing files:**
  ```
  sasori process list
  ```

- **Undo last processing change:**
  ```
  sasori process undo
  ```

- **Clear processing queue:**
  ```
  sasori process clear
  ```

### 🤖 Code Generation

Let Sasori and your LLM do the heavy lifting:

- **Generate unit tests for queued files:**
  ```
  sasori code unit-test
  ```

- **Generate a README.md for your project:**
  ```
  sasori code readme
  ```

  Add `--force` to overwrite existing files without confirmation.

### 🌎 Global Commands

- **Show all prompts, shared files, and processing files:**
  ```
  sasori show
  ```

- **Clear everything (prompts, shared files, processing files):**
  ```
  sasori clear
  ```
