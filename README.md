# Scripts

## Dev Setup Instructions ⚙️

### Prerequisites: Install Python

```bash
brew install python
python3 -m pip install --upgrade pip
python3 -m pip install virtualenv
```

### Setting Up Your Development Environment

```bash
python3 -m venv venv
source venv/bin/activate
pip install -e .
```

## Environment Configuration 🔐

Configure your environment by setting up your API key in a `.env` file in the project root:

```env
OPENAI_API_KEY=sk-...
```

Alternatively, you can export the key directly in your shell session:

```bash
export OPENAI_API_KEY=sk-...
```

## Using the Scripts 🧪

### AI Analysis with Kirby

Execute an analysis by combining files and instructions through AI:

```bash
python -m scripts.kirby analyze
```

### File Management with Kirby

Manage file paths seamlessly with the following commands:

- **Add a folder or file to your path list:**
  ```bash
  python -m scripts.kirby file add "path/to/folder"
  python -m scripts.kirby file add "path/to/file"
  ```

- **Override the current path list with a new file or folder:**
  ```bash
  python -m scripts.kirby file override "path/to/file"
  python -m scripts.kirby file override "path/to/folder"
  ```

- **View the current file summary:**
  ```bash
  python -m scripts.kirby file list
  ```

- **Undo the last file operation:**
  ```bash
  python -m scripts.kirby file undo
  ```

- **Clear all file paths from the list:**
  ```bash
  python -m scripts.kirby file clear
  ```

### Instruction Management with Kirby

Organize AI instructions effectively using these commands:

- **Append a message to the current instructions:**
  ```bash
  python -m scripts.kirby instruction add "message"
  ```

- **Override instructions with a new message:**
  ```bash
  python -m scripts.kirby instruction override "message"
  ```

- **Display a summary of current instructions:**
  ```bash
  python -m scripts.kirby instruction list
  ```

- **Undo the last instruction modification:**
  ```bash
  python -m scripts.kirby instruction undo
  ```

- **Clear all instructions:**
  ```bash
  python -m scripts.kirby instruction clear
  ```
