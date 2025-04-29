
# Prompt Craft CLI 🧰

Welcome to **Prompt Craft CLI** – command-line toolkit for managing prompts, files, and AI-powered workflows! Prompt Craft CLI helps you organize prompt histories, file queues, and code-gen tasks, so you can focus on what matters: getting things done (with a sprinkle of fun).

<div align="center">
  <img src="./media/kirby-eat.webp" alt="eat" height="200" />
  <img src="./media/kirby-work.gif" alt="work" height="200" />
</div>

## 📚 Table of Contents

- [Prompt Craft CLI 🧰](#prompt-craft-cli-)
  - [📚 Table of Contents](#-table-of-contents)
  - [✨ Features](#-features)
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
  - [🔄 Example Workflow](#-example-workflow)
  - [💬 Questions? Bugs?](#-questions-bugs)

## ✨ Features

- **Prompt history management:** Add, remove, list, undo, and clear prompts for your AI workflows.
- **File queueing:** Track files to share or process with AI, with full undo/clear support.
- **Clipboard integration:** Instantly add prompts from your clipboard.
- **Code generation:** Auto-generate unit tests or README files using your favorite LLM.
- **Batch operations:** Clear or show all tracked items in one go.
- **Undo support:** Oops? Undo your last action for prompts, files, or processing queues.

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
git clone https://github.com/gardusig/prompt_craftCLI.git
cd prompt_craftCLI
python3 -m venv venv
source venv/bin/activate
pip install -e .
```

For development tools:

```bash
pip install -e ".[dev]"
```

## 🔐 Environment Configuration

Prompt Craft CLI uses OpenAI (or other LLM) APIs. Set your API key in a `.env` file at the project root:

```env
OPENAI_API_KEY=sk-...
```

Or export it in your shell:

```bash
export OPENAI_API_KEY=sk-...
```

## 🛠️ CLI Usage

Invoke Prompt Craft CLI with:

```bash
python -m prompt_craft [COMMANDS...]
```

Or, if installed as a script:

```bash
prompt_craft [COMMANDS...]
```

### 💡 Prompt Management

Manage your prompt history for AI interactions:

- **Add a prompt:**
  ```
  prompt_craft prompt add "Summarize the following text"
  ```

- **Remove a prompt:**
  ```
  prompt_craft prompt remove "Summarize the following text"
  ```

- **List all prompts:**
  ```
  prompt_craft prompt list
  ```

- **Undo last prompt change:**
  ```
  prompt_craft prompt undo
  ```

- **Clear all prompts:**
  ```
  prompt_craft prompt clear
  ```

- **Add prompt from clipboard:**
  ```
  prompt_craft clipboard
  ```

### 📁 File Management

Track files you want to share with your LLM:

- **Add a file or directory:**
  ```
  prompt_craft file add path/to/file_or_folder
  ```

- **Remove a file:**
  ```
  prompt_craft file remove path/to/file
  ```

- **List shared files:**
  ```
  prompt_craft file list
  ```

- **Undo last file change:**
  ```
  prompt_craft file undo
  ```

- **Clear all shared files:**
  ```
  prompt_craft file clear
  ```

### ⚙️ Processing Queue

Queue files for processing (e.g., for test generation):

- **Add file(s) to process:**
  ```
  prompt_craft process add path/to/file_or_folder
  ```

- **Remove file from process queue:**
  ```
  prompt_craft process remove path/to/file
  ```

- **List processing files:**
  ```
  prompt_craft process list
  ```

- **Undo last processing change:**
  ```
  prompt_craft process undo
  ```

- **Clear processing queue:**
  ```
  prompt_craft process clear
  ```

### 🤖 Code Generation

Let Prompt Craft and your LLM do the heavy lifting:

- **Generate unit tests for queued files:**
  ```
  prompt_craft code unit-test
  ```

- **Generate a README.md for your project:**
  ```
  prompt_craft code readme
  ```

  Add `--force` to overwrite existing files without confirmation.

### 🌎 Global Commands

- **Show all prompts, shared files, and processing files:**
  ```
  prompt_craft show
  ```

- **Clear everything (prompts, shared files, processing files):**
  ```
  prompt_craft clear
  ```

## 🔄 Example Workflow

Let's say you want to generate tests for your codebase:

```
# Add files to process
python -m prompt_craft process add src/my_module.py

# Add a prompt for the LLM
python -m prompt_craft prompt add "Write comprehensive unit tests."

# Generate tests
python -m prompt_craft code unit-test

# Review the generated tests in your project!
```

Or, to quickly create a README:

```
python -m prompt_craft code readme
```

## 💬 Questions? Bugs?

Open an issue or start a discussion on the [GitHub repo](https://github.com/gardusig/prompt_craftCLI). Prompt Craft is always hungry for feedback!

<div align="center">
  <img src="./media/kirby-cook.gif" alt="prompt_craft-cook" height="100" />
</div>
