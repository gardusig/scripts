# scripts

## ⚙️ Dev Setup Instructions

### Install Python

```bash
brew install python
python3 -m pip install --upgrade pip
python3 -m pip install virtualenv
```

### Create and Activate Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
python3 -m pip install .
```

## 🔐 Environment Variables

Make sure to create a `.env` file in the project root with the following content:

```env
OPENAI_API_KEY=sk-...
```

Or set it directly in your shell:

```bash
export OPENAI_API_KEY=sk-...
```

## 🧪 Usage

### Dump a folder as Markdown (prints to stdout):

```bash
python src/main.py ./your-folder
```

## 📋 Clipboard Copy

```bash
python src/main.py ./your-folder --copy
```
