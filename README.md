# Kirby CLI README

Welcome to the Kirby CLI! This handy tool provides a suite of CLI subcommands for managing file paths, evaluating AI models, and maintaining instruction records with flair and efficiency. Let's dive in and see how it ticks! 🚀

## Commands Overview

### Main Application

At the heart of the action is our main CLI application, acting as a launchpad to explore the various subcommands and functionalities.

## Usage

Feed it with all your context; then shrink it all into one robust message for an LLM to evaluate.

![kirby](./resources/media/kirby.webp)

### LLM Evaluation

To perform an analysis by fusing files and instructions through the power of AI, run:

```bash
python -m kirby evaluate
```

### File Management 📁

Become a maestro in managing file paths using these enigmatic commands:

- **Add a folder or file to your path list:**
  ```bash
  python -m kirby file add "path/to/folder"
  ```

- **View the current file summary:**
  ```bash
  python -m kirby file list
  ```

- **Undo the last file operation:**
  ```bash
  python -m kirby file undo
  ```

- **Clear all file paths from the list:**
  ```bash
  python -m kirby file clear
  ```

### Instruction Management 💡

Organize your AI instructions like a pro with these intuitive commands:

- **Append a message to the current instructions:**
  ```bash
  python -m kirby instruction add "message"
  ```

- **Display a summary of current instructions:**
  ```bash
  python -m kirby instruction list
  ```

- **Undo the last instruction modification:**
  ```bash
  python -m kirby instruction undo
  ```

- **Clear all instructions:**
  ```bash
  python -m kirby instruction clear
  ```

### Dev Setup Instructions ⚙️

Want to become part of the Kirby CLI development journey? Here's how to get started.

#### Prerequisites: Install Python 🐍

```bash
brew install python
python3 -m pip install --upgrade pip
python3 -m pip install virtualenv
```

#### Setting Up Your Development Environment

Ready to roll? Set up your dev environment like this:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -e .
```

## Environment Configuration 🔐

Time to unleash the power of AI! Configure your environment by storing your API key in a `.env` file in the project's root directory:

```env
OPENAI_API_KEY=sk-...
```

Or, if you're feeling adventurous, directly export the key in your shell session:

```bash
export OPENAI_API_KEY=sk-...
```
