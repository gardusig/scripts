
from typing import Protocol
import typer

class AIConfig(Protocol):
    temperature: float
    max_tokens: int
    top_p: float
    model: str

def load_ai_config(config_path: str) -> AIConfig:
    typer.secho(f'ℹ️ Loading AI config from: {config_path}', fg='green')
    # Placeholder for actual config loading logic
    try:
        # Simulate loading config
        config = {
            "temperature": 0.7,
            "max_tokens": 256,
            "top_p": 0.9,
            "model": "gpt-4"
        }
        typer.secho('✅ AI config loaded successfully.', fg='green')
        return config  # This should be replaced with actual AIConfig implementation
    except Exception as e:
        typer.secho(f'❌ Failed to load AI config: {e}', fg='red', err=True)
        raise
