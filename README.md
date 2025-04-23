# Kirby CLI

Welcome to the Kirby CLI! Designed to streamline your workflow and boost your productivity with some real-world AI functionality. Manage files and instructions efficiently like a pro! Let's get started.

<div align="justify-center">
  <img src="./media/kirby-eat.webp" alt="kirby-eat" height="175" />
  <img src="./media/kirby-cook.gif" alt="kirby-cook" height="175" />
  <img src="./media/kirby-work.gif" alt="kirby-work" height="175" />
</div>

## Usage 🛠️

Imagine Kirby CLI as your diligent sous-chef, sorting and organizing all your files and instructions so you can focus on creating the perfect AI-assisted project. Once everything is in order, pass it on to your language model for an efficient, focused analysis.


### Efficient File Management at Your Fingertips

#### File Management 📁

Effortlessly manage your files with these commands:

- **Add a file or folder to your designated paths:**
  ```bash
  python -m kirby file add "path/to/your/file"
  ```

- **View your current list of file paths:**
  ```bash
  python -m kirby file list
  ```

- **Undo the last modification to your file list:**
  ```bash
  python -m kirby file undo
  ```

- **Clear out all file paths to start fresh:**
  ```bash
  python -m kirby file clear
  ```

#### Instruction Management 💡

Manage your AI instructions with clarity using these commands:

- **Add a new instruction to your list:**
  ```bash
  python -m kirby instruction add "Write clear documentation"
  ```

- **List all current instructions:**
  ```bash
  python -m kirby instruction list
  ```

- **Undo the last change to your instructions:**
  ```bash
  python -m kirby instruction undo
  ```

- **Clear all instructions:**
  ```bash
  python -m kirby instruction clear
  ```

#### Recipe Creation with LLM 🍲

Once you've organized your files and instructions, get a focused response with:

```bash
python -m kirby evaluate
```

## Example Flow 🔄

Here's a step-by-step example: say you want to understand a recipe and get a solid response from AI:

```bash
python -m kirby file add "recipes/delicious_dish.txt"
python -m kirby instruction add "Describe the main steps clearly."
python -m kirby evaluate
```

## Dev Setup Instructions ⚙️

Ready to start developing with Kirby? Here's your setup guide:

### Python Setup 🐍

First, ensure Python is installed:

```bash
brew install python
python3 -m pip install --upgrade pip
python3 -m pip install virtualenv
```

### Creating Your Development Environment

Set up your development environment efficiently with:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -e .
```

### Environment Configuration 🔐

To access AI features, set your API key in a `.env` file at the project's root:

```env
OPENAI_API_KEY=sk-...
```

Alternatively, export the key directly for each session:

```bash
export OPENAI_API_KEY=sk-...
```