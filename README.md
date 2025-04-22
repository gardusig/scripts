# Kirby CLI

Welcome to the Kirby CLI! This snazzy tool is here to enhance your workflow with a sprinkle of command-line magic. Manage your file paths, harness the power of AI, and analyze instructions with flair and efficiency! Let's dive in and have some fun! 😎

## Commands Overview 📜

### Main Application

At the heart of our magical CLI journey is the central application, guiding you through a maze of commands and features.

## Usage 🛠️

Think of Kirby CLI as a master chef, helping you collect all the ingredients (files and instructions) to cook up a delicious AI recipe. Once you've gathered your magical ingredients, fuse them for an LLM to savor.

![kirby](./resources/media/kirby.webp)

### Kirby Wizardry at Your Fingertips

#### File Management 📁

Manage your files like a maestro with these harmonious commands:

- **Add a file or folder to your list of magical paths:**
  ```bash
  python -m kirby file add "path/to/your/ingredient"
  ```

- **Summon a summary of your current file paths:**
  ```bash
  python -m kirby file list
  ```

- **Reverse the last file-related enchantment:**
  ```bash
  python -m kirby file undo
  ```

- **Wipe the slate clean of all file paths:**
  ```bash
  python -m kirby file clear
  ```

#### Instruction Management 💡

Cast spells on your AI instructions with these intuitive commands:

- **Inscribe a message into your scroll of instructions:**
  ```bash
  python -m kirby instruction add "Write captivating storylines"
  ```

- **Reveal the secrets of your current instructions:**
  ```bash
  python -m kirby instruction list
  ```

- **Undo the last tweak to your instructions:**
  ```bash
  python -m kirby instruction undo
  ```

- **Vanish all instructions into thin air:**
  ```bash
  python -m kirby instruction clear
  ```

#### Recipe Creation with LLM 🍲

Once you've collected your ingredients and instructions, cook up your recipe with:

```bash
python -m kirby evaluate
```

## Example Flow 🔄

Let's put it all together with a simple example flow. Imagine you want to add a recipe and get the magic response from AI:

```bash
python -m kirby file add "recipes/special_dish.txt"
python -m kirby instruction add "Explain the cooking process clearly."
python -m kirby evaluate
```

## Dev Setup Instructions ⚙️

Ready to join the Kirby development brigade? Here's your quick start guide:

### Essential Ingredients: Python Installation 🐍

```bash
brew install python
python3 -m pip install --upgrade pip
python3 -m pip install virtualenv
```

### Creating Your Development Environment

Embark on your dev adventure with these simple steps:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -e .
```

### Environment Configuration 🔐

Unlock the full flavor of AI by setting your secret API key in a `.env` file at the root of the project:

```env
OPENAI_API_KEY=sk-...
```

Or enjoy the thrill of a direct key export before each session:

```bash
export OPENAI_API_KEY=sk-...
```
