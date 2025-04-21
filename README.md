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
pip install -e .
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

### Kirby

```
python -m scripts.kirby clear
python -m scripts.kirby summary
python -m scripts.kirby append --from clipboard
python -m scripts.kirby append --from message --message "message content..."
python -m scripts.kirby append --from filepath --path path/to/file
python -m scripts.kirby analyze --instructions "Summarize this"
```
